from ModuloCells import HashedEnvelopedCombo
from ParallelPrefixCells import Parallel
import BinaryArithmeticUtils


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
    parallel_adders_stage_output = []

    def __init__(self, n_bits, input_a, input_b, input_k):
        self.stages = int(n_bits / 2)
        self.parallel_adders_count = self.stages
        self.n_bits = n_bits
        self.input_a_list = BinaryArithmeticUtils.get_binary_list_from_int(input_a, n_bits)
        self.input_b_list = BinaryArithmeticUtils.get_binary_list_from_int(input_b, n_bits)
        self.input_k_list = BinaryArithmeticUtils.get_binary_list_from_int(input_k, n_bits)
        self.c_out = BinaryArithmeticUtils.calculate_c_out(input_a, input_b, n_bits)

    def calculate(self):
        # inicjowanie hashed cells oraz enveloped cells do obliczen modulo
        for i in range(self.n_bits):
            self.n_hashed_enveloped_cell_list.append(HashedEnvelopedCombo())
            self.parallel_adders_stage_output.append(0)

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
                    cell.generate_enveloped_cell_output(cell.gi_or_bi1_ifk0, cell.hi_or_ai_ifk0)
                else:
                    cell.generate_enveloped_cell_output(cell.pi_or_bi1_ifk1, cell.ai_ifk1)

        # faza obliczen parallel prefix adder
        level0_index = self.n_bits - 1
        level1_index = self.n_bits - 3
        level2_index = self.n_bits - 5

        level1_parallel_index = len(self.parallel_adders_list[0]) - 1
        level1_cell_indicator = len(self.parallel_adders_list[1]) - 1

        level2_parallel_index = len(self.parallel_adders_list[1]) - 1
        level2_cell_indicator = len(self.parallel_adders_list[2]) - 1
        level2_level1_parallel_index = len(self.parallel_adders_list[1]) - 2
        level2_level0_parallel_index = len(self.parallel_adders_list[0]) - 3

        for level in range(self.stages):
            parallel_prefix_stage_indicator = 2 ** level
            parallel_prefix_stage_window = 2 ** (level + 1)
            parallel_prefix_stage_cluster = 2 ** level

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
                elif level == 2 and level2_index >= 0 and level2_parallel_index >= 0 \
                        and level2_level1_parallel_index >= 0:
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
                                           self.parallel_adders_list[1][level2_level1_parallel_index].gi_out,
                                           self.n_hashed_enveloped_cell_list[level2_index].pi_or_bi1_ifk1,
                                           self.parallel_adders_list[1][level2_level1_parallel_index].pi_out
                                           )
                    cell1.generate_output2(self.n_hashed_enveloped_cell_list[level2_index].gi_prim,
                                           self.parallel_adders_list[1][level2_level1_parallel_index].gi2_out,
                                           self.n_hashed_enveloped_cell_list[level2_index].pi_prim,
                                           self.parallel_adders_list[1][level2_level1_parallel_index].pi2_out
                                           )
                    if cell2 is not None:
                        level2_level1_parallel_index -= 1
                        cell2.generate_output1(self.parallel_adders_list[0][level2_level0_parallel_index].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 1].gi_out,
                                               self.parallel_adders_list[0][level2_level0_parallel_index].pi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 1].pi_out
                                               )
                        cell2.generate_output2(self.parallel_adders_list[0][level2_level0_parallel_index].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 1].gi2_out,
                                               self.parallel_adders_list[0][level2_level0_parallel_index].pi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 1].pi2_out
                                               )
                    if cell3 is not None:
                        t1 = self.parallel_adders_list[1][level2_level1_parallel_index].gi_out
                        t2 = self.parallel_adders_list[1][level2_level1_parallel_index].pi_out
                        cell3.generate_output1(self.parallel_adders_list[1][level2_level1_parallel_index].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 2].gi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index].pi_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 2].pi_out
                                               )
                        cell3.generate_output2(self.parallel_adders_list[0][level2_level1_parallel_index].gi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 2].gi2_out,
                                               self.parallel_adders_list[0][level2_level1_parallel_index].pi2_out,
                                               self.parallel_adders_list[1][level2_level1_parallel_index + 2].pi2_out
                                               )

                    if cell4 is not None:
                        pass
                        # tutaj bedzie lell nr 4

                    level2_level1_parallel_index -= 1
                    level2_index -= 8
                    level2_cell_indicator -= 1
        # koniec fazy parallel prefix adder

        bit0 = self.n_hashed_enveloped_cell_list[6].hi_or_ai_ifk0 if self.c_out == 0 else \
            self.n_hashed_enveloped_cell_list[6].hi_prim

        # zrobione dla n=7 bitow
        # TODO: carry 1 --- to samo tylko ze z primami
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

        print(f"K: {self.input_k_list}")
        print(f"carry = {self.c_out}")
        print("WYNIK - carry 0 :")
        print(f"{bit6} {bit5} {bit4} {bit3} {bit2} {bit1} {bit0}")
        print("WYNIK - carry 1 :")
        print(f"{bit6c} {bit5c} {bit4c} {bit3c} {bit2c} {bit1c} {bit0}")
