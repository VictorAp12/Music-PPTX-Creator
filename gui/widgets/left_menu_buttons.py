"""
This module contains the code for the LeftMenuButtons class.
"""

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from variables import SMALL_FONT_SIZE


class LeftMenuButtons(QPushButton):
    """
    This class represents the button class, which is a grid of buttons.
    It inherits from the QPushButton class from PySide6.

    It's like an Abstract class for the main buttons.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        menu_button: bool = False,
    ) -> None:
        """
        Creates the button.

        :param parent (QWidget | None): the parent widget.
        :param menu_button (bool): if the button is a menu button.
        """
        super().__init__(parent)

        self.menu_button = menu_button
        self.active = False

        if self.active:
            self.set_active(True)

        self._config_style()

    def _config_style(self) -> None:
        """
        This method configures the style of the button.
        """
        font = self.font()
        font.setPixelSize(SMALL_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(50, 50)

        if self.menu_button:
            self.convert_to_menu_button()

    def set_active(self, state: bool) -> None:
        """
        This method sets the state of the button.

        :param state (bool): if the button is active.
        """
        self.active = state

        if not self.active:
            self._config_style()
        else:
            self.setStyleSheet(
                "LeftMenuButtons {background-color: rgba(20, 28 , 251, 0.4);}"
            )

    def convert_to_menu_button(self) -> None:
        """
        This method converts the button to a menu button.
        """
        self.setStyleSheet("margin: 5px;")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
