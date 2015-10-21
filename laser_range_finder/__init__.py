VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))

from .laser_range_finder import LaserRangeFinder
from . import utils
