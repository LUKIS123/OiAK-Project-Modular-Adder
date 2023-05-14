def negate(num: int):
    if num == 0:
        return 1
    else:
        bits = num.bit_length()
        bitmask = (1 << bits) - 1
        return ~num & bitmask
