from enum import Enum


class I18n:

    """
     I18n language settings.
    """
    class Language(Enum):

        """
         Available languages.
        """
        en = "en"
        fr = "fr"
        de = "de"

    def __init__(self, language: 'Language' = None):
        # The language setting.  Supported languages are ["en", "fr", "de"].
        self.language = language


