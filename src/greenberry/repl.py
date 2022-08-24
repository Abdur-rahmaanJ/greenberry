"""
Created on Sun Dec 31 22:21:00 2017

@author: ARJ
"""
from greenberry.gb import greenberry_eval

print(
    """
      ---greenberry(c)---
      welcome to the .gb REPL
      ---greenberry(c)---
      """
)
isSessionOn = 1
while isSessionOn == 1:
    x = input("---> ")
    greenberry_eval(x)
    if x == "berry exit":
        isSessionOn = 0
    print()
print(
    """
      ---greenberry(c)---
      .gb REPL exited. see you soon _ _
      ---greenberry(c)---
      """
)
