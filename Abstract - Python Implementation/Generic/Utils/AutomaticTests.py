from GenericAdder import Adder
from Utils import ArythmeticUtils


def test():
    input_a_min = int(input("Enter A min value: "))
    input_a_max = int(input("Enter A max value: "))
    input_b_min = int(input("Enter B min value: "))
    input_b_max = int(input("Enter B max value: "))
    input_k = int(input("Enter K: "))

    with open("Resources/catch_error.txt", 'a') as catch_error_file:
        catch_error_file.write(
            f"Automatic Tests arguments: A_min={input_a_min}, A_max={input_a_max}, "
            f"B_min={input_b_min}, B_max={input_b_max}, K={input_k}"
        )

    dist_a = (input_a_max - input_a_min) + 1
    dist_b = (input_b_max - input_b_min) + 1

    error_count = 0
    for index_a in range(dist_a):
        input_a = input_a_min + index_a
        for index_b in range(dist_b):
            input_b = input_b_min + index_b

            input_a_list = ArythmeticUtils.get_binary_list_from_int(input_a)
            input_b_list = ArythmeticUtils.get_binary_list_from_int(input_b)
            n_bits = len(input_a_list) if len(input_a_list) >= len(input_b_list) else len(input_b_list)
            print(f"======================== A={input_a}, B={input_b}, N_bits={n_bits} ========================")

            expected_result = (input_a + input_b) % ((2 ** n_bits) - input_k)
            adder = Adder(n_bits)
            result = adder.calculate(input_a, input_b, input_k)

            if result != expected_result:
                error_count += 1
                with open("Resources/catch_error.txt", 'a') as catch_error_file:
                    catch_error_file.write(f"Error with input: A={input_a}, B={input_b}, N_bits={n_bits}\n")
                    catch_error_file.write(f"Expected result={expected_result}")
                    catch_error_file.write(f"Generic adder output={result}")
                    catch_error_file.write("\n")

            adder.reset(n_bits)

    print(f"TESTS FINISHED WITH >> {error_count} << ERRORS!")
