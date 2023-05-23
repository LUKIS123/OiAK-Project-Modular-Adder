def negate(num: int):
    if num == 0:
        return 1
    else:
        bits = num.bit_length()
        bitmask = (1 << bits) - 1
        return ~num & bitmask


def get_int_from_binary(binary_list):
    weight = 0
    result = 0
    for i in range(len(binary_list) - 1, -1, -1):
        result += binary_list[i] * pow(2, weight)
        weight += 1
    return result


def get_binary_list_from_int(num: int, n_bits):
    bit_list = [int(bit) for bit in bin(num)[2:]]
    for i in range(n_bits - len(bit_list)):
        bit_list.insert(0, 0)
    return bit_list
