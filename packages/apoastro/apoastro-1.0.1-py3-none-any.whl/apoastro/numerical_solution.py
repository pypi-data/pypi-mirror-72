#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

from numpy import *

class NumericalSolution(object):

    # class constructor
    def __init__(self, G, m, x0, v0, dt, T, ef, method):
        self.G = G
        self.m = m
        self.x = x0
        self.v = v0
        self.dt = dt
        self.T = T
        self.ef = ef
        self.method = method
        self.nb = len(self.m)  # number of bodies
        self.vet0 = [array([.0, .0, .0]) for i in range(self.nb)]
    
    # calculate gravitational force
    def gravity_force(self, i, m, x):
        G = self.G
        ax = ay = az = 0
        for j in range(self.nb):
           if i != j:  # or multiplying by (1-Delta[i][j]) where Delta is the Kronecker delta function
              ax += -G * m[j] * (x[i][0] - x[j][0]) / (((x[i][0] - x[j][0]) ** 2 + (x[i][1] - x[j][1]) ** 2 + (x[i][2] - x[j][2]) ** 2) ** (3.0 / 2))
              ay += -G * m[j] * (x[i][1] - x[j][1]) / (((x[i][0] - x[j][0]) ** 2 + (x[i][1] - x[j][1]) ** 2 + (x[i][2] - x[j][2]) ** 2) ** (3.0 / 2))
              az += -G * m[j] * (x[i][2] - x[j][2]) / (((x[i][0] - x[j][0]) ** 2 + (x[i][1] - x[j][1]) ** 2 + (x[i][2] - x[j][2]) ** 2) ** (3.0 / 2))
        a = array([ax, ay, az])
        return a

    # calculate speed and position using Euler's method
    def euler(self, m, x0, v0, dt):
        v = list(self.vet0)
        x = list(self.vet0)
        a = list(self.vet0)
        for i in range(self.nb):
            if self.ef == None:
                a[i] = self.gravity_force(i, m, x0)
            else:
                a[i] = self.gravity_force(i, m, x0)+self.ef(i, m, x0, v0)
            x[i] = x0[i] + dt * v0[i]  # x=x0+v*dt
            v[i] = v0[i] + dt * a[i]   # v=v0+a*dt
        return [x, v, a]
    
    # calculate speed and position using improved Euler method
    def eulerm(self, m, x0, v0, dt):
        v = list(self.vet0)
        x = list(self.vet0)
        a = list(self.vet0)
        for i in range(self.nb):
           x1 = list(x0)
           if self.ef == None:
               a1 = self.gravity_force(i, m, x0)  # a1=f(m,x0)
           else:
               a1 = self.gravity_force(i, m, x0)+self.ef(i, m, x0, v0)
           x1[i] = x0[i] + dt * v0[i]  # x1=x0+v0*dt
           v1 = v0[i] + dt * a1  # v1=v0+a1*dt

           if self.ef == None:
               a[i] = 0.5 * (a1 + self.gravity_force(i, m, x1))  # a=1/2*(f(m,x0)+f(m,x1))
           else:
               a[i] = 0.5 * (a1 + self.gravity_force(i, m, x1)+self.ef(i, m, x1, v1))
           x[i] = x0[i] + dt * (0.5 * (v0[i] + v1))  # x=x0+1/2*(v0+v1)*dt
           v[i] = v0[i] + dt * a[i]  # v=v0+a*dt
        return [x, v, a]
    
    # calculate speed and position using Runge Kutta method of 4th order
    def rk4(self, m, x0, v0, dt):
        v = list(self.vet0)
        x = list(self.vet0)
        a = list(self.vet0)
        for i in range(self.nb):
           xk = list(x0)
           v1 = v0[i]
           if self.ef == None:
               a1 = self.gravity_force(i, m, x0)
           else:
               a1 = self.gravity_force(i, m, x0)+self.ef(i, m, x0, v1)
           v2 = v0[i] + a1 * dt / 2.
           xk[i] = x0[i] + v1 * dt / 2.
           if self.ef == None:
               a2 = self.gravity_force(i, m, xk)
           else:
               a2 = self.gravity_force(i, m, xk)+self.ef(i, m, xk, v2)
           v3 = v0[i] + a2 * dt / 2.
           xk[i] = x0[i] + v2 * dt / 2.
           if self.ef == None:
               a3 = self.gravity_force(i, m, xk)
           else:
               a3 = self.gravity_force(i, m, xk)+self.ef(i, m, xk, v3)
           v4 = v0[i] + dt * a3
           xk[i] = x0[i] + v3 * dt
           if self.ef == None:
               a4 = self.gravity_force(i, m, xk)
           else:
               a4 = self.gravity_force(i, m, xk)+self.ef(i, m, xk, v4)
           x[i] = x0[i] + dt * (v1 + 2.*v2 + 2.*v3 + v4) / 6.0
           v[i] = v0[i] + dt * (a1 + 2.*a2 + 2.*a3 + a4) / 6.0
           a[i] = (a1 + 2.*a2 + 2.*a3 + a4) / 6.0
        return [x, v, a]
    
    # calculate a step
    def solve_step(self):
        if self.method == 'rk4':
           [self.x, self.v, self.a] = self.rk4(self.m, self.x, self.v, self.dt)
        else:
           [self.x, self.v, self.a] = self.eulerm(self.m, self.x, self.v, self.dt)

        self.t += self.dt
        return [self.t, self.x, self.v, self.a]

    # calculate all steps
    def solve_all(self):
        t = [0]
        x = [list(self.vet0)]
        v = [list(self.vet0)]
        a = [list(self.vet0)]
        x[0] = self.x
        v[0] = self.v

        for i in range(int(self.T / self.dt) - 1):
            t.append(0)
            x.append(list(self.vet0))
            v.append(list(self.vet0))
            a.append(list(self.vet0))
            if self.method == 'rk4':
                [x[i + 1], v[i + 1], a[i + 1]] = self.rk4(self.m, x[i], v[i], self.dt)
            else:
                [x[i + 1], v[i + 1], a[i + 1]] = self.eulerm(self.m, x[i], v[i], self.dt)
            # time
            t[i + 1] = t[i] + self.dt
        return [t, x, v, a]

# x[i][n][c]
# i = vector index of all positions at the same time
# n = identifies the body
# c = identifies the component [x=0,y=1,z=2]
# x.pop(0) remove older

