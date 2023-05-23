from enum import Enum


class ParallelCellType(Enum):
    BlackDot = 1
    Delay = 2
    NoneType = 3


class ParallelPrefix:
    type_enum = ParallelCellType.NoneType

    pi_out = None
    gi_out = None
    pi2_out = None
    gi2_out = None

    def __init__(self, cell_type: ParallelCellType):
        self.type_enum = cell_type

    def get_type(self):
        return self.type_enum
