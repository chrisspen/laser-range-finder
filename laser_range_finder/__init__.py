VERSION = (0, 1, 1)
__version__ = '.'.join(map(str, VERSION))

from .laser_range_finder import LaserRangeFinder
from . import utils
