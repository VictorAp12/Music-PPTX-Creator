"""
This module contains the MainWindow class.
"""

# from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSpacerItem,
    QStackedWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
)
from PySide6.QtCore import Qt, QRect


from gui.widgets.menu_bar import MenuBar
from gui.pages.ui_pages import UiPagesWidget
from language_manager import LanguageManager


class MainWindow(QMainWindow):
    """
    This class is used to create the main window.
    """

    def __init__(self, language_manager: LanguageManager) -> None:
        """
        Creates the main window.

        :param language_manager (LanguageManager): the language manager instance.
        """
        super().__init__()

        self.menu_bar = MenuBar(self, language_manager)
        self.setMenuBar(self.menu_bar)

        # CENTRAL WIDGET
        # ///////////////////////////////////////////////////////////////
        # creates the central widget
        self.central_frame = QFrame()

        # create main layout
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT MENU FRAME
        # /////////////////////////////////////////////////////////////
        # creates the menu frame
        self.left_menu_frame = QFrame(self)
        self.left_menu_frame.setGeometry(QRect(0, 0, 100, self.height()))
        self.left_menu_frame.setMinimumWidth(170)
        self.left_menu_frame.setMinimumHeight(170)
        self.left_menu_frame.resize(200, 170)

        self.left_menu_frame.setStyleSheet("border: 2px solid rgb(30, 112, 162);")

        # left menu layout
        self.left_menu_layout = QVBoxLayout(self.left_menu_frame)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_layout.setSpacing(0)

        # CONTENT FRAME
        # /////////////////////////////////////////////////////////////
        # creates the content frame
        self.content_frame = QFrame()
        self.content_frame.resize(620, 400)

        # creates the content layout
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # creates application pages
        self.pages = QStackedWidget()
        self.pages_ui = UiPagesWidget(self, language_manager, self.pages, self.menu_bar)

        self.pages.setCurrentWidget(self.pages_ui.page_one)

        # ADD CONTENT LAYOUT
        # ///////////////////////////////////////////////////////////////
        self.content_layout.addWidget(self.pages)

        # ADD SPLITTER
        # ////////////////////////////////////////////////////////////
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_menu_frame)
        self.splitter.addWidget(self.content_frame)

        # ADD WIDGETS TO APP
        # ///////////////////////////////////////////////////////////////
        self.main_layout.addWidget(self.splitter)

        # SET CENTRAL WIDGET
        # ///////////////////////////////////////////////////////////////
        self.setCentralWidget(self.central_frame)

        # window title
        self.setWindowTitle("Music PPTX Creator")

        # set the inicial size
        self.resize(782, self.height())

    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     """
    #     This method adjusts the size of the window.
    #     I used it to print the size of the window.

    #     :param event (QResizeEvent): the resize event.
    #     """
    #     print("Window size: ", self.size())
    #     print("Left_menu size: ", self.left_menu_frame.size())
    #     print("Content size: ", self.content_frame.size())
    #     return super().resizeEvent(event)

    def adjust_fixed_size(self) -> None:
        """
        This method adjusts the fixed size of the window.
        """
        self.adjustSize()

    def add_widget_to_vlayout(
        self, widget: QWidget, alignment: Qt.AlignmentFlag | None = None
    ) -> None:
        """
        This method adds a widget to the v_layout of the main window.

        :param widget (QWidget): the widget to add.
        :param alignment (Qt.AlignmentFlag): the alignment of the widget.
        """
        if alignment:
            self.content_layout.addWidget(widget, alignment=alignment)
        else:
            self.content_layout.addWidget(widget)

    def add_widget_to_menu_frame(
        self, widget: QWidget | QSpacerItem, alignment: Qt.AlignmentFlag | None = None
    ) -> None:
        """
        This method adds a widget to the menu frame of the main window.

        :param widget (QWidget): the widget to add.
        :param alignment (Qt.AlignmentFlag): the alignment of the widget.
        """
        if isinstance(widget, QWidget):

            if alignment:
                self.left_menu_layout.addWidget(widget, alignment=alignment)
            else:
                self.left_menu_layout.addWidget(widget)

        else:
            self.left_menu_layout.addItem(widget)
