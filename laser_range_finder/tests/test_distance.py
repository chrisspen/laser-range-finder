import os
import csv
import pytest

from laser_range_finder import LaserRangeFinder, utils

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def test_samples(**kwargs):
    fn = os.path.join(CURRENT_DIR, '../../docs/data/samples.csv')
    assert_test = kwargs.pop('assert_test', True)
    verbose = kwargs.pop('verbose', True)
    errors = []
    if verbose:
        print
    for line in csv.DictReader(open(fn)):
        
        cnt = int(line["cnt"])
        #if cnt != 10: continue
        distances_10 = map(int, line["distances_10"].split(','))
            
        lrf = LaserRangeFinder(
            laser_position=kwargs.get(
                'laser_position', line["laser_position"]),
            rpc=kwargs.get(
                'rpc', float(line["rpc"])),
            ro=kwargs.get(
                'ro', float(line["ro"])),
            blur_radius=kwargs.get(
                'blur_radius', int(line["blur_radius"])),
            filter_outliers=kwargs.get(
                'filter_outliers', bool(int(line["filter_outliers"]))),
            outlier_filter_threshold=kwargs.get(
                'outlier_filter_threshold', float(line["outlier_filter_threshold"])),
            normalize_brightness=kwargs.get(
                'normalize_brightness', bool(int(line["normalize_brightness"]))),
        )
        
        distances = lrf.get_distance(
            off_img=os.path.join(
                CURRENT_DIR, '../../docs/images/sample{cnt}/sample{cnt}-a-0.jpg'.format(cnt=cnt)),
            on_img=os.path.join(
                CURRENT_DIR, '../../docs/images/sample{cnt}/sample{cnt}-b-0.jpg'.format(cnt=cnt)),
            save_images_dir=os.path.join(
                CURRENT_DIR, '../../docs/images/sample{cnt}'.format(cnt=cnt)),
            off_img_norm_fn='_sample{cnt}-a-1.jpg'.format(cnt=cnt),
            on_img_norm_fn='_sample{cnt}-b-1.jpg'.format(cnt=cnt),
            off_img_norm_red_fn='_sample{cnt}-a-2.jpg'.format(cnt=cnt),
            on_img_norm_red_fn='_sample{cnt}-b-2.jpg'.format(cnt=cnt),
            diff_img_fn='_sample{cnt}-diff-3.jpg'.format(cnt=cnt),
            diff_blur_img_fn='_sample{cnt}-diff-4.jpg'.format(cnt=cnt),
            line_img1_fn='_sample{cnt}-line-1.jpg'.format(cnt=cnt),
            line_img2_fn='_sample{cnt}-line-2.jpg'.format(cnt=cnt),
            line_img3_fn='_sample{cnt}-line-3.jpg'.format(cnt=cnt),
        )
        _distances_10 = utils.compress_list(distances, as_int=1)
        if verbose:
            print 'distances:', cnt, _distances_10
        if assert_test:
            assert _distances_10 == distances_10
        
        errors.append(sum(abs(_a - _b) for _a, _b in zip(_distances_10, distances_10)))
    
    return sum(errors)/float(len(errors))

def product(*args):
    from functools import reduce # Valid in Python 2.6+, required in Python 3
    import operator
    return reduce(operator.mul, args, 1)

def test_optimize():
    #import numpy as np
    #from scipy.optimize import minimize
    import itertools
    
    # Define all the independent variables to test
    blur_radius = [2, 3]
    filter_outliers = [False, True]
    outlier_filter_threshold = [1, 2, 3]
    normalize_brightness = [False, True]
    
    # Generate all combinations.
    param_keys = [
        'blur_radius',
        'filter_outliers',
        'outlier_filter_threshold',
        'normalize_brightness',
    ]
    parts = [blur_radius, filter_outliers, outlier_filter_threshold, normalize_brightness]
    total = product(*map(len, parts))
    combs = itertools.product(*parts)
    
    # Test all combinations, tracking the one with the least error.
    best = (+1e999999, None)
    i = 0
    for params in combs:
        blur_radius, filter_outliers, outlier_filter_threshold, normalize_brightness = params
        i += 1
        print '%i of %i' % (i, total),
        error = test_samples(
            blur_radius=blur_radius,
            filter_outliers=filter_outliers,
            outlier_filter_threshold=outlier_filter_threshold,
            normalize_brightness=normalize_brightness,
            assert_test=False,
            verbose=False,
        )
        best = min(best, (error, params))
        print error, params
    
    print
    best_error, best_params = best
    best_params = dict(zip(param_keys, best_params))
    print 'best:', best_error, best_params
    