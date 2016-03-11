VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))

try:
    from .laser_range_finder import LaserRangeFinder, pixels_to_distance, calibrate
    from . import utils
except ImportError:
    pass
    