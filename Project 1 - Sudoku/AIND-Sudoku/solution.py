import sys

# Global Variables
assignments = []
boxes = []
row_unit = []
col_unit = []
square_unit = []
unit_list = []
units = {}
peers = {}
diag_unit = []
hasBeenInitialized = False

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Check if the initialize function has already been called.
    if hasBeenInitialized is False:
        initialize()
    
    # Stores the list of naked twins
    list_of_naked_twins = {}

    # This for loop is used to find all the naked twins
    for unit in unit_list:
        # box_value_count dictionary stores the number of times a value repeats in a unit
        box_value_count = {}
        for box in unit:
            if values[box] not in box_value_count.keys():
                box_value_count[values[box]] = []
            box_value_count[values[box]].append(box)
        # Iterate through all the items in box_value_count. eg. value = "12", box_list = ["A1", "D1"]
        for value, box_list in box_value_count.items():
            if len(value) == len(box_list) and len(value) == 2:
                if value not in list_of_naked_twins.keys():
                    list_of_naked_twins[value] = []
                # The below if statement makes sure that if the for example A1 and B1 have values '12',
                if box_list not in list_of_naked_twins[value]:
                    list_of_naked_twins[value].append(box_list)
    
    # This for loop is used to eliminate the digits of naked twins from the respective unit.
    for value, unit_lists_for_value in list_of_naked_twins.items():
        for unit_list_for_value in unit_lists_for_value:
            for unit in unit_list:
                if all(x in unit for x in unit_list_for_value):
                    for box in unit:
                        if box not in unit_list_for_value:
                            for digit in value:
                                values = assign_value(values, box, values[box].replace(digit, ''))
                                # values[box] = values[box].replace(digit, '')

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    
    values = []
    for value in grid:
        if value == '.':
            values.append('123456789')
        else:
            values.append(value)
    assert len(values) == 81
    return dict(zip(boxes, values))



def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in row_string:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in col_string))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Go over all the boxes in the sudoku. If there is a box with only one digit, then remove this digit 
    from all the units that it belongs to
    Args:
        values(dict): The sudoku in dictionary form
    Return:
        Sudoku in dictionary form after making changes
    """
    list_of_keys_with_size_1 = [box for box in values.keys() if len(values[box]) == 1]
    for box in list_of_keys_with_size_1:
        for peer in peers[box]:
            # values[peer] = values[peer].replace(values[box], '')
            values = assign_value(values, peer, values[peer].replace(values[box], ''))
    return values

def only_choice(values):
    """
    Go through all the boxes in the sudoku. If in any box there is a digit such that it only occurs once in a 
    particular unit, then set the confirm value of that box as the digit.
    Args:
        values(dict): The sudoku in dictionary form
    Return:
        Sudoku in dictionary form after making changes
    """
    for unit in unit_list:
        for digit in '123456789':
            digit_list = [box for box in unit if digit in values[box]]
            if len(digit_list) == 1:
                # values[digit_list[0]] = digit
                values = assign_value(values, digit_list[0], digit)
    return values

def reduce_puzzle(values):
    """
    Perform eliminate(), naked_twins() and only_choice() until they stop offering any change to the input sudoku
    Args:
        values(dict): The sudoku in dictionary form
    Return:
        Sudoku in dictionary form after making changes
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Call reduce_puzzle() and if the sudoku returned is not solved then apply Depth-First Search to assume value
    in the box with the least number of digits (!= 1) and go ahead solving it by calling search() with the new sudoku
    Args:
        values(dict): The sudoku in dictionary form
    Return:
        Sudoku in dictionary form after making changes
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    initialize()
    values = grid_values(grid)
    values = search(values)
    return values

def initialize():
    """
    Used to initialize all the global variables that we will need
    """
    global boxes, row_unit, col_unit, square_unit, unit_list, units, peers, row_string, col_string, diag_unit, hasBeenInitialized
    row_string = 'ABCDEFGHI'
    col_string = '123456789'
    boxes = cross(row_string, col_string).copy()
    row_unit = [cross(r, col_string) for r in row_string]
    col_unit = [cross(row_string, c) for c in col_string]
    diag_unit.append([row_string[i] + col_string[i] for i in range(9)])
    diag_unit.append([row_string[8-i] + col_string[i] for i in range(9)])
    square_unit = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]
    unit_list = row_unit + col_unit + square_unit + diag_unit
    # unit_list = row_unit + col_unit + square_unit
    units = dict((s, [t for t in unit_list if s in t]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
    hasBeenInitialized = True

if __name__ == '__main__':
    diag_sudoku_grid = '.8..794...........3..5..9........1..........2..........72......8.1.....7...4.7.1.'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
