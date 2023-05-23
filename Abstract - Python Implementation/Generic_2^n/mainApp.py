from GenericAdder import Adder

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

while True:
    # wersja generyczna dla n o potegach dwojki
    n_bits = 8

    input_a = int(input("Enter A: "))
    input_b = int(input("Enter B: "))
    input_k = int(input("Enter K: "))
    print(f"Expected value = {(input_a + input_b) % ((2 ** n_bits) - input_k)}")

    adder = Adder(n_bits)
    print("Calculating output...\n")
    adder.calculate(input_a, input_b, input_k)
    adder.reset(n_bits)

    choice = str(input("\nRepeat? [Y/N]: "))
    if choice.lower() == 'n' or choice.lower() == 'no':
        break
