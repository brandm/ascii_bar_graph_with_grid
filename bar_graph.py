# * bar_graph.py --- ASCII bar graph with grid
#   - Copyright (C) 2017-2018 Michael Brand <michael.ch.brand at gmail.com>
#   - Licensed under GPLv3, see http://www.gnu.org/licenses/gpl-3.0.html
#   - URL: http://github.com/brandm/ascii_bar_graph_with_grid

# * Commentary:
"""Python 3 module to draw an ASCII bar graph with optional major and minor
grid.
"""
#   - Written with flake8 with "ignore =
#     E129,E201,E241,E271,E302,E305,E306,W503".
#   - Written with the live-py-plugin (Eclipse, Emacs and PyCharm) for
#     Python live coding.
#   - Supports Emacs Outshine mode.

# * Code:

# * Live coding
_lc = __name__ == '__live_coding__'  # Global ingredients, global value
if _lc:
    import sys # Trigger E261 with this comment to verify that flake8 works
    _ = sys.executable, sys.version

    def regression_test_failures(function, tests):
        """Test FUNCTION with TESTS and list the failures.

        TESTS is a list of lists with the expected result and the
        corresponding function arguments. Returns a list of lists with the
        expected result, the function result and the function arguments of
        the test cases where the function result is not as expected. The
        list is empty when there is no regression.

        Examples:

        0 failure: regression_test_failures(int, [[10, "10"], [2, "10", 2]])

        1 failure: regression_test_failures(int, [[10, "10"], [2, "10", 4]])
        """
        # - Keep in sync with feature.el:f-regression-test-failures.
        # - TODO: Rename function and move definition into a common test
        #   utility module.

        return [[expected, result, *arguments]
                for expected, *arguments in tests
                for result in [function(*arguments)]
                if expected != result]

    def regression_test_failures_doubled_result_string(function, tests):
        """Very similar to regression_test_failures, which see.
        """
        return [[expected, 2 * result, *arguments]
                for expected, *arguments in tests
                for result in [function(*arguments)]
                if expected != 2 * result]

    def single_argument_plus_minus_offset(tests):
        """Add +/- offset to tests with a single argument.
        """
        return [[expected, argument + offset]
                for expected, argument in tests
                for offset in [-.49999, .49999]]

# * Function orgtbl_ascii_draw
# ** Definition
def orgtbl_ascii_draw(value, min, max, width=None, characters=None):
    """Draw an ascii bar in a table.
    VALUE is the value to plot, it determines the width of the bar to draw.
    MIN is the value that will be displayed as empty (zero width bar).
    MAX is the value that will draw a bar filling all the WIDTH.
    WIDTH is the span in characters from MIN to MAX.
    CHARACTERS is a string that will compose the bar, with shades of grey
    from pure white to pure black. It defaults to a 10 characters string of
    regular ascii characters.

    This is a Python reimplementation of the Emacs Lisp function
    orgtbl-ascii-draw from Emacs Org mode, the docstring is copied one to
    one.
    """

    from math import ceil

    width = ceil(width or 12)
    characters = characters or " .:;c!lhVHW"
    length = len(characters[1:])
    relative = (value - min) / (max - min)
    steps = round(relative * width * length)
    if steps < 0:
        return "too small"
    if steps > width * length:
        return "too large"
    else:
        int_division, remainder = divmod(steps, length)
        last_draw = characters[remainder]
        if last_draw == ' ':
            last_draw = ''
        return int_division * characters[-1] + last_draw

# ** Unit tests.
if _lc:
    from functools import partial

    # The same use cases as Emacs Org mode ert-deftest
    # test-org-table/orgtbl-ascii-draw

    _failures = regression_test_failures(
        partial(orgtbl_ascii_draw,
                min=0, max=24, width=3, characters=" 12345678"),
        single_argument_plus_minus_offset(
            [
                ["too small", -1],
                ["",           0],
                ["1",          1],
                ["883",       19],
                ["887",       23],
                ["888",       24],
                ["too large", 25],
            ]))

    _failures = regression_test_failures(
        partial(orgtbl_ascii_draw, min=0, max=3, width=3, characters="$-"),
        single_argument_plus_minus_offset(
            [
                ["too small", -1],
                ["$",          0],
                ["-$",         1],
                ["--$",        2],
                ["---$",       3],
                ["too large",  4],
            ]))

