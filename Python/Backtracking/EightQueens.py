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
                row.append(TableObject())
            self.table.append(row)

    def __str__(self):
        graphical_representation = ""
        for row in self.table:
            row_representation = ""
            for row_element in row:
                row_representation += " " + unicode(row_element) + " "
            graphical_representation += row_representation + "\n"
        return graphical_representation

    def set(self, row, column, value=True):
        self.table[row][column].set(value)


def main():
    table = Table(4)
    print unicode(table)
    table.set(0, 2)
    print unicode(table)
    table.set(2, 0)
    print unicode(table)


if __name__ == '__main__':
    main()

