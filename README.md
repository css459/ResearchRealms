# ResearchRealms
A Slack and Discord Bot for Quantitative Research in Python

[Add this bot to your discord server!](https://discordapp.com/api/oauth2/authorize?client_id=700004199844282369&permissions=593024&scope=bot)

# Introduction

**ResearchRealms** is a Python program and execution envrionment for running arbitrary code. Its purpose is to be extensible, and easy to run your own instance. ResearchRealms is made to run on cloud machines with high-replication in mind. Each quantum of computation in ResearchRealms is natually parallel and containerized using our `command` framework.

The `command` framework is what makes ResearchRealms unique. It is self-bootstrapping: While this framework supports running arbitrary code from Slack and Discord, it is also used to *execute our built-in commands*. It is containerized: In this way, we are able to *share the same environment* that ResearchRealms uses to run, to also run arbitrary code.

# Cross-Cutting Aspects

All of our design documents can be found under the `doc/` directory of this repository. It contains:

* Business Model Canvas
* UML Architecture
* Requirements Documentation
* Use-Case Documentation

We desgined this project by first documenting the functional requirements, and then expanding upon those by defining the non-fuctional requirements. This is documented in the **Requirements Documentation**. Moreover, we define some key use-cases (documented in the **Use-Case Documentation**) and implemented the core use-case: Executing arbitrary Python code. Once we knew how our application needed to perform, we worked on designing an architecture and how to implement it. This is documented in the **UML Architecture**.

Finally, we thought about how this application fits into the overall objectives of a business. This was an interesting exercise for us, because our application isn't necessarily geared towards business needs, but rather academic needs. Moreoever, the P2P nature of the application isn't as monolithic as most business applications. Nonetheless, we attemped to frame the application within a business scenario, and outlined that context in the **Business Model Canvas**.

# Setup

## Discord
For most users, clicking the link in the top of this document and choosing the target server should be sufficient. **It is possible to run your own node** by running the `discord_bot.py` python file. You are free to modify this file, and create your bot on top of this framework.

## Slack
TODO

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
Formatting ticks \`\`\` will be removed automatically, but there should be at least a space between
them and the code. `exec` will deliver back to your channel the **standard output** of the program.

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

## `!latex`

The `latex` command allows you and your colleagues to render `LaTeX` equations directly from the chat. The command
expects input in the same format at LaTeX math mode. The command will deliver back the rendered version of the equation
inputted

### Formatting

    !latex
    `$\int_{y} e^{-\beta F(y,x)}$`
