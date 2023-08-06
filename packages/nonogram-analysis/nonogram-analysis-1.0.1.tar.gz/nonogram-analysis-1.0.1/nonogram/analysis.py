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

import datetime
import enum
import math
import os


# Relative weights of the efficiency (ratio between the optional number
# of actions to solve a nonogram and the number of actions actually
# performed by a player to complete the nonogram) and the speed (ratio
# between the optimal duration to solve a nonogram and the actual
# duration it took to a player to complete the nonogram).  These weights
# are used to calculate the overall score of the player.
EFFICIENCY_AND_SPEED_SCORE_WEIGHTS = {
    3: (1, 1),
    5: (3/5, 2/5),
    8: (2/3, 1/3),
    10: (3/4, 1/4)
}

# Duration in milliseconds for a player to think and perform the next
# action in order to solve a nonogram.  This value is totally empirical.
OPTIMAL_TIME_PER_ACTION = {
    3: 0.8 * 1000,
    5: 0.9 * 1000,
    8: 1.3 * 1000,
    10: 1.8 * 1000
}


class NonogramAction:
    """
    Represent an action performed by a player on the cell of a nonogram.

    A player can either fill the cell, either mark the cell to indicate
    that this cell actually is blank, or either clear the cell.
    """
    # Represent the different possible action of a player.
    ActionType = enum.Enum(
        'ActionType',
        'F M C'
    )

    EPOCH = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)

    @classmethod
    def __get_unix_timestamp_milliseconds(cls, timestamp):
        return int((timestamp - cls.EPOCH).total_seconds() * 1000)

    def __init__(self, action_type, x, y, action_time):
        """
        Build an object `NonogramAction`.


        :param action_type: An item of the enumeration `ActionType`.

        :param x: The column number of the cell, starting with `0`.

        :param y: The row number of the cell, starting with `0`.

        :param action_time: An object `datetime`, with milliseconds precision,
            representing the exact time when the player performed this action.
        """
        self.__x = x
        self.__y = y
        self.__type = action_type
        self.__time = action_time

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'{self.__class__.__name__}.{self.__type}, ' \
               f'{self.__x}, {self.__y}, ' \
               f'{repr(self.__time)})'

    def __str__(self):
        return f'{str(self.__type).split(".")[1]}' \
               f'-{self.__x}-{self.__y}' \
               f'-{self.__get_unix_timestamp_milliseconds(self.__time)}'

    @classmethod
    def from_strings(cls, s):
        if s:
            return [
                cls.from_string(substring)
                for substring in s.strip().split(',')
            ]

    @classmethod
    def from_string(cls, s):
        """
        Convert a string representation of an action performed on the cell of
        a nonogram to an object `NonogramAction`.


        :param s: A string representation of a player's action performed on
            the cell of a nonogram:

                action ::= action_type "-" cell_x "-" cell_y "-" action_time
                action_time ::= integer
                action_type ::= "F" | "M" | "C"
                cell_x ::= integer
                cell_y ::= integer

            For example:

                F-3-5-1586485456389


        :return: An object `NonogramAction`
        """
        if s:
            action_type, x, y, timestamp = s.strip().split('-')
            return NonogramAction(
                cls.ActionType[action_type],
                int(x),
                int(y),
                datetime.datetime.fromtimestamp(int(timestamp) / 1000, tz=datetime.timezone.utc))

    @property
    def time(self):
        return self.__time

    @property
    def type(self):
        return self.__type

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class NonogramClues:
    """
    Represent the clues of a nonogram.

    The clues of a nonogram indicate for each column and each row of the
    nonogram the length of groups of marks of a column, respectively of a
    row, separated with one or more blanks:

                ║   | 1 |   | 3 | 1 |   |   | 2 ║
                ║ 6 | 3 | 6 | 1 | 1 | 1 | 3 | 2 ║
                ║ 1 | 1 | 1 | 2 | 1 | 6 | 1 | 1 ║å
        ========+===+===+===+===+===+===+===+===+
              6 ║ X | X | X | X | X | X |   |   ║
        --------+---+---+---+---+---+---+---+---+
          1 2 1 ║ X |   | X | X |   |   |   | X ║
        --------+---+---+---+---+---+---+---+---+
              8 ║ X | X | X | X | X | X | X | X ║
        --------+---+---+---+---+---+---+---+---+
            3 2 ║ X | X | X |   |   | X | X |   ║
        --------+---+---+---+---+---+---+---+---+
              8 ║ X | X | X | X | X | X | X | X ║
        --------+---+---+---+---+---+---+---+---+
        1 1 1 1 ║ X |   | X |   |   | X |   | X ║
        --------+---+---+---+---+---+---+---+---+
            1 2 ║   |   |   | X |   | X | X |   ║
        --------+---+---+---+---+---+---+---+---+
          4 1 1 ║ X | X | X | X |   | X |   | X ║
        ========+===+===+===+===+===+===+===+===+

    The clues of a nonogram can be represented with a string that follows
    the specification of the Nonogram Clues Language v1.0:

    ```text
    column_clues ::= integer "-" column_clues | integer
    columns_clues ::= column_clues "," columns_clues | column_clues

    row_clues ::= integer "-" row_clues | integer
    rows_clues ::= row_clues "," rows_clues | row_clues

    clues :== columns_clues "|" rows_clues
    ```

    The clues of the previous nonogram can be represented with the following string:

    ```text
    6-1,1-3-1,6-1,3-1-2,1-1-1,1-6,3-1,2-2-1|6,1-2-1,8,3-2,8,1-1-1-1,1-2,4-1-1
    ```
    """
    @staticmethod
    def __convert_clues_to_string(clues):
        """
        Return a string representation of the clues o the nonogram's columns
        or rows.

        The format of this string respect the



        :param clues: A tuple of tuples of integers representing the clues of
            the nonogram's columns or rows.


        :return: A string representation of these clues.
        """
        return ','.join([
            '-'.join([str(clue) for clue in components])
            for components in clues
        ])

    def __init__(self, column_clues, row_clues):
        """

        :param column_clues: A tuple of tuples of integers representing the
            clues of the nonogram's columns from left to right.

        :param row_clues: A tuple of tuples of integers representing the clues
            of the nonogram's rows from top to bottom.
        """
        self.__column_clues = column_clues
        self.__row_clues = row_clues

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__column_clues}, {self.__row_clues})'

    def __str__(self):
        return f'{self.__convert_clues_to_string(self.__column_clues)}' \
               f'|{self.__convert_clues_to_string(self.__row_clues)}'

    @staticmethod
    def __split_lines_clues(s):
        """
        Split the string representing the clues of the columns or the rows of
        a Nonogram to arrays of integers.


        :param s: A string representation of the clues of the columns or the
            rows of a Nonogram, as recognized by the following regular
            expression:

                ((\d-)*\d,)*(\d-)*\d

            For example:

                '6-1,1-3-1,6-1,3-1-2,1-1-1,1-6,3-1,2-2-1'


        :return: An array representing the clues of each column (or each row)
            of the nonogram.

            For example:

                ((6, 1), (1, 3, 1), (6, 1), (3, 1, 2), (1, 1, 1), (1, 6), (3, 1), (2, 2, 1))
        """
        lines_clues = tuple((
            tuple((int(clue_str) for clue_str in line_clues_str.split('-')))
            for line_clues_str in s.split(',')
        ))

        return lines_clues

    @property
    def column_clues(self):
        """
        Return the row clues of the nonogram.


        :return: A tuple of clues for each column of the nonogram, from left to
            right.  The clues of a particular column correspond to a tuple of
            integers that indicate the length of vertical groups of
            marks, from top to bottom, separated with one or more blanks.

            For example:

                ((6, 1), (1, 3, 1), (6, 1), (3, 1, 2), (1, 1, 1), (1, 6), (3, 1), (2, 2, 1))
        """
        return self.__column_clues

    @classmethod
    def from_string(cls, s):
        """
        Convert a string representation of the clues of a nonogram to an
        object `NonogramClues`.


        :param s: A string representation of the columns' and the rows' clues
            of a nonogram.

            The clues of a column from to to bottom, respectively the clues of a
            row from left to right, correspond to integers separated with the
            character hyphen (`-`).

                column_clues ::= integer "-" column_clues | integer
                row_clues ::= integer "-" row_clues | integer

            The clues of all the columns from left to right, respectively the
            clues of all the rows for top to bottom, are separated with the
            character comma (`,`):

                columns_clues ::= column_clues "," columns_clues | column_clues
                rows_clues ::= row_clues "," rows_clues | row_clues

            The column clues and the row clues, in that order, are separated with
            the character pipe (`|`):

                clues :== columns_clues "|" rows_clues


        :return: An object `NonogramClues`.
        """
        if not isinstance(s, str):
            raise TypeError("The argument 's' MUST be a string")

        if not s:
            raise ValueError("The argument 's' MUST not be empty")

        try:
            column_clues_str, row_clues_str = s.strip().split('|')
            column_clues = cls.__split_lines_clues(column_clues_str)
            row_clues = cls.__split_lines_clues(row_clues_str)
        except ValueError:
            raise ValueError("The argument 's' MUST respect the Backus–Naur Form of a nonogram clues")

        return NonogramClues(column_clues, row_clues)

    @property
    def row_clues(self):
        """
        Return the row clues of the nonogram.


        :return: A tuple of clues for each row of the nonogram, from top to
            bottom.  The clues of a particular row correspond to a tuple of
            integers that indicate the length of horizontal groups of marks,
            from left to right, separated with one or more blanks.

            For example:

                ((6), (1, 2, 1), (8), (3, 2), (8), (1, 1, 1, 1), (1, 2), (4, 1, 1))
        """
        return self.__row_clues


