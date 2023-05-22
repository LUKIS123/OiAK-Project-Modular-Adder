from Adder import Adder

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

# NIE DZIALA...
# input_a = 69
# input_b = 69
# input_k = 10

# Enter A: 69
# Enter B: 45
# Enter K: 20

while True:
    n_bits = 7

    input_a = int(input("Enter A: "))
    input_b = int(input("Enter B: "))
    input_k = int(input("Enter K: "))

    adder = Adder(n_bits)
    print("Calculating output...\n")
    adder.calculate(input_a, input_b, input_k)

    choice = str(input("\nRepeat? [Y/N]: "))
    if choice.lower() == 'n' or choice.lower() == 'no':
        break
