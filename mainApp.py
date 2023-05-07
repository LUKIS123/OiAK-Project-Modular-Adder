print(~0)
print(~1)


def negate(number: int):
    if number == 0:
        return 1
    else:
        bits = number.bit_length()
        bitmask = (1 << bits) - 1
        return ~number & bitmask


xd = negate(0)
print(xd)

xe = negate(4)
print(xe)


def decimal_to_rns(number, moduli):
    residues = [number % modulus for modulus in moduli]
    print(residues)
    return residues


def rns_to_decimal(residues, moduli):
    total = 0
    M = 1
    for modulus in moduli:
        M *= modulus

    for i in range(len(residues)):
        m_i = M // moduli[i]
        total += residues[i] * m_i * pow(m_i, -1, moduli[i])

    return total % M


def rns_addition(x, y, moduli):
    result = [(x_i + y_i) % modulus for x_i, y_i, modulus in zip(x, y, moduli)]
    print(result)
    return result


moduli = [3, 5, 7]

num1 = 10
num2 = 15

num1_rns = decimal_to_rns(num1, moduli)
num2_rns = decimal_to_rns(num2, moduli)

print("SUMA")
result_rns = rns_addition(num1_rns, num2_rns, moduli)
result_decimal = rns_to_decimal(result_rns, moduli)

print(f"Dodawanie liczb {num1} i {num2}:")
print(f"{num1_rns} (RNS) + {num2_rns} (RNS) = {result_rns} (RNS)")
print(f"W systemie dziesiętnym: {num1} + {num2} = {result_decimal}")
