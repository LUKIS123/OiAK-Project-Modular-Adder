def negate(num: int):
    if num == 0:
        return 1
    else:
        return 0


def get_int_from_binary(binary_list):
    weight = 0
    result = 0
    for i in range(len(binary_list) - 1, -1, -1):
        result += binary_list[i] * pow(2, weight)
        weight += 1
    return result


def get_binary_aligned_list_from_int(num: int, n_bits):
    bit_list = [int(bit) for bit in bin(num)[2:]]
    for i in range(n_bits - len(bit_list)):
        bit_list.insert(0, 0)
    return bit_list


def get_binary_list_from_int(num: int):
    bit_list = [int(bit) for bit in bin(num)[2:]]
    return bit_list


def negate_binary_list_(bit_list):
    output_list = []
    for i in range(len(bit_list)):
        if bit_list[i] == 0:
            output_list.append(1)
        else:
            output_list.append(0)
    carry = False
    if output_list[-1] == 0:
        output_list[-1] = 1
    else:
        output_list[-1] = 0
        carry = True
    if carry:
        if len(output_list) >= 2:
            for i in range(len(output_list) - 2, -1, -1):
                if output_list[i] == 0:
                    output_list[i] = 1
                    break
                else:
                    output_list[i] = 0
    if output_list[0] == 0:
        output_list.insert(0, 1)
    return output_list
