"""
This module contains the code for the page insert manually.
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
    QLineEdit,
    QPushButton,
)

from gui.widgets.image_label import ImageLabel
from gui.widgets.slider import TransparencySlider
from gui.widgets.text_edit import TextEdit
from language_manager import LanguageManager


class PageInsertManually(QWidget):
    """
    This class is used to create the page insert manually.
    """

    def __init__(self, language_manager: LanguageManager) -> None:
        """
        Creates the page insert manually.

        :param language_manager (LanguageManager): the language manager instance.
        """
        super().__init__()
        self.setObjectName("page_insert_manually")

        self.language_manager = language_manager
        self.language_manager.language_changed.connect(self.retranslate_ui)

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

        # CREATES THE WIDGETS
        # creates music label
        self.music_label = QLabel(self.frame)
        self.music_label.setObjectName("music_label")
        self.music_label.setMaximumHeight(30)

        self.grid_layout.addWidget(self.music_label, 0, 0)

        # creates music line edit
        self.music_line_edit = QLineEdit(self.frame)
        self.music_line_edit.setObjectName("music_line_edit")
        self.music_line_edit.setMaximumHeight(30)
        self.music_line_edit.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )

        self.grid_layout.addWidget(self.music_line_edit, 1, 0)

        # creates singer label
        self.singer_label = QLabel(self.frame)
        self.singer_label.setObjectName("singer_label")
        self.singer_label.setMaximumHeight(30)
        self.singer_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.grid_layout.addWidget(self.singer_label, 0, 1)

        # creates singer line edit
        self.singer_line_edit = QLineEdit(self.frame)
        self.singer_line_edit.setObjectName("singer_line_edit")
        self.singer_line_edit.setMaximumHeight(30)
        self.singer_line_edit.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        )

        self.grid_layout.addWidget(self.singer_line_edit, 1, 1)

        # creates text edit
        self.text_edit = TextEdit(self.frame)
        self.text_edit.setObjectName("text_edit")
        self.text_edit.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
            """
        )
        self.text_edit.setMinimumHeight(300)
        self.grid_layout.addWidget(self.text_edit, 2, 0, 1, 2)

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
            self.music_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira o nome da música", None
                )
            )
            self.singer_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira o nome do(a) cantor(a)", None
                )
            )

            self.text_edit.setPlaceholderText(
                """
            Exemplo de texto (geraria 3 slides):
            Prenderam meu Jesus, chicotearam, ferido Ele foi
            Levando sobre si, os meus pecados
            Colocaram em sua cabeça
            Uma coroa de espinhos uma lança o transpassou
            Sozinho Ele ficou sem seus amigos

            E por onde Ele passava
            Na rua de Jerusalém
            Cada passo que Ele dava sangue puro derramava
            Como uma ovelha muda Ele não reclamou
            E no alto daquele calvário
            Ele expirou, mas no terceiro dia meu Jesus Ressuscitou

            Ressuscitou o Amado o Adorado
            É a raiz de Davi a estrela da manhã
            Ancião dos dias é o príncipe da paz
            """
            )

            self.text_edit.setToolTip(
                "Insire a letra da musica, para separar os slides "
                "deixe uma linha em branco como no exemplo"
            )

            self.background_image_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Insira a imagem de fundo do slide", None
                )
            )

            self.background_image.setText(
                "\n\n Arraste a imagem de fundo do slide aqui \n\n"
            )

            self.background_image.setToolTip(
                "Clique para abrir o seletor de arquivo ou clique com o "
                "direito para abrir a imagem em tela inteira"
            )

            self.transparency_slider_label.setText(
                QCoreApplication.translate(
                    "PagesWidget",
                    "Insira a transparência da imagem de background",
                    None,
                )
            )

            self.transparency_slider.setToolTip(
                f"Opacidade selecionada: {self.transparency_slider.value()}\n"
                "Role a barra para alterar"
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
            self.music_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Enter the name of the music", None
                )
            )
            self.singer_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Enter the name of the singer", None
                )
            )
            self.background_image_label.setText(
                QCoreApplication.translate(
                    "PagesWidget", "Enter with the background image", None
                )
            )

            self.text_edit.setPlaceholderText(
                """
            Example of text (generates 3 slides):
            Break out the cymbals and tambourines
            Call up the trumpets and horns
            Raise up a banner and come with me
            It's time to worship the Lord

            Praise Him together in unity
            We've got a reason to sing
            Lift up a heavenly harmony
            It's time to worship the King

            With one voice
            Every tribe will Praise Him
            With one voice
            Every tongue will tell
            That the Lord is good
            And his love endures
            And His mercy lasts forever
            """
            )

            self.text_edit.setToolTip(
                "Enter the text of the music, separate the slides "
                "with a blank line as in the example"
            )
            self.background_image.setText(
                "\n\n Drag the slide background image here \n\n"
            )

            self.background_image.setToolTip(
                "Click to open the file selector or right click to open the image in fullscreen"
            )

            self.transparency_slider_label.setText(
                QCoreApplication.translate(
                    "PagesWidget",
                    "Enter the transparency of the slide background image",
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
