# ResearchRealms
A Slack and Discord Bot for Quantitative Research in Python

[Add this bot to your discord server!](https://discordapp.com/api/oauth2/authorize?client_id=700004199844282369&permissions=593024&scope=bot)

# Commands 

## `!exec`

The `exec` command allows you and your colleagues to **execute small python snippets** directly
from Slack or Discord. Under the hood, `exec` supports a number of features, offered transparently
to the user.

### Formatting

    !exec
    ```python
    import matplotlib.pyplot as plt
    print('hello wolrd!')
    plt.figure()
    plt.plot([1, 2])
    plt.title("test")
    plt.show()
    ```
Formatting ticks \`\`\` will be removed automically, but there should be at least a space between
them and the code. `exec` will devlier back to your channel the **standard output** of the program.

### Attachments

`exec` supports attachments. You can send up to one attachment with your Python
program. It will be available by its **original file name** at the **current directory**.

### Matplotlib

`exec` supports matplotlib. If you write `plt.show()` in your program. RR will capture this and
write it to a **special file**: `rr-out.png`. You are always allowed to write to this file, and
it will be delivered back to your channel as an attachment when your program finishes.

### Limits

`exec` runs Python snippets in a **minimal sandbox**. Namely, it executes within its own `tmp`
directory where intermediate files can be written to and read from. **There is no limit to the
size of the files you write here**, so please use files respectfully.

The following python modules are blacklisted within the sandbox:

* `os`
* `sys`
* `urllib`
* `requests`

These can be conifgured to be whatever you want, except `sys` is always **implicitly forbidden**,
since `sys` itself is used to forebid packages.

**Programs have a maximum execution time of 30 seconds.** 

