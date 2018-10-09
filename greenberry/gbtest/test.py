import sys
sys.path.append("..")
import contextlib
from io import StringIO
import unittest
from greenBerry import greenBerry_eval


class TestGreenBerryFunctions(unittest.TestCase):

    def test_printd(self):
        pass

    def test_null(self):
        # check null input
        x = ''
        try:
            greenBerry_eval(x)
        except:
            error = True
        self.assertTrue(error)


if __name__ == '__main__':
    unittest.main(exit=False)
