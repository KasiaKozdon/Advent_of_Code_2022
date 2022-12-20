import matplotlib.pyplot as plt
import numpy as np
import unittest


def count_visible(height_matrix: np.ndarray, plotting=False) -> int:
    if plotting:
        plot_data(height_matrix, title="Input data")
    mask_visible = np.zeros_like(height_matrix)
    # Check visibility from four possible directions
    # Row-wise left-right view
    mask_visible += find_visible(height_matrix)
    # Column-wise top-down view
    assert np.all(height_matrix == height_matrix.T.T), "Transpose does not return a matching mask."
    mask_visible += find_visible(height_matrix.T).T
    # Column-wise top-down view
    assert np.all(height_matrix == np.flip(np.flip(height_matrix, axis=0).T.T, axis=0)), \
        "Flip axis 0 does not return a matching mask."
    mask_visible += np.flip(find_visible(np.flip(height_matrix, axis=0).T).T, axis=0)
    # Row-wise right-left view
    assert np.all(height_matrix == np.flip(np.flip(height_matrix, axis=1), axis=1)), \
        "Flip axis 1 does not return a matching mask."
    mask_visible += np.flip(find_visible(np.flip(height_matrix, axis=1)), axis=1)
    mask_visible = mask_visible.astype('bool')
    if plotting:
        plot_data(mask_visible, title="Visible trees")
    count_of_visible = int(np.sum(mask_visible))
    return count_of_visible


def find_visible(heights: np.ndarray) -> np.ndarray:
    mask = np.zeros_like(heights)
    for idx_row, row in enumerate(heights):
        max_val = -1
        for idx_col, item in enumerate(row):
            if item > max_val:
                mask[idx_row, idx_col] = 1
                max_val = item
    return mask


def plot_data(height_matrix: np.ndarray, title: str):
    plt.imshow(height_matrix, cmap="Accent_r")
    plt.title(title)
    plt.colorbar()
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, np.shape(height_matrix)[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, np.shape(height_matrix)[0], 1), minor=True)
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
    plt.show()


def calculate_viewing_distance_all_directions(height_matrix: np.ndarray, plotting=False) -> int:
    if plotting:
        plot_data(height_matrix, title="Input data")
    distances = np.ones_like(height_matrix)
    # Calculae viewing distance in four possible directions
    # Row-wise left-right view
    distances = np.multiply(distances, calculate_viewing_distance(height_matrix))
    # Column-wise top-down view
    assert np.all(height_matrix == height_matrix.T.T), "Transpose does not return a matching mask."
    distances = np.multiply(distances, calculate_viewing_distance(height_matrix.T).T)
    # Column-wise top-down view
    assert np.all(height_matrix == np.flip(np.flip(height_matrix, axis=0).T.T, axis=0)), \
        "Flip axis 0 does not return a matching mask."
    distances = np.multiply(distances, np.flip(calculate_viewing_distance(np.flip(height_matrix, axis=0).T).T, axis=0))
    # Row-wise right-left view
    assert np.all(height_matrix == np.flip(np.flip(height_matrix, axis=1), axis=1)), \
        "Flip axis 1 does not return a matching mask."
    distances = np.multiply(distances, np.flip(calculate_viewing_distance(np.flip(height_matrix, axis=1)), axis=1))
    if plotting:
        plot_data(distances, title="Visible trees")
    return np.max(distances)


def calculate_viewing_distance(heights: np.ndarray) -> np.ndarray:
    mask = np.zeros_like(heights)
    for idx_row, row in enumerate(heights):
        for idx_col, item in enumerate(row):
            for neighbour in row[idx_col+1:]:
                mask[idx_row, idx_col] += 1
                if item <= neighbour:
                    break
    return mask


class Test(unittest.TestCase):
    def test_provided_examples(self):
        example_data = np.asarray([[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
        """Part a"""
        predicted_answer_a = count_visible(example_data)
        correct_answer_a = 21
        self.assertEqual(predicted_answer_a, correct_answer_a)

        """Part b"""
        predicted_answer_b = calculate_viewing_distance_all_directions(example_data)
        correct_answer_b = 8
        self.assertEqual(predicted_answer_b, correct_answer_b)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False)

with open("inputs/input8.txt") as f:
    data = f.readlines()
data = [line.strip() for line in data]
data = np.array([[int(number) for number in line] for line in data])

answer_a = count_visible(data)
print(f"Part a answer is: {answer_a}")

answer_b = calculate_viewing_distance_all_directions(data)
print(f"Part b answer is: {answer_b}")
