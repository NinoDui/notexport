import unittest

from notexport.vocabulary import MDictConverter


class MDXTest(unittest.TestCase):
    def test_mdd_load(self):
        mdx_path = "resources/柯林斯COBUILD高阶英汉双解学习词典 1.7.mdx"
        converter = MDictConverter(mdx_path)

        converter.test_print()


if __name__ == "__main__":
    unittest.main()
