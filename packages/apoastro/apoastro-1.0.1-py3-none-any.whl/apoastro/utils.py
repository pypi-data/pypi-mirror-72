#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

def toJulianEphemerisDate(value):
    return (value / 86400.0) + 2440588.0

def toJ2000(T):
    return (toJulianEphemerisDate(T) - 2451545.0) / 36525.
