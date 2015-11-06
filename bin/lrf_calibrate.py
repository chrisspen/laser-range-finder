#!/usr/bin/env python
"""
Helps calibrating a laser range finder by calculating the rpc and ro parameters.

https://shaneormonde.wordpress.com/2014/01/25/webcam-laser-rangefinder/

theta = arctan(h/actual_d)

theta = pfc * rpc + ro
"""
import sys
from math import *
import argparse

import yaml
from scipy import stats
import numpy as np

from laser_range_finder import pixels_to_distance

def percent_error(expected, actual):
    return (expected - actual)/float(actual)*100

def run(conf_fn):

    conf = yaml.load(open(conf_fn))

    readings = conf['readings']

    distances = conf['distances'] # {position: distance}
    
    h = float(conf['h'])
    
    image_width = int(conf['image_width'])

    image_height = int(conf['image_height'])
    
    measurements = []
    for col in sorted(distances.keys()):
        actual_d = distances[col]
        pix_dist = readings[col]
        assert pix_dist > 0
        pfc = abs(pix_dist - image_height/2)
        #theta = atan(h/actual_d)
        measurements.append((actual_d, pfc))
    
    #print '\nmeasurements:', measurements
    
    x = [_pix_dist for _actual_d, _pix_dist in measurements]
    y = [atan(h/_actual_d) for _actual_d, _pix_dist in measurements]
        
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    #print '\nlinreg:', slope, intercept, r_value, p_value, std_err
    # y = m * x + b => theta = rpc * pfc + ro
    # slope = m = rpc
    # intercept = b = ro
    rpc = slope
    ro = intercept
    print '\n--rpc=%s --ro=%s\n' % (slope, intercept)
    
#     estimated_distances = pixels_to_distance(
#         pixel_rows=readings,
#         rpc=rpc,
#         ro=ro,
#         h=h,
#         max_height=image_height,
#         max_width=image_width,
#     )
    #print '\nestimated_distances:', estimated_distances
#     estimated_distances2 = [_v for _i, _v in enumerate(estimated_distances) if _i in distances.keys()]
    #print '\nestimated_distances:', estimated_distances2
    
#     print '\npixels from center,calc D (mm),actual D (mm),% error'
#     differences = []
#     for col in distances.keys():
#         actual_d = distances[col]
#         pix_dist = readings[col]
#         pfc = abs(pix_dist - image_height/2)
#         estimated_d = estimated_distances[col]
#         print '%s,%s,%s,%s' % (pfc, estimated_d, actual_d, percent_error(estimated_d, actual_d))
#         differences.append(abs(actual_d - estimated_d))
#     print '\naverage error:', sum(differences)/float(len(differences))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Helps calibrate measurements.')
    parser.add_argument('conf_fn',
                   help='configuration file')
    args = parser.parse_args()
    run(**args.__dict__)
