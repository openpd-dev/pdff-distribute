__author__ = "Zhenyu Wei"
__maintainer__ = "Zhenyu Wei" 
__email__ = "zhenyuwei99@gmail.com"
__copyright__ = "Copyright 2021-2021, Southeast University and Zhenyu Wei"
__license__ = "GPLv3"

ELEMENT_MASS = {
    'H': 1.00800,
    'C': 12.01100, 
    'N': 14.00700,
    'O': 15.9990,
    'S': 32.06000
}

from pdff_script.pdbManipulator import PDBManipulator

__all__ = [
    'PDBManipulator'
]