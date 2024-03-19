"""
This module contains the MenuBar class.
The class is used to create the menu bar on the top of the main window.
"""

import os
from typing import Literal
import webbrowser
from pathlib import Path

from PySide6.QtWidgets import QMenuBar, QMenu, QMainWindow
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QActionGroup
from dotenv import load_dotenv

from gui.dialogs.ui_simple_dialog import UIGeniusKey, UiSelectedFolder
from gui.slides_adjusts.ui_create_slide_style import UICreateSlideStyle
from gui.slides_adjusts.ui_modify_slide_style import UIModifySlideStyle
from language_manager import LanguageManager


class MenuBar(QMenuBar):
    """
    This class is used to create the menu bar.
    """

    def __init__(self, parent: QMainWindow, language_manager: LanguageManager) -> None:
        """
        Creates the menu bar.

        :param parent (QMainWindow): the main window.
        :param language_manager (LanguageManager): the language manager instance.
        """
        super().__init__(parent)

        self.mainwindow = parent

        self.language_manager = language_manager
        self.language_manager.language_changed.connect(self.retranslate_ui)

        self.setGeometry(QRect(0, 0, 634, 22))
        self._create_config_menu()
        self._create_slide_style_menu()
        self._create_change_language_menu()
        self._create_about_menu()

        self.retranslate_ui()

    def _create_config_menu(self) -> None:
        """
        Creates the config menu.
        """
        # setup and creates the menubar
        self.menu = QMenu("Configurações", self)
        self.menu.setToolTipsVisible(True)
        self.menu.setStyleSheet(
            "QToolTip {background-color: dark; color: white;border: black solid 1px}"
        )

        self.addMenu(self.menu)

        # creates the "Criar Novo Estilo de Slide" menu action
        self.menu_create_slides_stiles = self.menu.addAction(
            "Criar Novo Estilo de Slide"
        )
        self.menu_create_slides_stiles.triggered.connect(self._config_slides)

        # creates the "Modificar Slides Existentes" menu action
        self.menu_modify_slides = self.menu.addAction("Modificar Slides Existentes")

        self.menu_modify_slides.triggered.connect(self._modify_slides)

        # creates the "Escolher Pasta de Destino"
        self.menu_choose_folder = self.menu.addAction("Escolher Pasta de Destino")

        self.menu_choose_folder.triggered.connect(self._choose_folder)

        # creates the "Escolher Chave de API"
        self.menu_choose_api_key = self.menu.addAction("Escolher Chave de API")

        self.menu_choose_api_key.triggered.connect(self._type_api_key)

    def _config_slides(self) -> None:
        create_slides_style_ui = UICreateSlideStyle(self.get_selected_language(), self)

        # create_slides_ui.adjustSize()

        # place the window in the center of the app
        config_slides_window_width = create_slides_style_ui.frameGeometry().width()

        create_slides_style_ui.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(config_slides_window_width / 3.7, 100)  # type: ignore
        )

        self.mainwindow.setEnabled(False)
        create_slides_style_ui.exec()
        self.mainwindow.setEnabled(True)

    def _modify_slides(self) -> None:
        modify_slides_style = UIModifySlideStyle(self, self.get_selected_language())

        # modify_slides_style.adjustSize()

        # place the window in the center of the app
        config_slides_window_width = modify_slides_style.frameGeometry().width()

        modify_slides_style.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(config_slides_window_width / 3.7, 100)  # type: ignore
        )

        self.mainwindow.setEnabled(False)
        modify_slides_style.exec()
        self.mainwindow.setEnabled(True)

    def _choose_folder(self) -> None:
        """
        Opens a dialog to choose the folder where the slides will be saved.
        """
        load_dotenv(
            os.path.join(os.getcwd(), "settings", ".env"),
            override=True,
            encoding="utf-8",
        )

        current_folder = os.getenv("SELECTED_FOLDER")

        if not current_folder:
            current_folder = os.path.join(os.getcwd(), "files")
            os.environ["SELECTED_FOLDER"] = current_folder

        selected_folder_ui = UiSelectedFolder(
            self.get_selected_language(), path=current_folder
        )

        # place the window in the center of the app
        simple_dialog_window_width = selected_folder_ui.frameGeometry().width()
        selected_folder_ui.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(simple_dialog_window_width / 3.7, 100)  # type: ignore
        )

        self.mainwindow.setEnabled(False)
        selected_folder_ui.exec()
        self.mainwindow.setEnabled(True)

    def _type_api_key(self) -> None:
        """
        Opens a dialog to type the API key.
        """
        load_dotenv(
            os.path.join(os.getcwd(), "settings", ".env"),
            override=True,
            encoding="utf-8",
        )

        current_api_key = os.getenv("GENIUS_API_KEY")

        genius_ui = UIGeniusKey(self.get_selected_language(), key=current_api_key)

        genius_ui.adjustSize()

        # place the window in the center of the app
        api_key_dialog_width = genius_ui.frameGeometry().width()
        genius_ui.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(api_key_dialog_width / 3.7, 100)  # type: ignore
        )

        self.mainwindow.setEnabled(False)
        genius_ui.exec()
        self.mainwindow.setEnabled(True)

    def _create_about_menu(self) -> None:
        """
        Creates the about menu.
        """
        # setup and creates the menubar
        self.about_menu = QMenu("Sobre", self)
        self.about_menu.setToolTipsVisible(True)
        self.about_menu.setStyleSheet(
            "QToolTip {background-color: dark; color: white;border: black solid 1px}"
        )

        self.addMenu(self.about_menu)

        # creates the "Repositório Git Hub" menu action
        self.about_menu_repository = self.about_menu.addAction("Repositório Git Hub")
        self.about_menu_repository.triggered.connect(self._open_git_hub_project)

        # creates the "Git Hub do Criador" menu action
        self.about_menu_creator = self.about_menu.addAction("Git Hub do Criador")
        self.about_menu_creator.triggered.connect(self._open_creator_git_hub)

        # creates the "Linkedin do Criador" menu action
        self.about_menu_creator_linkedin = self.about_menu.addAction(
            "Linkedin do Criador"
        )
        self.about_menu_creator_linkedin.triggered.connect(self._open_creator_linkedin)

    def _open_git_hub_project(self) -> None:
        """
        Opens the git hub project in the web browser.
        """
        webbrowser.open("https://github.com/VictorAp12/fazer-slides-de-musica")

    def _open_creator_git_hub(self) -> None:
        """
        Opens the git hub of the creator in the web browser.
        """
        webbrowser.open("https://github.com/VictorAp12")

    def _open_creator_linkedin(self) -> None:
        """
        Opens the linkedin of the creator in the web browser.
        """
        webbrowser.open("https://www.linkedin.com/in/victor-adriano-pereira")

    def _create_slide_style_menu(self) -> None:
        """
        Creates the slide style menu.
        """
        # setup and creates the "Selecionar Estilo de Slides" menu
        self.slide_style_menu = QMenu("Selecionar Estilo de Slides", self)
        self.slide_style_menu.setToolTipsVisible(True)
        self.slide_style_menu.setStyleSheet(
            "QToolTip {background-color: dark; color: white;border: black solid 1px}"
        )

        self.addMenu(self.slide_style_menu)

        # creates the styles
        self.slide_style_group = QActionGroup(self.slide_style_menu)
        for style in Path("app/slides styles").iterdir():
            active_style = self.slide_style_menu.addAction(style.name[:-5])
            active_style.setCheckable(True)
            self.slide_style_group.addAction(active_style)

        self.slide_style_group.actions()[0].setChecked(True)

    def get_selected_style(self) -> str:
        """
        Returns the selected style.

        :return (str): the selected style.
        """
        return self.slide_style_group.checkedAction().text()

    def _create_change_language_menu(self) -> None:
        """
        Creates the change language menu.
        """
        # setup and creates the "Selecionar Idioma" menu
        self.change_language_menu = QMenu("Selecionar Idioma", self)
        self.change_language_menu.setToolTipsVisible(True)
        self.change_language_menu.setStyleSheet(
            "QToolTip {background-color: dark; color: white;border: black solid 1px}"
        )

        self.addMenu(self.change_language_menu)

        # creates the languages
        self.language_group = QActionGroup(self.change_language_menu)

        self.portuguese_language = self.change_language_menu.addAction("Português")
        self.portuguese_language.triggered.connect(
            lambda: self.language_manager.change_to_language("pt")
        )
        self.portuguese_language.setCheckable(True)

        self.language_group.addAction(self.portuguese_language)

        self.english_language = self.change_language_menu.addAction("English")
        self.english_language.triggered.connect(
            lambda: self.language_manager.change_to_language("en")
        )
        self.english_language.setCheckable(True)

        self.language_group.addAction(self.english_language)

        self.language_group.actions()[0].setChecked(True)

    def get_selected_language(self) -> Literal["pt", "en"]:
        """
        Returns the selected style.

        :return (Literal ["pt", "en"]): the selected style.
        """
        return (
            "pt" if self.language_group.checkedAction().text() == "Português" else "en"
        )

    def retranslate_ui(self, language: Literal["pt", "en"] = "pt"):
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if language == "pt":

            self.menu.setTitle("Configurações")

            # config menu
            self.menu_create_slides_stiles.setText("Criar Novo Estilo de Slide")

            self.menu_create_slides_stiles.setToolTip(
                "Cria configuração personalizada para os slides criados com essa aplicação"
            )

            self.menu_modify_slides.setText("Modificar Slides Existentes")
            self.menu_modify_slides.setToolTip(
                "Somente modifica o slide que foi criado com essa aplicação"
            )

            self.menu_choose_folder.setText("Escolher Pasta de Destino")
            self.menu_choose_folder.setToolTip(
                "Seleciona a pasta de destino dos slides criados com essa aplicação"
            )

            self.menu_choose_api_key.setText("Digitar Chave de API")
            self.menu_choose_api_key.setToolTip(
                "Seleciona a chave de API para usar na busca de musicas"
            )

            # about menu
            self.about_menu.setTitle("Sobre")
            self.about_menu_repository.setText("Repositório Git Hub")
            self.about_menu_repository.setToolTip("Repositório do projeto no GitHub")

            self.about_menu_creator.setText("Git Hub do Criador")
            self.about_menu_creator.setToolTip(
                "Repositório do criador do projeto no GitHub"
            )

            self.about_menu_creator_linkedin.setText("Linkedin do Criador")
            self.about_menu_creator_linkedin.setToolTip(
                "Acesse o perfil do criador do projeto no Linkedin"
            )

            # change language
            self.change_language_menu.setTitle("Selecionar Idioma")

            # change slide style
            self.slide_style_menu.setTitle("Selecionar Estilo de Slides")
            for style in self.slide_style_group.actions():
                if style.text() == "black background":
                    style.setText("fundo preto")

                elif style.text() == "white background":
                    style.setText("fundo branco")

        else:

            self.menu.setTitle("Settings")

            # config menu
            self.menu_create_slides_stiles.setText("Create New Slide Style")

            self.menu_create_slides_stiles.setToolTip(
                "Creates custom configurations for slides created with this application"
            )

            self.menu_modify_slides.setText("Modify Existing Slides")
            self.menu_modify_slides.setToolTip(
                "Only modifies the slides that were created with this application"
            )

            self.menu_choose_folder.setText("Choose Destination Folder")
            self.menu_choose_folder.setToolTip(
                "Select the destination folder for slides created with this application"
            )

            self.menu_choose_api_key.setText("Type API Key")
            self.menu_choose_api_key.setToolTip(
                "Select the API key to use in the music search"
            )

            # about menu
            self.about_menu.setTitle("About")
            self.about_menu_repository.setText("Git Hub Repository")
            self.about_menu_repository.setToolTip("Repository of the project on GitHub")

            self.about_menu_creator.setText("Git Hub of the Creator")
            self.about_menu_creator.setToolTip(
                "Repository of the creator of the project on GitHub"
            )

            self.about_menu_creator_linkedin.setText("Linkedin of the Creator")
            self.about_menu_creator_linkedin.setToolTip(
                "Access the creator's profile on Linkedin"
            )

            # change language
            self.change_language_menu.setTitle("Select Language")

            # change slide style
            self.slide_style_menu.setTitle("Select Slide Style")
            for style in self.slide_style_group.actions():
                if style.text() == "fundo preto":
                    style.setText("black background")

                elif style.text() == "fundo branco":
                    style.setText("white background")
