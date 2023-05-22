from ModuloCells import HashedEnvelopedCombo
from Adder import Adder
import BinaryArithmeticUtils

# UWAGA ->>> modulo 2^n - K
# n=7
# A+B <=127
# modulo = 2**n-K = 128 - K
# 3 <= K <= 2**(n-1) -1 = 63

# S = (A+B) modulo
# S = A+B           if A+B < modulo
# S = A+B - modulo  if A + B >= modulo

# S = A+B           if cout =0
#     A+B + K       if cout =0
# cout out carry z A+B+K
# cout == A+B+K and 128 binarnie dla n=7

# m = HashedEnvelopedCombo()
# m.generate_hashed_cell_output(1, 1)
# print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
# m.generate_hashed_cell_output(1, 0)
# print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
# m.generate_hashed_cell_output(0, 1)
# print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
# m.generate_hashed_cell_output(0, 0)
# print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
#
# print(BinaryArithmeticUtils.get_int_from_binary([1, 1, 1]))
# print(BinaryArithmeticUtils.get_binary_list_from_int(32, 7))

# ======= test dla n=7 =======
# UWAGA! -> k_max = 63
n_bits = 7
input_a = 70
input_b = 20
input_k = 31
# input_k = 63

adder = Adder(n_bits, input_a, input_b, input_k)
adder.calculate()
