"""
This is the main file of the application.

It creates the application, calls the main self.window and sets the icon.

The objective of this project was to apply my knowledge of Object Oriented Programming and PySide6
(thats why it has many strong typing classes and methods)
and the main focus was on the GUI part, because I am a back-end developer
and needed to improve my front-end.
skills.

VictorAp12 10/03/2024 ~ 19/03/2024
"""

import sys
from typing import Literal

from PySide6.QtWidgets import QApplication, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from gui.main_window.ui_main_window import MainWindow
from gui.widgets.left_menu_buttons import LeftMenuButtons
from styles import setup_theme
from variables import WINDOW_ICON_PATH
from language_manager import LanguageManager


class MusicPPTXCreator(MainWindow):
    """
    Creates the application.
    """

    def __init__(self, app: QApplication) -> None:
        """
        Creates the application.

        :param app (QApplication): the application.
        """

        # creates the instance of language manager (a class that uses signals)
        # which is used to change the language
        # all over the application, it has to be the same instance for all the widgets.
        self.language_manager = LanguageManager()
        self.language_manager.language_changed.connect(self.retranslate_ui)

        super().__init__(self.language_manager)

        # creates the application
        self.app = app

        setup_theme()

        self._add_menu_buttons()

        self.retranslate_ui()

    # def _setup_app(self) -> None:
    #     """
    #     Sets up the application.
    #     """

    #     setup_theme()

    def _add_menu_buttons(self) -> None:
        """
        Adds the buttons to the left menu frame.
        """
        self.button_one = LeftMenuButtons(self, True)
        self.button_one.set_active(True)
        self.button_one.clicked.connect(self.show_page_one)

        self.add_widget_to_menu_frame(
            self.button_one, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.button_many = LeftMenuButtons(self, True)
        self.button_many.clicked.connect(self.show_page_many)

        self.add_widget_to_menu_frame(
            self.button_many, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.button_insert_manual = LeftMenuButtons(self, True)
        self.button_insert_manual.clicked.connect(self.show_page_insert_manually)

        self.add_widget_to_menu_frame(
            self.button_insert_manual, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.add_widget_to_menu_frame(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def retranslate_ui(self, language: Literal["pt", "en"] = "pt") -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if language == "pt":
            self.button_one.setText("Buscar Uma Música")
            self.button_many.setText("Buscar Várias Músicas")
            self.button_insert_manual.setText("Inserir Manualmente")

        elif language == "en":
            self.button_one.setText("Search Music")
            self.button_many.setText("Search Many Music")
            self.button_insert_manual.setText("Insert Manually")

    def reset_selection(self) -> None:
        """
        Resets the selection of the buttons changing the active status,
        which will change the style of the button.
        """
        for btn in self.left_menu_frame.findChildren(LeftMenuButtons):
            try:
                btn.set_active(False)
            except:
                pass

    def show_page_one(self) -> None:
        """
        Shows the first page.
        """
        self.reset_selection()
        self.pages.setCurrentWidget(self.pages_ui.page_one)
        self.button_one.set_active(True)

    def show_page_many(self) -> None:
        """
        Shows the second page.
        """
        self.reset_selection()
        self.pages.setCurrentWidget(self.pages_ui.page_many)
        self.button_many.set_active(True)

    def show_page_insert_manually(self) -> None:
        """
        Shows the third page.
        """
        self.reset_selection()
        self.pages.setCurrentWidget(self.pages_ui.page_insert_manually)
        self.button_insert_manual.set_active(True)

    def set_icon(self) -> None:
        """
        Sets the icon of the application.
        """
        # sets the icon
        icon = QIcon(str(WINDOW_ICON_PATH))
        self.setWindowIcon(icon)
        self.app.setWindowIcon(icon)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    music_pptx_creator_app = MusicPPTXCreator(application)
    music_pptx_creator_app.show()
    music_pptx_creator_app.app.exec()
    music_pptx_creator_app.setFocus()
