# Nonogram Analysis

A [nonogram](https://en.wikipedia.org/wiki/Nonogram) is a puzzle game in which cells in a grid must be colored or left blank according to numbers at the side of the grid to reveal a hidden picture.

**Nonogram Analysis** is a Python library used to score a player who has completed a nonogram.

## Nonogram Clues

The clues of a nonogram indicate for each column and each row of the nonogram the length of groups of marks of a column, respectively of a row, separated with one or more blanks.

For example:

```text
            ║   | 1 |   | 3 | 1 |   |   | 2 ║
            ║ 6 | 3 | 6 | 1 | 1 | 1 | 3 | 2 ║
            ║ 1 | 1 | 1 | 2 | 1 | 6 | 1 | 1 ║
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
```

We define the following language, using [Backus–Naur Form (BNF)](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form), to declare the clues of a nonogram:

```text
column_clues ::= integer "-" column_clues | integer
columns_clues ::= column_clues "," columns_clues | column_clues

row_clues ::= integer "-" row_clues | integer
rows_clues ::= row_clues "," rows_clues | row_clues

clues :== columns_clues "|" rows_clues
```

The clues of the nonogram above are:

```text
6-1,1-3-1,6-1,3-1-2,1-1-1,1-6,3-1,2-2-1|6,1-2-1,8,3-2,8,1-1-1-1,1-2,4-1-1
```

**Nonogram Analysis** supports the class `NonogramClues` to build the clues of a nonogram.

For example:

```python
>>> from nonogram.analysis import NonogramClues
>>> nonogram_clues = NonogramClues.from_string('1-1,1-1,2|2,1,3')
```

## Nonogram Actions

We define the following Backus–Naur Form (BNF) to describe the syntax of a player's action performed on the cell of a nonogram:

```text
action ::= action_type "-" cell_x "-" cell_y "-" action_time
action_time ::= integer
action_type ::= "F" | "M" | "C"
cell_x ::= integer
cell_y ::= integer
```

The term `cell_x` and `cell_y` represent the location of a cell in the nonogram's matrix. The origin `(0, 0)` of the nonogram is located at the topmost leftmost of the matrix.

The term `action_time` represents a variant of the [UNIX timestamp](https://www.epochconverter.com/), that is the number of milliseconds that have elapsed since the Unix epoch (00:00:00 UTC on 1 January 1970), minus leap seconds.

The term `action_type` represents the different possible action of a player:

- `F`: Fill the cell
- `M`: Mark the cell to indicate it is empty
- `C`: Clear the cell

For example:

```text
F-5-3-1586485456389
```

Represents the action of filling the cell `(5, 3)` of a nonogram, performed by a player on Friday, April 10, 2020 at 02:24:16.389 AM:

```text
      ║   |   |   |   |   |   |   |
    ==+===+===+===+===+===+===+===+...
      ║   |   |   |   |   |   |   |
    --+---+---+---+---+---+---+---+...
      ║   |   |   |   |   |   |   |
    --+---+---+---+---+---+---+---+...
      ║   |   |   |   |   |   |   |
    --+---+---+---+---+---+---+---+...
      ║   |   |   |   |   | X |   |
    --+---+---+---+---+---+---+---+...
      :   :   :   :   :   :   :   :
      .   .   .   .   .   .   .   .
```

**Nonogram Analysis** supports the class `NonogramClues` to build the actions performed by a player on a nonogram.

For example:

```python
>>> from nonogram.analysis import NonogramAction
>>> nonogram_actions = NonogramAction.from_strings('F-0-0-1593160278088,F-0-1-1593160279070,M-0-1-1593160279246,F-0-2-1593160281156,F-1-2-1593160281839,F-2-2-1593160282492,F-1-0-1593160284516,F-1-1-1593160285415,M-1-1-1593160285586,F-2-1-1593160288354')
```

## Nonogram Game Session

**Nonogram Analysis** supports the class `NonogramSession` to build the game session of a player who attempted to solve a nonogram. The constructor of this class accepts the following arguments:

- `user`: An object `User` representing the player who played a nonogram.
- `start_time`: The object `datetime.datetime` that represents the time when the nonogram game session started.
- `clues`: The list of objects `NonogramClues` corresponding to the clues of the nonogram that was given to the player to solve.
- `actions`: The list of objects `NonogramActions` that represent the actions the player performed.

For example:

```python
>>> import datetime
>>> from nonogram.analysis import NonogramSession
>>> nonogram_session = NonogramSession(
>>> ... None,
>>> ... datetime.datetime(2020, 6, 26, 8, 31, 14, 729000, tzinfo=datetime.timezone.utc),
>>> ... nonogram_clues,
>>> ... nonogram_actions)
>>> print(str(nonogram_session))
XX.
..X
XXX
>>> nonogram_session.is_solved
True
>>> calculate_nonogram_score(nonogram_session)
>>> 0.5152905198776758
```
