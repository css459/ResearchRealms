# Latex formatting functions. Should render latex to an image
# or return an error
import re
from .executor import _check_matplotlib_output, MATPLOTLIB_OUTPUT_FILE

FONT_SIZE = 25
COLOR = 'black'


def preprocess_latex(equation):
    """
    Formatting done to the string equation in order for it to render correctly
    """
    equation = equation.replace('\'', '^{\prime}')
    return equation


def stringify(string):
    return f'\'{string}\''


def generate_plot(equation):
    """
    Injects the inputted latex equation into a formatted string
    for plotting. Can control the size and color of text with
     FONT_SIZE and COLOR

    :param equation: LaTeX equation in correct math mode
    :return: Single formatted string ready to be executed and rendered
    """

    latex = f'r{stringify(equation)}'

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
        color={stringify(COLOR)})

plt.axis('off')
plt.savefig({stringify(MATPLOTLIB_OUTPUT_FILE)})
"""

    return plot


def render_latex(latex_equation):
    """
    Renders a given LaTeX equation using matplotlib

    :param latex_equation: LaTeX equation
    :return: rendered image
    """

    # Remove formatting from code
    latex_equation = re.sub(r'```\w*', '', latex_equation)

    # inject latex equation and generate the plot
    s = generate_plot(preprocess_latex(latex_equation))
    exec(s)

    # Check if a matplotlib chart was created
    img = _check_matplotlib_output()
    if img:
        return {'img': img}
    else:
        return {'code': 'Unable to render LaTeX (Error)'}