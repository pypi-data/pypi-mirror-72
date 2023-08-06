import io
import os.path
from clint.textui import puts, indent, colored
from coref import *
from consolemd import Renderer
import pyfiglet

def nsHelp(ns, path):
    help = nsGet(ns, path)
    if isNothing(help):
        help = Just(colored.red("Help not found"))
    template = Tpl(help.value)
    help = Just(template(ns))
    r = Renderer()
    out = io.StringIO()
    r.render(help.value, output=out)
    help = out.getvalue()
    out.close()
    pyfiglet.print_figlet("HELP: {} >".format(os.path.basename(path)))
    with indent(4, quote=colored.blue(' > ')):
        for h in help.split('\n'):
            puts(h)
    return ns
