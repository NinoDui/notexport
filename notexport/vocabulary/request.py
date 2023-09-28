from typing import Dict, List

import requests


class WordParser:
    """
    Word Meaning Fetcher for:
    1) request online Merriam Webster API
        - doc: https://dictionaryapi.com/products/json
        - website: https://www.merriam-webster.com/
    2) parse the meaning content
    """

    LEGAL_VOCABULARY = ["collegiate", "learner"]
    URL_FORMAT = (
        "https://www.dictionaryapi.com/api/v3/references/{voc}/json/{word}?key={key}"
    )

    def __init__(self, vocabulary_id, user_key, timeout=None):
        self._identifier = vocabulary_id
        self._key = user_key
        self._timeout = timeout

        if self._identifier not in WordParser.LEGAL_VOCABULARY:
            print(
                f"{self._identifier} is not recognized by {__name__}, replaced by collegiate. (options: collegiate/learner)"
            )
            self._identifier = WordParser.LEGAL_VOCABULARY[0]
        if not user_key:
            raise ValueError(f"User Key MISSED!")

    def _generate_url(self, word):
        return WordParser.URL_FORMAT.format(
            voc=self._identifier, word=word, key=self._key
        )

    def _request(self, url, timeout, format="json"):
        with requests.get(url, stream=True, timeout=timeout) as response:
            if response.status_code != 200:
                raise ConnectionError(
                    f"Failed to request content from {url}, error code is {response.status_code}"
                )
            if format == "json":
                return response.json()
            else:
                return response.text

    def parse_json(self, body) -> Dict[str, List[str]]:
        raise NotImplementedError(f"Method is not supported yet.")
