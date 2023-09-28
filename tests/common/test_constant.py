import unittest

from notexport.common import CONST_VACABULARY


class ConstantTest(unittest.TestCase):
    def test_str_enum(self):
        v = CONST_VACABULARY.OTHERS
        self.assertEqual("NOT IMPLEMENTED", v)
        self.assertEqual("OTHERS", v.name)


if __name__ == "__main__":
    unittest.main()
