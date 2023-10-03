import getpass
from datetime import datetime
from enum import StrEnum
from zoneinfo import ZoneInfo


class CONST_COMM(object):
    __slots__ = ()

    TIME_FORMAT = "%Y%m%d-%H%M%S"
    DATA_FOLDER = "data"
    DEFAULT_START_TIME = "19700101-000000"
    COCOA_UNIX_DELTA_SEC = (datetime(2001, 1, 1) - datetime(1970, 1, 1)).total_seconds()
    DEFAULT_TIME_ZONE = ZoneInfo("Asia/Shanghai")


class CONST_IBOOK(object):
    __slots__ = ()

    DEFAULT_ROOT = f"/Users/{getpass.getuser()}/Library/Containers/com.apple.iBooksX/Data/Documents"
    DEFAULT_BKLIBRARY = "BKLibrary"
    DEFAULT_ANNOTATION = "AEAnnotation"
    BOOK_ID_COL_IN_BKLIBRARY = "ZASSETID"
    BOOK_ID_COL_IN_ANNOTATION = "ZANNOTATIONASSETID"
    NOTE_COL = "HighlightedText"
    NOTE_COMPLETE_COL = "BroaderText"
    NOTE_WORD_COL = "CleanedWord"


class CONST_VACABULARY(StrEnum):
    COLLINS = "resources/柯林斯COBUILD高阶英汉双解学习词典 1.7.sqlite.db"
    MERRIAM_WEBSTER = (
        "resources/Merriam-Webster's Collegiate Dictionary 11th Edtion.sqlite.db"
    )
    OTHERS = "NOT IMPLEMENTED"
