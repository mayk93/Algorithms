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


class QueenProblem(object):
    def __init__(self, size=0):
        self.size = size
        self.queenArray = [None for index in range(self.size)]

    def solve(self):
        self.place_queens(0)

    def place_queens(self, column_number):
        for row_number in range(self.size):
            if self.is_valid(row_number, column_number):
                '''
                # There is 1 queen per column. The queen of column column_number is on row row_number
                '''
                self.queenArray[column_number] = row_number

                if column_number == self.size - 1:
                    self.print_board()
                else:
                    self.place_queens(column_number + 1)

    def is_valid(self, row_number, column_number):
        for column in range(column_number):
            if self.queenArray[column] == row_number:
                return False
            if (column - column_number) == (self.queenArray[column] - row_number):
                return False
            if (column - column_number) == (row_number - self.queenArray[column]):
                return False
        return True

    def print_board(self):
        for column_number in range(self.size):
            for row_number  in range(self.size):
                if self.queenArray[column_number] == row_number:
                    print ("[Q]"),
                else:
                    print ("[ ]"),
            print "\n"
        print "\n"


def main():
    queensProblem = QueenProblem(6)
    queensProblem.solve()

# XY
if __name__ == "__main__":
    main()