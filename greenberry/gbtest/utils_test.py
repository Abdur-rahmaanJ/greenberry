#
# utils test
#

import sys
sys.path.append("..")

import unittest
from utils import capture_maths_eval_print

class GBUtilsTests(unittest.TestCase):

    def test_maths_eval_add(self):
        x = '3+2-1'
        output = capture_maths_eval_print(x)
        self.assertEqual(output, '4')

if __name__ == '__main__':
    unittest.main(exit=False)
