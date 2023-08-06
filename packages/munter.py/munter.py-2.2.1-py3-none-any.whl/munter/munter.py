# -*- coding: utf-8 -*-


"""
Munter Time Calculation
Alexander Vasarab
Wylark Mountaineering LLC

A rudimentary program which implements the Munter time calculation.
"""

import sys
import argparse

from . import __progname__ as progname
from . import __version__ as version

class InvalidUnitsException(Exception):
    """Exception class for when invalid units are specified"""

RATES = {
    'uphill': {'rate': 4, 'direction': '↑'},
    'flat': {'rate': 6, 'direction': '→'}, # or downhill on foot
    'downhill': {'rate': 10, 'direction': '↓'},
    'bushwhacking': {'rate': 2, 'direction': '↹'},
}

FITNESSES = {
    'slow': 1.2,
    'average': 1,
    'fast': .7,
}

UNIT_CHOICES = ['metric', 'imperial']
TRAVEL_MODE_CHOICES = RATES.keys()
FITNESS_CHOICES = FITNESSES.keys()

def time_calc(distance, elevation, fitness='average', rate='uphill',
              units='imperial'):
    """
    the heart of the program, the Munter time calculation implementation
    """
    retval = {}

    if units not in UNIT_CHOICES:
        raise InvalidUnitsException

    unit_count = 0

    if units == 'imperial':
        # convert to metric
        distance = (distance * 1.609) # mi to km
        elevation = (elevation * .305) # ft to m

    unit_count = distance + (elevation / 100.0)

    retval['time'] = (distance + (elevation / 100.0)) / RATES[rate]['rate']
    retval['time'] = retval['time'] * FITNESSES[fitness]

    retval['unit_count'] = unit_count
    retval['direction'] = RATES[rate]['direction']
    retval['pace'] = RATES[rate]['rate']

    return retval

def print_ugly_estimate(est):
    """plain-jane string containing result"""
    hours = int(est['time'])
    minutes = int((est['time'] - hours) * 60)
    print("{human_time}".format(
        human_time="{hours} hours {minutes} minutes".format(
            hours=hours, minutes=minutes)))

def print_pretty_estimate(est):
    """more elaborate, console-based 'GUI' displaying result"""
    hours = int(est['time'])
    minutes = int((est['time'] - hours) * 60)

    # NOTE: Below, the line with the unicode up arrow uses an alignment
    #       value of 31. In the future, consider using e.g. wcwidth
    #       library so that this is more elegant.
    print("\n\t╒═══════════════════════════════╕")
    print("\t╎▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╎╮")
    print("\t╎▒{:^29}▒╎│".format(''))
    print("\t╎▒{pace_readable:^31}▒╎│".format(
        pace_readable="{units} {direction} @ {pace}".format(
            units=round(est['unit_count']),
            direction=est['direction'],
            pace=est['pace'])))
    print("\t╎▒{human_time:^29}▒╎│".format(
        human_time="{hours} hours {minutes} minutes".format(
            hours=hours,
            minutes=minutes)))
    print("\t╎▒{:^29}▒╎│".format(''))
    print("\t╎▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╎│")
    print("\t╘═══════════════════════════════╛│")
    print("\t └───────────────────────────────┘\n")

def get_parser():
    """return ArgumentParser for this program"""
    parser = argparse.ArgumentParser(description='Implementation of '
                                     'the Munter time calculation')

    # No required args anymore, since -g overrides any requirement
    parser.add_argument('--distance',
                        '-d',
                        default=0.0,
                        type=float,
                        required=False,
                        help='Distance (in km, by default)')

    parser.add_argument('--elevation',
                        '-e',
                        default=0.0,
                        type=float,
                        required=False,
                        help='Elevation change (in m, by default)')

    parser.add_argument('--travel-mode',
                        '-t',
                        type=str,
                        default='uphill',
                        choices=TRAVEL_MODE_CHOICES, required=False,
                        help='Travel mode (uphill, by default)')

    parser.add_argument('--fitness',
                        '-f',
                        type=str,
                        default='average',
                        choices=FITNESS_CHOICES, required=False,
                        help='Fitness modifier (average, by default)')

    parser.add_argument('--units',
                        '-u',
                        type=str,
                        default='imperial',
                        required=False,
                        choices=UNIT_CHOICES,
                        help='Units of input values')

    parser.add_argument('--pretty',
                        '-p',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Make output pretty')

    parser.add_argument('--gui',
                        '-g',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Launch GUI mode (overrides --pretty)')

    parser.add_argument('--version',
                        '-v',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Print version and exit')

    return parser

def main():
    """main routine: sort through args, decide what to do"""
    parser = get_parser()
    opts = parser.parse_args()

    distance = opts.distance
    elevation = opts.elevation
    fitness = opts.fitness
    units = opts.units
    travel_mode = opts.travel_mode
    pretty = opts.pretty
    gui = opts.gui
    get_version = opts.version

    if get_version:
        print("%s - v%s" % (progname, version))
        return 0

    time_estimate = time_calc(distance=distance, elevation=elevation,
                              fitness=fitness, rate=travel_mode,
                              units=units)

    if gui:
        from . import gui
        gui.startup()
    else:
        if pretty:
            print_pretty_estimate(time_estimate)
        else:
            print_ugly_estimate(time_estimate)

    return 0

if __name__ == "__main__":
    sys.exit(main())
