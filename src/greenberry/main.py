"""
Created on Sun Dec 31 22:54:37 2017

@author: ARJ
"""

import os
import sys

from greenberry.gb import greenberry_eval


def main():
    if len(sys.argv) == 2:
        with open(os.path.join(os.getcwd(), sys.argv[1])) as f:
            x = f.read()

        greenberry_eval(x)


if __name__ == "__main__":
    x = ""

    with open("main.gb") as f:
        x = f.read()

    greenberry_eval(x)
