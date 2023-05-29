import math

from Utils import ArythmeticUtils
from Cells.ModuloCellCombo import HashedEnvelopedCellCombo
from Cells.ParallelPrafixCellCombo import ParallelPrefixCells
from Cells.DelayCell import DelayCell
from Cells.PrefixStageCell import ParallelPrefix
from Cells.PrefixStageCell import ParallelCellType


class Adder:
    # parameters
    n_bits = 0
    input_a_list = None
    input_b_list = None
    input_k_list = None
    # computational systems
    stages = 0
    parallel_adders_count = 0
    n_hashed_enveloped_cell_list = []
    parallel_adders_list = []
    # outputs
    c_out = 0

    def __init__(self, n_bits):
        self.stages = math.ceil(math.log2(n_bits))
        self.parallel_adders_count = int(n_bits / 2)
        self.n_bits = n_bits

    def reset(self, n_bits):
        self.stages = math.ceil(math.log2(n_bits))
        self.parallel_adders_count = int(n_bits / 2)
        self.n_bits = n_bits
        self.parallel_adders_list.clear()
        self.n_hashed_enveloped_cell_list.clear()
        self.parallel_adders_count = 0
        self.input_a_list = None
        self.input_b_list = None
        self.input_k_list = None

    def calculate(self, input_a, input_b, input_k):
        self.input_a_list = ArythmeticUtils.get_binary_list_from_int(input_a, self.n_bits)
        self.input_b_list = ArythmeticUtils.get_binary_list_from_int(input_b, self.n_bits)
        self.input_k_list = ArythmeticUtils.get_binary_list_from_int(input_k, self.n_bits)

        # inicjowanie hashed cells oraz enveloped cells do obliczen modulo
        for i in range(self.n_bits):
            self.n_hashed_enveloped_cell_list.insert(0, HashedEnvelopedCellCombo())

        # inicjowanie ukladu sumujacego parralel prefix cells
        init_counter = 0
        for i in range(self.stages):
            tmp_cells = []
            parallel_prefix_stage_cluster = 2 ** i
            for j in range(math.ceil(self.n_bits / parallel_prefix_stage_cluster)):
                for k in range(parallel_prefix_stage_cluster):
                    if init_counter == self.n_bits:
                        continue
                    if (j % 2) == 0:
                        tmp_cells.append(DelayCell())
                    else:
                        tmp_cells.append(ParallelPrefixCells())
                    init_counter += 1
            init_counter = 0
            self.parallel_adders_list.append(tmp_cells)

        # faza obliczen modularnych hashed cells oraz enveloped cells
        for i in range(self.n_bits):
            k_i = self.input_k_list[i]
            a_i = self.input_a_list[i]
            b_i = self.input_b_list[i]
            cell = self.n_hashed_enveloped_cell_list[i]
            cell.generate_hashed_cell_output(a_i, b_i)
            if i == 0:
                if k_i == 0:
                    cell.generate_enveloped_cell_output(0, cell.hi_or_ai_ifk0)
                else:
                    cell.generate_enveloped_cell_output(0, cell.ai_ifk1)
            else:
                if k_i == 0:
                    if self.input_k_list[i - 1] == 0:
                        cell.generate_enveloped_cell_output(
                            self.n_hashed_enveloped_cell_list[i - 1].gi_or_bi1_ifk0,
                            cell.hi_or_ai_ifk0)
                    else:
                        cell.generate_enveloped_cell_output(
                            self.n_hashed_enveloped_cell_list[i - 1].pi_or_bi1_ifk1,
                            cell.hi_or_ai_ifk0)
                else:
                    if self.input_k_list[i - 1] == 0:
                        cell.generate_enveloped_cell_output(
                            self.n_hashed_enveloped_cell_list[i - 1].gi_or_bi1_ifk0,
                            cell.ai_ifk1)
                    else:
                        cell.generate_enveloped_cell_output(
                            self.n_hashed_enveloped_cell_list[i - 1].pi_or_bi1_ifk1,
                            cell.ai_ifk1)

        print()
