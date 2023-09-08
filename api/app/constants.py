from enum import Enum

class PrivacyLevelEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class ThemeEnum(str, Enum):
    LIGHT = "light"
    DARK = "dark"

class LanguageEnum(str, Enum):
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"