import math

def split_sequence(start, end, num_parts):
    result = []

    # Return range if only 1 part
    if num_parts == 1:
        return [start, end + 1]

    # Return list from start to end+1 if more parts than elements
    if num_parts > end - start + 1:
        return list(range(start, end + 2))

    length = (end - start + 1)
    part_length_short = length // num_parts
    part_length_long = math.ceil(length / num_parts)
    cut_pos = length % num_parts

    # Add long ranges
    i = start
    while i < start + cut_pos * part_length_long:
        result.append(i)
        i += part_length_long

    # Add short ranges
    i = start + cut_pos * part_length_long
    while i <= end + 1:
        result.append(i)
        i += part_length_short

    return result

def equal_doubles(first, second, epsilon=1e-10):
    if math.isnan(first):
        return math.isnan(second)
    return abs(first - second) < epsilon

def load_data(file_name):
    num_rows = 0
    num_cols = 0

    # Open input file
    with open(file_name, 'r') as input_file:
        # Count number of rows
        lines = input_file.readlines()
        num_rows = len(lines)
        first_line = lines[0]

        # Determine the number of columns from the first line
        num_cols = len(first_line.split())

        # Read the entire contents
        storage = []
        for line in lines:
            tokens = line.split()
            for token in tokens:
                storage.append(float(token))

        if len(tokens) > num_cols:
            raise ValueError("Too many columns in a row.")
        elif len(tokens) < num_cols:
            raise ValueError("Too few columns in a row. Are all values numeric?")

    dim = [num_rows, num_cols]

    return storage, dim

def set_data(data, row, col, value):
    storage, dim = data
    num_rows = dim[0]

    storage[col * num_rows + row] = value