class NonogramSession:
    """
    Represent the game session of a user who played a nonogram puzzle.
    """
    @staticmethod
    def __build_cells(clues, actions):
        """
        Build the 2D array of the player's answer to the nonogram.


        :param clues: An object `NonogramClues` representing the clues of the
            nonogram that the player tried or succeeded in solving.

        :param actions: A list of objects `NonogramActions`, order by
            ascending time, corresponding to the actions that the player
            performed to solve the nonogram.


        :return: A 2D array that represents the cells, from top to down, and
            from left to right, which boolean values indicate whether the
            respective cell has been filled or not.

            For example:

                [
                    [True, False, True, True, True, False],
                    [False, True, False, False, True, False],
                    [True, True, False, True, True, False],
                    [True, False, True, True, False, True],
                    [True, True, True, True, False, True],
                    [False, True, True, False, True, True],
                    [False, True, False, True, False, True]
                ]
        """
        # Build the 2D array of cells with the initial value `False` that
        # indicates that the cells are empty.
        #
        # @warning: Don't try this "optimization":
        #
        #     [[False] * len(clues.column_clues)] * len(clues.row_clues)
        #
        # https://docs.python.org/3/faq/programming.html#how-do-i-create-a-multidimensional-list
        cells = [
            [False] * len(clues.column_clues)
            for _ in range(len(clues.row_clues))
        ]

        # Replay the actions of the player to fill or to clear the cells of
        # his answer to the nonogram.
        for action in actions:
            cells[action.y][action.x] = action.type == NonogramAction.ActionType.F

        return cells

    @staticmethod
    def __build_clues(line):
        """
        Build the clues corresponding to a line of pixels.


        :param line: A string representing the line of a nonogram (either a
            column or a row) which cells has been colored (whatever character
            except a space character) or left blank (a space character).  For
            example:

                ' XXX X  XX  '


        :return: A list of numbers that indicate how many groups of filled or
            colored squares are contained in each row or column, and how many
            uninterrupted colored squares each group contains.  For example:

                (3, 1, 2)
        """
        pixel_groups = line.split()
        clues = (0,) if len(pixel_groups) == 0 else tuple([len(s) for s in pixel_groups])
        return clues

    def __init__(self, user, start_time, clues, actions):
        """
        Build a new object `NonogramSession`.


        :param user: An object `User` representing the player who solved (or
            not) a nonogram.

         :param start_time: Time when the nonogram game session started, i.e.,
            the time when nonogram was displayed to the player.

        :param clues: A list of objects `NonogramClues` corresponding to the
            clues of the nonogram that was given to the player to solve.

        :param actions: A list of objects `NonogramActions` that represent the
            actions the player performed to solve (or not) the nonogram.  This
            list can be given in whatever order of the actions that were
            performed.
        """
        self.__user = user
        self.__start_time = start_time
        self.__clues = clues
        self.__actions = [] if actions is None else sorted(actions, key=lambda action: action.time)

        # All the following attributes are evaluated using a lazy loading
        # technique.  THESE ATTRIBUTES MUST NOT BE DIRECTLY USED, BUT THEIR
        # RESPECTIVE PROPERTIES.
        self.__cells = None
        self.__is_solved = None
        self.__score = None
        self.__width = None
        self.__height = None

    def __is_nonogram_solved(self):
        """
        Indicate whether a given proposed solution of a nonogram successfully
        matches the clues of this nonogram.

        For instance, providing the following clues of a nonogram:

                  ║   |   |   | 1 |   |   ║
                  ║ 1 | 2 | 1 | 3 | 3 |   ║
                  ║ 3 | 3 | 3 | 1 | 1 | 4 ║
            ======+===+===+===+===+===+===+
              1 3 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
              1 1 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
              2 2 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
            1 2 1 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
              4 1 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
              2 2 ║   |   |   |   |   |   ║
            ------+---+---+---+---+---+---+
            1 1 1 ║   |   |   |   |   |   ║
            ======+===+===+===+===+===+===+

        represented as:

        ```python
        >>> nonogram_session.clues.column_clues
        ((1, 3), (2, 3), (1, 3), (1, 3, 1), (3, 1), (4))
        >>> nonogram_session.clues.row_clues
        ((1, 3), (1, 1), (2, 2), (1, 2, 1), (4, 1), (2, 2), (1, 1, 1))
        ```

        and a user-defined solution of this nonogram:

                  ║   |   |   | 1 |   |   ║
                  ║ 1 | 2 | 1 | 3 | 3 |   ║
                  ║ 3 | 3 | 3 | 1 | 1 | 4 ║
            ======+===+===+===+===+===+===+
              1 3 ║ 1 | 0 | 1 | 1 | 1 | 0 ║
            ------+---+---+---+---+---+---+
              1 1 ║ 0 | 1 | 0 | 0 | 1 | 0 ║
            ------+---+---+---+---+---+---+
              2 2 ║ 1 | 1 | 0 | 1 | 1 | 0 ║
            ------+---+---+---+---+---+---+
            1 2 1 ║ 1 | 0 | 1 | 1 | 0 | 1 ║
            ------+---+---+---+---+---+---+
              4 1 ║ 1 | 1 | 1 | 1 | 0 | 1 ║
            ------+---+---+---+---+---+---+
              2 2 ║ 0 | 1 | 1 | 0 | 1 | 1 ║
            ------+---+---+---+---+---+---+
            1 1 1 ║ 0 | 1 | 0 | 1 | 0 | 1 ║
            ======+===+===+===+===+===+===+

        represented as:

        ```python
        >>> cells = [
        ...    [True, False, True, True, True, False],
        ...    [False, True, False, False, True, False],
        ...    [True, True, False, True, True, False],
        ...    [True, False, True, True, False, True],
        ...    [True, True, True, True, False, True],
        ...    [False, True, True, False, True, True],
        ...    [False, True, False, True, False, True]
        ]
        ```

        The function `is_nonogram_solved` checks whether the given proposed
        solution matches the clues of the nonogram:

        ```python
        >>> print(nonogram_session.__is_nonogram_solved())  # Fake call of a private method
        True
        ```

        :return: `True` if the given proposed solution successfully matches
            the clues of the nonogram; `False` otherwise.
        """
        # Build the nonogram's columns clues and rows clues from the proposed
        # solution, and check whether they both match the given nonogram's
        # clues.
        #
        # The following code first processes the columns, then the rows of the
        # proposed solution.
        #
        # 1. It converts the cell's content of a given column (then row) of the
        #    proposed solution to a string composed of `X` if the corresponding
        #    cell is filled, or ` ` if not. For instance:
        #
        #         (1, 0, 1, 1, 1, 0, 0) -> 'X XXX  '
        #
        # 2. It splits the string with ` ` into sequences. For instance:
        #
        #         'X XXX  ' -> ['X', 'XXX']
        #
        # 3. It counts the length of each sequence, and convert the list in a
        #    tuple. For instance:
        #
        #         ['X', 'XXX'] -> [1, 3] -> [1, 3]
        #
        # 4. It repeats this operation for each column (then row) of the proposed
        #    solution. For instance:
        #
        #        [[1, 0, 1, 1, 1, 0, 0] -> [[1, 3],
        #         [0, 1, 1, 0, 1, 1, 1]     [2, 3],
        #         [1, 0, 0, 1, 1, 1, 0]     [1, 3],
        #         [1, 0, 1, 1, 1, 0, 1]     [1, 3, 1],
        #         [1, 1, 1, 0, 0, 1, 0]     [3, 1],
        #         [0, 0, 0, 1, 1, 1, 1]]    [4,]]
        #
        # 5. It compares the built clues of the columns (rows) with the given
        #    clues of these columns (rows).
        answer_column_clues = tuple([
            self.__build_clues(
                ''.join([
                    'X' if self.cells[y][x] else ' '
                    for y in range(self.height)
                ]))
            for x in range(self.width)
        ])

        if answer_column_clues != self.__clues.column_clues:
            return False

        answer_row_clues = tuple([
            self.__build_clues(
                ''.join([
                    'X' if self.cells[y][x] else ' '
                    for x in range(self.width)
                ]))
            for y in range(self.height)
        ])

        return answer_row_clues == self.__clues.row_clues

    def __str__(self):
        return os.linesep.join([
            ''.join([
                'X' if column else '.'
                for column in row
            ])
            for row in self.cells
        ])

    @property
    def actions(self):
        """
        Return the actions performed by the user who player the nonogram.


        :return: A list of objects `NonogramActions` that represent the
            actions the player performed to solve (or not) the nonogram.
        """
        return self.__actions

    @property
    def cells(self):
        """
        Return A 2D array of the player's answer to the nonogram.


        :return: A 2D array that represents the cells, from top to bottom, and
            from left to right, which boolean values indicate whether the
            respective cell has been filled or not.

            For example:

                [
                    [True, False, True, True, True, False],
                    [False, True, False, False, True, False],
                    [True, True, False, True, True, False],
                    [True, False, True, True, False, True],
                    [True, True, True, True, False, True],
                    [False, True, True, False, True, True],
                    [False, True, False, True, False, True]
                ]
        """
        if self.__cells is None:
            self.__cells = self.__build_cells(self.__clues, self.__actions)

        return self.__cells

    @property
    def clues(self):
        """
        Return the clues of the nonogram.


        :return: A list of objects `NonogramClues` corresponding to the clues
            of the nonogram that was given to the player to solve.
        """
        return self.__clues

    @property
    def height(self):
        """
        Return the number of rows of the nonogram.


        :return: The number of rows of the nonogram.
        """
        if self.__height is None:
            self.__height = len(self.cells)

        return self.__height

    @property
    def is_solved(self):
        if self.__is_solved is None:
            self.__is_solved = self.__is_nonogram_solved()

        return self.__is_solved

    @property
    def size(self):
        """
        Return the size of the nonogram's matrix.


        :return: A tuple `(width, height)` that represents the number of
            columns, respectively the number of rows, of the nonogram.
        """
        return self.width, self.height

    @property
    def start_time(self):
        """
        Return the time when the nonogram game session started.


        :return: The time when nonogram was displayed to the player.
        """
        return self.__start_time

    @property
    def user(self):
        return self.__user

    @property
    def width(self):
        """
        Return the number of columns of the nonogram.


        :return: The number of columns of the nonogram.
        """
        if self.__width is None:
            self.__width = len(self.cells[0])

        return self.__width


