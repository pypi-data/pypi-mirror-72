#
# aiotsl2591 - TSL2591 sensor asyncio library
#
# Copyright (C) 2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# NOTE: Lux calculation taken from Adafruit library.
#

# distutils: language = c
# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str

import logging
import os

from libc.errno cimport errno
from libc.stdint cimport int8_t, int16_t, int32_t, int64_t, \
    uint8_t, uint16_t, uint32_t, uint64_t
from posix.unistd cimport read, write, close, usleep
from posix.fcntl cimport open, O_RDWR
from posix.time cimport itimerspec, timespec, clock_gettime
from posix.ioctl cimport ioctl

from .error import *

logger = logging.getLogger(__name__)

# Delay [us] needed for measurement for maximum gain. Relates to TIME_*
# constants.
DELAY = 600 * 1000

GAIN_MEDIUM = 0x01 << 4  # general purpose
TIME_MAX = 0x05  # 600 ms, page 8 of the datasheet
DEFAULT_CONFIGURATION = GAIN_MEDIUM | TIME_MAX

REGISTER_COMMAND = 0xa0
REGISTER_CONTROL = REGISTER_COMMAND | 0x01
REGISTER_C0DATAL = REGISTER_COMMAND | 0x14

REGISTER_DISABLE = 0x00
REGISTER_ENABLE_POWER_ON = 0x01  # PON
REGISTER_ENABLE_AEN = 0x02

# no support for the interrupt at the moment (AIEN)
REGISTER_ENABLE = REGISTER_ENABLE_POWER_ON | REGISTER_ENABLE_AEN

# `AGAIN` and `ATIME` depend on DEFAULT_CONFIGURATION (GAIN_MEDIUM and
# TIME_MAX); this might be configurable in the future and setting of
# the two variables need to change in the future
AGAIN = 25
ATIME = 600
CPL = ATIME * AGAIN / 408

I2C_SLAVE = 0x0703

CMD_LEN = 2
CMD_LEN_SENSOR_READ_ADC = 1

cdef uint8_t *CMD_SENSOR_CONFIGURE = [REGISTER_CONTROL, DEFAULT_CONFIGURATION]
cdef uint8_t *CMD_SENSOR_ENABLE = [REGISTER_COMMAND, REGISTER_ENABLE]
cdef uint8_t *CMD_SENSOR_DISABLE = [REGISTER_COMMAND, REGISTER_DISABLE]
cdef uint8_t *CMD_SENSOR_READ_ADC = [REGISTER_C0DATAL]

cdef extern from "<sys/timerfd.h>":
    enum: CLOCK_MONOTONIC

    int timerfd_create(int, int)
    int timerfd_settime(int, int, itimerspec*, itimerspec*)

#cdef extern from "<sys/ioctl.h>":
#    enum: I2C_SLAVE

cdef class SensorData:
    cdef public float lux

    cdef public int i2c_fd
    cdef public int timer_fd

    def __init__(self, int i2c_fd, int timer_fd):
        self.i2c_fd = i2c_fd
        self.timer_fd = timer_fd


cdef float calc_lux(uint16_t full, uint16_t ir):
    """
    Calculate lux value using raw data.

    TSL2591 datasheet does not contain any equation to calculate the lux
    value. The "Developing a Custom Lux Equation" document provides an
    equation, but comparing to Adafruit library, the coefficients are
    different

        https://github.com/adafruit/Adafruit_TSL2591_Library/blob/master/Adafruit_TSL2591.cpp
        https://github.com/adafruit/Adafruit_CircuitPython_TSL2591/blob/master/adafruit_tsl2591.py

    See also discussion at

        https://github.com/adafruit/Adafruit_CircuitPython_TSL2591/issues/7
        https://github.com/adafruit/Adafruit_TSL2591_Library/issues/14

    """
    return (<float>full - <float>ir) * (1 - <float>ir / <float>full) / CPL

#
# High level helper functions to enable sensor, reset sensor and read data
# from sensor.
#

cdef int reset_sensor(int i2c_fd):
    r = write(i2c_fd, CMD_SENSOR_CONFIGURE, CMD_LEN)
    if r != CMD_LEN:
        return -1

    r = disable_sensor(i2c_fd)
    if r != 0:
        return -1

    logger.debug('sensor reset performed')
    return 0

