
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_units = [[r+c for r, c in zip(rows, cols)], [r+c for r, c in zip(rows, cols[::-1])]]
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    for unit in unitlist:
        two_values = [values[box] for box in unit if len(values[box]) == 2]
        if not two_values:
            continue
        if any([value for value in two_values if two_values.count(value) > 2]):
            return False
        
        twin_values = set(value for value in two_values if two_values.count(value) == 2)
        if not twin_values:
            continue
        twin_values_digits = ''.join(twin_values)
        if any([digit for digit in twin_values_digits if twin_values_digits.count(digit) > 1]):
            return False
        
        for value in twin_values:
            for box in unit:
                if value == values[box]:
                    continue
                if value[0] in values[box]:
                    assign_value(values, box, values[box].replace(value[0], ''))
                    #values[box] = values[box].replace(value[0], '')
                if value[1] in values[box]:
                    assign_value(values, box, values[box].replace(value[1], ''))
                    #values[box] = values[box].replace(value[1], '')
                    
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_boxes = [key for key, value in values.items() if len(value) == 1]
    for solved_box in solved_boxes:
        solved_value = values[solved_box]
        for peer_box in peers[solved_box]:
            assign_value(values, peer_box, values[peer_box].replace(solved_value, ''))
            #values[peer_box] = values[peer_box].replace(solved_value, '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            digit_boxes = [box for box in unit if digit in values[box]]
            if len(digit_boxes) == 1:
                assign_value(values, digit_boxes[0], digit)
                #values[digit_boxes[0]] = digit
                
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    if not reduce_puzzle(values):
        return False
    
    if not naked_twins(values):
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = [key for key, value in values.items() if len(value) > 1]
    if not unsolved_boxes:
        return values
    
    length, unsolved_box = min((len(values[unsolved_box]), unsolved_box) for unsolved_box in unsolved_boxes)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    #for unsolved_box in unsolved_boxes:
    for value in values[unsolved_box]:
        values_copy = values.copy()
        values_copy[unsolved_box] = value
        values_result = search(values_copy)
        if values_result:
            return values_result


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
