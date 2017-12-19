# * bar_graph.py --- ASCII bar graph with grid
#   - Copyright (C) 2017-2017 Michael Brand <michael.ch.brand at gmail.com>
#   - Licensed under GPLv3, see http://www.gnu.org/licenses/gpl-3.0.html
#   - URL: http://github.com/brandm/ascii_bar_graph_with_grid

# * Commentary:
"""Python 3 module to draw an ASCII bar graph with major and minor grid.
"""
#   - Written with the help of flake8 with "ignore = E201,E241,E302,E305",
#     the live-py-plugin (Eclipse, Emacs, PyCharm) for Python live coding
#     and Outshine mode (Emacs).

# * Code:

# * Live coding
_lc = __name__ == '__live_coding__'  # Global ingredients, global value
if _lc:
    import sys
    _ = sys.executable, sys.version

# * orgtbl_ascii_draw
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
        int_division = steps // length
        remainder = steps - int_division * length
        last = characters[remainder]
        if last is ' ':
            last = ''
        return int_division * characters[-1] + last

if _lc:
    # The same use cases as Emacs Org mode ert-deftest
    # test-org-table/orgtbl-ascii-draw

    _t = [
        [      19, "883"],
        [-0.50001, "too small"],
        [-0.49999, ""],
        [ 0.49999, ""],
        [ 0.50001, "1"],
        [ 1.49999, "1"],
        [22.50001, "887"],
        [23.49999, "887"],
        [23.50001, "888"],
        [24.49999, "888"],
        [24.50001, "too large"],
    ]
    _ = all([expected == orgtbl_ascii_draw(value, 0, 24, 3, " 12345678")
             for value, expected in _t])
    _t = [
        [-1, "too small"],
        [ 0, "$"],
        [ 1, "-$"],
        [ 2, "--$"],
        [ 3, "---$"],
        [ 4, "too large"],
    ]
    _ = all([expected == orgtbl_ascii_draw(value, 0, 3, 3, "$-")
             for value, expected in _t])

# * File config
#   Local Variables:
#     coding: us-ascii-unix
#     fill-column: 76
#   End:
