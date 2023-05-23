import math

from Cells.ModuloCellCombo import HashedEnvelopedCombo
from Cells.ParallelPrefixCellCombo import Parallel
from Utils import BinaryArithmeticUtils


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
        self.input_a_list = BinaryArithmeticUtils.get_binary_list_from_int(input_a, self.n_bits)
        self.input_b_list = BinaryArithmeticUtils.get_binary_list_from_int(input_b, self.n_bits)
        self.input_k_list = BinaryArithmeticUtils.get_binary_list_from_int(input_k, self.n_bits)

        # inicjowanie hashed cells oraz enveloped cells do obliczen modulo
        for i in range(self.n_bits):
            self.n_hashed_enveloped_cell_list.append(HashedEnvelopedCombo())

        # inicjowanie ukladu sumujacego parralel prefix cells
        for i in range(self.stages):
            tmp_list = []
            for j in range(self.parallel_adders_count):
                tmp_list.append(Parallel())
            self.parallel_adders_list.append(tmp_list)

        # faza obliczen modularnych hashed cells oraz enveloped cells
        for i in range(self.n_bits - 1, -1, -1):
            k_i = self.input_k_list[i]
            a_i = self.input_a_list[i]
            b_i = self.input_b_list[i]
            cell = self.n_hashed_enveloped_cell_list[i]

            cell.generate_hashed_cell_output(a_i, b_i)

            if i == self.n_bits - 1:
                if k_i == 0:
                    cell.generate_enveloped_cell_output(0, cell.hi_or_ai_ifk0)
                else:
                    cell.generate_enveloped_cell_output(0, cell.ai_ifk1)
            else:
                if k_i == 0:
                    if self.input_k_list[i + 1] == 0:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i + 1].gi_or_bi1_ifk0,
                                                            cell.hi_or_ai_ifk0)
                    else:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i + 1].pi_or_bi1_ifk1,
                                                            cell.hi_or_ai_ifk0)
                else:
                    if self.input_k_list[i + 1] == 0:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i + 1].gi_or_bi1_ifk0,
                                                            cell.ai_ifk1)
                    else:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i + 1].pi_or_bi1_ifk1,
                                                            cell.ai_ifk1)

        # faza obliczen parallel prefix adder
        level0_index = self.n_bits - 1
        level1_index = self.n_bits - 3
        level2_index = self.n_bits - 5

        # indeksy pomocnicze dla stage 2
        level1_parallel_index = len(self.parallel_adders_list[0]) - 1
        level1_cell_indicator = len(self.parallel_adders_list[1]) - 1

        # indeksy pomocnicze dla stage 3
        level2_cell_indicator = len(self.parallel_adders_list[2]) - 1
        level2_level1_parallel_index12 = len(self.parallel_adders_list[1]) - 2
        level2_level1_parallel_index34 = len(self.parallel_adders_list[1]) - 3
        level2_level0_parallel_index = len(self.parallel_adders_list[0]) - 3

        for level in range(self.stages):
            # parallel_prefix_stage_indicator = 2 ** level
            # parallel_prefix_stage_window = 2 ** (level + 1)
            # parallel_prefix_stage_cluster = 2 ** level

            for j in range(len(self.parallel_adders_list[level]) - 1, -1, -1):
                if level == 0 and level0_index > 0:

                    cell = self.parallel_adders_list[level][j]
                    cell.generate_output1(self.n_hashed_enveloped_cell_list[level0_index - 1].gi_or_bi1_ifk0,
                                          self.n_hashed_enveloped_cell_list[level0_index].gi_or_bi1_ifk0,
                                          self.n_hashed_enveloped_cell_list[level0_index - 1].pi_or_bi1_ifk1,
                                          self.n_hashed_enveloped_cell_list[level0_index].pi_or_bi1_ifk1
                                          )
                    cell.generate_output2(self.n_hashed_enveloped_cell_list[level0_index - 1].gi_prim,
                                          self.n_hashed_enveloped_cell_list[level0_index].gi_prim,
                                          self.n_hashed_enveloped_cell_list[level0_index - 1].pi_prim,
                                          self.n_hashed_enveloped_cell_list[level0_index].pi_prim
                                          )
                    level0_index -= 2
                elif level == 1 and level1_index >= 0 and level1_parallel_index >= 0:

                    cell1 = self.parallel_adders_list[level][level1_cell_indicator]
                    level1_cell_indicator -= 1
                    cell2 = self.parallel_adders_list[level][level1_cell_indicator]

                    cell1.generate_output1(self.n_hashed_enveloped_cell_list[level1_index].gi_or_bi1_ifk0,
                                           self.parallel_adders_list[0][level1_parallel_index].gi_out,
                                           self.n_hashed_enveloped_cell_list[level1_index].pi_or_bi1_ifk1,
                                           self.parallel_adders_list[0][level1_parallel_index].pi_out
                                           )
                    cell1.generate_output2(self.n_hashed_enveloped_cell_list[level1_index].gi_prim,
                                           self.parallel_adders_list[0][level1_parallel_index].gi2_out,
                                           self.n_hashed_enveloped_cell_list[level1_index].pi_prim,
                                           self.parallel_adders_list[0][level1_parallel_index].pi2_out
                                           )
                    if level1_index > 0 and level1_parallel_index > 0:
                        cell2.generate_output1(self.parallel_adders_list[0][level1_parallel_index - 1].gi_out,
                                               self.parallel_adders_list[0][level1_parallel_index].gi_out,
                                               self.parallel_adders_list[0][level1_parallel_index - 1].pi_out,
                                               self.parallel_adders_list[0][level1_parallel_index].pi_out
                                               )
                        cell2.generate_output2(self.parallel_adders_list[0][level1_parallel_index - 1].gi2_out,
                                               self.parallel_adders_list[0][level1_parallel_index].gi2_out,
                                               self.parallel_adders_list[0][level1_parallel_index - 1].pi2_out,
                                               self.parallel_adders_list[0][level1_parallel_index].pi2_out,
                                               )
                    level1_index -= 4
                    level1_parallel_index -= 2
                    level1_cell_indicator -= 1
                elif level == 2 and level2_index >= 0 and level2_level1_parallel_index12 >= 0:

                    cell1 = self.parallel_adders_list[level][level2_cell_indicator]
                    cell2 = None
                    cell3 = None
                    cell4 = None

                    if level2_cell_indicator > 0:
                        level2_cell_indicator -= 1
                        cell2 = self.parallel_adders_list[level][level2_cell_indicator]
                    if level2_cell_indicator > 0:
                        level2_cell_indicator -= 1
                        cell3 = self.parallel_adders_list[level][level2_cell_indicator]
                    if level2_cell_indicator > 0:
                        level2_cell_indicator -= 1
                        cell4 = self.parallel_adders_list[level][level2_cell_indicator]

                    cell1.generate_output1(self.n_hashed_enveloped_cell_list[level2_index].gi_or_bi1_ifk0,
                                           self.parallel_adders_list[1][level2_level1_parallel_index12].gi_out,
                                           self.n_hashed_enveloped_cell_list[level2_index].pi_or_bi1_ifk1,
                                           self.parallel_adders_list[1][level2_level1_parallel_index12].pi_out
                                           )
                    cell1.generate_output2(self.n_hashed_enveloped_cell_list[level2_index].gi_prim,
                                           self.parallel_adders_list[1][level2_level1_parallel_index12].gi2_out,
                                           self.n_hashed_enveloped_cell_list[level2_index].pi_prim,
                                           self.parallel_adders_list[1][level2_level1_parallel_index12].pi2_out
                                           )
                    if cell2 is not None:
                        level2_level1_parallel_index12 -= 1
                        cell2.generate_output1(self.parallel_adders_list[0][level2_level0_parallel_index].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 1].gi_out,
                                               self.parallel_adders_list[0][level2_level0_parallel_index].pi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 1].pi_out
                                               )
                        cell2.generate_output2(self.parallel_adders_list[0][level2_level0_parallel_index].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 1].gi2_out,
                                               self.parallel_adders_list[0][level2_level0_parallel_index].pi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 1].pi2_out
                                               )
                    if cell3 is not None:
                        level2_level1_parallel_index12 -= 1
                        cell3.generate_output1(self.parallel_adders_list[1][level2_level1_parallel_index34].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 2].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index34].pi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 2].pi_out
                                               )
                        cell3.generate_output2(self.parallel_adders_list[1][level2_level1_parallel_index34].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 2].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index34].pi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 2].pi2_out
                                               )

                    if cell4 is not None:
                        level2_level1_parallel_index12 -= 1
                        level2_level1_parallel_index34 -= 1
                        cell4.generate_output1(self.parallel_adders_list[1][level2_level1_parallel_index34].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 3].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index34].pi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 3].pi_out
                                               )
                        cell4.generate_output2(self.parallel_adders_list[1][level2_level1_parallel_index34].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 3].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index34].pi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index12 + 3].pi2_out
                                               )
                    level2_level1_parallel_index12 -= 1
                    level2_level1_parallel_index34 -= 1
                    level2_index -= 8
                    level2_cell_indicator -= 1

        # koniec fazy parallel prefix adder

        # zrobione dla n=7 bitow
        self.c_out = self.parallel_adders_list[2][0].gi2_out

        bit0 = self.n_hashed_enveloped_cell_list[6].hi_or_ai_ifk0 if self.c_out == 0 else \
            self.n_hashed_enveloped_cell_list[6].hi_prim

        bit1 = self.n_hashed_enveloped_cell_list[6].gi_or_bi1_ifk0 ^ self.n_hashed_enveloped_cell_list[5].hi_or_ai_ifk0
        bit2 = self.parallel_adders_list[0][2].gi_out ^ self.n_hashed_enveloped_cell_list[4].hi_or_ai_ifk0
        bit3 = self.parallel_adders_list[1][2].gi_out ^ self.n_hashed_enveloped_cell_list[3].hi_or_ai_ifk0
        bit4 = self.parallel_adders_list[1][1].gi_out ^ self.n_hashed_enveloped_cell_list[2].hi_or_ai_ifk0
        bit5 = self.parallel_adders_list[2][2].gi_out ^ self.n_hashed_enveloped_cell_list[1].hi_or_ai_ifk0
        bit6 = self.parallel_adders_list[2][1].gi_out ^ self.n_hashed_enveloped_cell_list[0].hi_or_ai_ifk0

        bit1c = self.n_hashed_enveloped_cell_list[6].gi_prim ^ self.n_hashed_enveloped_cell_list[5].hi_prim
        bit2c = self.parallel_adders_list[0][2].gi2_out ^ self.n_hashed_enveloped_cell_list[4].hi_prim
        bit3c = self.parallel_adders_list[1][2].gi2_out ^ self.n_hashed_enveloped_cell_list[3].hi_prim
        bit4c = self.parallel_adders_list[1][1].gi2_out ^ self.n_hashed_enveloped_cell_list[2].hi_prim
        bit5c = self.parallel_adders_list[2][2].gi2_out ^ self.n_hashed_enveloped_cell_list[1].hi_prim
        bit6c = self.parallel_adders_list[2][1].gi2_out ^ self.n_hashed_enveloped_cell_list[0].hi_prim

        print(f"Vector A: {self.input_a_list}")
        print(f"Vector B: {self.input_b_list}")
        print(f"Vector K: {self.input_k_list}")
        print(f"\nCarry = {self.c_out}\n")
        print("Output for Carry = 0:")
        print(
            f"[ {bit6} {bit5} {bit4} {bit3} {bit2} {bit1} {bit0} ] => "
            f"{BinaryArithmeticUtils.get_int_from_binary([bit6, bit5, bit4, bit3, bit2, bit1, bit0])}")
        print("Output for carry = 1:")
        print(
            f"[ {bit6c} {bit5c} {bit4c} {bit3c} {bit2c} {bit1c} {bit0} ] => "
            f"{BinaryArithmeticUtils.get_int_from_binary([bit6c, bit5c, bit4c, bit3c, bit2c, bit1c, bit0])}")
        print("============================================================================================")

        # TODO: n <= 8
        self.c_out = self.parallel_adders_list[-1][0].gi2_out
        hashed_cell_index = len(self.n_hashed_enveloped_cell_list) - 2
        output_list = []

        bit0 = self.n_hashed_enveloped_cell_list[-1].hi_or_ai_ifk0 if self.c_out == 0 else \
            self.n_hashed_enveloped_cell_list[-1].hi_prim
        output_list.insert(0, bit0)

        if self.c_out == 0:
            bit1 = self.n_hashed_enveloped_cell_list[hashed_cell_index + 1].gi_or_bi1_ifk0 ^ \
                   self.n_hashed_enveloped_cell_list[
                       hashed_cell_index].hi_or_ai_ifk0
        else:
            bit1 = self.n_hashed_enveloped_cell_list[hashed_cell_index + 1].gi_prim ^ \
                   self.n_hashed_enveloped_cell_list[
                       hashed_cell_index].hi_prim

        output_list.insert(0, bit1)

        hashed_cell_index -= 1
        for i in range(0, self.stages, +1):
            counter = 0
            for j in range(2 ** i, -1, -1):
                if counter == 2 ** i or len(output_list) == self.n_bits:
                    break
                try:
                    if self.c_out == 0:
                        bit_n = self.parallel_adders_list[i][-(counter + 1)].gi_out ^ \
                                self.n_hashed_enveloped_cell_list[
                                    hashed_cell_index].hi_or_ai_ifk0
                    else:
                        bit_n = self.parallel_adders_list[i][-(counter + 1)].gi2_out ^ \
                                self.n_hashed_enveloped_cell_list[hashed_cell_index].hi_prim
                    output_list.insert(0, bit_n)
                    hashed_cell_index -= 1
                    counter += 1
                except IndexError:
                    continue

        print(f"{output_list} => {BinaryArithmeticUtils.get_int_from_binary(output_list)}")
