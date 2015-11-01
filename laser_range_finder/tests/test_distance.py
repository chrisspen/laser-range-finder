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
        off_img_norm_fn='sample-a-1.jpg',
        on_img_norm_fn='sample-b-1.jpg',
        off_img_norm_red_fn='sample-a-2.jpg',
        on_img_norm_red_fn='sample-b-2.jpg',
        diff_img_fn='sample-diff-3.jpg',
        diff_blur_img_fn='sample-diff-4.jpg',
        line_img1_fn='sample-line-1.jpg',
        line_img2_fn='sample-line-2.jpg',
        line_img3_fn='sample-line-3.jpg',
    )
    print 'distances:', distances

def test_sample2():
    
    lrf = LaserRangeFinder(ro=0)
    lrf.blur_radius = 2
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample2/sample2-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample2/sample2-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images/sample2'),
        off_img_norm_fn='sample2-a-1.jpg',
        on_img_norm_fn='sample2-b-1.jpg',
        off_img_norm_red_fn='sample2-a-2.jpg',
        on_img_norm_red_fn='sample2-b-2.jpg',
        diff_img_fn='sample2-diff-3.jpg',
        diff_blur_img_fn='sample2-diff-4.jpg',
        line_img1_fn='sample2-line-1.jpg',
        line_img2_fn='sample2-line-2.jpg',
        line_img3_fn='sample2-line-3.jpg',
    )
    print 'distances:', distances
    print 'distances:', utils.compress_list(distances, as_int=1)
