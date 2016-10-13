# -*- coding: utf-8 -*-

import math

# Constants


class FireMarshalMath(object):
    standard_gravity = 9.82

    def __init__(self,
                 mass_initial=0,
                 mass_initial_fuel=0,
                 impulse=0,
                 thrust=0,
                 velocity_delta=0,
                 g0=standard_gravity,
                 ):
        self.m_i = mass_initial
        self.m_i_f = mass_initial_fuel
        self.impulse = impulse
        self.thrust = thrust
        self.v_d = velocity_delta
        self.g0 = g0

    def velocity_exhaust(self):
        self.v_e = self.g0 * self.impulse
        return self.v_e

    def burn_time(self):
        self.b_t = ((self.m_i * self.v_e) / self.thrust) * (1 - math.exp(
            -1 * self.v_d / self.v_e))
        return self.b_t

    def mass_dict(self):
        # Calculate fuel expended
        self.f_e = self.m_i * (1 - math.exp(-1 * self.v_d / self.v_e))
        # Calculate final mass
        self.m_fin = self.m_i - self.f_e
        # Calculate final fuel
        self.m_f_fin = self.m_i_f - self.f_e
        self.twr_initial = self.thrust / self.m_i
        self.twr_final = self.thrust / self.m_fin
        return {'fuel_expended': self.f_e,
                'mass_final': self.m_fin,
                'mass_fuel_final': self.m_f_fin,
                'twr_initial': self.twr_initial,
                'twr_final': self.twr_final}
