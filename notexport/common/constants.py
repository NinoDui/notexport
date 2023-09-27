import getpass


class CONST_COMM(object):
    __slots__ = ()
    TIME_FORMAT = "%Y%m%d-%H%M%S"


class CONST_IBOOK(object):
    __slots__ = ()

    DEFAULT_ROOT = f"/Users/{getpass.getuser()}/Library/Containers/com.apple.iBooksX/Data/Documents"
    DEFAULT_BKLIBRARY = "BKLibrary"
    DEFAULT_ANNOTATION = "AEAnnotation"
    BOOK_ID_COL_IN_BKLIBRARY = "ZASSETID"
    BOOK_ID_COL_IN_ANNOTATION = "ZANNOTATIONASSETID"
