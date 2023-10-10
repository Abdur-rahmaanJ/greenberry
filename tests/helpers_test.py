import unittest

from greenberry.helpers import capture_print, maths_eval

class GBUtilsTests(unittest.TestCase):
    def test_maths_eval_add(self):
        x = "3+2-1"
        output = capture_print(maths_eval, x)
        self.assertEqual(output, "4")


if __name__ == "__main__":
    unittest.main(exit=False)
