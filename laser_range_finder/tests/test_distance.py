import os
import pytest

from laser_range_finder import LaserRangeFinder, utils

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def test_sample():
    
    lrf = LaserRangeFinder()
    distances = lrf.get_distance(
        off_img=os.path.join(CURRENT_DIR, '../../docs/images/sample-a-0.jpg'),
        on_img=os.path.join(CURRENT_DIR, '../../docs/images/sample-b-0.jpg'),
        save_images_dir=os.path.join(CURRENT_DIR, '../../docs/images'),
        off_img_norm_fn='sample-a-1.jpg',
        on_img_norm_fn='sample-b-1.jpg',
        off_img_norm_red_fn='sample-a-2.jpg',
        on_img_norm_red_fn='sample-b-2.jpg',
        diff_img_fn='sample-diff-3.jpg',
        line_img1_fn='sample-line-1.jpg',
        line_img2_fn='sample-line-2.jpg',
        line_img3_fn='sample-line-3.jpg',
    )
    print 'distances:', distances
