from oslash import Just
from typing import Callable, Any, Generic, TypeVar
from .Namespace import Namespace
from Cheetah.Template import Template

class Tpl(Just):
    def __init__(self, value: Any) -> None:
        Just.__init__(self, value)
    def __call__(self, ns: Namespace) -> str:
        return str(Template(self.value, searchList=[ns.raw().raw()]))

def nsTxt(ns, msg):
    return Tpl(msg)(ns)