# * Function bar_graph
# ** Definition
def bar_graph(val, val_per_char, char_total,
              char_per_minor=None, minor_per_major=None):

    # * History:
    #   - 2018-03-24 Create

    # Check arguments.
    if not val_per_char > 0:
        raise ValueError(val_per_char)
    if not (isinstance(char_total, int) and char_total >= 1):
        raise ValueError(char_total)
    if char_per_minor is not None:
        if not (isinstance(char_per_minor, int) and char_per_minor >= 1):
            raise ValueError(char_per_minor)
    if minor_per_major is not None:
        if char_per_minor is None:
            raise ValueError(char_per_minor, minor_per_major)
        if not (isinstance(minor_per_major, int) and minor_per_major >= 2):
            raise ValueError(minor_per_major)

    # Calculation.
    #    Ruler: ▄ ▄ ▄ ▄ ▄
    sub_chars = " ▏▎▍▌▋▊▉"  # 0/8 to 7/8
    sub_per_char = len(sub_chars)
    sub_per_val = round(val * sub_per_char / val_per_char)
    full = sub_per_val // sub_per_char
    remainder = sub_per_val - full * sub_per_char

    if sub_per_val < 0:
        # Underflow.
        bar = "╢" if char_total == 1 else "▒"
    elif sub_per_val == 0:
        # Zero.
        bar = "·"
    elif (full == char_total - 1 and remainder > sub_per_char - 3
          or full >= char_total):
        # Overflow. The magic number 3 above is to get more space (3/8) for
        # the clearance of the maximum value bar to the right border of the
        # string than for the width of the major division (2/8).
        bar = "╣" if char_total == 1 else "▓" * (char_total - 1)
    else:
        # Bar with minor and major divisions and padding.
        bar = ''
        for next_pos in range(1, full + 1):
            this_char = "█"  # 8/8
            if next_pos < full or remainder:
                if   (minor_per_major is not None
                      and not next_pos % (char_per_minor
                                          * minor_per_major)):
                    this_char = "▊"  # 6/8
                elif (char_per_minor is not None
                      and not next_pos % char_per_minor):
                    this_char = "▉"  # 7/8
            bar += this_char
        bar += sub_chars[remainder]
    return bar + " " * (char_total - len(bar))

# ** Unit tests.
if _lc:
    # Doubled result strings to see how adjacent graphs can visually be
    # distinguished.

    from functools import partial

    # Bar graph with tiny under- and overflow indicators (without grid).
    _failures = regression_test_failures_doubled_result_string(
        partial(bar_graph, val_per_char=8, char_total=1),
        single_argument_plus_minus_offset(
            [
                ["╢╢", -1],  # Underflow indication for char_total == 1
                ["··",  0],  # Zero
                ["▏▏",  1],  # Smallest non-zero
                ["▎▎",  2],
                ["▍▍",  3],
                ["▌▌",  4],
                ["▋▋",  5],  # Largest
                ["╣╣",  6],  # Overflow indication for char_total == 1
                ["╣╣",  7],
                ["╣╣",  8],
                ["╣╣",  9],
            ]))

    # Bar graph with grid.
    _failures = regression_test_failures_doubled_result_string(
        partial(bar_graph, val_per_char=8, char_total=2, char_per_minor=1),
        single_argument_plus_minus_offset(
            [
                ["▒ ▒ ", -1],  # Underflow indication for char_total > 1
                ["· · ",  0],  # Zero
                ["▏ ▏ ",  1],  # Smallest non-zero
                ["▉▋▉▋", 13],  # Largest
                ["▓ ▓ ", 14],  # Overflow indication for char_total > 1
                ["▓ ▓ ", 15],
                ["▓ ▓ ", 16],
                ["▓ ▓ ", 17],
            ]))

    # Bar graph with major and minor grid.
    _failures = regression_test_failures_doubled_result_string(
        partial(bar_graph, val_per_char=8, char_total=4,
                char_per_minor=1, minor_per_major=2),
        single_argument_plus_minus_offset(
            [
                ["▒   ▒   ", -1],  # Underflow indication for char_total > 1
                ["·   ·   ",  0],  # Zero
                ["▏   ▏   ",  1],  # Smallest non-zero
                ["▎   ▎   ",  2],
                ["▍   ▍   ",  3],
                ["▌   ▌   ",  4],
                ["▋   ▋   ",  5],
                ["▊   ▊   ",  6],
                ["▉   ▉   ",  7],
                ["█   █   ",  8],
                ["▉▏  ▉▏  ",  9],
                ["▉▎  ▉▎  ", 10],
                ["▉▍  ▉▍  ", 11],
                ["▉▌  ▉▌  ", 12],
                ["▉▋  ▉▋  ", 13],
                ["▉▊  ▉▊  ", 14],
                ["▉▉  ▉▉  ", 15],
                ["▉█  ▉█  ", 16],
                ["▉▊▏ ▉▊▏ ", 17],
                ["▉▊▎ ▉▊▎ ", 18],
                ["▉▊▍ ▉▊▍ ", 19],
                ["▉▊▌ ▉▊▌ ", 20],
                ["▉▊▋ ▉▊▋ ", 21],
                ["▉▊▊ ▉▊▊ ", 22],
                ["▉▊▉ ▉▊▉ ", 23],
                ["▉▊█ ▉▊█ ", 24],
                ["▉▊▉▏▉▊▉▏", 25],
                ["▉▊▉▎▉▊▉▎", 26],
                ["▉▊▉▍▉▊▉▍", 27],
                ["▉▊▉▌▉▊▉▌", 28],
                ["▉▊▉▋▉▊▉▋", 29],  # Largest
                ["▓▓▓ ▓▓▓ ", 30],  # Overflow indication for char_total > 1
                ["▓▓▓ ▓▓▓ ", 31],
                ["▓▓▓ ▓▓▓ ", 32],
                ["▓▓▓ ▓▓▓ ", 33],
            ]))

    # Some larger examples.
    _failures = regression_test_failures_doubled_result_string(
        partial(bar_graph, val_per_char=8, char_total=13,
                char_per_minor=3, minor_per_major=2),
        single_argument_plus_minus_offset(
            [
                ["▒            ▒            ",  -1],
                ["·            ·            ",   0],
                ["▏            ▏            ",   1],
                ["██▉██▊██▉██▊▋██▉██▊██▉██▊▋", 101],
                ["▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓ ", 102],
            ]))

# * File config
#   Local Variables:
#     coding: utf-8-unix
#     fill-column: 76
#   End:
