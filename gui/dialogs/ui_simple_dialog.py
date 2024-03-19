"""
This module contains the code for the SimpleDialog class.

It's used to create a simple dialog.
"""

import os
from pathlib import Path
from typing import Literal
from PySide6.QtCore import QRect, QSize, QMetaObject, QCoreApplication
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QProgressBar,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QDialog,
)
from dotenv import load_dotenv, dotenv_values, set_key


class UiSelectedFolder(QDialog):
    """
    This class is used to create window that shows the path of the selected folder
    and allows the user to change it.
    """

    def __init__(
        self,
        language: Literal["pt", "en"] = "pt",
        parent: QMainWindow | None = None,
        path: Path | str = Path.cwd() / "files",
    ) -> None:
        """
        Creates the simple dialog.

        :param language (Literal["pt", "en"]): the language.
        :param parent (QMainWindow, optional): the parent window.
        :param path (Path | str): the path of the folder.
        """
        super().__init__(parent)

        self.language = language

        self.setObjectName("SelectedFolder")
        self.setWindowTitle(
            "Pasta Selecionada" if self.language == "pt" else "Selected Folder"
        )
        self.path = path

        # creates the vertical layout widget
        self.vertical_layout_widget = QWidget(self)
        self.vertical_layout_widget.setObjectName("vertical_layout_widget")
        self.vertical_layout_widget.setGeometry(QRect(5, 5, 340, 110))  # 261, 111))

        # creates the grid layout
        self.grid_layout = QGridLayout(self.vertical_layout_widget)
        self.grid_layout.setObjectName("grid_layout")
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # creates the title_label
        self.title_label = QLabel(self.vertical_layout_widget)
        self.title_label.setObjectName("title_label")
        self.title_label.setMaximumSize(QSize(16777215, 20))
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 2)

        # creates the current_folder_line_edit
        self.current_folder_line_edit = QLineEdit(self.vertical_layout_widget)
        self.current_folder_line_edit.setObjectName("current_folder_line_edit")

        self.grid_layout.addWidget(self.current_folder_line_edit, 1, 0, 1, 2)

        # creates the select another folder button
        self.select_another_folder_button = QPushButton(self.vertical_layout_widget)
        self.select_another_folder_button.setObjectName("select_another_folder_button")
        self.select_another_folder_button.clicked.connect(self._open_folder)

        self.grid_layout.addWidget(self.select_another_folder_button, 2, 0, 1, 1)

        # creates the confirm button
        self.confirm_button = QPushButton(self.vertical_layout_widget)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.clicked.connect(self._confirm_button_clicked)

        self.grid_layout.addWidget(self.confirm_button, 2, 1, 1, 1)

        self.retranslate_ui()

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def retranslate_ui(self) -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if self.language == "pt":
            self.title_label.setText(
                QCoreApplication.translate("SelectedFolder", "Pasta atual:", None)
            )

            self.current_folder_line_edit.setText(str(self.path))
            self.current_folder_line_edit.setReadOnly(True)

            self.select_another_folder_button.setText(
                QCoreApplication.translate(
                    "SelectedFolder", "Selecionar Outra Pasta", None
                )
            )

            self.confirm_button.setText(
                QCoreApplication.translate("SelectedFolder", "Confirmar", None)
            )

        elif self.language == "en":
            self.title_label.setText(
                QCoreApplication.translate("SelectedFolder", "Current Folder:", None)
            )

            self.current_folder_line_edit.setText(str(self.path))
            self.current_folder_line_edit.setReadOnly(True)

            self.select_another_folder_button.setText(
                QCoreApplication.translate(
                    "SelectedFolder", "Select Another Folder", None
                )
            )

            self.confirm_button.setText(
                QCoreApplication.translate("SelectedFolder", "Confirm", None)
            )

    # retranslateUi

    def _confirm_button_clicked(self) -> None:
        """
        This method is called when the confirm button is clicked.
        """

        self.path = self.current_folder_line_edit.text()

        if (
            not Path(self.path).exists()
            or not Path(self.path).is_dir()
            or not self.path
        ):
            return

        env_vars = dotenv_values("settings/.env")
        env_vars["SELECTED_FOLDER"] = Path(self.path).as_posix()
        set_key("settings/.env", "SELECTED_FOLDER", env_vars["SELECTED_FOLDER"])

        load_dotenv(os.path.abspath("settings/.env"), override=True, encoding="utf-8")

        self.close()

    def _open_folder(self) -> None:
        """
        Opens a folder dialog.
        """
        new_path = QFileDialog.getExistingDirectory(None, "Selecionar pasta")

        self.current_folder_line_edit.setText(str(new_path))


