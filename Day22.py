import numpy as np
import unittest


def parse_input(raw_data):
    monkeys_map, movement_instructions = raw_data.split("\n\n")
    movement_instructions = movement_instructions.strip("\n")
    monkeys_map = monkeys_map.split('\n')
    monkeys_map = np.array([np.array(line) for line in monkeys_map])
    # parse jagged lengths
    n_rows = len(monkeys_map)
    n_cols = max([len(row) for row in monkeys_map])
    monkeys_map_parsed = np.full((n_rows, n_cols), " ")
    for idx_row, line in enumerate(monkeys_map):
        for idx_col, symbol in enumerate(line):
            monkeys_map_parsed[idx_row, idx_col] = symbol
    return monkeys_map_parsed, movement_instructions


def direction_to_axis(direction: str):
    assert direction in ["up", "right", "down", "left"], f"Incorrect direction {direction}; " \
                                                         f"should be up, down, left or right."
    if direction == "up":
        x_increment = 0
        y_increment = -1
    elif direction == "down":
        x_increment = 0
        y_increment = 1
    elif direction == "left":
        x_increment = -1
        y_increment = 0
    elif direction == "right":
        x_increment = 1
        y_increment = 0
    return x_increment, y_increment


def detecting_wall(pixel: str):
    return pixel == "#"


def wrap(x: int, y: int, direction: str, board_map: np.ndarray):
    """
    :param x: absolute value has to be 0 or 1
    :param y: absolute value has to be 0 or 1
    :param direction:
    :param board_map:
    :return:
    """
    x_increment, y_increment = direction_to_axis(direction)
    if abs(x_increment):
        new_y = y
        if x_increment > 0:
            new_x = np.where(board_map[y] == ".")[0][0]
            if "#" in board_map[y, :new_x]:  # If a wall would be crossed, do not wrap
                new_x = x
        else:
            new_x = np.where(board_map[y] == ".")[0][-1]
            if "#" in board_map[y, new_x:]:
                new_x = x
    else:
        new_x = x
        if y_increment > 0:
            new_y = np.where(board_map[:, x] == ".")[0][0]
            if "#" in board_map[:new_y, x]:
                new_y = y
        else:
            new_y = np.where(board_map[:, x] == ".")[0][-1]
            if "#" in board_map[new_y:, x]:
                new_y = y
    return new_x, new_y


def location_within_board(x: int, y: int, board_map: list):
    pixel_valid = False
    x_valid = len(board_map[0]) > x != -1
    y_valid = len(board_map) > y != -1
    if x_valid and y_valid:
        pixel_valid = board_map[y][x] != " "
    return x_valid and y_valid and pixel_valid


def move(x, y, nr_steps: int, direction: str, board_map: list):
    x_increment, y_increment = direction_to_axis(direction)
    for step_idx in range(nr_steps):
        x_new = x + x_increment
        y_new = y + y_increment
        # check if in range
        if location_within_board(x=x_new, y=y_new, board_map=board_map):
            pixel = board_map[y_new][x_new]
            if detecting_wall(pixel):
                break
            else:
                x = x_new
                y = y_new
        else:
            x, y = wrap(x, y, direction, board_map)
    return x, y


def rotate(rotation_dir: str, movement_dir: str):
    directions = ["up", "right", "down", "left"]
    assert movement_dir in directions, f"Incorrect direction {movement_dir}; should be up, down, left or right."
    if rotation_dir == "R":
        new_dir = directions[(directions.index(movement_dir) + 1) % len(directions)]
    elif rotation_dir == "L":
        new_dir = directions[directions.index(movement_dir) - 1]
    return new_dir


def follow_instructions(instructions: str, board_map: list):
    possible_rotations = ["R", "L"]
    current_direction = "right"
    position_y = 0
    position_x = np.where(board_map[position_y] == ".")[0][0]

    instruction_idx = 0
    while instruction_idx < len(instructions):
        instruction = instructions[instruction_idx]
        if instruction in possible_rotations:
            current_direction = rotate(rotation_dir=instruction, movement_dir=current_direction)
            instruction_idx += 1
        else:
            try:
                if possible_rotations[0] in instructions[instruction_idx:]:
                    l_idx = instructions[instruction_idx:].index(possible_rotations[0])
                else:
                    l_idx = len(instructions[instruction_idx:]) + 1
                if possible_rotations[1] in instructions[instruction_idx:]:
                    r_idx = instructions[instruction_idx:].index(possible_rotations[1])
                else:
                    r_idx = len(instructions[instruction_idx:]) + 1
                number_end_idx = instruction_idx + min(l_idx, r_idx)
                stride = int(instructions[instruction_idx:number_end_idx])
                instruction_idx = number_end_idx
            except ValueError:
                stride = len(instructions) - instruction_idx
                instruction_idx = len(instructions)
            position_x, position_y = move(x=position_x, y=position_y, nr_steps=stride,
                                          direction=current_direction, board_map=board_map)

    return position_y, position_x, current_direction


def calculate_answer(row: int, column: int, facing: str):
    facing_score = {"right": 0, "down": 1, "left": 2, "up": 3}
    combined_score = 1000 * (row + 1) + 4 * (column + 1) + facing_score[facing]
    return combined_score

class Test(unittest.TestCase):
    def test_wrap(self):
        expected_x = 2
        expected_y = 0
        board_map = np.array([[" ", " ", "."], [" ", " ", "."]])
        predicted_x, predicted_y = wrap(x=2, y=0, direction="right", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

        expected_x = 2
        expected_y = 0
        board_map = np.array([[" ", " ", "."], [" ", " ", "."]])
        predicted_x, predicted_y = wrap(x=2, y=0, direction="left", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

        expected_x = 2
        expected_y = 1
        board_map = np.array([[" ", " ", "."], [" ", " ", "."]])
        predicted_x, predicted_y = wrap(x=2, y=0, direction="up", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

        expected_x = 2
        expected_y = 0
        board_map = np.array([[" ", " ", "."], [" ", " ", "."]])
        predicted_x, predicted_y = wrap(x=2, y=1, direction="down", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

        expected_x = 2
        expected_y = 0
        board_map = np.array([["#", ".", "."], [" ", " ", "."]])
        predicted_x, predicted_y = wrap(x=2, y=0, direction="right", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

        expected_x = 3
        expected_y = 0
        board_map = np.array([[" ", "#", ".", "."], [" ", "#", ".", "."]])
        predicted_x, predicted_y = wrap(x=3, y=0, direction="right", board_map=board_map)
        self.assertEqual(expected_x, predicted_x)
        self.assertEqual(expected_y, predicted_y)

    def test_provided_example(self):
        data = "        ...#    \n        .#..\n        #...\n        ....\n...#.......#\n........#...\n..#....#....\n" \
           "..........#.\n        ...#....\n        .....#..\n        .#......\n        ......#.\n\n10R5L5R10L4R5L5"
        monkeys_map_parsed, movement_instructions = parse_input(data)
        row, column, facing = follow_instructions(instructions=movement_instructions, board_map=monkeys_map_parsed)
        predicted_answer = calculate_answer(row, column, facing)
        self.assertEqual(6032, predicted_answer)

if __name__ == '__main':
    unittest.main(argv=[''], verbosity=3, exit=False)

with open("inputs/input22.txt") as f:
    data = f.read()

monkeys_map_parsed, movement_instructions = parse_input(data)
final_row, final_column, final_facing = follow_instructions(instructions=movement_instructions, board_map=monkeys_map_parsed)
print(final_row, final_column, final_facing)
answer = calculate_answer(final_row, final_column, final_facing)
print(f"Answer: {answer}")
