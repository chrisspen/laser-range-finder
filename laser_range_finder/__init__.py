VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))

from .laser_range_finder import LaserRangeFinder, pixels_to_distance
from . import utils
