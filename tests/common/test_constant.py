import unittest

from notexport.common import CONST_IBOOK, CONST_VACABULARY


class ConstantTest(unittest.TestCase):
    def test_str_enum(self):
        v = CONST_VACABULARY.OTHERS
        self.assertEqual("NOT IMPLEMENTED", v)
        self.assertEqual("OTHERS", v.name)

    def test_int_enum(self):
        self.assertEqual(1, CONST_IBOOK.NOTE_TYPE.GREEN)


if __name__ == "__main__":
    unittest.main()
