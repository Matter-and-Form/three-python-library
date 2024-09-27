from enum import Enum


class I18n:
    # I18n language settings.
    # Available languages.
    class Language(Enum):
        en = "en"
        fr = "fr"
        de = "de"

    def __init__(self, language: 'Language' = None):
        # The language setting.  Supported languages are ["en", "fr", "de"].
        self.language = language


