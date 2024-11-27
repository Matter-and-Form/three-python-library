from MF.V3.Settings.I18n import I18n as MF_V3_Settings_I18n_I18n


class I18n:

    """
     I18n language settings descriptor.
    """
    class Language:

        """
         Language settings descriptor.
        """
        def __init__(self, value: MF_V3_Settings_I18n_I18n.Language, default: MF_V3_Settings_I18n_I18n.Language):
            self.value = value
            self.default = default

    def __init__(self, language: 'Language'):
        # Language settings descriptor.
        self.language = language


