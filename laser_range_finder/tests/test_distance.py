import os
import pytest

from laser_range_finder import LaserRangeFinder, utils

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def test_sample():
    
    lrf = LaserRangeFinder()
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample1/sample-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample1/sample-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images/sample1'),
        off_img_norm_fn='_sample-a-1.jpg',
        on_img_norm_fn='_sample-b-1.jpg',
        off_img_norm_red_fn='_sample-a-2.jpg',
        on_img_norm_red_fn='_sample-b-2.jpg',
        diff_img_fn='_sample-diff-3.jpg',
        diff_blur_img_fn='_sample-diff-4.jpg',
        line_img1_fn='_sample-line-1.jpg',
        line_img2_fn='_sample-line-2.jpg',
        line_img3_fn='_sample-line-3.jpg',
    )
    print 'distances:', distances

def test_sample2():
    
    lrf = LaserRangeFinder(
        laser_position='bottom',
        rpc=0.00329743488774,
        ro=-0.00494930380293,
        blur_radius=2,
        outlier_filter_threshold=1,
        normalize_brightness=0,
    )
    lrf.blur_radius = 2
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample2/sample2-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample2/sample2-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images/sample2'),
        off_img_norm_fn='_sample2-a-1.jpg',
        on_img_norm_fn='_sample2-b-1.jpg',
        off_img_norm_red_fn='_sample2-a-2.jpg',
        on_img_norm_red_fn='_sample2-b-2.jpg',
        diff_img_fn='_sample2-diff-3.jpg',
        diff_blur_img_fn='_sample2-diff-4.jpg',
        line_img1_fn='_sample2-line-1.jpg',
        line_img2_fn='_sample2-line-2.jpg',
        line_img3_fn='_sample2-line-3.jpg',
    )
    print 'distances:', distances
    distances_10 = utils.compress_list(distances, as_int=1)
    print 'distances:', distances_10
    assert distances_10 == [-1, 288, 296, 324, 345, 309, 287, 327, 320, 297]

def test_sample3():
    
    lrf = LaserRangeFinder(
        laser_position='top',
        rpc=0.00329743488774,
        ro=-0.00494930380293,
        blur_radius=2,
        outlier_filter_threshold=1,
        normalize_brightness=0,
    )
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample3/sample3-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample3/sample3-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images/sample3'),
        off_img_norm_fn='_sample3-a-1.jpg',
        on_img_norm_fn='_sample3-b-1.jpg',
        off_img_norm_red_fn='_sample3-a-2.jpg',
        on_img_norm_red_fn='_sample3-b-2.jpg',
        diff_img_fn='_sample3-diff-3.jpg',
        diff_blur_img_fn='_sample3-diff-4.jpg',
        line_img1_fn='_sample3-line-1.jpg',
        line_img2_fn='_sample3-line-2.jpg',
        line_img3_fn='_sample3-line-3.jpg',
    )
    print 'distances:', distances
    distances_10 = utils.compress_list(distances, as_int=1)
    print 'distances:', distances_10
    assert distances_10 == [1318, 4552, 7479, 185, 180, 181, 187, 2327, 4495, 4495]

def test_sample4():
    
    lrf = LaserRangeFinder(
        laser_position='top',
        rpc=0.00329743488774,
        ro=-0.00494930380293,
        blur_radius=2,
        outlier_filter_threshold=3,
        normalize_brightness=0,
    )
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample4/sample4-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample4/sample4-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images/sample4'),
        off_img_norm_fn='_sample4-a-1.jpg',
        on_img_norm_fn='_sample4-b-1.jpg',
        off_img_norm_red_fn='_sample4-a-2.jpg',
        on_img_norm_red_fn='_sample4-b-2.jpg',
        diff_img_fn='_sample4-diff-3.jpg',
        diff_blur_img_fn='_sample4-diff-4.jpg',
        line_img1_fn='_sample4-line-1.jpg',
        line_img2_fn='_sample4-line-2.jpg',
        line_img3_fn='_sample4-line-3.jpg',
    )
    print 'distances:', distances
    distances_10 = utils.compress_list(distances, as_int=1)
    print 'distances:', distances_10
    assert distances_10 == [2271, 3251, 390, 390, 381, 368, 368, 368, 368, 368]
