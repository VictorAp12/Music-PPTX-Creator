"""
This module contains the code for the ComboBox class.
"""
from typing import List
from PySide6.QtWidgets import QComboBox, QWidget
from PySide6.QtCore import Qt

from variables import SMALL_FONT_SIZE
from styles import setup_theme


class ComboBox(QComboBox):
    """
    This class is used to create the combobox.
    """

    def __init__(self, parent: QWidget | None = None, options: List[str] = []) -> None:
        """
        Creates the combobox.

        :param parent (QWidget | None): the parent widget.
        """
        super().__init__(parent)

        self.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
        """
        )

        if len(options) > 1:
            self.addItems(options)

    def set_options(
        self, options: List[str], tooltips: List[str] | None = None
    ) -> None:
        """
        Sets the options of the combobox.

        :param options (List[str]): the options to set.
        :param tooltips (List[str]): the tooltips to set.
        """
        self.clear()

        for i, item in enumerate(options):
            self.addItem(item)

            if tooltips:
                self.setItemData(i, tooltips[i], Qt.ItemDataRole.ToolTipRole)

    def _config_style(self) -> None:
        """
        This method configures the style of the combobox.
        """
        setup_theme()
        self.setStyleSheet("QComboBox {font-size: " + str(SMALL_FONT_SIZE) + "px ;}")
