"""
Created on Sun Dec 31 22:21:00 2017

@author: ARJ
"""
from greenberry.gb import greenberry_eval


def run_repl():
    print(
        """
  ---greenberry(c)---
  welcome to the .gb REPL
  ---greenberry(c)---
  """
    )
    try:
        while True:
            x = input("---> ")
            if x == "berry exit":
                break

            greenberry_eval(x)

            print()

    except KeyboardInterrupt:
        pass

    print(
        """
  ---greenberry(c)---
  .gb REPL exited. see you soon _ _
  ---greenberry(c)---
  """
    )


if __name__ == "__main__":
    run_repl()
