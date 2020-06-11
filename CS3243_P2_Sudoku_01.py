# CS3243 Introduction to Artificial Intelligence
# Project 2, Part 1: Sudoku

import sys
import copy
import operator


# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


class Node:
    def __init__(self, unassigned_vars, assigned_vars):
        unassigned_vars.sort(key=lambda x: len(x.domain))
        self.variables = unassigned_vars
        self.assigned_vars = assigned_vars


class Cell:
    def __init__(self, cell_id, dom):
        self.domain = dom
        self.cell_id = cell_id

    def remove_number(self, current_number):
        if current_number in self.domain:
            self.domain.remove(current_number)


def init_solve(puzzle_grid, coordinates):
    unassigned_vars = []
    assigned_vars = dict()
    cell_id = 1

    for index in xrange(0, 9):
        for index2 in xrange(0, 9):

            cell_integer = puzzle_grid[index][index2]
            if cell_integer != 0:
                assigned_vars[cell_id] = cell_integer
            else:
                domain = set(xrange(1, 10))
                unassigned_vars.append(Cell(cell_id, domain))

            coordinates[cell_id] = (index + 1, index2 + 1, (index // 3) * 3 + ((index2 // 3) + 1))
            cell_id += 1

    return init_domain_update(unassigned_vars, assigned_vars, coordinates)


def init_domain_update(unassigned_vars, assigned_vars, coordinates):
    for init_var in assigned_vars.items():
        retrieved_num = coordinates.get(init_var[0])
        row_num = retrieved_num[0]
        col_num = retrieved_num[1]
        box_num = retrieved_num[2]

        for unassigned_var in unassigned_vars:
            retrieved_unassigned_num = coordinates.get(unassigned_var.cell_id)

            if (row_num == retrieved_unassigned_num[0]
                    or col_num == retrieved_unassigned_num[1]
                    or box_num == retrieved_unassigned_num[2]):
                unassigned_var.remove_number(init_var[1])

    return Node(unassigned_vars, assigned_vars)


def domain_update(unassigned_vars, assigned_vars, number, coordinates):
    working_list = []
    new_assigned_vars = assigned_vars.copy()

    new_assigned_vars[unassigned_vars[0].cell_id] = number

    retrieved_num = coordinates.get(unassigned_vars[0].cell_id)
    row_num = retrieved_num[0]
    col_num = retrieved_num[1]
    box_num = retrieved_num[2]

    # skip the first element
    iter_vars = iter(unassigned_vars)
    next(iter_vars)

    # update the domain of the rest of the variables
    for unassigned_vars in iter_vars:
        retrieved_unassigned_num = coordinates.get(unassigned_vars.cell_id)

        if (row_num == retrieved_unassigned_num[0]
                or col_num == retrieved_unassigned_num[1]
                or box_num == retrieved_unassigned_num[2]):

            # check if domain has only 1 domain left and then if the number is in it, return false
            if len(unassigned_vars.domain) == 1 and number in unassigned_vars.domain:
                return False, False
            else:
                working_list.append(Cell(unassigned_vars.cell_id, unassigned_vars.domain.difference({number})))

        else:
            working_list.append(unassigned_vars)

    return True, Node(working_list, new_assigned_vars)


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

    def solve(self):
        # self.ans is a list of lists
        # outer list is the row, inner list is col-wise
        global current_state
        coordinates = dict()
        stack = [init_solve(puzzle, coordinates)]

        while stack:
            current_state = stack.pop()

            if current_state.variables:
                assignment_list = find_value(current_state.variables, coordinates)
                for n in assignment_list:
                    result = domain_update(current_state.variables, current_state.assigned_vars, n, coordinates)
                    if result[0]:
                        stack.append(result[1])
            else:
                # no variables left to perform assignment
                break

        for var in current_state.assigned_vars.items():
            coords = coordinates.get(var[0])

            self.ans[coords[0] - 1][coords[1] - 1] = var[1]

        return self.ans


def find_value(variables, coordinates):
    if len(variables[0].domain) == 1:
        return variables[0].domain
    else:
        tracker = dict()

        retrieved_num = coordinates.get(variables[0].cell_id)

        row_num = retrieved_num[0]
        col_num = retrieved_num[1]
        box_num = retrieved_num[2]

        for numbers in variables[0].domain:
            tracker[numbers] = 1

        iter_vars = iter(variables)
        next(iter_vars)
        for var in iter_vars:

            other_retrieved_num = coordinates.get(var.cell_id)

            if (row_num == other_retrieved_num[0]
                    or col_num == other_retrieved_num[1]
                    or box_num == other_retrieved_num[2]):
                for scanning_var in var.domain:
                    if scanning_var in tracker:
                        tracker[scanning_var] += 1

    ordered_variables = sorted(tracker.items(), key=lambda x: x[1])
    assignment_list = map(operator.itemgetter(0), ordered_variables)

    return assignment_list


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
