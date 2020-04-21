import os
import re
import sys
from io import StringIO, BytesIO

from PIL import Image

"""
A list of packages that are not allowed in
the Python execution environment. `sys` is
implicit in this list and will always be
forbidden.
"""
FORBIDDEN_PACKAGES = ['urllib', 'os']

"""
If the python script writes to this file,
it will be delivered along with the output
of the program to the user.
"""
MATPLOTLIB_OUTPUT_FILE = 'rr-out.png'


def _forbidden_packages_preamble():
    """
    Returns a string python code which will disallow
    certain packages from being used.

    :return: String
    """
    if not FORBIDDEN_PACKAGES:
        return ""
    s = 'import sys; '
    for f in FORBIDDEN_PACKAGES:
        s += 'sys.modules[\'' + f + '\'] = None; '

    s += 'sys.modules[\'sys\'] = None;'

    return s + '\n'


def _detect_matplotlib(s):
    """
    Detects the presence of `plt` in a code string
    `s` and injects the script with a routine to capture
    the current figure, and render the resulting chart as a
    PNG in the `img` output field.

    This function will detect the presence of `plt.show()`
    and replace it with the rendering routine.

    :param s: A valid Python script as text
    :return:  Array: The (modified) python string
    """
    if 'plt.show()' in s:
        s = s.replace('plt.show()',
                      'plt.savefig(\'' + MATPLOTLIB_OUTPUT_FILE + '\')')
    return s


def _check_matplotlib_output():
    """
    Checks for the presence of the file defined by
    `MATPLOTLIB_OUTPUT_FILE`. If it exists, return
    the bytes of that file.

    :return: PNG image bytes or `None`
    """
    if os.path.exists(MATPLOTLIB_OUTPUT_FILE):
        img = Image.open(MATPLOTLIB_OUTPUT_FILE)
        arr = BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)
        return arr
    return


def exec_str(s):
    """
    Executes a string `s` as a Python
    script using the `exec()` function. Ideally,
    this function will run in a new process as to
    containerize the arbitrary code away from its
    caller.

    :param s: A valid Python script as text
    :return:  The STDOUT of the Python script
              or its exception and traceback as
              a string
    """
    # Remove formatting from code
    s = re.sub(r'```\w*', '', s)

    # Forbid certain packages
    # s = _forbidden_packages_preamble() + s

    # Detect matplotlib
    s = _detect_matplotlib(s)

    # Redirect STDOUT
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(s)
    sys.stdout = old_stdout

    # An output of only 'python' means the program had
    # no output
    out = str(redirected_output.getvalue())
    if not out:
        out = 'No text output! (Success)'

    # Check if a matplotlib chart was created
    img = _check_matplotlib_output()
    if img:
        return {'code': out, 'img': img}
    else:
        return {'code': out}
