import numpy as np
import unittest


def parse_data(data_to_parse):
    parsed_data = data_to_parse.strip().split('\n')
    parsed_data = [line.split(',') for line in parsed_data]
    parsed_data = np.array([np.array(line, dtype=int) for line in parsed_data])
    return parsed_data


def calculate_exposed_surface(scan_data):
    exposed_surface = 2 * len(scan_data[0]) * len(scan_data)
    for entry in scan_data:
        exposed_surface -= np.any(np.all([entry[0] + 1, entry[1], entry[2]] == scan_data, axis=1))
        exposed_surface -= np.any(np.all([entry[0] - 1, entry[1], entry[2]] == scan_data, axis=1))
        exposed_surface -= np.any(np.all([entry[0], entry[1] + 1, entry[2]] == scan_data, axis=1))
        exposed_surface -= np.any(np.all([entry[0], entry[1] - 1, entry[2]] == scan_data, axis=1))
        exposed_surface -= np.any(np.all([entry[0], entry[1], entry[2] + 1] == scan_data, axis=1))
        exposed_surface -= np.any(np.all([entry[0], entry[1], entry[2] - 1] == scan_data, axis=1))
    return exposed_surface


class Test(unittest.TestCase):
    def test_with_provided_input_one(self):
        provided_data = "1,1,1\n2,1,1\n"
        parsed_data = parse_data(provided_data)
        predicted_answer = calculate_exposed_surface(parsed_data)
        expected_answer = 10
        self.assertEqual(expected_answer, predicted_answer)

    def test_with_provided_input(self):
        provided_data = "2,2,2\n1,2,2\n3,2,2\n2,1,2\n2,3,2\n2,2,1\n2,2,3\n2,2,4\n2,2,6\n1,2,5\n3,2,5\n2,1,5\n2,3,5"
        parsed_data = parse_data(provided_data)
        predicted_answer = calculate_exposed_surface(parsed_data)
        expected_answer = 64
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input18.txt") as f:
        data = f.read()
    data = parse_data(data)
    my_answer = calculate_exposed_surface(data)
    print(f"Answer part a: {my_answer}")
