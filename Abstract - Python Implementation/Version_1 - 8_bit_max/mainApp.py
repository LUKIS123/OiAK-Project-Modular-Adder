from Adder import Adder
from Utility import BinaryArithmeticUtils

# UWAGA >>> modulo 2^n - K
# n=7
# A+B <= 127
# modulo = 2**n-K = 128 - K
# 3 <= K <= 2**(n-1) -1 = 63

# S = (A+B) modulo
# S = A+B           if A+B < modulo
# S = A+B - modulo  if A + B >= modulo

# S = A+B           if c_out =0
#     A+B + K       if c_out =0
# c_out -> carry z A+B+K
# c_out == A+B+K and 128 binarnie dla n=7

# ======= testy dla n=7 =======
# input_a = 70
# input_b = 20
# input_k = 31

# input_a = 70
# input_b = 20
# input_k = 63

# input_a = 8
# input_b = 22
# input_k = 40

# input_a = 22
# input_b = 18
# input_k = 61

# input_a = 7
# input_b = 50
# input_k = 55

# Enter A: 69
# Enter B: 45
# Enter K: 20

# input_a = 69
# input_b = 69
# input_k = 10

# TODO: do przetestowania tryb 8 bit
while True:
    n_bits = 7
    input_n = int(input("Choose n_bit mode (7 or 8): "))
    if input_n == 7 or input_n == 8:
        n_bits = input_n

    input_a = int(input("Enter A: "))
    input_b = int(input("Enter B: "))
    input_k = int(input("Enter K: "))

    if BinaryArithmeticUtils.get_binary_list_aligned_from_int(input_k, n_bits)[0] != 0:
        print("ERROR: Invalid K (MODULO)!!!")
        continue

    if input_a + input_b >= ((2 ** n_bits) - input_k):
        expected_result = (input_a + input_b) - ((2 ** n_bits) - input_k)
    else:
        expected_result = (input_a + input_b) % ((2 ** n_bits) - input_k)
    if expected_result > (2 ** n_bits) - 1 or input_a >= 2 ** n_bits or input_b >= 2 ** n_bits:
        print("ERROR: Numbers to big for N_bits given!!!")
        continue
    print(f"Expected value = {expected_result}")
    print("Calculating output...")

    adder = Adder(n_bits)
    adder.calculate(input_a, input_b, input_k)
    adder.reset(n_bits)

    choice = str(input("\nRepeat? [Y/N]: "))
    if choice.lower() == 'n' or choice.lower() == 'no':
        break
