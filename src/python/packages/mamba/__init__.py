"""
The mamba package contains all the mathematical morphology operators
defined in mamba that apply to 2D images.
"""

VERSION = "2.0.1"

# importing all the modules
from .error import *
from .grids import *
from .base import *
from .copies import *
from .arithmetic import *
from .conversion import *
from .draw import *
from .erodil import *
from .erodilLarge import *
from .openclose import *
from .contrasts import *
from .geodesy import *
from .filter import *
from .residues import *
from .thinthick import *
from .measure import *
from .segment import *
from .statistic import *
from .miscellaneous import *
from .hierarchies import *
from .partitions import *
from .extrema import *
from .labellings import *