def calculate_nonogram_effective_action_number(nonogram_session, toggle_mode=False):
    """
    Return the number of effective actions that the player performed to
    solve (or not) the nonogram.

    An effective action is an action that the player performs to fill or
    to clear a cell of the nonogram.


    :param nonogram_session: An object `NonogramSession`.

    :param toggle_mode: Indicate whether actions `F`ill, `M`ark, and
        `C`lear on a cell are performed by multiple clicks on this cell.
        In this mode,  marking a cell requires two clicks on the cell: the
        first click fills the cell, the second click marks the cell to
        indicate it should remain empty; a third click eventually clears
        the cell.  When this mode is active, a `M`ark action actually
        replaces a `F`ill action; the function ignores the first action `F`,
        when a second action `M` is perfomed on this cell.


    :return: The number of times the player filled or cleared cells of the
        nonogram.
    """
    return sum([
        -toggle_mode if action.type == NonogramAction.ActionType.M else 1
        for action in nonogram_session.actions
    ])


def calculate_nonogram_effective_duration(nonogram_session):
    """
    Return the duration of a nonogram session.


    :param nonogram_session: An object `NonogramSession`.


    :return: Duration in milliseconds between the time when the game
        session started and the time when the player performed his last
        action.
    """
    last_action = nonogram_session.actions[-1]
    time_delta = last_action.time - nonogram_session.start_time
    duration = time_delta.seconds * 1000 + time_delta.microseconds / 1000
    return duration


