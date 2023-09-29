import unittest

from notexport.ibook import IBookNoteProcessor
from notexport.runner import fetch_vocabulary


class IBookNoteProcessorTest(unittest.TestCase):
    def test_lemmatize(self):
        src_path = "resources/fake_dump_note.csv"
        processor = IBookNoteProcessor(src_path, threshold=5)
        processor.lemmatize()

        df_w, df_s = processor.get_data()
        self.assertTrue(IBookNoteProcessor.LEMMATIZED_COLUMN in df_w.columns)

    def test_merge_meaning(self):
        processor = IBookNoteProcessor("resources/fake_dump_note.csv")
        words = processor.lemmatize().get_words()
        voc = fetch_vocabulary(words, "collins")

        df_w, df_s = processor.merge_explanation_from_vocabulary(voc).get_data()
        self.assertTrue("meaning" in df_w.columns)


if __name__ == "__main__":
    unittest.main()
