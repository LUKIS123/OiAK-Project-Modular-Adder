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


def get_binary_list_aligned_from_int(num: int, n_bits):
    bit_list = [int(bit) for bit in bin(num)[2:]]
    for i in range(n_bits - len(bit_list)):
        bit_list.insert(0, 0)
    return bit_list


def calculate_mask(input_a: int, input_b: int, n_bits: int):
    out_list = get_binary_list_aligned_from_int(2 ** n_bits, n_bits)
    ab_list = get_binary_list_aligned_from_int(input_a + input_b, n_bits)
    if len(out_list) > len(ab_list):
        for i in range(len(out_list) - len(ab_list)):
            ab_list.insert(0, 0)
    if out_list[0] & ab_list[0] == 1:
        return 1
    else:
        return 0
