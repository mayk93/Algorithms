#!/usr/bin/python
# -*- coding: utf-8 -*-

# Unicode
from __future__ import unicode_literals

import sys
reload(sys)
# -----

# Logging
import logging
logging.basicConfig(level=logging.INFO)
# -----


# Libs

# -----


# Constants

'''
IMPORTANT!

Refactor Table Object to be self aware of it's position on the table.
'''

class TableObject(object):
    def __init__(self, is_set=False, set_representation="[Q]", unset_representation = "[ ]"):
        self.set_representation = set_representation if isinstance(set_representation, unicode) else "[Q]"
        self.unset_representation = unset_representation if isinstance(unset_representation, unicode) else "[ ]"
        self.is_set = is_set
        self.representation = self.set_representation if self.is_set else self.unset_representation

    def __str__(self):
        return self.representation

    def set(self, value=True):
        self.is_set = value
        self.representation = self.set_representation if self.is_set else self.unset_representation


class Table(object):
    def __init__(self, size=0):
        # The actual table is a list of lists. In this contexts, a list of rows.
        self.table = []
        self.size = size

        for row_number in range(self.size):
            row = []
            for column_number in range(self.size):
                element = TableObject()
                element.representation = "[" + unicode(row_number) + " , " + unicode(column_number) + "]"
                row.append(element)
            self.table.append(row)

    def __str__(self):
        graphical_representation = ""
        for row in self.table:
            row_representation = ""
            for row_element in row:
                row_representation += " " + unicode(row_element) + " "
            graphical_representation += row_representation + "\n"
        return graphical_representation

    def get_column(self, column_number):
        if column_number > self.size:
            column_number = self.size
            logging.info("Clamped column_number to size.")
        column = []
        for row in self.table:
            column.append(row[column_number])
        return column

    def get_main_diagonal(self, row_number=0, column_number=0):
        diagonal = []
        original_row_number = row_number
        original_column_number = column_number
        while row_number < self.size and column_number < self.size:
            diagonal.append(self.table[row_number][column_number])
            row_number += 1
            column_number += 1
        row_number = original_row_number
        column_number = original_column_number
        while row_number > 0 and column_number > 0:
            row_number -= 1
            column_number -= 1
            diagonal.append(self.table[row_number][column_number])
        return diagonal

    def get_second_diagonal(self, row_number=0, column_number=0):
        diagonal = []
        original_row_number = row_number
        original_column_number = column_number
        while row_number >= 0 and column_number < self.size:
            diagonal.append(self.table[row_number][column_number])
            row_number -= 1
            column_number += 1
        row_number = original_row_number
        column_number = original_column_number
        while row_number < self.size and column_number >= 0:
            diagonal.append(self.table[row_number][column_number])
            row_number += 1
            column_number -= 1
        return list(set(diagonal))

    def set(self, row, column, value=True):
        self.table[row][column].set(value)

    def check(self, row_number, column_number):
        '''

        :param row_number: Row it is on
        :param column_number: Column it is on
        :return: True if no one attacks this element, False otherwise

           0   1   2   3
        0 [ ] [ ] [ ] [ ]
        1 [ ] [ ] [Q] [ ]
        2 [ ] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ]

        Consider this board.

        We must check for the element with row_number = 1 and column_number = 2 if:
            1. There are any other elements on the row (Check for elements in table[row_number])
            2. There are any other elements on the column (Check every column_number element of every row)
            3. There are any other elements on the diagonals
        '''
        set_elements_on_row = 0
        for element in self.table[row_number]:
            if element.is_set:
                set_elements_on_row += 1
            if set_elements_on_row > 1:
                return False

        set_elements_on_column = 0
        for element in self.get_column(column_number):
            if element.is_set:
                set_elements_on_column += 1
            if set_elements_on_column > 1:
                return False

        set_elements_on_main_diagonal = 0
        for element in self.get_main_diagonal(row_number, column_number):
            if element.is_set:
                set_elements_on_main_diagonal += 1
            if set_elements_on_main_diagonal > 1:
                return False

        set_elements_on_second_diagonal = 0
        for element in self.get_second_diagonal(row_number, column_number):
            if element.is_set:
                set_elements_on_second_diagonal += 1
            if set_elements_on_second_diagonal > 1:
                return False

        return True

    def is_correct(self):
        for row_number, row in enumerate(self.table):
            for column_number, element in enumerate(row):
                if element.is_set:  # We are only checking queens, that is, set elements
                    if not self.check(row_number, column_number):
                        return False
        return True

    def reset(self):
        for row in self.table:
            for element in row:
                element.set(value=False)


def main():
    table = Table(4)

if __name__ == '__main__':
    main()

import unittest

class TestTable(unittest.TestCase):
    def setUp(self):
        self.size = 4
        self.table = Table(self.size)

    def test_get_column(self):
        self.table.set(0, 0)
        self.table.set(2, 0)
        self.table.set(3, 0)

        column = self.table.get_column(0)

        self.assertEquals(3, len([table_object for table_object in column if table_object.is_set]))

        self.assertTrue(column[0].is_set)
        self.assertTrue(column[2].is_set)
        self.assertTrue(column[3].is_set)

        self.table.reset()

    def test_get_main_diagonal(self):
        '''
        [ <0, 0> <0, 1> [0, 2] [0, 3] ]
        [ [1, 0] [1, 1] <1, 2> [1, 3] ]
        [ [2, 0] [2, 1] [2, 2] <2, 3> ]
        [ [3, 0] [3, 1] [3, 2] [3, 3] ]

        Set (0, 0) and (0, 1), (1, 2), (2, 3)

        Main diagonal of (0, 1), (1, 2), (2, 3) should be the same and should not include (0, 0)

        :return:
        '''
        self.table.set(0, 0)
        self.table.set(0, 1)
        self.table.set(1, 2)
        self.table.set(2, 3)

        main_diagonal_0 = self.table.get_main_diagonal(0, 1)
        main_diagonal_1 = self.table.get_main_diagonal(1, 2)
        main_diagonal_2 = self.table.get_main_diagonal(2, 3)

        self.assertEquals(3, len([table_object for table_object in main_diagonal_0 if table_object.is_set]))
        self.assertEquals(3, len([table_object for table_object in main_diagonal_1 if table_object.is_set]))
        self.assertEquals(3, len([table_object for table_object in main_diagonal_2 if table_object.is_set]))

        main_diagonal_3 = self.table.get_main_diagonal(1, 1)


        self.assertEquals(1, len([table_object for table_object in main_diagonal_3 if table_object.is_set]))
