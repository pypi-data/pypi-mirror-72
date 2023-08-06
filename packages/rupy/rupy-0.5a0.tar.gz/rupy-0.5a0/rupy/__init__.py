__version__ = "0.5a"
from rupy.buf import buf
from rupy.hexdump import hexdump
from rupy import fields
from rupy.fields import FieldMap
from rupy.ranges import Range
from rupy.stream import Stream
import sys
if sys.version_info >= (3, 6):
    from rupy.pretty import *
