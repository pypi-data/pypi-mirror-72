from coref.mod import nsValues, nsList

_set = nsValues(
    {
        '/help/cmd/default': """
# THE HELP
This is a default HELP page for the core.F application command-line.

## BASICS OF core.F CLI interface

core.F CLI interface consists of two parts: Setting the global flags and
calling for the pre-configured *commands*. You do have a help, available to you
within context when you will specify __--help__ after the command.

### Setting of the global flags

You can set global flag by __+flagname__ to set a global flag to a __True__
or __-flagname__ to set it to the __False__

| __+/-daemonize__ | Daemonize process or keep it running in foreground |
| __+/-color__     | Turn the terminal colors on or off                 |
| __+/-console__   | Turn on or off output to the application console   |
| __+/-log__       | Enable or disable writing the log file             |

### Calling preconfigured commands

Each pre-configured command is defined by the function(s) located in the
directory, which is pre-set in */config/cmd.path* variable in your namespace. The default
is */usr/local/bin* Pre-configured commands are called in order that yo specify them
in command line. In this example:

```
command A B C
```

command __A__ will be called before command __B__ and command __B__ will be called before
command __C__. General cormat of the commands are:

*command* (zero or more command options), where the command option is defiend as
__--commandoption__ *option value*.


Keep exploring ! __73__ !
Rendered at: $time.asctime($time.localtime($time.time()))
        """,
    }
)

_mkdir = [
    '/help',
    '/help/cmd',
]
