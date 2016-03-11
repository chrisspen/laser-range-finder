#!/usr/bin/env python
"""
Helps calibrating a laser range finder by calculating the rpc and ro parameters.

https://shaneormonde.wordpress.com/2014/01/25/webcam-laser-rangefinder/

theta = arctan(h/actual_d)

theta = pfc * rpc + ro
"""
import argparse

from laser_range_finder import calibrate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Helps calibrate measurements.')
    parser.add_argument('conf_fn',
                   help='configuration file')
    args = parser.parse_args()
    calibrate(**args.__dict__)
