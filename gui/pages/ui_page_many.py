"""
This module contains the code for the page many.
"""

from typing import Literal
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QLabel,
    QPushButton,
)


from gui.widgets.combobox import ComboBox
from gui.widgets.image_label import ImageLabel
from gui.widgets.slider import TransparencySlider
from gui.widgets.text_edit import TextEdit
from gui.widgets.treeview import TreeView
from language_manager import LanguageManager


class PageMany(QWidget):
    """
    This class is used to create the page many.
    """

    def __init__(self, language_manager: LanguageManager) -> None:
        """
        Creates the page many.

        :param language_manager (LanguageManager): the language manager instance.
        """
        super().__init__()
        self.setObjectName("page_many")

        self.language_manager = language_manager
        self.language_manager.language_changed.connect(self.retranslate_ui)

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

        # CREATES THE WIDGETS
        # creates input method label
        self.input_method = QLabel(self.frame)
        self.input_method.setObjectName("input_method")
        self.input_method.setMaximumHeight(30)

        self.grid_layout.addWidget(self.input_method, 0, 0)

        # creates input method combo box
        self.input_method_combobox = ComboBox(self.frame)
        self.input_method_combobox.setObjectName("input_method_combobox")
        self.input_method_combobox.setMaximumHeight(30)
        self.input_method_combobox.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )

        self.grid_layout.addWidget(self.input_method_combobox, 1, 0)

        # creates confirm input method button
        self.confirm_csv = QPushButton(self.frame)
        self.confirm_csv.setObjectName("singer_line_edit")
        self.confirm_csv.setMaximumHeight(30)
        self.confirm_csv.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )
        self.confirm_csv.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}

            """
        )

        self.grid_layout.addWidget(self.confirm_csv, 1, 1)

        # creates treeview
        self.treeview = TreeView(self.frame)
        self.treeview.setVisible(False)
        self.treeview.setEnabled(False)

        self.grid_layout.addWidget(self.treeview, 2, 0, 1, 2)

        # creates text edit
        self.text_edit = TextEdit(self.frame)
        self.text_edit.setVisible(False)
        self.text_edit.setEnabled(False)
        self.text_edit.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
            """
        )

        # creates background image label
        self.background_image_label = QLabel(self.frame)
        self.background_image_label.setObjectName("background_image_label")
        self.background_image_label.setMaximumHeight(30)
        self.background_image_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignCenter
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.background_image_label.setAcceptDrops(True)

        self.grid_layout.addWidget(self.background_image_label, 3, 0, 1, 2)

        # creates background image
        self.background_image = ImageLabel()
        self.background_image.setObjectName("background_image")
        self.background_image.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        self.grid_layout.addWidget(
            self.background_image, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        # creates transparency slider label
        self.transparency_slider_label = QLabel(self.frame)
        self.transparency_slider_label.setObjectName("transparency_slider_label")
        self.transparency_slider_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.transparency_slider_label, 5, 0)

        # creates transparency slider
        self.transparency_slider = TransparencySlider(self.background_image)
        self.transparency_slider.setObjectName("transparency_slider")

        self.grid_layout.addWidget(self.transparency_slider, 6, 0)

        # creates set transparency button
        self.set_transparency_button = QPushButton(self.frame)
        self.set_transparency_button.setObjectName("set_transparency_button")
        self.set_transparency_button.setMaximumHeight(30)

        self.grid_layout.addWidget(self.set_transparency_button, 6, 1)

        # creates open destiny folder button
        self.open_destiny_folder_button = QPushButton(self.frame)
        self.open_destiny_folder_button.setObjectName("open_destiny_folder_button")
        self.open_destiny_folder_button.setMaximumHeight(30)
        self.open_destiny_folder_button.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}

            """
        )

        self.grid_layout.addWidget(self.open_destiny_folder_button, 7, 0)

        # creates confirm button
        self.confirm_button = QPushButton(self.frame)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.setMaximumHeight(30)

        self.grid_layout.addWidget(self.confirm_button, 7, 1)

        self.vertical_layout.addWidget(
            self.frame,
        )

        # creates status bar
        self.statusbar = QFrame(self)
        self.statusbar.setObjectName("statusbar")

        self.horizontal_layout = QHBoxLayout(self.statusbar)

        self.statusbar_label = QLabel("", self.statusbar)

        self.horizontal_layout.addWidget(
            self.statusbar_label, 1, Qt.AlignmentFlag.AlignLeft
        )

        self.vertical_layout.addWidget(self.statusbar)

        self.retranslate_ui()

    def retranslate_ui(self, language: Literal["pt", "en"] = "pt") -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if language == "pt":
            self.input_method.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira o método de busca", None
                )
            )

            self.input_method.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira o método de busca", None
                )
            )

            self.input_method_combobox.set_options(
                [
                    "Buscar Músicas por CSV",
                    "Buscar Músicas Digitando o Nome e Cantor(a)",
                ],
                [
                    "O CSV deve ser estruturado como: Nome da música \
                    VÍRGULA cantor e ENTER (QUEBRA DE LINHA)",
                    "Digite o nome da música e o cantor separados por virgula \
                    e dê enter para incluir outra música",
                ],
            )

            self.confirm_csv.setText("Selecionar CSV")

            self.confirm_csv.setToolTip(
                "O CSV deve ser estruturado como: Nome da música \
                VÍRGULA cantor e ENTER (QUEBRA DE LINHA)"
            )

            self.treeview.add_headers("Itens Selecionados", ["Música", "Cantor(a)"])

            self.text_edit.setPlaceholderText(
                "Me Atraiu, Gabriela Rocha\n"
                "Deserto, Maria Marçal\n"
                "Todavia Me Algrarei, Samuel Messias"
            )

            self.text_edit.setToolTip(
                "Digite o nome da música e o cantor separados por virgula \
                e dê enter para incluir outra música"
            )

            self.background_image_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira a imagem de fundo dos slides", None
                )
            )

            self.background_image.setText(
                "\n\n Arraste a imagem de fundo dos slides aqui \n\n"
            )

            self.background_image.setToolTip(
                "Clique para abrir o seletor de arquivo ou clique com o \
                direito para abrir a imagem em tela inteira"
            )

            self.transparency_slider_label.setText(
                QCoreApplication.translate(
                    "PagesWidget",
                    "Insira a transparência da imagem de background",
                    None,
                )
            )

            self.transparency_slider.setToolTip(
                f"Opacidade selecionada: {self.transparency_slider.value()}\n \
                Role a barra para alterar"
            )

            self.transparency_slider.valueChanged.connect(
                lambda: self.transparency_slider.update_tooltip(language)
            )

            self.set_transparency_button.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Confirmar Transparência", None
                )
            )

            self.open_destiny_folder_button.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Abrir pasta de destino", None
                )
            )

            self.open_destiny_folder_button.setToolTip(
                "Você pode mudar o diretório de destino nas configurações"
            )

            self.confirm_button.setText(
                QCoreApplication.translate("PagesWidget", "Confirmar", None)
            )

        else:
            self.input_method.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insert the search method", None
                )
            )

            self.input_method_combobox.set_options(
                ["Search Music by CSV", "Search Music by typing Name and Singer"],
                [
                    "The CSV must be structured as: Name of the Music COMMA \
                    singer and ENTER (NEW LINE)",
                    "Type the name of the music and the singer separated by comma \
                    and enter to include another music",
                ],
            )

            self.confirm_csv.setText("Select CSV")

            self.confirm_csv.setToolTip(
                "The CSV must be structured as: Name of the Music COMMA singer and ENTER (NEW LINE)"
            )

            self.treeview.add_headers("Selected Items", ["Music", "Singer"])

            self.text_edit.setToolTip(
                "Enter the name of the music and the singer separated by comma \
                and enter to include another music"
            )

            self.background_image_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Enter with the slides background images", None
                )
            )

            self.text_edit.setPlaceholderText(
                "I Saw the Light, Hank Williams\n"
                "Peace in the Valley, Sam Cooke\n"
                "The Lord’s Prayer, Dinah Washington"
            )

            self.background_image.setText(
                "\n\n Drag the slides background images here \n\n"
            )

            self.background_image.setToolTip(
                "Click to open the file selector or right click to open the image in fullscreen"
            )

            self.transparency_slider_label.setText(
                QCoreApplication.translate(
                    "PagesWidget",
                    "Enter the transparency of the background image",
                )
            )
            self.transparency_slider.setToolTip(
                f"Opacity selected: {self.transparency_slider.value()}\n Drag the slider to change"
            )

            self.transparency_slider.valueChanged.connect(
                lambda: self.transparency_slider.update_tooltip(language)
            )

            self.set_transparency_button.setText(
                QCoreApplication.translate("PagesWidget", "Confirm Transparency", None)
            )

            self.open_destiny_folder_button.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Open Destination Folder", None
                )
            )

            self.open_destiny_folder_button.setToolTip(
                "You can change the destination folder in the settings"
            )

            self.confirm_button.setText(
                QCoreApplication.translate("PagesWidget", "Confirm", None)
            )
