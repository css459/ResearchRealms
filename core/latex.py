# Latex formatting functions. Should render latex to an image
# or return an error
import re
from .executor import _check_matplotlib_output, MATPLOTLIB_OUTPUT_FILE

FONT_SIZE = 25
COLOR = 'black'

def generate_plot(equation):
    latex = 'r\'' + equation + '\''
    latex_color = '\'' + COLOR + '\''
    out_file = '\'' + MATPLOTLIB_OUTPUT_FILE + '\''

    plot = f"""
import numpy as np
import matplotlib.pyplot as plt

left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

x = 0.5*(left+right)
y = 0.5*(bottom+top)

plt.text(x, y,
        {latex},
        horizontalalignment='center',
        verticalalignment='center',
        fontsize={FONT_SIZE}, 
        color={latex_color})

plt.axis('off')
plt.savefig({out_file})
"""

    return plot


def render_latex(latex_equation):

    # Remove formatting from code
    latex_equation = re.sub(r'```\w*', '', latex_equation)

    # inject latex equation and generate the plot
    s = generate_plot(latex_equation)
    exec(s)

    # Check if a matplotlib chart was created
    img = _check_matplotlib_output()
    if img:
        return {'img': img}
    else:
        return {'code': 'Unable to render LaTeX (Error)'}