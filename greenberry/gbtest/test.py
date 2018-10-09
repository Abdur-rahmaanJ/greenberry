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
        
    def test_eval_add(self):
        x = 'print eval 1+2'
        temp_stdout = StringIO()
        # redirect stdout to catch print statement from eval function
        with contextlib.redirect_stdout(temp_stdout):
            greenBerry_eval(x)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, '3')

if __name__ == '__main__':
    unittest.main(exit=False)
