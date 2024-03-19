"""
This module contains the code for the modify slide style page.
"""

import json
from typing import Literal, TYPE_CHECKING
import os
from glob import glob

from PySide6.QtCore import QPoint, QEvent
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QLabel,
    QLineEdit,
    QPushButton,
)

from gui.slides_adjusts.ui_create_slide_style import UICreateSlideStyle
from gui.widgets.combobox import ComboBox
from gui.widgets.treeview import TreeView

from app.create_pptx import SlidesConfig, create_slides, extract_presentation_infos

if TYPE_CHECKING:
    from gui.widgets.menu_bar import MenuBar


class UIModifySlideStyle(QDialog):
    """
    This class represents the modify slide style dialog.
        It is used to modify the slides style that were created on this app.
    """

    def __init__(
        self,
        menu_bar: "MenuBar",
        language: Literal["pt", "en"] = "pt",
        parent: QWidget | None = None,
    ) -> None:
        """
        Creates the modify slide style dialog.


        :param language_manager (LanguageManager): the language manager instance.
        :param menu_bar (MenuBar): the menu bar.
        :param parent (QWidget, optional): the parent widget.
        """
        super().__init__(parent)

        self.language: Literal["pt", "en"] = language
        self.menu_bar = menu_bar

        self.setObjectName("modify_slide_style")
        self.setWindowTitle(
            "Modificar Estilo de Slides"
            if self.language == "pt"
            else "Modify Slides Style"
        )

        # creates the vertical layout
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setObjectName("vertical_layout")

        # creates the group box
        self.group_box = QGroupBox()
        self.group_box.setObjectName("group_box")
        self.group_box.setGeometry(self.rect())
        self.group_box.setFlat(True)

        self.group_box.setLayout(self.vertical_layout)

        # creates the scroll area
        self.scroll_ = QScrollArea()
        self.scroll_.setObjectName("scroll")
        self.scroll_.setWidget(self.group_box)
        self.scroll_.setWidgetResizable(True)

        # creates the layout for the scroll area
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.addWidget(self.scroll_)

        self.setLayout(self.scroll_layout)

        # creates the frame
        self.frame = QFrame(self.group_box)
        self.frame.setObjectName("frame")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.frame.setSizePolicy(size_policy)

        # creates the grid layout for the frame
        self.vertical_layout.addWidget(self.frame, 1, Qt.AlignmentFlag.AlignCenter)

        self.grid_layout = QGridLayout(self.frame)
        self.grid_layout.setObjectName("grid_layout")

        # creates the selected input folder label
        self.selected_input_folder_label = QLabel(self.frame)
        self.selected_input_folder_label.setObjectName("selected_input_folder_label")

        self.grid_layout.addWidget(self.selected_input_folder_label, 0, 0)

        # creates the select input folder line edit
        self.select_input_folder_line_edit = QLineEdit(self.frame)
        self.select_input_folder_line_edit.setObjectName(
            "select_input_folder_line_edit"
        )
        self.select_input_folder_line_edit.setReadOnly(True)

        self.grid_layout.addWidget(self.select_input_folder_line_edit, 1, 0)

        # creates the select folder button
        self.select_input_folder_button = QPushButton(self.frame)
        self.select_input_folder_button.setObjectName("select_input_folder_button")
        self.select_input_folder_button.setMaximumHeight(30)
        self.select_input_folder_button.clicked.connect(self._open_input_folder)

        self.grid_layout.addWidget(self.select_input_folder_button, 1, 1)

        # creates treeview
        self.treeview = TreeView(self.frame)
        self.treeview.setVisible(False)
        self.treeview.setEnabled(False)

        self.grid_layout.addWidget(self.treeview, 2, 0, 1, 2)

        # creates the selected output folder label
        self.selected_output_folder_label = QLabel(self.frame)
        self.selected_output_folder_label.setObjectName("selected_output_folder_label")

        self.grid_layout.addWidget(self.selected_output_folder_label, 3, 0)

        # creates the select output folder line edit
        self.select_output_folder_line_edit = QLineEdit(self.frame)
        self.select_output_folder_line_edit.setObjectName(
            "select_output_folder_line_edit"
        )
        self.select_output_folder_line_edit.setReadOnly(True)

        self.grid_layout.addWidget(self.select_output_folder_line_edit, 4, 0)

        # creates the select output folder button
        self.select_output_folder_button = QPushButton(self.frame)
        self.select_output_folder_button.setObjectName("select_output_folder_button")
        self.select_output_folder_button.setMaximumHeight(30)

        self.select_output_folder_button.clicked.connect(self._open_output_folder)

        self.grid_layout.addWidget(self.select_output_folder_button, 4, 1)

        # creates the styles label
        self.styles_label = QLabel(self.frame)
        self.styles_label.setObjectName("styles_label")

        self.grid_layout.addWidget(self.styles_label, 5, 0)

        # creates the styles combobox
        self.styles_combobox = ComboBox(self.frame)
        self.styles_combobox.setObjectName("styles_combobox")
        self.styles_combobox.set_options(
            [style.text() for style in self.menu_bar.slide_style_group.actions()]
        )
        self.styles_combobox.currentTextChanged.connect(self._create_new_style_selected)

        self.grid_layout.addWidget(self.styles_combobox, 6, 0)

        # creates the confirm button
        self.confirm_button = QPushButton(self.frame)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.setMaximumHeight(30)
        self.confirm_button.setStyleSheet("margin: 4px;")

        self.confirm_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.confirm_button.clicked.connect(self._confirm)

        self.grid_layout.addWidget(self.confirm_button, 7, 0, 1, 2)

        # adds the grid layout to the frame
        self.vertical_layout.addWidget(self.frame)

        # creates status bar
        self.statusbar = QFrame(self)
        self.statusbar.setObjectName("statusbar")

        self.horizontal_layout = QHBoxLayout(self.statusbar)

        self.statusbar_label = QLabel("", self.statusbar)

        self.horizontal_layout.addWidget(
            self.statusbar_label, 1, Qt.AlignmentFlag.AlignLeft
        )

        # adds the status bar to the frame
        self.vertical_layout.addWidget(self.statusbar)

        self.retranslate_ui()

        self.setMinimumWidth(450)

    def retranslate_ui(self) -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.
        """
        if self.language == "pt":
            self.selected_input_folder_label.setText("Pasta Selecionada:")

            self.select_input_folder_button.setText("Selecionar Pasta")

            self.selected_output_folder_label.setText("Pasta de Destino Selecionada:")

            self.select_output_folder_button.setText("Selecionar Pasta de Destino")

            self.treeview.add_headers(
                "Itens Selecionados",
                ["Nomes dos Arquivos"],
            )

            self.styles_label.setText("Estilo escolhido:")

            self.styles_combobox.addItem("Crie seu estilo")

            self.confirm_button.setText("Confirmar")

        else:
            self.selected_input_folder_label.setText("Selected Folder:")

            self.select_input_folder_button.setText("Select Folder")

            self.selected_output_folder_label.setText("Selected Destiny Folder:")

            self.select_output_folder_button.setText("Select Destiny Folder")

            self.treeview.add_headers(
                "Selected Items",
                ["File Names"],
            )

            self.styles_label.setText("Selected style:")

            self.styles_combobox.addItem("Create your own style")

            self.confirm_button.setText("Confirm")

    def _open_input_folder(self) -> None:
        """
        Opens a folder dialog.
        """
        new_path = QFileDialog.getExistingDirectory(None, "Selecionar pasta")

        self.select_input_folder_line_edit.setText(str(new_path))

        files_found = glob(os.path.join(new_path, "*.pptx"), recursive=False)

        if files_found:
            file_names = [os.path.basename(file) for file in files_found]

            self.treeview.clear()

            self.treeview.add_values(file_names)

            self.treeview.setVisible(True)

            self.treeview.setEnabled(True)

            if self.height() < 240:
                self.resize(self.width(), 240)

    def _open_output_folder(self) -> None:
        """
        Opens a folder dialog.
        """
        new_path = QFileDialog.getExistingDirectory(None, "Selecionar pasta")

        self.select_output_folder_line_edit.setText(str(new_path))

    def _create_new_style_selected(self, _: QEvent) -> None:
        """
        This method is called when the user selects a style from the combobox.
        If the user selects "Crie seu estilo" or "Create your own style",
        it opens the create slide style

        :param _ (QEvent): the event.
        """

        if not self.styles_combobox.currentText() in (
            "Crie seu estilo",
            "Create your own style",
        ):
            return

        create_slides_style_ui = UICreateSlideStyle(self.language, self.menu_bar)  # type: ignore

        # place the window in the center of the app
        config_slides_window_width = create_slides_style_ui.frameGeometry().width()

        create_slides_style_ui.move(
            self.frameGeometry().center()
            - QPoint(config_slides_window_width / 3.7, 100)  # type: ignore
        )

        self.setEnabled(False)
        create_slides_style_ui.exec()
        self.setEnabled(True)

        self.styles_combobox.set_options(
            [style.text() for style in self.menu_bar.slide_style_group.actions()]
        )

        self.styles_combobox.addItem(
            "Crie seu estilo" if self.language == "pt" else "Create your own style"
        )

    def _confirm(self) -> None:
        """
        This method confirms the changes.
        """

        if self.styles_combobox.currentText() in (
            "Crie seu estilo",
            "Create your own style",
        ):
            return

        style = self.styles_combobox.currentText() + ".json"

        style = style.replace("black background", "fundo preto").replace(
            "white background", "fundo branco"
        )

        style_path = os.path.join(os.getcwd(), "app", "slides styles", style)

        with open(
            style_path,
            "r",
            encoding="utf-8",
        ) as style_config:
            config = json.load(style_config)
            slide_config = SlidesConfig(**config)

        file_names_list = []

        for i in range(self.treeview.topLevelItemCount()):
            item = self.treeview.topLevelItem(i)
            if item.checkState(0) == Qt.CheckState.Checked:
                file_names_list.append(item.text(1).strip())

        for presentation in file_names_list:
            (
                presentation_title,
                presentation_subtitle,
                presentation_text,
                image,
                bg_image,
            ) = extract_presentation_infos(
                presentation_path=os.path.join(
                    self.select_input_folder_line_edit.text(), presentation
                )
            )

            create_slides(
                widget=self.statusbar_label,
                music_title=presentation_title,
                music_singer=presentation_subtitle,
                music_lyric=presentation_text,
                slides_config=slide_config,
                FILES_FOLDER=self.select_output_folder_line_edit.text(),
                image=image,
                background_image=bg_image,
                language=self.language,
            )

        self.statusbar_label.clear()

        QMessageBox.information(
            self,
            "Sucesso!" if self.language == "pt" else "Success!",
            (
                "As mudanças foram realizadas com sucesso"
                if self.language == "pt"
                else "The changes were made successfully!"
            ),
            QMessageBox.StandardButton.Ok,
        )
