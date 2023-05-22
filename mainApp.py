from Adder import Adder

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


# ======= test dla n=7 =======

n_bits = 7
# input_a = 70
# input_b = 20
# input_k = 31
# input_k = 63

# input_a = 8
# input_b = 22
# input_k = 40

input_a = 22
input_b = 18
input_k = 61

# input_a = 7
# input_b = 50
# input_k = 55

adder = Adder(n_bits, input_a, input_b, input_k)
adder.calculate()
