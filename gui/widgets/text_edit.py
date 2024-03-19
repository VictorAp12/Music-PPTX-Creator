"""
This module contains the code for the TextEdit class.
"""
from PySide6.QtWidgets import QTextEdit, QWidget


class TextEdit(QTextEdit):
    """
    This class is used to create the UI for the TextEdit.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
        """
        )
        self.setMaximumHeight(500)

        self._config_style()

    def _config_style(self) -> None:
        """
        This method configures the style of the TextEdit.
        """
        self.setStyleSheet("QTextEdit {border: 0px;}")
