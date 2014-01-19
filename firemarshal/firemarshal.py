#!/usr/bin/env python

# KSP FireMarshal
# draeath@gmail.com
# LICENSE: Creative Commons Attribution 4.0 International (CC BY 4.0)
#          http://creativecommons.org/licenses/by/4.0/deed.en_US

# This script computes burn time and other related data for Δv planning.
# TODO: command-line argument support, as alternative to interactive input.

# please visit the forum post for discussion/comments/etc:
# http://forum.kerbalspaceprogram.com/threads/65515

from math import exp
from math import fabs
from sys import exit

print("\n")
print("Welcome! This utility will compute burn time and fuel usage for a given delta-v.")
print("\tTip: Mg = metric ton = 1000kg")
print("\tTip: combine expended resources for these calculations. (eg fuel+oxi)")
print("\tTip: liquid fuel and oxidizer mass is 5kg per unit.")
print("\tTip: monopropellant mass is 4kg per unit.")
print("\tTip: specify only the fuel mass for the current stage.")
print("\tTip: (wet_mass - dry_mass) / capacity = mass per unit")
print("\n")

velocity_delta    = fabs(float(input("Desired delta-v in m/s?\t\t")))
mass_initial      = fabs(float(input("Vessel mass in Mg?\t\t")))
mass_initial_fuel = fabs(float(input("Fuel mass in Mg?\t\t")))
print("\n")

enginenumber = 1
engines = list()
print("Thrust and Isp entry will loop - make one entry per engine.")
print("Provide value of 0 to stop adding engines.")
while True:
    inputThrust = fabs(float(input("Engine " + str(enginenumber) + " thrust in kN?\t\t\t")))
    if (inputThrust == 0):
        break
    inputImpulse = fabs(float(input("Engine " + str(enginenumber) + " specific impulse in seconds?\t")))
    if (inputImpulse == 0):
        break
    enginenumber += 1
    engines.append([inputThrust,inputImpulse])

# Compute combined thrust and Isp - lists and iteration! Whee!
# I am sure there are better ways, but I am lazy.
thrust = float(0)
specific_impulse = float(0)
specific_impulse_denominator = float(0)
for item in engines:
    thrust += item[0]
    specific_impulse_denominator += (item[0] / item[1])
specific_impulse = thrust / specific_impulse_denominator

print("\n")
print("Calculated thrust:\t\t" + str(round(thrust,4)))
print("Calculated specific impulse:\t" + str(round(specific_impulse,4)))
print("\n")

# formulas here, leave them be (unless you need to change standard gravity to real value).
standard_gravity   = 9.82
velocity_exhaust   = (standard_gravity * specific_impulse)
burn_time          = ((mass_initial * velocity_exhaust) / thrust) * (1 - exp(-1 * velocity_delta / velocity_exhaust))
mass_fuel_expended = mass_initial * (1 - exp(-1 * velocity_delta / velocity_exhaust))
mass_final         = mass_initial - mass_fuel_expended
mass_final_fuel    = mass_initial_fuel - mass_fuel_expended


# output here, leave it be.
print("Burn time:\t"      + str(round(burn_time,2))          + "\tsec.")
print("Initial mass:\t"   + str(round(mass_initial,3))       + "\tMg.")
print("Final mass:\t"     + str(round(mass_final,3))         + "\tMg.")
print("Fuel spent:\t"     + str(round(mass_fuel_expended,3)) + "\tMg.")
print("Fuel remaining:\t" + str(round(mass_final_fuel,3))    + "\tMg.")
if (mass_final_fuel < 0):
    print("\n")
    print("WARNING: Insufficient fuel for burn!")

print("\n")

input("Press any key to continue")
