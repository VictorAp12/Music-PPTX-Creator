"""
This module contains the code for the create slide style page.
"""

from typing import Literal, Tuple, TYPE_CHECKING, Union
import os
import json

from PySide6.QtGui import Qt, QPalette
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QInputDialog,
    QMessageBox,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QLabel,
    QSpinBox,
    QColorDialog,
    QPushButton,
)

from gui.widgets.combobox import ComboBox
from app.create_pptx import SlidesConfig

from variables import MEDIUM_FONT_SIZE
from utils.get_font import get_available_fonts_name

if TYPE_CHECKING:
    from gui.widgets.menu_bar import MenuBar


class UICreateSlideStyle(QDialog):
    """
    This class represents the create slide style dialog.
    It is used to create a new style for the slides that will be/were created on this app.
    """

    def __init__(
        self,
        language: Literal["pt", "en"] = "pt",
        menu_bar: Union["MenuBar", None] = None,
        parent: QWidget | None = None,
    ) -> None:
        """
        Creates the page one.

        :param language_manager (LanguageManager): the language manager instance.
        :param menu_bar (MenuBar): the menu bar.
        :param parent (QWidget, optional): the parent widget.
        """
        super().__init__(parent)

        self.language = language
        self.menu_bar = menu_bar

        self.setObjectName("create_slide_style")
        self.setWindowTitle(
            "Criar Estilo de Slide" if self.language == "pt" else "Create Slide Style"
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

        # TITLE AND SUBTITLE Configuration
        # //////////////////////////////////////////////////////////////////////////////////
        # creates title subtitle label
        self.title_subtitle_label = QLabel(self.frame)
        self.title_subtitle_label.setObjectName("title_subtitle_label")
        self.title_subtitle_label.setStyleSheet(
            f"""
            font-size: {MEDIUM_FONT_SIZE}px;
            font-weight: bold;
            """
        )
        self.title_subtitle_label.setMaximumHeight(50)

        self.grid_layout.addWidget(
            self.title_subtitle_label,
            0,
            0,
            Qt.AlignmentFlag.AlignLeft,  # | Qt.AlignmentFlag.AlignTop,
        )

        # creates background color RGB label
        self.background_color_rgb_label = QLabel(self.frame)
        self.background_color_rgb_label.setObjectName("background_color_RGB_label")
        self.background_color_rgb_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.background_color_rgb_label, 1, 0)

        # creates background color RGB button
        self.background_color_rgb_button = QPushButton(self.frame)
        self.background_color_rgb_button.setObjectName("background_color_RGB")
        self.background_color_rgb_button.setMaximumHeight(30)
        self.background_color_rgb_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )
        self.background_color_rgb_button.setStyleSheet(
            "background-color: rgb(255, 255, 255);"
        )

        self.background_color_rgb_button.clicked.connect(
            lambda: self._show_color_dialog(self.background_color_rgb_button)
        )

        self.grid_layout.addWidget(self.background_color_rgb_button, 2, 0)

        # creates the title font size PT label
        self.title_font_size_pt_label = QLabel(self.frame)
        self.title_font_size_pt_label.setObjectName("title_font_size_PT_label")
        self.title_font_size_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.title_font_size_pt_label, 3, 0)

        # creates the title font size PT
        self.title_font_size_pt_spinbox = QSpinBox(self.frame)
        self.title_font_size_pt_spinbox.setObjectName("title_font_size_PT")
        self.title_font_size_pt_spinbox.setMaximumHeight(30)
        self.title_font_size_pt_spinbox.setRange(8, 96)
        self.title_font_size_pt_spinbox.setValue(56)

        self.grid_layout.addWidget(self.title_font_size_pt_spinbox, 4, 0)

        # creates the title font color RGB label
        self.title_font_color_rgb_label = QLabel(self.frame)
        self.title_font_color_rgb_label.setObjectName("title_font_color_RGB_label")
        self.title_font_color_rgb_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.title_font_color_rgb_label, 5, 0)

        # creates the title font color RGB button
        self.title_font_color_rgb_button = QPushButton(self.frame)
        self.title_font_color_rgb_button.setObjectName("title_font_color_RGB")
        self.title_font_color_rgb_button.setMaximumHeight(30)
        self.title_font_color_rgb_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )

        self.title_font_color_rgb_button.setStyleSheet(
            "background-color: rgb(0, 0, 0);"
        )

        self.title_font_color_rgb_button.clicked.connect(
            lambda: self._show_color_dialog(self.title_font_color_rgb_button)
        )

        self.grid_layout.addWidget(self.title_font_color_rgb_button, 6, 0)

        # creates the title font isbold label
        self.title_font_isbold_label = QLabel(self.frame)
        self.title_font_isbold_label.setObjectName("title_font_isbold_label")
        self.title_font_isbold_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.title_font_isbold_label, 7, 0)

        # creates the title font isbold combobox
        self.title_font_isbold_combobox = ComboBox(self.frame)
        self.title_font_isbold_combobox.setObjectName("title_font_isbold")
        self.title_font_isbold_combobox.setMaximumHeight(30)

        self.grid_layout.addWidget(self.title_font_isbold_combobox, 8, 0)

        # creates the title font name label
        self.title_font_name_label = QLabel(self.frame)
        self.title_font_name_label.setObjectName("title_font_name_label")
        self.title_font_name_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.title_font_name_label, 9, 0)

        # creates the title font name combobox
        self.title_font_name_combobox = ComboBox(self.frame)
        self.title_font_name_combobox.setObjectName("title_font_name")
        self.title_font_name_combobox.setMaximumHeight(30)

        self.title_font_name_combobox.set_options(get_available_fonts_name())

        self.grid_layout.addWidget(self.title_font_name_combobox, 10, 0)

        # creates the subtitle font size PT label
        self.subtitle_font_size_pt_label = QLabel(self.frame)
        self.subtitle_font_size_pt_label.setObjectName("subtitle_font_size_PT_label")
        self.subtitle_font_size_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.subtitle_font_size_pt_label, 11, 0)

        # creates the subtitle font size PT
        self.subtitle_font_size_pt_spinbox = QSpinBox(self.frame)
        self.subtitle_font_size_pt_spinbox.setObjectName("subtitle_font_size_PT")
        self.subtitle_font_size_pt_spinbox.setMaximumHeight(30)
        self.subtitle_font_size_pt_spinbox.setRange(8, 96)
        self.subtitle_font_size_pt_spinbox.setValue(44)

        self.grid_layout.addWidget(self.subtitle_font_size_pt_spinbox, 12, 0)

        # creates the subtitle font color RGB label
        self.subtitle_font_color_rgb_label = QLabel(self.frame)
        self.subtitle_font_color_rgb_label.setObjectName(
            "subtitle_font_color_RGB_label"
        )
        self.subtitle_font_color_rgb_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.subtitle_font_color_rgb_label, 13, 0)

        # creates the subtitle font color RGB button
        self.subtitle_font_color_rgb_button = QPushButton(self.frame)
        self.subtitle_font_color_rgb_button.setObjectName("subtitle_font_color_RGB")
        self.subtitle_font_color_rgb_button.setMaximumHeight(30)
        self.subtitle_font_color_rgb_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )
        self.subtitle_font_color_rgb_button.setStyleSheet(
            "background-color: rgb(0, 0, 0);"
        )

        self.subtitle_font_color_rgb_button.clicked.connect(
            lambda: self._show_color_dialog(self.subtitle_font_color_rgb_button)
        )

        self.grid_layout.addWidget(self.subtitle_font_color_rgb_button, 14, 0)

        # creates the subtitle font isbold label
        self.subtitle_font_isbold_label = QLabel(self.frame)
        self.subtitle_font_isbold_label.setObjectName("subtitle_font_isbold_label")
        self.subtitle_font_isbold_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.subtitle_font_isbold_label, 15, 0)

        # creates the subtitle font isbold combobox
        self.subtitle_font_isbold_combobox = ComboBox(self.frame)
        self.subtitle_font_isbold_combobox.setObjectName("subtitle_font_isbold")
        self.subtitle_font_isbold_combobox.setMaximumHeight(30)

        self.grid_layout.addWidget(self.subtitle_font_isbold_combobox, 16, 0)

        # creates the subtitle font name label
        self.subtitle_font_name_label = QLabel(self.frame)
        self.subtitle_font_name_label.setObjectName("subtitle_font_name_label")
        self.subtitle_font_name_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.subtitle_font_name_label, 17, 0)

        # creates the subtitle font name combobox
        self.subtitle_font_name_combobox = ComboBox(self.frame)
        self.subtitle_font_name_combobox.setObjectName("subtitle_font_name")
        self.subtitle_font_name_combobox.setMaximumHeight(30)

        self.subtitle_font_name_combobox.set_options(get_available_fonts_name())

        self.grid_layout.addWidget(self.subtitle_font_name_combobox, 18, 0)

        # TEXT Configuration
        # //////////////////////////////////////////////////////////////////////////////////
        # creates the text label
        self.text_label = QLabel(self.frame)
        self.text_label.setObjectName("text_label")
        self.text_label.setStyleSheet(
            f"""
            font-size: {MEDIUM_FONT_SIZE}px;
            font-weight: bold;
            """
        )
        self.text_label.setMaximumHeight(50)

        self.grid_layout.addWidget(
            self.text_label,
            19,
            0,
            Qt.AlignmentFlag.AlignLeft,  # | Qt.AlignmentFlag.AlignTop,
        )

        # creates the text font size PT label
        self.text_font_size_pt_label = QLabel(self.frame)
        self.text_font_size_pt_label.setObjectName("text_font_size_PT_label")
        self.text_font_size_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_size_pt_label, 20, 0)

        # creates the text font size PT
        self.text_font_size_pt_spinbox = QSpinBox(self.frame)
        self.text_font_size_pt_spinbox.setObjectName("text_font_size_PT")
        self.text_font_size_pt_spinbox.setMaximumHeight(30)
        self.text_font_size_pt_spinbox.setRange(8, 96)
        self.text_font_size_pt_spinbox.setValue(38)

        self.grid_layout.addWidget(self.text_font_size_pt_spinbox, 21, 0)

        # creates the text font color RGB label
        self.text_font_color_rgb_label = QLabel(self.frame)
        self.text_font_color_rgb_label.setObjectName("text_font_color_RGB_label")
        self.text_font_color_rgb_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_color_rgb_label, 22, 0)

        # creates the text font color RGB button
        self.text_font_color_rgb_button = QPushButton(self.frame)
        self.text_font_color_rgb_button.setObjectName("text_font_color_RGB")
        self.text_font_color_rgb_button.setMaximumHeight(30)
        self.text_font_color_rgb_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )
        self.text_font_color_rgb_button.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.text_font_color_rgb_button.clicked.connect(
            lambda: self._show_color_dialog(self.text_font_color_rgb_button)
        )

        self.grid_layout.addWidget(self.text_font_color_rgb_button, 23, 0)

        # creates the text font isbold label
        self.text_font_isbold_label = QLabel(self.frame)
        self.text_font_isbold_label.setObjectName("text_font_isbold_label")
        self.text_font_isbold_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_isbold_label, 24, 0)

        # creates the text font isbold combobox
        self.text_font_isbold_combobox = ComboBox(self.frame)
        self.text_font_isbold_combobox.setObjectName("text_font_isbold")
        self.text_font_isbold_combobox.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_isbold_combobox, 25, 0)

        # creates the text font alignment label
        self.text_font_alignment_label = QLabel(self.frame)
        self.text_font_alignment_label.setObjectName("text_font_alignment_label")
        self.text_font_alignment_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_alignment_label, 26, 0)

        # creates the text font alignment combobox
        self.text_font_alignment_combobox = ComboBox(self.frame)
        self.text_font_alignment_combobox.setObjectName("text_font_alignment")
        self.text_font_alignment_combobox.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_alignment_combobox, 27, 0)

        # creates the text_font_line_spacing_PT
        self.text_font_line_spacing_pt_label = QLabel(self.frame)
        self.text_font_line_spacing_pt_label.setObjectName(
            "text_font_line_spacing_PT_label"
        )
        self.text_font_line_spacing_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_line_spacing_pt_label, 28, 0)

        # creates the text font line spacing PT
        self.text_font_line_spacing_pt_spinbox = QSpinBox(self.frame)
        self.text_font_line_spacing_pt_spinbox.setObjectName(
            "text_font_line_spacing_PT"
        )
        self.text_font_line_spacing_pt_spinbox.setMaximumHeight(30)
        self.text_font_line_spacing_pt_spinbox.setRange(0, 1584)
        self.text_font_line_spacing_pt_spinbox.setValue(38)

        self.grid_layout.addWidget(self.text_font_line_spacing_pt_spinbox, 29, 0)

        # creates the text font space before_PT
        self.text_font_space_before_pt_label = QLabel(self.frame)
        self.text_font_space_before_pt_label.setObjectName(
            "text_font_space_before_PT_label"
        )
        self.text_font_space_before_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_space_before_pt_label, 30, 0)

        # creates the text font space before PT
        self.text_font_space_before_pt_spinbox = QSpinBox(self.frame)
        self.text_font_space_before_pt_spinbox.setObjectName(
            "text_font_space_before_PT"
        )
        self.text_font_space_before_pt_spinbox.setMaximumHeight(30)
        self.text_font_space_before_pt_spinbox.setRange(0, 1584)
        self.text_font_space_before_pt_spinbox.setValue(0)

        self.grid_layout.addWidget(self.text_font_space_before_pt_spinbox, 31, 0)

        # creates the text font space after PT
        self.text_font_space_after_pt_label = QLabel(self.frame)
        self.text_font_space_after_pt_label.setObjectName(
            "text_font_space_after_PT_label"
        )
        self.text_font_space_after_pt_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_space_after_pt_label, 32, 0)

        # creates the text font space after PT
        self.text_font_space_after_pt_spinbox = QSpinBox(self.frame)
        self.text_font_space_after_pt_spinbox.setObjectName("text_font_space_after_PT")
        self.text_font_space_after_pt_spinbox.setMaximumHeight(30)
        self.text_font_space_after_pt_spinbox.setRange(0, 1584)
        self.text_font_space_after_pt_spinbox.setValue(0)

        self.grid_layout.addWidget(self.text_font_space_after_pt_spinbox, 33, 0)

        # creates the text name label
        self.text_font_name_label = QLabel(self.frame)
        self.text_font_name_label.setObjectName("text_font_name_label")
        self.text_font_name_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.text_font_name_label, 34, 0)

        # creates the text font name combobox
        self.text_font_name_combobox = ComboBox(self.frame)
        self.text_font_name_combobox.setObjectName("text_font_name")
        self.text_font_name_combobox.setMaximumHeight(30)
        self.text_font_name_combobox.set_options(get_available_fonts_name())

        self.grid_layout.addWidget(self.text_font_name_combobox, 35, 0)

        # creates the confirm button
        self.confirm_button = QPushButton(self.frame)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.setMaximumHeight(30)
        self.confirm_button.setStyleSheet("margin: 4px;")
        self.confirm_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.confirm_button.clicked.connect(self._confirm)

        self.grid_layout.addWidget(self.confirm_button, 36, 0)

        # adds the grid layout to the frame
        self.vertical_layout.addWidget(self.frame)

        self.retranslate_ui()

        self.setMinimumWidth(330)

    def retranslate_ui(self) -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.
        """
        if self.language == "pt":
            # title and subtitle
            self.title_subtitle_label.setText("Título e Subtítulo")

            self.background_color_rgb_label.setText(
                "Cor de fundo dos slides da apresentação:"
            )

            self.title_font_size_pt_label.setText("Tamanho da fonte do título (PT):")

            self.title_font_color_rgb_label.setText("Cor da fonte do título:")

            self.title_font_isbold_label.setText("A fonte do título é em negrito?")

            self.title_font_isbold_combobox.set_options(
                ["Sim", "Não"],
                ["Aplica negrito ao título", "Não aplica negrito ao título"],
            )

            self.title_font_name_label.setText("Nome da fonte do título:")

            self.subtitle_font_size_pt_label.setText(
                "Tamanho da fonte do subtítulo (PT):"
            )

            self.subtitle_font_color_rgb_label.setText("Cor da fonte do subtítulo:")

            self.subtitle_font_isbold_label.setText(
                "A fonte do subtítulo é em negrito?"
            )

            self.subtitle_font_isbold_combobox.set_options(
                ["Sim", "Não"],
                ["Aplica negrito ao subtítulo", "Não aplica negrito ao subtítulo"],
            )

            self.subtitle_font_name_label.setText("Nome da fonte do subtítulo:")

            # text
            self.text_label.setText("Texto")

            self.text_font_size_pt_label.setText("Tamanho da fonte do texto (PT):")

            self.text_font_color_rgb_label.setText("Cor da fonte do texto:")

            self.text_font_isbold_label.setText("A fonte do texto é em negrito?")

            self.text_font_isbold_combobox.set_options(
                ["Sim", "Não"],
                ["Aplica negrito ao texto", "Não aplica negrito ao texto"],
            )

            self.text_font_alignment_label.setText("Alinhamento do texto:")

            self.text_font_alignment_combobox.set_options(
                ["Esquerda", "Centro", "Direita"],
            )
            self.text_font_alignment_combobox.setCurrentIndex(1)

            self.text_font_line_spacing_pt_label.setText(
                "Espacamento entre linhas do texto (PT):"
            )

            self.text_font_space_before_pt_label.setText(
                "Espacamento antes do texto (PT):"
            )

            self.text_font_space_after_pt_label.setText(
                "Espacamento depois do texto (PT):"
            )

            self.text_font_name_label.setText("Nome da fonte do texto:")

            # confirm button
            self.confirm_button.setText("Confirmar")

        else:
            # title and subtitle
            self.title_subtitle_label.setText("Title and Subtitle")

            self.background_color_rgb_label.setText("Background Color of Slides:")

            self.title_font_size_pt_label.setText("Title Font Size (PT):")

            self.title_font_color_rgb_label.setText("Title Font Color:")

            self.title_font_isbold_label.setText("Title Font is Bold?")

            self.title_font_isbold_combobox.set_options(
                ["Yes", "No"], ["Apply Bold to Title", "Don't Apply Bold to Title"]
            )

            self.title_font_name_label.setText("Title Font Name:")

            self.subtitle_font_size_pt_label.setText("Subtitle Font Size (PT):")

            self.subtitle_font_color_rgb_label.setText("Subtitle Font Color:")

            self.subtitle_font_isbold_label.setText("Subtitle Font is Bold?")

            self.subtitle_font_isbold_combobox.set_options(
                ["Yes", "No"],
                ["Apply Bold to Subtitle", "Don't Apply Bold to Subtitle"],
            )

            self.subtitle_font_name_label.setText("Subtitle Font Name:")

            # text
            self.text_label.setText("Text")

            self.text_font_size_pt_label.setText("Text Font Size (PT):")

            self.text_font_color_rgb_label.setText("Text Font Color:")

            self.text_font_isbold_label.setText("Text Font is Bold?")

            self.text_font_isbold_combobox.set_options(
                ["Yes", "No"], ["Apply Bold to Text", "Don't Apply Bold to Text"]
            )

            self.text_font_alignment_label.setText("Text Alignment:")

            self.text_font_alignment_combobox.set_options(
                ["Left", "Center", "Right"],
            )

            self.text_font_line_spacing_pt_label.setText("Text Line Spacing (PT):")

            self.text_font_space_before_pt_label.setText("Text Space Before (PT):")

            self.text_font_space_after_pt_label.setText("Text Space After (PT):")

            self.text_font_name_label.setText("Text Font Name:")

            # confirm button
            self.confirm_button.setText("Confirm")

    def _show_color_dialog(self, button: QPushButton) -> None:
        """
        Shows the color dialog.
        """
        color_dialog = QColorDialog.getColor()

        if color_dialog.isValid():
            button.setStyleSheet(
                f"background-color: rgb({color_dialog.red()}, {color_dialog.green()}, \
                {color_dialog.blue()});"
            )

            # print(self.get_button_color(button))

    def get_button_color(self, button: QPushButton) -> Tuple[int, int, int]:
        """
        Gets the color of the button.

        :param button (QPushButton): the button.

        :return (Tuple[int, int, int]): the color of the button in RGB.
        """
        button_color = button.palette().color(QPalette.ColorRole.Button)
        rgb = button_color.getRgb()[:3]  # type: ignore

        return rgb

    def _confirm(self) -> None:
        """
        This method confirms the changes.
        """
        slides_config = list(SlidesConfig().__annotations__.keys())

        style = {}

        for row in range(self.grid_layout.rowCount()):
            for col in range(self.grid_layout.columnCount()):
                item = self.grid_layout.itemAtPosition(row, col)

                if item:
                    widget = item.widget()
                    object_name = widget.objectName()

                    if object_name in slides_config:
                        if isinstance(widget, QPushButton):
                            style.update({object_name: self.get_button_color(widget)})

                        elif isinstance(widget, ComboBox):
                            if object_name.endswith("font_alignment"):
                                if widget.currentText() in ("Esquerda", "Left"):
                                    style.update({object_name: 1})  # type: ignore
                                elif widget.currentText() in ("Centro", "Center"):
                                    style.update({object_name: 1})  # type: ignore
                                elif widget.currentText() in ("Direita", "Right"):
                                    style.update({object_name: 3})  # type: ignore

                            elif object_name.endswith("isbold"):
                                style.update(
                                    {
                                        object_name: widget.currentText()
                                        in ("Sim", "Yes")
                                    }
                                )

                            else:
                                style.update({object_name: widget.currentText()})

                        elif isinstance(widget, QSpinBox):
                            style.update({object_name: widget.value()})

        result = self._save_style(style)

        if result:
            self.close()

    def _save_style(self, style: dict) -> tuple[dict, str] | None:
        slide_style_dir = os.path.join(os.getcwd(), "app", "slides styles")

        os.makedirs(slide_style_dir, exist_ok=True)

        file_name = QInputDialog.getText(
            self,
            (
                "Salvar arquivo de configuração"
                if self.language == "pt"
                else "Save config file"
            ),
            (
                "Qual nome deseja dar ao arquivo de configuração?\n"
                f"Configurações existentes: {os.listdir(slide_style_dir)}"
                if self.language == "pt"
                else (
                    "What do you want to name the config file?\n"
                    f"Existing configurations: {os.listdir(slide_style_dir)}"
                )
            ),
        )[0]

        if not file_name:
            return None

        if not file_name.endswith(".json"):
            if "." in file_name:
                file_name = file_name.split(".")[0]

            file_name += ".json"

        file_path = os.path.join(slide_style_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as arquivo_json:
            json.dump(style, arquivo_json)

        if self.menu_bar:
            active_style = self.menu_bar.slide_style_menu.addAction(file_name[:-5])
            active_style.setCheckable(True)
            self.menu_bar.slide_style_group.addAction(active_style)

        QMessageBox.information(
            self,
            "Configuração salva" if self.language == "pt" else "Config file saved",
            (
                f"Configuração salva em: {file_path}"
                if self.language == "pt"
                else f"Config file saved at: {file_path}"
            ),
        )

        return style, file_path
