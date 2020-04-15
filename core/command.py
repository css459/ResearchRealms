# Ingress object for all text inputs from the bot.
# Receives text input and produces text output. Also handles
# registry information.

# Every command should spawn a subprocess (as to not have the bot itself wait)


def test(s):
    return str(s)


"""
Valid commands with their corresponding function
"""
commands = {
    'test': test
}


def _exception_wrapper(fn, *args):
    """
    Captures all exceptions from a provided
    function with arguments and returns either
    the function output or a string with the
    exception.

    :param fn:      Function to run
    :param kwargs:  Function arguments
    :return:        Function output or string
    """
    try:
        return fn(*args)
    except Exception as e:
        return str(e)


def run_command(cmd_str, *args):
    """
    All commands are called using an identifier string
    from the `commands` dictionary. The arguments are then
    passed to the corresponding function.

    :param cmd_str:     A valid key from `commands`
    :param kwargs:      Arguments for function
    :return:            Function output or string
    """
    # Sanity checks for insane input
    if len(cmd_str) > 100 or len(args) > 100:
        return

    if cmd_str not in commands:
        return 'ERROR: ' + cmd_str + ' is not a valid command!'

    cmd = commands[str(cmd_str)]
    return _exception_wrapper(cmd, *args)
