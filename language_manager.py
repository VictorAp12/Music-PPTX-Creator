"""
This module contains the LanguageManager class.
It is used to change the language of the application.

The signal is emitted with the language as a parameter and its called on the menu_bar module
in the change_language_menu
"""

from PySide6.QtCore import QObject, Signal


class LanguageManager(QObject):
    """
    This class is used to change the language of the application.
    """

    language_changed = Signal(str)

    def change_to_language(self, language: str):
        """
        Changes the language of the application.

        :param language (Literal["pt", "en"]): the language to use.
        """
        self.language_changed.emit(language)
