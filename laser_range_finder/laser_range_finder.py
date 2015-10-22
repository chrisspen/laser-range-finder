from __future__ import print_function
import os
from math import pi, tan

from PIL import Image
from PIL.ImageChops import difference
import numpy as np

from . import utils

class LaserRangeFinder(object):
    
    def __init__(self, **kwargs):
        
        # Camera's verticial field-of-view in degrees.
        self.vert_fov_deg = float(kwargs.pop('vert_fov_deg', 41.41))
        
        # Camera's horizontal field-of-view in degrees.
        self.horz_fov_deg = float(kwargs.pop('horz_fov_deg', 53.50))
        
        # Radian offset.
        self.ro = float(kwargs.pop('ro', -0.21))
        
        # Distance between camera center and laser.
        self.h = float(kwargs.pop('h', 22.5))
        
        # If true, laser pixels that are less bright than the mean brightness minus
        # a factor of the standard deviation will be considered noise and ignored.
        self.filter_outliers = bool(kwargs.pop('filter_outliers', True))
        
        # The number of standard deviations below the mean above which a laser pixel will
        # be considered valid.
        self.outlier_filter_threshold = float(kwargs.pop('outlier_filter_threshold', 1))
        
    def get_distance(self, off_img, on_img, save_images_dir=None, **kwargs):
        """
        Calculates distance using two images.
        
        Keyword arguments:
        off_img -- a stream or filename of an image assumed to have no laser projection
        on_img -- a stream of filename of an image assumed to have a laser projection
        """
        
        if save_images_dir:
            assert os.path.isdir(save_images_dir), 'Invalid directory: %s' % save_images_dir
        
        if isinstance(off_img, basestring):
            off_img = Image.open(os.path.expanduser(off_img)).convert('RGBA')
            
        if isinstance(on_img, basestring):
            on_img = Image.open(os.path.expanduser(on_img)).convert('RGBA')
        
        # Normalize image brightness.
        off_img = Image.fromarray(utils.normalize(np.array(off_img)).astype('uint8'), 'RGBA')
        if save_images_dir:
            off_img.save(os.path.join(save_images_dir, kwargs.pop('off_img_norm_fn', 'off_img_norm.jpg')))
        on_img = Image.fromarray(utils.normalize(np.array(on_img)).astype('uint8'), 'RGBA')
        if save_images_dir:
            on_img.save(os.path.join(save_images_dir, kwargs.pop('on_img_norm_fn', 'on_img_norm.jpg')))
        
        # Strip out non-red channels.
        off_img = utils.only_red(off_img)
        if save_images_dir:
            off_img.save(os.path.join(save_images_dir, kwargs.pop('off_img_norm_red_fn', 'off_img_norm_red.jpg')))
        on_img = utils.only_red(on_img)
        if save_images_dir:
            on_img.save(os.path.join(save_images_dir, kwargs.pop('on_img_norm_red_fn', 'on_img_norm_red.jpg')))
                
        # Calculate difference.
        # The laser line should now be the brightest pixels. 
        diff_img = difference(off_img, on_img)
        if save_images_dir:
            diff_img.save(os.path.join(save_images_dir, kwargs.pop('diff_img_fn', 'diff_img.jpg')))
        
        # Estimate the pixels that are the laser by
        # finding the row in each column with maximum brightness.
        width, height = size = diff_img.size
        x = diff_img.convert('L')
        if save_images_dir:
            # If saving a result image, create an empty black image which we'll later map
            # the laser line into.
            out1 = Image.new("L", x.size, "black")
            pix1 = out1.load()
            out2 = Image.new("L", x.size, "black")
            pix2 = out2.load()
            out3 = Image.new("L", x.size, "black")
            pix3 = out3.load()
        y = np.asarray(x.getdata(), dtype=np.float64).reshape((x.size[1], x.size[0]))
        laser_measurements = [0]*width # [row]
        laser_brightness = [0]*width # [brightness]
        for col_i in xrange(y.shape[1]):
            col_max = max([(y[row_i][col_i], row_i) for row_i in xrange(y.shape[0])])
            col_max_brightness, col_max_row = col_max
            #print col_i, col_max
            #pix[col_i, col_max_row] = 255
            laser_measurements[col_i] = col_max_row
            laser_brightness[col_i] = col_max_brightness
            
        # Ignore all columns with dim brightness outliers.
        # These usually indicate a region where the laser is absorbed or otherwise scattered
        # too much to see.
        if self.filter_outliers:
            brightness_std = np.std(laser_brightness)
            brightness_mean = np.mean(laser_brightness)
            outlier_level = brightness_mean - brightness_std * self.outlier_filter_threshold
        final_measurements = [-1]*width # [brightest row]
        for col_i, col_max_row in enumerate(laser_measurements):
        
            if save_images_dir:    
                pix1[col_i, col_max_row] = 255
                    
            if not self.filter_outliers \
            or (self.filter_outliers and laser_brightness[col_i] > outlier_level):
                if save_images_dir:
                    pix2[col_i, col_max_row] = 255
                    
            # Assuming the laser is mounted below the camera,
            # we can assume all points above the centerline are noise.
            if col_max_row < height/2:
                continue
                
            if not self.filter_outliers \
            or (self.filter_outliers and laser_brightness[col_i] > outlier_level):
                if save_images_dir:
                    pix3[col_i, col_max_row] = 255
                final_measurements[col_i] = col_max_row
        
        if save_images_dir:
            out1.save(os.path.join(save_images_dir, kwargs.pop('line_img1_fn', 'line1.jpg')))
            out2.save(os.path.join(save_images_dir, kwargs.pop('line_img2_fn', 'line2.jpg')))
            out3.save(os.path.join(save_images_dir, kwargs.pop('line_img3_fn', 'line3.jpg')))
        
        #https://sites.google.com/site/todddanko/home/webcam_laser_ranger
        #https://shaneormonde.wordpress.com/2014/01/25/webcam-laser-rangefinder/
        
        #https://www.raspberrypi.org/documentation/hardware/camera.md
        #Horizontal field of view     53.50 +/- 0.13 degrees
        #Vertical field of view     41.41 +/- 0.11 degress
        
        # h = distance between laser and camera in mm
        
        # D = h/tan(theta)
        # theta = pfc*rpc + ro
        
        # pfc = ? # number of pixels from center of focal plane
        # Calculated per pixel.
        
        # rpc = ? # radians per pixel pitch
        # 180 deg=pi rad
        rpc = (self.vert_fov_deg*pi/180.)/height
        
        # ro = ? # radian offset (compensates for alignment errors)
        
        # Convert the pixel measurements to distance.
        D_lst = []
        for laser_row_i in final_measurements:
            if laser_row_i < 0:
                # No laser could be detected in this column.
                D_lst.append(laser_row_i)
            else:
                pfc = abs(laser_row_i - height)
                D = self.h/tan(pfc*rpc + self.ro)
                D_lst.append(D)
            
        return D_lst
    