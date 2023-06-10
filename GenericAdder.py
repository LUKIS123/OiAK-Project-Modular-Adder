import math

from Cells.DelayCell import DelayCell
from Cells.ModuloCellCombo import HashedEnvelopedCellCombo
from Cells.ParallelPrafixCellCombo import ParallelPrefixCells
from Utils import ArithmeticUtils


class Adder:
    # parameters
    n_bits = 0
    input_a_list = None
    input_b_list = None
    input_k_list = None
    # computational systems
    stages = 0
    n_hashed_enveloped_cell_list = []
    parallel_adders_list = []
    # outputs
    c_out = 0

    def __init__(self, n_bits: int):
        self.stages = math.ceil(math.log2(n_bits))
        self.n_bits = n_bits

    def reset(self, n_bits: int):
        self.stages = math.ceil(math.log2(n_bits))
        self.n_bits = n_bits
        self.parallel_adders_list.clear()
        self.n_hashed_enveloped_cell_list.clear()
        self.input_a_list = None
        self.input_b_list = None
        self.input_k_list = None

    def calculate(self, input_a: int, input_b: int, input_k: int, is_second_mode: bool, k_vector_if_second_mode: list):
        self.input_a_list = ArithmeticUtils.get_binary_aligned_list_from_int(input_a, self.n_bits)
        self.input_b_list = ArithmeticUtils.get_binary_aligned_list_from_int(input_b, self.n_bits)
        if is_second_mode:
            self.input_k_list = k_vector_if_second_mode
        else:
            self.input_k_list = ArithmeticUtils.get_binary_aligned_list_from_int(input_k, self.n_bits)

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
            k_i = self.input_k_list[self.n_bits - (i + 1)]
            a_i = self.input_a_list[self.n_bits - (i + 1)]
            b_i = self.input_b_list[self.n_bits - (i + 1)]
            cell = self.n_hashed_enveloped_cell_list[i]
            cell.generate_hashed_cell_output(a_i, b_i)
            if i == 0:
                if k_i == 0:
                    cell.generate_enveloped_cell_output(0, cell.hi_or_ai_ifk0)
                else:
                    cell.generate_enveloped_cell_output(0, cell.ai_ifk1)
            else:
                if k_i == 0:
                    if self.input_k_list[self.n_bits - i] == 0:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i - 1].gi_or_bi1_ifk0,
                                                            cell.hi_or_ai_ifk0)
                    else:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i - 1].pi_or_bi1_ifk1,
                                                            cell.hi_or_ai_ifk0)
                else:
                    if self.input_k_list[self.n_bits - i] == 0:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i - 1].gi_or_bi1_ifk0,
                                                            cell.ai_ifk1)
                    else:
                        cell.generate_enveloped_cell_output(self.n_hashed_enveloped_cell_list[i - 1].pi_or_bi1_ifk1,
                                                            cell.ai_ifk1)

        # faza obliczen parallel prefix
        for level in range(self.stages):
            parallel_prefix_stage_cluster = 2 ** level
            counter = 0
            is_delay_cell = True
            previous_above_cell_index = (2 ** level) - 1
            for index in range(len(self.parallel_adders_list[level])):
                if level == 0:
                    cell = self.parallel_adders_list[level][index]
                    if is_delay_cell:
                        cell.generate_output1(self.n_hashed_enveloped_cell_list[index].pi_or_bi1_ifk1,
                                              self.n_hashed_enveloped_cell_list[index].gi_or_bi1_ifk0,
                                              self.n_hashed_enveloped_cell_list[index].pi_prim,
                                              self.n_hashed_enveloped_cell_list[index].gi_prim)
                    else:
                        cell.generate_output1(self.n_hashed_enveloped_cell_list[index].gi_or_bi1_ifk0,
                                              self.n_hashed_enveloped_cell_list[index - 1].gi_or_bi1_ifk0,
                                              self.n_hashed_enveloped_cell_list[index].pi_or_bi1_ifk1,
                                              self.n_hashed_enveloped_cell_list[index - 1].pi_or_bi1_ifk1)

                        cell.generate_output2(self.n_hashed_enveloped_cell_list[index].gi_prim,
                                              self.n_hashed_enveloped_cell_list[index - 1].gi_prim,
                                              self.n_hashed_enveloped_cell_list[index].pi_prim,
                                              self.n_hashed_enveloped_cell_list[index - 1].pi_prim)
                    counter += 1

                else:
                    above_cell = self.parallel_adders_list[level - 1][index]
                    previous_above_cell = None
                    try:
                        previous_above_cell = self.parallel_adders_list[level - 1][previous_above_cell_index]
                    except IndexError:
                        pass

                    if is_delay_cell:
                        self.parallel_adders_list[level][index].generate_output1(
                            above_cell.pi_out,
                            above_cell.gi_out,
                            above_cell.pi2_out,
                            above_cell.gi2_out
                        )
                    else:
                        self.parallel_adders_list[level][index].generate_output1(
                            above_cell.gi_out,
                            previous_above_cell.gi_out,
                            above_cell.pi_out,
                            previous_above_cell.pi_out
                        )
                        self.parallel_adders_list[level][index].generate_output2(
                            above_cell.gi2_out,
                            previous_above_cell.gi2_out,
                            above_cell.pi2_out,
                            previous_above_cell.pi2_out
                        )
                    counter += 1

                if counter == parallel_prefix_stage_cluster:
                    if not is_delay_cell:
                        previous_above_cell_index += 2 ** (level + 1)
                    is_delay_cell = not is_delay_cell
                    counter = 0
        # koniec fazy parallel prefix adder

        # obliczanie carry
        if self.input_k_list[0] == 0:
            last_b_i = self.n_hashed_enveloped_cell_list[-1].gi_or_bi1_ifk0
        else:
            last_b_i = self.n_hashed_enveloped_cell_list[-1].pi_or_bi1_ifk1

        if last_b_i == 0:
            self.c_out = self.parallel_adders_list[-1][-1].gi2_out
        else:
            self.c_out = self.parallel_adders_list[-1][-1].gi_out

        # obliczanie wynikow dla carry 0 i 1 oraz wlasciwego wyniku
        carry_output_list = []
        no_carry_output_list = []
        final_output_list = []

        bit0 = self.n_hashed_enveloped_cell_list[0].hi_or_ai_ifk0 if self.c_out == 0 else \
            self.n_hashed_enveloped_cell_list[0].hi_prim

        no_carry_output_list.insert(0, self.n_hashed_enveloped_cell_list[0].hi_or_ai_ifk0)
        carry_output_list.insert(0, self.n_hashed_enveloped_cell_list[0].hi_prim)
        final_output_list.insert(0, bit0)

        bit1 = self.n_hashed_enveloped_cell_list[0].gi_or_bi1_ifk0 ^ self.n_hashed_enveloped_cell_list[1].hi_or_ai_ifk0
        bit1c = self.n_hashed_enveloped_cell_list[0].gi_prim ^ self.n_hashed_enveloped_cell_list[1].hi_prim

        if self.c_out == 0:
            final_output_list.insert(0, bit1)
        else:
            final_output_list.insert(0, bit1c)
        no_carry_output_list.insert(0, bit1)
        carry_output_list.insert(0, bit1c)

        for i in range(2, self.n_bits, +1):
            bit_n = self.parallel_adders_list[-1][i - 1].gi_out ^ self.n_hashed_enveloped_cell_list[i].hi_or_ai_ifk0
            bit_c_n = self.parallel_adders_list[-1][i - 1].gi2_out ^ self.n_hashed_enveloped_cell_list[i].hi_prim
            if self.c_out == 0:
                final_output_list.insert(0, bit_n)
            else:
                final_output_list.insert(0, bit_c_n)
            no_carry_output_list.insert(0, bit_n)
            carry_output_list.insert(0, bit_c_n)

        result = ArithmeticUtils.get_int_from_binary(final_output_list)
        print(f">> Vector A: {self.input_a_list}")
        print(f">> Vector B: {self.input_b_list}")
        print(f">> Vector K: {self.input_k_list}")
        print("--------------------------------")
        print(">> Output for Carry = 0:")
        print(f">> {no_carry_output_list} -> {ArithmeticUtils.get_int_from_binary(no_carry_output_list)}")
        print(">> Output for carry = 1:")
        print(f">> {carry_output_list} -> {ArithmeticUtils.get_int_from_binary(carry_output_list)}")
        print(f"\n>> Carry = {self.c_out}")
        print(">> OUTPUT:")
        print(f">> {final_output_list} -> {result}")
        print("--------------------------------")
        return result
