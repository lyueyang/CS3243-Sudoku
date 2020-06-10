# CS3243 Introduction to Artificial Intelligence
# Project 2, Part 1: Sudoku

import sys
import copy


# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


class Node:
    def __init__(self, unassigned_vars, assigned_vars):
        unassigned_vars.sort(key=lambda x: len(x.domain), reverse=False)
        self.variables = unassigned_vars
        self.assigned_vars = assigned_vars


class Cell:
    def __init__(self, cell_id, dom, new_number):
        self.domain = dom
        self.cell_id = cell_id
        self.assigned_number = new_number

    def assign_number(self, new_number):
        new_cell = Cell(self.cell_id, set(), new_number)
        new_cell.remove_domain()
        return new_cell

    def remove_number(self, current_number):
        if current_number in self.domain:
            self.domain.remove(current_number)

    def remove_domain(self):
        del self.domain

    def get_row(self):
        return (self.cell_id - 1) // 9 + 1

    def get_col(self):
        return (self.cell_id - 1) % 9 + 1

    def get_box(self):
        return ((self.get_row() - 1) // 3) * 3 + (((self.get_col() - 1) // 3) + 1)


def init_solve(puzzle_grid):
    unassigned_vars = []
    assigned_vars = dict()
    cell_id = 1

    for index in xrange(0, len(puzzle_grid)):
        for index2 in xrange(0, len(puzzle_grid[index])):

            cell_integer = puzzle_grid[index][index2]
            if cell_integer != 0:
                assigned_vars[cell_id] = cell_integer
            else:
                domain = set(xrange(1, 10))
                unassigned_vars.append(Cell(cell_id, domain, cell_integer))

            cell_id += 1

    return init_domain_update(unassigned_vars, assigned_vars)


def init_domain_update(unassigned_vars, assigned_vars):
    for init_var in assigned_vars.items():
        row_num = (init_var[0] - 1) // 9 + 1
        col_num = (init_var[0] - 1) % 9 + 1
        box_num = ((row_num - 1) // 3) * 3 + (((col_num - 1) // 3) + 1)

        for index_2 in xrange(0, len(unassigned_vars)):
            unassigned_row_num = unassigned_vars[index_2].get_row()
            unassigned_col_num = unassigned_vars[index_2].get_col()
            unassigned_box_num = unassigned_vars[index_2].get_box()

            if (row_num == unassigned_row_num
                    or col_num == unassigned_col_num
                    or box_num == unassigned_box_num):
                unassigned_vars[index_2].remove_number(init_var[1])

    return Node(unassigned_vars, assigned_vars)


def domain_update(unassigned_vars, assigned_vars, number):
    working_list = []
    new_assigned_vars = assigned_vars.copy()

    var = unassigned_vars[0].assign_number(number)
    # new_assigned_vars.append(var)
    new_assigned_vars[var.cell_id] = number

    for index in xrange(1, len(unassigned_vars)):
        row_num = var.get_row()
        col_num = var.get_col()
        box_num = var.get_box()

        if (row_num == unassigned_vars[index].get_row()
                or col_num == unassigned_vars[index].get_col()
                or box_num == unassigned_vars[index].get_box()):

            if len(unassigned_vars[index].domain) > 0:
                working_domain = set()

                if number in unassigned_vars[index].domain:
                    for n in unassigned_vars[index].domain:
                        if number != n:
                            working_domain.add(n)
                else:
                    for n in unassigned_vars[index].domain:
                        working_domain.add(n)

            else:
                working_domain = set()
            working_number = Cell(unassigned_vars[index].cell_id, working_domain, 0)
            working_list.append(working_number)
        else:
            working_list.append(unassigned_vars[index])

    return Node(working_list, new_assigned_vars)


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

    def solve(self):
        # self.ans is a list of lists
        # outer list is the row, inner list is col-wise
        global current_state
        stack = [init_solve(puzzle)]

        while len(stack) > 0:
            current_state = stack.pop()

            if len(current_state.variables) > 0:
                if len(current_state.variables[0].domain) > 0:
                    for n in current_state.variables[0].domain:
                        stack.append(domain_update(current_state.variables, current_state.assigned_vars, n))
                else:
                    # no vars with valid domains left.
                    # domain is valid when it is more than 0
                    # continue to quit this state
                    continue
            else:
                # no variables left to perform assignment
                break

        for var in current_state.assigned_vars.items():
            row_num = (var[0] - 1) // 9
            col_num = (var[0] - 1) % 9

            self.ans[row_num][col_num] = var[1]

        return self.ans


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
