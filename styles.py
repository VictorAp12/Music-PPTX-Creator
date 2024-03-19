"""
This module contains the styles of the application.

QSS - QT for Python Styles
https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html

Dark Theme
https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html
"""

import qdarktheme
from variables import PRIMARY_COLOR


def setup_theme() -> None:
    """
    This method sets up the theme of the application.

    It uses the qdarktheme library to set the theme.
    """
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
    )
