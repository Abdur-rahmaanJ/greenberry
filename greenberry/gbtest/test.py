import unittest
from files.greenBerry import greenBerry_eval


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
