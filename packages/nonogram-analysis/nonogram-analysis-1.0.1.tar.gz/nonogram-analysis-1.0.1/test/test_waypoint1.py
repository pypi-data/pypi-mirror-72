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

import pytest

from nonogram import analysis

def __generate_random_clues():
    return tuple([
        tuple([random.randint(1, 3) for _ in range(random.randint(1, 3))])
        for _ in range(random.randint(3, 10))
    ])


def __convert_clues_to_string(clues):
    return ','.join(['-'.join([str(clue) for clue in components]) for components in clues])


def test_convert_nonogram_clues_string_to_tuples():
    column_clues = __generate_random_clues()
    row_clues = __generate_random_clues()
    clues = column_clues, row_clues

    clues_string = '|'.join([
        __convert_clues_to_string(column_clues),
        __convert_clues_to_string(row_clues)
    ])

    assert analysis.convert_nonogram_clues_string_to_tuples(clues_string) == clues


def test_convert_nonogram_clues_string_to_tuples_wrong_argument():
    with pytest.raises(TypeError) as exception_info:
        analysis.convert_nonogram_clues_string_to_tuples(True)
        analysis.convert_nonogram_clues_string_to_tuples(False)

