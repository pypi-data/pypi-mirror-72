#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

# https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf

import numpy as np
from math import *
import time

class KeplerianElements():

    # class constructor
    # a  - semi-major axis
    # e  - eccentricity
    # I  - inclination, angle of the apoastro plane
    # ml - mean longitude
    # lp - longitude of perihelion
    # la - longitude of the ascending node
    def __init__(self, a, e, I, ml, lp, la):
        self.scale = 1
        self.a0 = a
        self.e0 = e
        self.I0 = radians(I)
        self.ml0 = radians(ml)
        self.lp0 = radians(lp)
        self.la0 = radians(la)
        self.rate_a = 0
        self.rate_e = 0
        self.rate_I = 0
        self.rate_ml = 0
        self.rate_lp = 0
        self.rate_la = 0
        self.b = 0
        self.c = 0
        self.s = 0
        self.f = 0

    def setValues(self, a,  e,  I,  ml,  lp,  la):
        self.a0 = a
        self.e0 = e
        self.I0 = radians(I)
        self.ml0 = radians(ml)
        self.lp0 = radians(lp)
        self.la0 = radians(la)

    def setRates(self, a,  e,  I,  ml,  lp,  la):
        self.rate_a = a
        self.rate_e = e
        self.rate_I = radians(I)
        self.rate_ml = radians(ml)
        self.rate_lp = radians(lp)
        self.rate_la = radians(la)

    def setAdditionalTerms(self,  b,  c,  s,  f):
        self.b = radians(b)
        self.c = radians(c)
        self.s = radians(s)
        self.f = radians(f)

    def setScale(self, value):
        self.scale = value

    def getM(self, T):  # mean anomaly
        return self.ml - self.lp + self.b * T**2 + self.c * cos(self.f * T) + self.s * sin(self.f * T)

    def get_pa(self):  # perihelion argument
        return self.lp - self.la

    def getE(self, T):  # eccentric anomaly
        M = self.getM(T)
        E = M + self.e*sin(M)
        for i in range(100):
            dM = M - (E - self.e * sin(E))
            dE = dM / (1. - self.e * cos(E))
            E = E + dE
            if abs(dE) < 1e-8:
                break
        return E

    def get_rx(self, angle):
        return self.scale * self.a * (cos(angle) - self.e)

    def get_ry(self, angle):
        return self.scale * self.a * sin(angle) * sqrt(1. - self.e**2)

    def get_r(self, angle):
        return self.scale * self.a * (1.0 - self.e * cos(angle))

    def get_x(self, angle):
        return self.x[0] * self.get_rx(angle) + self.x[1] * self.get_ry(angle)

    def get_y(self, angle):
        return self.y[0] * self.get_rx(angle) + self.y[1] * self.get_ry(angle)

    def get_z(self, angle):
        return self.z[0] * self.get_rx(angle) + self.z[1] * self.get_ry(angle)

    def updateElements(self, T):
        self.a = self.a0 + self.rate_a * T
        self.I = self.I0 + self.rate_I * T
        self.e = self.e0 + self.rate_e * T
        self.ml = self.ml0 + self.rate_ml * T
        self.lp = self.lp0 + self.rate_lp * T
        self.la = self.la0 + self.rate_la * T

    def getPosition(self, T):

        self.updateElements(T)

        E = self.getE(T)
        rx = self.get_rx(E)
        ry = self.get_ry(E)

        pa = self.get_pa()
        self.x = [cos(pa) * cos(self.la) - sin(pa) * sin(self.la) * cos(self.I), -sin(pa) * cos(self.la) - cos(pa) * sin(self.la) * cos(self.I)]
        self.y = [cos(pa) * sin(self.la) + sin(pa) * cos(self.la) * cos(self.I), -sin(pa) * sin(self.la) + cos(pa) * cos(self.la) * cos(self.I)]
        self.z = [sin(pa) * sin(self.I), cos(pa) * sin(self.I)]

        x = self.x[0] * rx + self.x[1] * ry
        y = self.y[0] * rx + self.y[1] * ry
        z = self.z[0] * rx + self.z[1] * ry

        return np.array([x, y, z])