cdef int enable_sensor(int i2c_fd):
    cdef int r

    r = write(i2c_fd, CMD_SENSOR_ENABLE, CMD_LEN)
    if r != CMD_LEN:
        return -1

    return 0

cdef int disable_sensor(int i2c_fd):
    cdef int r

    r = write(i2c_fd, CMD_SENSOR_ENABLE, CMD_LEN)
    if r != CMD_LEN:
        return -1

    return 0

cdef int read_data_end(SensorData data):
    cdef int r
    cdef uint8_t buff[4]
    cdef uint16_t full, ir;

    r = write(data.i2c_fd, CMD_SENSOR_READ_ADC, CMD_LEN_SENSOR_READ_ADC)
    if r != 1:
        return -1

    # read all 4 ADC bytes in sequence, page 21 of the datasheet
    r = read(data.i2c_fd, buff, 4)
    if r != 4:
        return -1

    r = disable_sensor(data.i2c_fd)
    if r != 0:
        return -1

    # interpret raw data, check values and calculate lux value
    full = (buff[1] << 8) | buff[0]
    ir = (buff[3] << 8) | buff[1]

    logger.debug('full: 0x{:04x}, ir: 0x{:04x}'.format(full, ir))

    if full == 0xffff or ir == 0xffff:
        logger.error('overflow reading data')
        return -2

    data.lux = calc_lux(full, ir)

    return 0

#
# Sensor functions API implementation.
#

def tsl2591_init(bytes f_dev, uint8_t address) -> SensorData:
    cdef int r
    cdef int i2c_fd
    cdef int timer_fd
    cdef uint16_t result
    cdef uint8_t result8

    i2c_fd = open(f_dev, O_RDWR)
    if i2c_fd < 0:
        raise SensorInitError(
            'cannot open device {}: {}'
            .format(f_dev.decode(), os.strerror(errno))
        )

    r = ioctl(i2c_fd, I2C_SLAVE, address)
    if r < 0:
        raise SensorInitError(
            'cannot initalize i2c device at address 0x{:02x}: {}'
            .format(address, os.strerror(errno))
        )

    timer_fd = timerfd_create(CLOCK_MONOTONIC, 0)
    if timer_fd < 0:
        raise SensorInitError(
            'cannot create timer: {}'
            .format(os.strerror(errno))
        )
    r = reset_sensor(i2c_fd)
    if r != 0:
        raise SensorInitError(
            'sensor reset failed: {}'
            .format(os.strerror(errno))
        )

    data = SensorData(i2c_fd, timer_fd)
    return data

def tsl2591_read_start(SensorData data):
    cdef itimerspec ts
    cdef int r

    r = enable_sensor(data.i2c_fd)
    if r != 0:
        raise SensorReadError(
            'cannot start sensor read: {}'
            .format(os.strerror(errno))
        )

    ts.it_interval.tv_sec = 0
    ts.it_interval.tv_nsec = 0
    ts.it_value.tv_sec = 0
    ts.it_value.tv_nsec = DELAY * 1000   # usleep(DELAY)
    r = timerfd_settime(data.timer_fd, 0, &ts, NULL)
    if r != 0:
        raise SensorReadError(
            'cannot start sensor read timer: {}'
            .format(os.strerror(errno))
        )

def tsl2591_read_end(SensorData data):
    cdef int r
    cdef uint64_t value

    # disable timer
    r = read(data.timer_fd, &value, 8)
    if r != 8:
        raise SensorReadError(
            'cannot stop sensor read timer (result={}): {}'
            .format(r, os.strerror(errno))
        )

    # read sensor data
    r = read_data_end(data)
    if r == -2:
        raise ayncio.CancelledError('data overflow')
    elif r != 0:
        raise SensorReadError(
            'sensor data read failed: {}'
            .format(os.strerror(errno))
        )

def tsl2591_close(SensorData data):
    cdef int r
    r = close(data.timer_fd)
    if r != 0:
        raise SensorCloseError(
            'cannot stop sensor timer: {}'
            .format(os.strerror(errno))
        )

    r = close(data.i2c_fd)
    if r != 0:
        raise SensorCloseError(
            'cannot close i2c device: {}'
            .format(os.strerror(errno))
        )

# vim: sw=4:et:ai
