import nltk

nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
from typing import List, Tuple, Union

import pandas as pd
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from notexport.common import CONST_IBOOK

wordnet._exception_map["a"]["lest"] = ["lest"]


def get_wordnet_pos(treebank_tag: str):
    # Special Case
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.VERB  # as verb instead of None (wordnet.NOUN)


def lemmatize_sentence(sentence):
    res = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos)
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))

    return res


class IBookNoteProcessor:
    SENTENCE_MARKS = [",", "\.", "!", "\?", ":"]
    LEMMATIZED_COLUMN = "CleanedWord"

    def __init__(self, data: Union[str, pd.DataFrame], threshold=5):
        if isinstance(data, str):
            self._data = pd.read_csv(data, index_col=0)
        elif isinstance(data, pd.DataFrame):
            self._data = data
        else:
            raise TypeError(
                f"{data} should be of type str or pandas DataFrame, now in {type(data)}"
            )

        self._threshold = threshold
        self._df_word: pd.DataFrame = None
        self._df_sentence = pd.DataFrame = None

        self._split_word_and_sentences(threshold=self._threshold)

    def _split_word_and_sentences(self, threshold: int):
        sentence_mask = self._data[CONST_IBOOK.NOTE_COL].apply(
            lambda x: len(x.split()) >= threshold
        ) & self._data[CONST_IBOOK.NOTE_COL].str.contains(
            "|".join(IBookNoteProcessor.SENTENCE_MARKS), case=False
        )
        self._df_word = self._data[~sentence_mask]
        self._df_sentence = self._data[sentence_mask]

    def lemmatize(self):
        self._df_word[IBookNoteProcessor.LEMMATIZED_COLUMN] = self._df_word[
            CONST_IBOOK.NOTE_COL
        ].apply(lambda x: lemmatize_sentence(x)[0] if len(x.split()) == 1 else x)

        # For Chain Opeartion
        return self

    def get_words(self, cleaned=False) -> List:
        column_name = CONST_IBOOK.NOTE_COL
        if cleaned and IBookNoteProcessor.LEMMATIZED_COLUMN in self._df_word.columns:
            column_name = IBookNoteProcessor.LEMMATIZED_COLUMN
        return self._df_word[column_name].to_list()

    def get_sentences(self) -> List:
        return self._df_sentence[CONST_IBOOK.NOTE_COL].to_list()

    def get_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return (self._df_word, self._df_sentence)

    def merge_explanation_from_vocabulary(
        self, vocabulary: pd.DataFrame, voc_key="word"
    ):
        left_on_key = (
            IBookNoteProcessor.LEMMATIZED_COLUMN
            if IBookNoteProcessor.LEMMATIZED_COLUMN
            in self._df_word.columns  # Lemmatized
            else CONST_IBOOK.NOTE_COL  # Not lemmatized
        )
        self._df_word = pd.merge(
            self._df_word,
            vocabulary,
            how="left",
            left_on=left_on_key,
            right_on=voc_key,
            right_index=False,
        )
        # For Chain Operation
        return self

    def reset(self):
        self._df_word = None
        self._df_sentence = None
        self._split_word_and_sentences(threshold=self._threshold)

        # For Chain Operation
        return self