def calculate_nonogram_line_difficulty(clues, line_length):
    """
    Return the difficulty of a row or a column of a nonogram.


    :param clues: A tuple of integers representing the clues of the row or
        the column.

    :param line_length: The number of cells of the row or the column.


    :return: A decimal value between `0.0` and `1.0` representing the
        difficulty of the row or the column.
    """
    # Calculate the difficulty to fill the line based on the degree of
    # freedom (dof).
    #
    # Our methodology relies on the number of clues that are given to the
    # player to solve the line and the number of cells these clues allow
    # the player to fill in this line. The less choices (degree of freedom)
    # the player has to complete the line, the more deterministic, the
    # easier. The more possibilities, the more difficult.
    clues_count = len(clues)
    clues_cell_count = sum(clues)
    dof_difficulty = 1.0 - (clues_count - 1 + clues_cell_count) / line_length

    # Calculate the difficulty to read and interpret the clues.
    #
    # A line can have a maximum of `n` clues, where `n` is half the number
    # of the cells contained in this line (each filled cell is followed
    # with an empty cell). For example, if a line has `8` cells, the
    # maximum number of clues is `4`:
    #
    # ```text
    # --------+---+---+---+---+---+---+---+---+
    # 1 1 1 1 ║ X |   | X |   | X |   | X |   ║
    # --------+---+---+---+---+---+---+---+---+
    # ```
    # We define the difficulty to read and interpret the clues of a line as
    # the ratio of the number of clues that are given (minus `1`) and the
    # maximum of clues a line of this length can have (minus `1`).
    max_clues_count = math.ceil(line_length / 2)
    clue_readability_difficulty = (clues_count - 1) / (max_clues_count - 1)

    # Calculate the overall difficulty to solve the line as the average of
    # the degree of freedom difficulty and the readability difficulty.
    overall_difficulty = (dof_difficulty + clue_readability_difficulty) / 2

    return overall_difficulty


