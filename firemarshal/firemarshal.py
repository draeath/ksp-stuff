#!/usr/bin/env python

# KSP FireMarshal
# draeath@gmail.com
# LICENSE: Creative Commons Attribution 4.0 International (CC BY 4.0)
#          http://creativecommons.org/licenses/by/4.0/deed.en_US

# This script computes burn time and other related data for Δv planning.
# TODO: command-line argument support, as alternative to interactive input.

# please visit the forum post for discussion/comments/etc:
# http://forum.kerbalspaceprogram.com/threads/65515

import argparse
from math import fabs
from sys import exit

from firemath import FireMarshalMath as FMM

if __name__ == '__main__':

    helptext = """
Welcome! This utility will compute burn time and fuel usage for a given delta-v.
        Tip: Mg = metric ton = 1000kg
        Tip: combine expended resources for these calculations. (eg fuel+oxi)
        Tip: liquid fuel and oxidizer mass is 5kg per unit.
        Tip: monopropellant mass is 4kg per unit.
        Tip: specify only the fuel mass for the current stage.
        Tip: (wet_mass - dry_mass) / capacity = mass per unit
"""

    # Get arguments for application
    parser = argparse.ArgumentParser(
        description='A utility to compute burn time and fuel useage',
        epilog=helptext, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--delta-v', '-d',
                        help='Desired delta-v in m/s',
                        type=float)
    parser.add_argument('--mass', '-m',
                        help='Initial mass in metric tonnes',
                        type=float)
    parser.add_argument('--fuel', '-f',
                        help='Initial fuel mass in metric tonnes',
                        type=float)

    parser.add_argument('--thrust', '-t',
                        help='Thruts of engines, space separated list (-t 100 600 1400)',
                        nargs='+',
                        type=float)
    parser.add_argument('--impulse', '-i',
                        help='Impulse of engines, space separated list (-i 100 600 1400)',
                        nargs='+',
                        type=float)

    args = parser.parse_args()

    if args.delta_v:
        velocity_delta = args.delta_v
    else:
        velocity_delta = fabs(float(input("Desired delta-v in m/s?\t\t")))

    if args.mass:
        mass_initial = args.mass
    else:
        mass_initial = fabs(float(input("Vessel mass in Mg?\t\t")))

    if args.fuel:
        mass_initial_fuel = args.fuel
    else:
        mass_initial_fuel = fabs(float(input("Fuel mass in Mg?\t\t")))

    if args.thrust and args.impulse:
        engines = zip(args.thrust, args.impulse)
    else:
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
            engines.append((inputThrust, inputImpulse))

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
    print("Calculated thrust:\t\t" + str(round(thrust, 4)))
    print("Calculated specific impulse:\t" + str(round(specific_impulse, 4)))
    print("\n")

    # Initiate math and neeeded functions
    maths = FMM(mass_initial, mass_initial_fuel, specific_impulse, thrust,
                velocity_delta)

    # Run all the maths
    maths.velocity_exhaust()
    maths.burn_time()
    maths.mass_dict()

    # output here, leave it be.
    print("Burn time:        " + str(round(maths.b_t, 2)) + "sec.")
    print("Initial mass:     " + str(round(mass_initial, 3)) + "Mg.")
    print("Final mass:       " + str(round(maths.m_fin, 3)) + "Mg.")
    print("Fuel spent:       " + str(round((maths.m_i_f - maths.m_f_fin), 3)) + "Mg.")
    print("Fuel remaining:   " + str(round(maths.m_f_fin, 3)) + "Mg.")
    if (maths.m_f_fin < 0):
        print("\n")
        print("WARNING: Insufficient fuel for burn!")

    print("\n")

    input("Press enter to continue")
