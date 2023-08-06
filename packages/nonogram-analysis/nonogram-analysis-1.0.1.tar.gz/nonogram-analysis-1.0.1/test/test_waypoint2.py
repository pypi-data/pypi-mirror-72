#!/usr/bin/env python
#
# Copyright (C) 2020 Intek Institute.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Intek Institute or one of its subsidiaries.  You shall not disclose
# this confidential information and shall use it only in accordance
# with the terms of the license agreement or other applicable
# agreement you entered into with Intek Institute.
#
# INTEK INSTITUTE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  INTEK
# INSTITUTE SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY
# LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS
# SOFTWARE OR ITS DERIVATIVES.

import random

from nonogram import analysis

def __generate_random_clues():
    return tuple([
        tuple([random.randint(1, 3) for _ in range(random.randint(1, 3))])
        for _ in range(random.randint(3, 10))
    ])


def __convert_clues_to_string(clues):
    return ','.join(['-'.join([str(clue) for clue in components]) for components in clues])


def test_nonogram_clues_constructor():
    column_clues = __generate_random_clues()
    row_clues = __generate_random_clues()
    analysis.NonogramClues(column_clues, row_clues)


def test_nonogram_clue_properties():
    column_clues = __generate_random_clues()
    row_clues = __generate_random_clues()
    nonogram_clues = analysis.NonogramClues(column_clues, row_clues)
    assert nonogram_clues.column_clues == column_clues
    assert nonogram_clues.row_clues == row_clues


def test_nonogram_clues_from_string():
    column_clues = __generate_random_clues()
    row_clues = __generate_random_clues()

    clues_string = '|'.join([
        __convert_clues_to_string(column_clues),
        __convert_clues_to_string(row_clues)
    ])

    nonogram_clues = analysis.NonogramClues.from_string(clues_string)
    assert nonogram_clues.column_clues == column_clues
    assert nonogram_clues.row_clues == row_clues


# def test_nonogram_clues_repr():  # comparison with Reference Implementation
#     column_clues = __generate_random_clues()
#     row_clues = __generate_random_clues()
#
#     clues_string = '|'.join([
#         __convert_clues_to_string(column_clues),
#         __convert_clues_to_string(row_clues)
#     ])
#
#     nonogram_clues = nonogram_analysis.NonogramClues.from_string(clues_string)

# def test_nonogram_clues_str():  # comparison with Reference Implementation
#     column_clues = __generate_random_clues()
#     row_clues = __generate_random_clues()
#
#     clues_string = '|'.join([
#         __convert_clues_to_string(column_clues),
#         __convert_clues_to_string(row_clues)
#     ])
#
#     nonogram_clues = nonogram_analysis.NonogramClues.from_string(clues_string)

