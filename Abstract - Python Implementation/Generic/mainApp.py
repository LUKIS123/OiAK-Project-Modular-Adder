import sys

from GenericAdder import Adder
from Utils import ArithmeticUtils
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

is_second_mode = False
input_n_bits = 0
choose_fixed_size = str(input("Set modulo (2^n + K) mode? [Y/N], >>>default (2^n - K)<<< : "))
if choose_fixed_size.lower() == 'y' or choose_fixed_size.lower() == 'yes':
    is_second_mode = True

# tryb sumatora modulo (2^n + K), domyslnie sumator modulo (2^n - K)
if is_second_mode:
    print(">> Simulating modulo (2^n + K) Adder...")
else:
    print(">> Simulating modulo (2^n - K) Adder...")

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

    input_a_list = ArithmeticUtils.get_binary_list_from_int(input_a)
    input_b_list = ArithmeticUtils.get_binary_list_from_int(input_b)
    input_k_list = ArithmeticUtils.get_binary_list_from_int(input_k)

    if is_second_mode:
        input_k_list = ArithmeticUtils.negate_binary_list_(input_k_list)

    # wyznaczanie wartosci n_bitow
    if is_fixed:
        n_bits = input_n_bits

        if is_second_mode:
            if n_bits >= len(input_k_list):
                for i in range(n_bits - len(input_k_list) - 1):
                    input_k_list.insert(0, 1)
            input_k_list.insert(0, 0)

    else:
        n_bits = len(ArithmeticUtils.get_binary_list_from_int(input_a + input_b))

        if is_second_mode:
            if n_bits >= len(input_k_list):
                for i in range(n_bits - len(input_k_list)):
                    input_k_list.insert(0, 1)
            input_k_list.insert(0, 0)
        if len(input_k_list) > n_bits:
            if is_second_mode:
                n_bits = len(input_k_list)
            else:
                n_bits = len(input_k_list) + 1
        elif ArithmeticUtils.get_binary_aligned_list_from_int(input_k, n_bits)[0] != 0:
            n_bits += 1

    if ArithmeticUtils.get_binary_aligned_list_from_int(input_k, n_bits)[0] != 0:
        print("ERROR: Invalid K (MODULO)!!!")
        continue

    # obliczanie wartosci oczekiwanej
    if is_second_mode:
        if input_a + input_b >= ((2 ** (n_bits - 1)) + input_k):
            expected_result = (input_a + input_b) - ((2 ** (n_bits - 1)) + input_k)
        else:
            expected_result = (input_a + input_b) % ((2 ** (n_bits - 1)) + input_k)
    else:
        if input_a + input_b >= ((2 ** n_bits) - input_k):
            expected_result = (input_a + input_b) - ((2 ** n_bits) - input_k)
        else:
            expected_result = (input_a + input_b) % ((2 ** n_bits) - input_k)

    if expected_result > (2 ** n_bits) - 1 or input_a >= 2 ** n_bits or input_b >= 2 ** n_bits:
        print("ERROR: Numbers to big for N_bits given!!!")
        continue

    print(f">> N_bits = {n_bits}\n>> Expected value = {expected_result}")
    if is_second_mode:
        print(f">> MODULO={((2 ** (n_bits - 1)) + input_k)}, Calculating output...")
    else:
        print(f">> MODULO={((2 ** n_bits) - input_k)}, Calculating output...")

    # dla modulo (2^n + K) calculate() przyjmuje zanegowany vektor K z 0 na pierwszej pozycji
    # w tym przypadku uklad musi skladac sie modulow dla n+1

    adder = Adder(n_bits)
    adder.calculate(input_a, input_b, input_k, is_second_mode, input_k_list)
    adder.reset(n_bits)

    choice = str(input("\n>> Repeat? [Y/N]: "))
    if choice.lower() == 'n' or choice.lower() == 'no':
        break
