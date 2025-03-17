"""
Created on Sun Dec 31 22:54:37 2017

@author: ARJ
"""

from argparse import ArgumentParser, Namespace
import sys
import os

from greenberry.utils.store import Memory
from greenberry.gb import greenberry_eval
from greenberry.repl import run_repl


def main():
    """
    The command line will take in two arguments, any combination of either a script name or a `repl` argument.
    First any provided scripts are executed, then the repl is run (if the `-repl` argument has been provided)
    If it has, the repl will operate in the same namespace as the executed program.
    """
    arg_parser = ArgumentParser(
        prog="Green Berry",
        description="A one line statement programming language.",
        epilog="https://github.com/Abdur-rahmaanJ/greenberry",
    )
    arg_parser.add_argument(
        "scriptname",
        nargs="*",
        type=str,
        help="The name of the script you want to run",
    )
    arg_parser.add_argument(
        "-repl",
        action="store_true",
        help="Will start a repl after the program has completed, with the program namepsace.",
    )

    namespace: Namespace = arg_parser.parse_args(sys.argv[1:])

    if namespace.scriptname:
        with open(namespace.scriptname, "r") as f:
            for line in f.readlines():
                greenberry_eval(line)

    if namespace.repl:
        run_repl()


if __name__ == "__main__":
    x = ""

    with open("main.gb") as f:
        x = f.read()

    Memory.g_vars = {}
    Memory.g_fs = {}
    Memory.g_cls = {}
    Memory.g_cls_instance = {}
    
    greenberry_eval(x)
