from Cells.PrefixStageCell import ParallelPrefix
from Cells.PrefixStageCell import ParallelCellType


class DelayCell(ParallelPrefix):
    type_enum = None
    pi_out = None
    gi_out = None
    pi2_out = None
    gi2_out = None

    def __init__(self):
        super().__init__(ParallelCellType.Delay)

    def generate_output1(self, pi_out, gi_out, pi2_out, gi2_out):
        self.pi_out = pi_out
        self.gi_out = gi_out
        self.pi2_out = pi2_out
        self.gi2_out = gi2_out
