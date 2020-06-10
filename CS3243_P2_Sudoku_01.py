# CS3243 Introduction to Artificial Intelligence
# Project 2, Part 1: Sudoku

import sys
import copy


# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Node:
    def __init__(self, list_of_variables):
        list_of_variables.sort(key=lambda x: x.domain_size, reverse=False)

        self.variables = list_of_variables
        # self.puzzle = grid


class Cell:
    domain = set()
    cell_id = -1
    domain_size = -1
    assigned_number = -1
    row_num = -1
    col_num = -1
    box_num = -1

    def __init__(self, cell_id, dom, new_number):
        self.domain = dom
        self.cell_id = cell_id
        self.domain_size = sys.maxint if len(dom) == 0 else len(dom)
        self.assigned_number = new_number

        working_id = cell_id - 1
        row_num = working_id // 9
        col_num = working_id % 9

        # these numbers start from index 1
        self.row_num = row_num + 1
        self.col_num = col_num + 1
        self.box_num = (((self.row_num - 1) // 3)) * 3 + (((self.col_num - 1) // 3) + 1)

    def __str__(self):
        return "domain size: {0}, ID: {1}, domain: {2}, assigned number: {3}, coordinates: ({4}, {5}, {6})".format(
            self.domain_size, self.cell_id, self.domain, self.assigned_number, self.row_num, self.col_num, self.box_num)

    def assign_number(self, new_number):
        self.assigned_number = new_number

        # empty the domain, no longer need to maintain domain after number is assigned
        self.domain = set()
        self.domain_size = sys.maxint

    def remove_number(self, current_number):
        if current_number in self.domain:
            self.domain.remove(current_number)
            self.domain_size = sys.maxint if len(self.domain) == 0 else len(self.domain)


def init_solve(puzzle_grid):
    l = []
    i = 1

    for index in xrange(0, len(puzzle_grid)):
        for index2 in xrange(0, len(puzzle_grid[index])):
            domain = set(xrange(1, 10))

            cell_integer = puzzle_grid[index][index2]
            if cell_integer != 0:
                domain = set()

            current_cell = Cell(i, domain, cell_integer)
            l.append(current_cell)
            i += 1

    return Node(domain_update(l))


def domain_update(my_list):
    working_list = copy.deepcopy(my_list)

    for index in xrange(0, len(working_list)):
        # if assigned number is 0 don't need to try to change anything else
        if working_list[index].assigned_number == 0:
            continue
        else:
            current_element = working_list[index]

            for index_2 in xrange(0, len(working_list)):

                # skip number if current number is not 0
                # skip number of it is itself
                if working_list[index_2].assigned_number > 0 or index == index_2:
                    continue
                else:
                    if (current_element.row_num == working_list[index_2].row_num
                            or current_element.col_num == working_list[index_2].col_num
                            or current_element.box_num == working_list[index_2].box_num):

                        working_list[index_2].remove_number(current_element.assigned_number)

    return working_list


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

    def solve(self):
        # self.ans is a list of lists
        # outer list is the row, inner list is col-wise
        # global current_state

        global current_state, v
        start_state = init_solve(puzzle)
        stack = [start_state]
        completed = False

        while len(stack) > 0 and not completed:
            current_state = stack.pop()

            cull_state = False

            # check for invalid domain, unassigned but domain is empty
            # variables are ordered from smallest domain to max domain
            # however, empty domains are given a length of maxint so they're pushed to the end
            # this is why the algo checks from end to the start
            for i in xrange(len(current_state.variables) - 1, -1, -1):
                inspector_variable = current_state.variables[i]
                # ensures that the scanning is only done for variables that have empty domain
                if inspector_variable.domain_size < sys.maxint:
                    break
                elif inspector_variable.assigned_number == 0:
                    cull_state = True
                    break
            if cull_state:
                continue

            if current_state.variables[0].domain_size < 10:
                for n in current_state.variables[0].domain:
                    current_state.variables[0].assign_number(n)
                    unsorted_list = domain_update(current_state.variables)
                    stack.append(Node(unsorted_list))
            else:
                break

        for var in current_state.variables:
            self.ans[var.row_num - 1][var.col_num - 1] = var.assigned_number

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
