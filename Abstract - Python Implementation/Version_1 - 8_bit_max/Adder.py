import math

from Cells.ModuloCellCombo import HashedEnvelopedCombo
from Cells.ParallelPrefixCellCombo import Parallel
from Utility import BinaryArithmeticUtils


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
        self.input_a_list = BinaryArithmeticUtils.get_binary_list_aligned_from_int(input_a, self.n_bits)
        self.input_b_list = BinaryArithmeticUtils.get_binary_list_aligned_from_int(input_b, self.n_bits)
        self.input_k_list = BinaryArithmeticUtils.get_binary_list_aligned_from_int(input_k, self.n_bits)

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
        print(f"Vector A: {self.input_a_list}")
        print(f"Vector B: {self.input_b_list}")
        print(f"Vector K: {self.input_k_list}")

        # obliczanie carry
        if self.input_k_list[0] == 0:
            last_b_i = self.n_hashed_enveloped_cell_list[0].gi_or_bi1_ifk0
        else:
            last_b_i = self.n_hashed_enveloped_cell_list[0].pi_or_bi1_ifk1

        if last_b_i == 0:
            self.c_out = self.parallel_adders_list[-1][0].gi2_out
        else:
            self.c_out = self.parallel_adders_list[-1][0].gi_out

        # obliczanie wynikow dla carry 0 i 1 oraz wlasciwego wyniku
        hashed_cell_index = len(self.n_hashed_enveloped_cell_list) - 2
        carry_output_list = []
        no_carry_output_list = []
        final_output_list = []

        no_carry_output_list.insert(0, self.n_hashed_enveloped_cell_list[-1].hi_or_ai_ifk0)
        carry_output_list.insert(0, self.n_hashed_enveloped_cell_list[-1].hi_prim)

        bit0 = self.n_hashed_enveloped_cell_list[-1].hi_or_ai_ifk0 if self.c_out == 0 else \
            self.n_hashed_enveloped_cell_list[-1].hi_prim
        final_output_list.insert(0, bit0)

        bit1 = self.n_hashed_enveloped_cell_list[hashed_cell_index + 1].gi_or_bi1_ifk0 ^ \
               self.n_hashed_enveloped_cell_list[hashed_cell_index].hi_or_ai_ifk0
        bit1c = self.n_hashed_enveloped_cell_list[hashed_cell_index + 1].gi_prim ^ self.n_hashed_enveloped_cell_list[
            hashed_cell_index].hi_prim

        if self.c_out == 0:
            final_output_list.insert(0, bit1)
        else:
            final_output_list.insert(0, bit1c)

        no_carry_output_list.insert(0, bit1)
        carry_output_list.insert(0, bit1c)

        hashed_cell_index -= 1
        for i in range(0, self.stages, +1):
            counter = 0
            for j in range(2 ** i, -1, -1):
                if counter == 2 ** i or len(final_output_list) == self.n_bits:
                    break
                try:
                    bit_n = self.parallel_adders_list[i][-(counter + 1)].gi_out ^ \
                            self.n_hashed_enveloped_cell_list[
                                hashed_cell_index].hi_or_ai_ifk0

                    bit_c_n = self.parallel_adders_list[i][-(counter + 1)].gi2_out ^ self.n_hashed_enveloped_cell_list[
                        hashed_cell_index].hi_prim

                    if self.c_out == 0:
                        final_output_list.insert(0, bit_n)
                    else:
                        final_output_list.insert(0, bit_c_n)

                    no_carry_output_list.insert(0, bit_n)
                    carry_output_list.insert(0, bit_c_n)
                    hashed_cell_index -= 1
                    counter += 1
                except IndexError:
                    break

        print("--------------------------------")
        print("Output for Carry = 0:")
        print(f"{no_carry_output_list} ==> {BinaryArithmeticUtils.get_int_from_binary(no_carry_output_list)}")
        print("Output for carry = 1:")
        print(f"{carry_output_list} ==> {BinaryArithmeticUtils.get_int_from_binary(carry_output_list)}")
        print(f"\nCarry = {self.c_out}")
        print("OUTPUT:")
        print(f"{final_output_list} ==> {BinaryArithmeticUtils.get_int_from_binary(final_output_list)}")
        print("--------------------------------")