def calculate_nonogram_optimal_action_number(nonogram_session):
    """
    Return the minimal number of actions to solve the nonogram.

    This number corresponds to the number of cells that need to be filled
    to solve the nonogram.


    :param nonogram_session: An object `NonogramSession`. The player MUST
        have solved this nonogram; the function does calculate a solution
        for this nonogram (which is out of the scope of this library only
        used for scoring a player who successfully solved a nonogram).


    :return: An integer corresponding to the minimal number of actions to
        solve the nonogram.

    :raise ValueError: If the player didn't solve the nonogram.
    """
    if not nonogram_session.is_solved:
        raise ValueError('This nonogram has not been solved')

    return len([cell for cell in flatten_list(nonogram_session.cells) if cell])


def calculate_nonogram_optimal_duration(nonogram_session, optimal_time_per_action):
    """
    Return the optimal duration to solve the nonogram.


    :param nonogram_session: An object `NonogramSession`. The player MUST
        have solved this nonogram; the function does calculate a solution
        for this nonogram (which is out of the scope of this library only
        used for scoring a player who successfully solved a nonogram).

    :param optimal_time_per_action: Duration in milliseconds for a player
        to think and perform the next action in order to solve a nonogram.
        This value is totally empirical.


    :return: The optimal duration in milliseconds to solve the nonogram.
    """
    cell_count = nonogram_session.width * nonogram_session.height

    # Calculate the overall average difficulty of the nonogram based on the
    # difficulty of every column and row of this nonogram.
    column_difficulties = sum([
        calculate_nonogram_line_difficulty(
            nonogram_session.clues.column_clues[i],
            nonogram_session.height)
       for i in range(nonogram_session.width)
    ])

    row_difficulties = sum([
        calculate_nonogram_line_difficulty(
            nonogram_session.clues.row_clues[j],
            nonogram_session.width)
        for j in range(nonogram_session.height)
    ])

    difficulty = (column_difficulties + row_difficulties) / cell_count

    # Calculate the estimated duration for a player to solve a nonogram
    # based on the number of cells that composed the nonogram and the
    # optimal time per action.
    standard_duration = cell_count * optimal_time_per_action

    # Calculate the optimal duration as the estimated duration to complete
    # a nonogram of this size, weighted with the actual difficulty of this
    # nonogram.
    optimal_duration = standard_duration * (1 - difficulty)

    return optimal_duration


