import os
import tempfile
import traceback
from multiprocessing import Queue, Process

import requests

from core.executor import exec_str
from core.latex import render_latex

# Multiprocessing Constants
MULTIPROCESS_TIMEOUT_SECONDS = 30.0
MULTIPROCESS_MAX_HEAP_MB = 2000.0
MULTIPROCESS_NICE_INCREMENT = 10

"""
Valid commands with their corresponding function.

Valid outputs consist of either a string (or variable
that can be cast to a string) or a dictionary using one
or more of the following options:
{
    'txt':  String (Will be displayed as normal text),
    'img':  BytesIO representing PNG image,
    'code': String (Will be displayed in a code block)
}

Other options will be ignored.
"""
commands = {
    'test': lambda x: x,
    'exec': exec_str,
    'latex': render_latex,
}


def _exception_wrapper(fn, *args):
    """
    Captures all exceptions from a provided
    function with arguments and returns either
    the function output or a string with the
    exception.

    :param fn:    Function to run
    :param args:  Function arguments
    :return:      Function output or formatted string
    """
    try:
        return fn(*args)
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        info_str = 'EXCEPTION:\n' + str(e) + '\nTraceback: \n' + traceback_str

        # Format as code block
        return '```' + info_str + '```'


def _process_wrapper(fn, *args):
    """
    Wraps call to `fn` in a new `Process` instance.
    The execution time and heap size will be limited.

    :param fn:    Function to run
    :param args:  Function arguments
    :return:      Function output or string
    """

    def niceness_queue_wrapper(q, fn, *args):
        """
        Pass through target function with args
        to child process, incrementing the child
        process' niceness along the way.

        :param q:     Queue object for result
        :param fn:    Function to run
        :param args:  Function arguments
        :return:      Function output or string
        """
        os.nice(MULTIPROCESS_NICE_INCREMENT)
        q.put(_exception_wrapper(fn, *args))

    # Create Queue to receive function output
    q = Queue()

    # Create the child process for function call
    p = Process(target=niceness_queue_wrapper, args=(q, fn, *args))
    p.start()

    # Receive the output from the child process
    try:
        out = q.get(block=True, timeout=MULTIPROCESS_TIMEOUT_SECONDS)
        p.join(MULTIPROCESS_TIMEOUT_SECONDS)

    # Capture timeout exceptions and notify user
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        info_str = 'EXCEPTION:\nProcess Timeout after ' + \
                   str(MULTIPROCESS_TIMEOUT_SECONDS) + \
                   ' seconds' + '\nTraceback: \n' + traceback_str

        # Format as code block
        return '```' + info_str + '```'

    return out


def run_command(cmd_str, att_name, att_url, *args):
    """
    All commands are called using an identifier string
    from the `commands` dictionary. The arguments are then
    passed to the corresponding function.

    :param cmd_str:   A valid key from `commands`
    :param att_name:  File name of an attachment or `None`
    :param att_url:   URL to to attachment or `None`
    :param args:      Arguments for function
    :return:          Function output or string
    """
    # Sanity checks for insane input
    if len(cmd_str) > 100 or len(args) > 100:
        return

    if cmd_str not in commands:
        return 'ERROR: ' + cmd_str + ' is not a valid command!'

    cmd = commands[str(cmd_str)]

    # Give and enter unique tmp directory for proc
    prev_path = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp_path:
        os.chdir(tmp_path)

        # If the attachment was passed, download it
        # to the environment
        if att_name is not None and att_url is not None:
            r = requests.get(att_url)
            with open(att_name, 'wb') as fp:
                fp.write(r.content)

        out = _process_wrapper(cmd, *args)
        os.chdir(prev_path)

    return out