class UIGeniusKey(QDialog):
    """
    This class is used to create the UI for the Genius API key.

    It's used to get the API key from the user.
    """

    def __init__(
        self,
        language: Literal["pt", "en"] = "pt",
        parent: QWidget | None = None,
        key: str | None = None,
    ) -> None:
        """
        Creates a simple dialog.

        :param language (Literal["pt", "en"]): the language to use.
        :param parent (QWidget, optional): the parent widget.
        :param key (str, optional): the API key.
        """
        super().__init__(parent)
        self.language = language

        self.key = key

        self.setObjectName("GeniusKey")
        self.setWindowTitle(
            "Genius API Key" if self.language == "pt" else "Genius API Key"
        )
        self.setFixedSize(350, 110)

        # creates the vertical layout widget
        self.vertical_layout_widget = QWidget(self)
        self.vertical_layout_widget.setObjectName("vertical_layout_widget")
        self.vertical_layout_widget.setGeometry(QRect(5, 5, 340, 110))

        # creates the grid layout
        self.grid_layout = QGridLayout(self.vertical_layout_widget)
        self.grid_layout.setObjectName("grid_layout")
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # creates the title_label
        self.title_label = QLabel(self.vertical_layout_widget)
        self.title_label.setObjectName("title_label")
        self.title_label.setMaximumSize(QSize(16777215, 20))
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 2)

        # creates the current_folder_line_edit
        self.current_api_key_line_edit = QLineEdit(self.vertical_layout_widget)
        self.current_api_key_line_edit.setObjectName("current_api_key_line_edit")

        self.grid_layout.addWidget(self.current_api_key_line_edit, 1, 0, 1, 2)

        # creates the confirm button
        self.confirm_button = QPushButton(self.vertical_layout_widget)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.clicked.connect(self._confirm_button_clicked)

        self.grid_layout.addWidget(
            self.confirm_button, 2, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter
        )

        self.retranslate_ui()

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def retranslate_ui(self) -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if self.language == "pt":
            self.title_label.setText(
                QCoreApplication.translate("GeniusKey", "Genius API Key:", None)
            )

            self.current_api_key_line_edit.setText(str(self.key))

            self.confirm_button.setText(
                QCoreApplication.translate("selected_folder", "Confirmar", None)
            )
        else:
            self.title_label.setText(
                QCoreApplication.translate("window", "Genius API Key:", None)
            )

            self.current_api_key_line_edit.setText(str(self.key))

            self.confirm_button.setText(
                QCoreApplication.translate("selected_folder", "Confirm", None)
            )

    def _confirm_button_clicked(self) -> None:
        """
        This method is called when the confirm button is clicked.
        """
        self.key = self.current_api_key_line_edit.text()

        if not self.key:
            return

        env_vars = dotenv_values("settings/.env")
        env_vars["GENIUS_API_KEY"] = self.key

        set_key("settings/.env", "GENIUS_API_KEY", env_vars["GENIUS_API_KEY"])

        load_dotenv(os.path.abspath("settings/.env"), override=True, encoding="utf-8")

        self.close()


class UIProgressBar(QDialog):
    """
    This class is used to create the UI for the progress bar.
    """

    def __init__(
        self,
        language: Literal["pt", "en"] = "pt",
        parent: QWidget | None = None,
    ) -> None:
        """
        Creates a simple dialog.

        :param language (Literal["pt", "en"]): the language to use.
        :param parent (QWidget, optional): the parent widget.
        :param progress (int, optional): the progress.
        """
        super().__init__(parent)
        self.language = language

        self.setObjectName("ProgressBar")
        self.setWindowTitle("Carregando..." if self.language == "pt" else "Loading...")

        # creates the vertical layout widget
        self.vertical_layout_widget = QWidget(self)
        self.vertical_layout_widget.setObjectName("vertical_layout_widget")
        self.vertical_layout_widget.setGeometry(QRect(5, 5, 340, 110))

        # creates the grid layout
        self.grid_layout = QGridLayout(self.vertical_layout_widget)
        self.grid_layout.setObjectName("grid_layout")
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # creates the title_label
        self.title_label = QLabel(self.vertical_layout_widget)
        self.title_label.setObjectName("title_label")
        self.title_label.setMaximumSize(QSize(16777215, 20))
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 2)

        self.progress = 0

        # creates the progressbar
        self.progress_bar = QProgressBar(self.vertical_layout_widget)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setValue(self.progress)

        self.progress_bar.setMinimumWidth(self.width() // 2)

        self.grid_layout.addWidget(
            self.progress_bar, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter
        )

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if self.language == "pt":
            self.title_label.setText(
                QCoreApplication.translate("ProgressBar", "Carregando...", None)
            )

        else:
            self.title_label.setText(
                QCoreApplication.translate("ProgressBar", "Loading...", None)
            )

    def update_progress(self, progress: int, total: int) -> None:
        """
        Updates the progress bar.

        :param progress (int): the progress.
        :param total (int): the total.
        """
        self.progress = progress

        self.progress_bar.setValue(int(self.progress / total) * 100)


# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     dialog = UIProgressBar()
#     dialog.show()
#     app.exec()