def calculate_nonogram_score(nonogram_session):
    """
    Calculate the score of the player who solved or not the nonogram.


    @note: The current implementation of this method is totally empiric,
        and it doesn't take into account the real complexity of the
        nonogram.


    :return: A decimal or an integer, from `0.0` to `1.0`, representing
        the score of the user's answer to the nonogram. `0.0` is the worst
        possible score, while `1.0` is the best possible score.
    """
    if not nonogram_session.is_solved:
        return 0.0

    # Calculate the player's efficiency as the ratio between the optimal
    # number of actions to solve the nonogram with the actual number of
    # actions the player performed to solved this nonogram.
    optimal_action_number = calculate_nonogram_optimal_action_number(nonogram_session)
    effective_action_number = calculate_nonogram_effective_action_number(nonogram_session)
    efficiency_score = optimal_action_number / effective_action_number

    # Calculate the player' speed to complete the nonogram as the ration
    # between the optimal duration to solve the nonogram with the actual
    # duration it took to the player to solve this nonogram.
    optimal_duration = calculate_nonogram_optimal_duration(
        nonogram_session,
        OPTIMAL_TIME_PER_ACTION[nonogram_session.width])
    effective_duration = calculate_nonogram_effective_duration(nonogram_session)
    speed_score = optimal_duration / effective_duration

    # Calculate the overall score of the player as the weighted average of
    # the efficiency score and the speed score of the player.
    efficiency_weight, speed_weight = EFFICIENCY_AND_SPEED_SCORE_WEIGHTS[nonogram_session.width]

    score = calculate_weighted_average([
        (efficiency_weight, efficiency_score),
        (speed_weight, speed_score)
    ])

    return score


