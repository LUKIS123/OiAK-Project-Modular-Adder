from GenericAdder import Adder
from Utils import ArithmeticUtils


def test():
    is_fixed = False
    input_n_bits = 0
    choose_fixed_size = str(input("Set fixed adder size (n_bits)? [Y/N]: "))
    if choose_fixed_size.lower() == 'y' or choose_fixed_size.lower() == 'yes':
        is_fixed = True
        input_n_bits = int(input("Enter N_bits: "))

    input_a_min = int(input("Enter A min value: "))
    input_a_max = int(input("Enter A max value: "))
    input_b_min = int(input("Enter B min value: "))
    input_b_max = int(input("Enter B max value: "))
    input_k_min = int(input("Enter K min value: "))
    input_k_max = int(input("Enter K max value: "))

    with open("Resources/catch_error.txt", 'a') as catch_error_file:
        catch_error_file.write(
            f"Automatic Tests arguments: A_min={input_a_min}, A_max={input_a_max}, "
            f"B_min={input_b_min}, B_max={input_b_max}, K_min={input_k_min}, K_max={input_k_max}\n"
        )

    dist_a = (input_a_max - input_a_min) + 1
    dist_b = (input_b_max - input_b_min) + 1
    dist_k = (input_k_max - input_k_min) + 1

    error_count = 0

    for index_a in range(dist_a):
        input_a = input_a_min + index_a
        for index_b in range(dist_b):
            input_b = input_b_min + index_b
            for index_k in range(dist_k):
                input_k = input_k_min + index_k
                input_k_list = ArithmeticUtils.get_binary_list_from_int(input_k)

                if is_fixed:
                    n_bits = input_n_bits
                else:
                    n_bits = len(ArithmeticUtils.get_binary_list_from_int(input_a + input_b))
                    if len(input_k_list) > n_bits:
                        n_bits = len(input_k_list) + 1
                    elif ArithmeticUtils.get_binary_aligned_list_from_int(input_k, n_bits)[0] != 0:
                        n_bits += 1

                if ArithmeticUtils.get_binary_aligned_list_from_int(input_k, n_bits)[0] != 0:
                    print("ERROR! Invalid K (MODULO)!!!")
                    break

                if input_a + input_b >= ((2 ** n_bits) - input_k):
                    expected_result = (input_a + input_b) - ((2 ** n_bits) - input_k)
                else:
                    expected_result = (input_a + input_b) % ((2 ** n_bits) - input_k)
                if expected_result > (2 ** n_bits) - 1 or input_a >= 2 ** n_bits or input_b >= 2 ** n_bits:
                    print("ERROR: Numbers to big for N_bits given!!!")
                    break

                print(f"======================== A={input_a}, B={input_b}, N_bits={n_bits} ========================")

                adder = Adder(n_bits)
                result = adder.calculate(input_a, input_b, input_k, False, [])

                if result != expected_result:
                    error_count += 1
                    with open("Resources/catch_error.txt", 'a') as catch_error_file:
                        catch_error_file.write(f"Error with input: A={input_a}, B={input_b}, N_bits={n_bits}\n")
                        catch_error_file.write(f"Expected result={expected_result}")
                        catch_error_file.write(f"Generic adder output={result}")
                        catch_error_file.write("\n")

                adder.reset(n_bits)

    print(f"TESTS PERFORMED: {dist_a * dist_b}, FINISHED WITH >> {error_count} << ERRORS!")
