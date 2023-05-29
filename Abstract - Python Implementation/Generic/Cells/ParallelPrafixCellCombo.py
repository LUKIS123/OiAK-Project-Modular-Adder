from Cells.PrefixStageCell import ParallelPrefix
from Cells.PrefixStageCell import ParallelCellType


class ParallelPrefixCells(ParallelPrefix):
    type_enum = None
    pi_out = None
    gi_out = None
    pi2_out = None
    gi2_out = None

    def __init__(self):
        super().__init__(ParallelCellType.BlackDot)

    def generate_output1(self, gi_input, gi_prev_input, pi_input, pi_prev_input):
        self.pi_out = pi_input & pi_prev_input
        self.gi_out = gi_input | (gi_prev_input & pi_input)
        return [self.pi_out, self.gi_out]

    def generate_output2(self, gi_input, gi_prev_input, pi_input, pi_prev_input):
        self.pi2_out = pi_input & pi_prev_input
        self.gi2_out = gi_input | (gi_prev_input & pi_input)
        return [self.pi2_out, self.gi2_out]
