import sys

from GenericAdder import Adder
from Utils import ArythmeticUtils
from Utils import AutomaticTests

# UWAGA -> modulo 2^n - K
# modulo = 2**n-K
# 3 <= K <= 2**(n-1) -1

# S = (A+B) modulo
# S = A+B           if A+B < modulo
# S = A+B - modulo  if A + B >= modulo

# S = A+B           if c_out = 0
# S = A+B + K       if c_out = 0
# c_out -> carry z A+B+K

choose_tests = str(input("Automatic Tests? [Y/N]: "))
if choose_tests.lower() == 'y' or choose_tests.lower() == 'yes':
    AutomaticTests.test()
    sys.exit()

is_fixed = False
choose_fixed_size = str(input("Set fixed adder size (n_bits)? [Y/N]: "))
if choose_fixed_size.lower() == 'y' or choose_fixed_size.lower() == 'yes':
    is_fixed = True

while True:
    if is_fixed:
        input_n_bits = int(input("Enter N_bits: "))
    input_a = int(input("Enter A: "))
    input_b = int(input("Enter B: "))
    input_k = int(input("Enter K: "))

    input_a_list = ArythmeticUtils.get_binary_list_from_int(input_a)
    input_b_list = ArythmeticUtils.get_binary_list_from_int(input_b)

    if is_fixed:
        n_bits = input_n_bits
    else:
        n_bits = len(input_a_list) if len(input_a_list) >= len(input_b_list) else len(input_b_list)

    if ArythmeticUtils.get_binary_aligned_list_from_int(input_k, n_bits)[0] != 0:
        print("ERROR: Invalid K (MODULO)!!!")
        continue

    if input_a + input_b >= ((2 ** n_bits) - input_k):
        expected_result = (input_a + input_b) - ((2 ** n_bits) - input_k)
    else:
        expected_result = (input_a + input_b) % ((2 ** n_bits) - input_k)
    if expected_result > (2 ** n_bits) - 1:
        print("ERROR: Numbers to big for N_bits given!!!")
        continue

    print(f">> N_bits = {n_bits}\n>> Expected value = {expected_result}")
    print(">> Calculating output...")

    adder = Adder(n_bits)
    adder.calculate(input_a, input_b, input_k)
    adder.reset(n_bits)

    choice = str(input("\n>> Repeat? [Y/N]: "))
    if choice.lower() == 'n' or choice.lower() == 'no':
        break