def calculate_weighted_average(weighted_values):
    """
    Return the average of a list of weighted values.


    :param weighted_values: A list of tuples `weight, value`.


    :return: The average of the weighted values.
    """
    weights, values = zip(*weighted_values)
    total_weight = sum(weights)
    total_value = sum(values)
    weighted_average = total_value / total_weight
    return weighted_average


def convert_nonogram_clues_string_to_tuples(s):
    """
    Convert a string representing the clues of a nonogram to tuples of
    integers.


    :param s: A string representation of the columns' and the rows' clues
        of a nonogram.

        The clues of a column from to to bottom, respectively the clues of a
        row from left to right, correspond to integers separated with the
        character hyphen (`-`).

            column_clues ::= integer "-" column_clues | integer
            row_clues ::= integer "-" row_clues | integer

        The clues of all the columns from left to right, respectively the
        clues of all the rows for top to bottom, are separated with the
        character comma (`,`):

            columns_clues ::= column_clues "-" columns_clues | column_clues
            rows_clues ::= row_clues "-" rows_clues | row_clues

        The column clues and the row clues, in that order, are separated with
        the character pipe (`|`):

            clues :== columns_clues "|" rows_clues


    :return: A tuple `(column_clues, row_clues)` where:

        * `column_clues`: A tuple of tuples of integers representing the clues
          of the nonogram's columns from left to right.

        * `row_clues`: A tuple of tuples of integers representing the clues of
          the nonogram's rows from top to bottom.
    """
    if not isinstance(s, str):
        raise TypeError("The argument 's' MUST be a string")

    if not s:
        raise ValueError("The argument 's' MUST not be empty")

    try:
        column_clues_str, row_clues_str = s.strip().split('|')
        column_clues = split_lines_clues(column_clues_str)
        row_clues = split_lines_clues(row_clues_str)
    except ValueError:
        raise ValueError("The argument 's' MUST respect the Backus–Naur Form of a nonogram clues")

    return column_clues, row_clues


def flatten_list(l):
    """
    Flatten the elements contained in the sub-lists of a list.


    :param l: A list containing sub-lists of elements.


    :return: A list with all the elements flattened from the sub-lists of
        the list `l`.
    """
    return [e for sublist in l for e in sublist]


def split_lines_clues(s):
    """
    Split the string representing the clues of the columns or the rows of
    a Nonogram to arrays of integers.


    :param s: A string representation of the clues of the columns or the
        rows of a Nonogram, as recognized by the following regular
        expression

            ((\d-)*\d,)*(\d-)*\d

        For example:

            '6-1,1-3-1,6-1,3-1-2,1-1-1,1-6,3-1,2-2-1'


    :return: A tuple representing the clues of each column (or each row)
        of the nonogram.

        For example:

            ((6, 1), (1, 3, 1), (6, 1), (3, 1, 2), (1, 1, 1), (1, 6), (3, 1), (2, 2, 1))
    """
    lines_clues = tuple([
        tuple([int(clue_str) for clue_str in line_clues_str.split('-')])
        for line_clues_str in s.split(',')
    ])

    return lines_clues
