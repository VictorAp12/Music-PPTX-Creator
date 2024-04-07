"""
This module contains the code for the pages widget.
including its pages and its functions.
"""

import csv
import json
from glob import glob
import os
import time
from threading import Thread
from typing import TYPE_CHECKING, Callable, List, Literal

from PySide6.QtCore import (
    QMetaObject,
    QCoreApplication,
    QObject,
    QPoint,
    Signal,
    QThread,
)
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QStackedWidget,
    QWidget,
    QFileDialog,
    QProgressDialog,
    QMessageBox,
    QHeaderView,
    QLabel,
    QPushButton,
)

from dotenv import load_dotenv

from app.create_pptx import create_slides, SlidesConfig
from app.search_music_lyric import search_lyrics_on_genius
from gui.pages.ui_page_insert_manually import PageInsertManually
from gui.pages.ui_page_many import PageMany
from gui.pages.ui_page_one import PageOne
from gui.widgets.slider import TransparencySlider
from language_manager import LanguageManager

if TYPE_CHECKING:
    from gui.widgets.menu_bar import MenuBar


class UiPagesWidget(object):
    """
    This class is used to create the pages widget.
    """

    def __init__(
        self,
        mainwindow: QMainWindow,
        language_manager: LanguageManager,
        pages_widget: QStackedWidget,
        menu_bar: "MenuBar",
    ) -> None:
        """
        Creates the pages widget.

        :param mainwindow (QMainWindow): the main window.
        :param language_manager (LanguageManager): the language manager instance.
        :param PagesWidget: the pages widget.
        :param menu_bar: the menu bar.
        """
        self.mainwindow = mainwindow

        self.worker = None
        self.worker_thread = None
        self.progress_dialog = None

        self.language_manager = language_manager
        self.language_manager.language_changed.connect(self.retranslate_ui)

        self.pages_widget = pages_widget
        if not self.pages_widget.objectName():
            self.pages_widget.setObjectName("PagesWidget")

        self.menu_bar = menu_bar

        # PAGE ONE
        # ///////////////////////////////////////////////////////////////////////////////////////
        self.page_one = PageOne(self.language_manager)

        self.pages_widget.addWidget(self.page_one)

        # set the transparency button function that will update the opacity
        # while blocking the confirm_button, background_image and set_transparency_button
        self.page_one.set_transparency_button.clicked.connect(
            lambda: self._update_opacity_threading(
                self.page_one.transparency_slider,
                self.page_one.statusbar_label,
                [
                    self.page_one.confirm_button,
                    self.page_one.background_image,
                    self.page_one.set_transparency_button,
                ],
            )
        )

        self.page_one.open_destiny_folder_button.clicked.connect(self._open_folder)

        self.page_one.confirm_button.clicked.connect(
            lambda: self._confirm(
                self.page_one.confirm_button,
                self.page_one,
                self.page_one.music_line_edit.text(),
                self.page_one.singer_line_edit.text(),
            )
        )

        # PAGE MANY
        # /////////////////////////////////////////////////////////////////////////////
        self.page_many = PageMany(self.language_manager)  # QWidget()

        self.pages_widget.addWidget(self.page_many)

        self.page_many.input_method_combobox.currentTextChanged.connect(
            lambda: self._input_method_changed(
                self.page_many.input_method_combobox.currentIndex()
            )
        )
        self.page_many.confirm_csv.clicked.connect(self._confirm_csv)

        # set the transparency button function that will update the opacity
        # while blocking the confirm_button, background_image and set_transparency_button
        self.page_many.set_transparency_button.clicked.connect(
            lambda: self._update_opacity_threading(
                self.page_many.transparency_slider,
                self.page_many.statusbar_label,
                [
                    self.page_many.confirm_button,
                    self.page_many.background_image,
                    self.page_many.set_transparency_button,
                ],
            )
        )

        self.page_many.open_destiny_folder_button.clicked.connect(self._open_folder)

        self.page_many.confirm_button.clicked.connect(self._confirm_page_many)

        # PAGE INSERT MANUALLY
        # //////////////////////////////////////////////////////////////////////////////////
        self.page_insert_manually = PageInsertManually(self.language_manager)

        self.pages_widget.addWidget(self.page_insert_manually)

        # set the transparency button function that will update the opacity
        # while blocking the confirm_button, background_image and set_transparency_button
        self.page_insert_manually.set_transparency_button.clicked.connect(
            lambda: self._update_opacity_threading(
                self.page_insert_manually.transparency_slider,
                self.page_insert_manually.statusbar_label,
                [
                    self.page_insert_manually.confirm_button,
                    self.page_insert_manually.background_image,
                    self.page_insert_manually.set_transparency_button,
                ],
            )
        )

        self.page_insert_manually.open_destiny_folder_button.clicked.connect(
            self._open_folder
        )

        self.page_insert_manually.confirm_button.clicked.connect(
            self._confirm_page_insert_manually
        )

        # END
        # //////////////////////////////////////////////////////////////////////////////////////////
        self.retranslate_ui()

        QMetaObject.connectSlotsByName(self.pages_widget)

    def retranslate_ui(self, language: Literal["pt", "en"] = "pt") -> None:
        """
        Changes the text of the buttons.
        This method is called when the language is changed.

        :param language (Literal["pt", "en"]): the language to use.
        """
        if language == "pt":

            self.pages_widget.setWindowTitle(
                QCoreApplication.translate("PagesWidget", "StackedWidget", None)
            )

        else:

            self.pages_widget.setWindowTitle(
                QCoreApplication.translate("PagesWidget", "StackedWidget", None)
            )

    # retranslateUi

    def _input_method_changed(self, index: int) -> None:
        """
        Changes the method selected by the user.

        :param index (int): the index of the method selected.
        """

        self.page_many.grid_layout.addWidget(self.page_many.treeview, 2, 0, 1, 2)
        self.page_many.grid_layout.addWidget(self.page_many.text_edit, 2, 0, 1, 2)
        self.page_many.grid_layout.addWidget(self.page_many.confirm_csv, 1, 1)

        if index == 0:
            self.page_many.treeview.setVisible(True)
            self.page_many.treeview.setEnabled(True)
            self.page_many.text_edit.setVisible(False)
            self.page_many.text_edit.setEnabled(False)
            self.page_many.confirm_csv.setVisible(True)

        else:
            self.page_many.treeview.setVisible(False)
            self.page_many.treeview.setEnabled(False)
            self.page_many.text_edit.setVisible(True)
            self.page_many.text_edit.setEnabled(True)
            self.page_many.confirm_csv.setVisible(False)

    def _confirm_csv(self) -> None:
        """
        Confirms the csv file.
        """

        if not self.page_many.input_method_combobox.currentIndex() == 0:
            return

        self.page_many.treeview.clear()

        csv_file = QFileDialog.getOpenFileName(
            self.page_many, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if csv_file[0]:
            with open(csv_file[0], "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                self.page_many.treeview.add_values(list(csv_reader))

            self.page_many.treeview.header().setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents
            )

        self._input_method_changed(0)

    def _update_opacity_threading(
        self,
        transparency_slider: TransparencySlider,
        status_bar_label: QLabel,
        widgets_to_deactivate: List[QWidget],
    ) -> None:
        """
        Updates the opacity of the image in the background.

        :param widgets_to_deactivate (List): List of widgets to disable during the process.
        """
        language = self.menu_bar.get_selected_language()

        self.modify_thread = Thread(
            target=transparency_slider.update_opacity,
            args=(status_bar_label, widgets_to_deactivate, language),
        )
        self.modify_thread.start()

    def _open_folder(self) -> None:
        """
        Opens the selected folder (the user has to select it in the settings of the app).
        """
        load_dotenv(os.path.join(os.getcwd(), "settings", ".env"))

        selected_folder = os.getenv("SELECTED_FOLDER")

        if not selected_folder:
            selected_folder = os.path.join(os.getcwd(), "files")

        os.startfile(selected_folder)

    def _confirm(
        self,
        button: QPushButton,
        active_page: PageOne | PageMany | PageInsertManually,
        music_search: str,
        singer_search: str,
        insert_manually_lyrics: List[str] | None = None,
    ) -> None:
        """
        Confirms all the operation.

        :param button (QPushButton): The button that was clicked.
        :param active_page (QWidget): The active page.
        :param music_search (str): The music to search and create the pptx.
        :param singer_search (str): The singer to search and create the pptx.
        :param insert_manually_lyrics (str | None): The lyrics to create the pptx directly.

        :raises: QMessageBox if music or singer field is empty.
        """

        language = self.menu_bar.get_selected_language()

        load_dotenv(os.path.join(os.getcwd(), "settings", ".env"))

        button.setEnabled(False)

        selected_folder = os.getenv("SELECTED_FOLDER")

        if not selected_folder:
            selected_folder = os.path.join(os.getcwd(), "files")

        genius_key = os.getenv("GENIUS_API_KEY")

        # check empty fields
        if not music_search and not singer_search:
            self._show_info_msg_box(
                active_page,
                (
                    "Preencha os campos de musica e cantor"
                    if language == "pt"
                    else "Fill in the music and singer fields"
                ),
                language,
            )

            button.setEnabled(True)
            return

        if not insert_manually_lyrics:
            active_page.statusbar_label.setText(
                "Buscando música..." if language == "pt" else "Searching music..."
            )
            QApplication.processEvents()

            result = search_lyrics_on_genius(
                active_page,
                music_search,
                singer_search,
                genius_key,
                language,
            )

            if not result:
                active_page.statusbar_label.setText(
                    "Nenhum resultado encontrado"
                    if language == "pt"
                    else "No results found"
                )
                button.setEnabled(True)

                return

            music, singer, lyrics, genius_image = result

            # update status bar
            active_page.statusbar_label.setText(
                f'Música "{music} - {singer}" encontrada, criando slide...'
                if language == "pt"
                else f'Music "{music} - {singer}" found, creating slide...'
            )
            QApplication.processEvents()

        else:
            music, singer, lyrics, genius_image = (
                music_search,
                singer_search,
                insert_manually_lyrics,
                "",
            )

        # getting the selected slide_config
        slide_config = self.get_slides_config(self.menu_bar.get_selected_style())

        background_image_bytes = None
        if active_page.background_image.img_path:
            background_image_bytes = active_page.background_image.image_data

        try:
            create_slides(
                widget=active_page.statusbar_label,
                music_title=music,
                music_singer=singer,
                music_lyric=lyrics,
                slides_config=SlidesConfig(**slide_config),
                FILES_FOLDER=selected_folder,
                method=active_page.objectName(),
                genius_image_link=genius_image,
                background_image=background_image_bytes,
                language=language,
            )
        except FileNotFoundError:

            self._show_error_msg_box(
                active_page,
                (
                    "Nome de arquivo inválido, mude o nome da música e cantor(a).\n"
                    'Tire os caracteres como /, , :, *, ?, ", <, >, |, and ~'
                    if language == "pt"
                    else "Invalid file name, change the music name and singer.\n"
                    'Remove characters like /, , :, *, ?, ", <, >, |, and ~'
                ),
                language,
            )

        button.setEnabled(True)

    def _confirm_page_many(self) -> None:
        """
        Confirms all the operation for page_many.
        """
        selected_method = self.page_many.input_method_combobox.currentIndex()

        musics, singers = [], []

        if selected_method == 0:
            for i in range(self.page_many.treeview.topLevelItemCount()):
                item = self.page_many.treeview.topLevelItem(i)
                if item.checkState(0) == Qt.CheckState.Checked:
                    musics.append(item.text(1).strip())
                    singers.append(item.text(2).strip())

        else:
            for line in self.page_many.text_edit.toPlainText().split("\n"):
                if line:
                    try:
                        singers.append(line.split(",")[1].strip())
                        musics.append(line.split(",")[0].strip())

                    except IndexError:
                        musics.append(line)
                        singers.append("")

        if len(musics) == 0:
            self._show_error_msg_box(
                self.page_many,
                "Nenhum item selecionado",
                self.menu_bar.get_selected_language(),
            )
            return

        self.setup_worker()

        if self.worker_thread and self.worker:
            self.worker_thread.started.connect(
                lambda: self.worker.run(  # type: ignore
                    musics,
                    singers,
                    self.progress_dialog,
                    self.menu_bar.get_selected_language(),
                )
            )

            self.worker_thread.start()

    def _confirm_page_insert_manually(self) -> None:
        """
        Confirms all the operation for page_insert_manually.
        """
        if self.page_insert_manually.text_edit.toPlainText() == "":
            self._show_error_msg_box(
                self.page_insert_manually,
                (
                    "Nenhum item selecionado"
                    if self.menu_bar.get_selected_language() == "pt"
                    else "No item selected"
                ),
                self.menu_bar.get_selected_language(),
            )
            return

        lyrics = self.page_insert_manually.text_edit.toPlainText().strip().split("\n\n")
        lyrics.insert(0, "")

        self._confirm(
            self.page_insert_manually.confirm_button,
            self.page_insert_manually,
            self.page_insert_manually.music_line_edit.text(),
            self.page_insert_manually.singer_line_edit.text(),
            lyrics,
        )

    def get_slides_config(self, choosed_slide_config: str) -> dict:
        """
        It chooses the slide configuration.

        :param choosed_slide_config (str): The name of the slide configuration file.

        :return: the slide configuration as a dict.
        """
        slide_config_folder = os.path.join(os.getcwd(), "app", "slides styles")
        slides_config = glob(os.path.join(slide_config_folder, "*.json"))

        # get the full path of the selected slide config
        choosed_slide_config = os.path.join(
            slide_config_folder, choosed_slide_config + ".json"
        )

        if choosed_slide_config not in slides_config:
            if choosed_slide_config.endswith("white background.json"):
                choosed_slide_config = choosed_slide_config.replace(
                    "white background.json", "fundo branco.json"
                )

            elif choosed_slide_config.endswith("black background.json"):
                choosed_slide_config = choosed_slide_config.replace(
                    "black background.json", "fundo preto.json"
                )

            else:
                choosed_slide_config = slides_config[0]

        with open(
            choosed_slide_config,
            "r",
            encoding="utf-8",
        ) as config:
            configuration = json.load(config)

        return configuration

    def _show_info_msg_box(
        self, active_page: QWidget, text: str = "", language: Literal["pt", "en"] = "pt"
    ) -> None:
        """
        Shows an info message box.

        :param active_page (QWidget): The active page (will be disabled during the message box).
        :param text (str, optional): The text of the message box. Defaults to "".
        :param language (Literal["pt", "en"], optional): The language of the message box.
            Defaults to "pt".
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Atenção" if language == "pt" else "Attention")
        msg_box.setText(text)
        msg_box.setIcon(msg_box.Icon.Information)

        msg_box_width = msg_box.frameGeometry().width()
        msg_box.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(msg_box_width / 3.7, 100)  # type: ignore
        )
        active_page.setEnabled(False)
        msg_box.exec()
        active_page.setEnabled(True)

    def _show_error_msg_box(
        self, active_page: QWidget, text: str = "", language: Literal["pt", "en"] = "pt"
    ) -> None:
        """
        Shows an error message box.

        :param active_page (QWidget): The active page (will be disabled during the message box).
        :param text (str, optional): The text of the message box. Defaults to "".
        :param language (Literal["pt", "en"], optional): The language of the message box.
            Defaults to "pt".
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro" if language == "pt" else "Error")
        msg_box.setText(text)
        msg_box.Icon(msg_box.Icon.Critical)

        msg_box_width = msg_box.frameGeometry().width()
        msg_box.move(
            self.mainwindow.frameGeometry().center()
            - QPoint(msg_box_width / 3.7, 100)  # type: ignore
        )
        active_page.setEnabled(False)
        msg_box.exec()
        active_page.setEnabled(True)

    def setup_worker(self) -> None:
        """
        Sets up the worker to update the progress bar for page many.
        """
        self.worker = WorkerPageMany(
            self._confirm, self.page_many.confirm_button, self.page_many
        )
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)

        self.worker.finished.connect(self.on_thread_finished)

        self.progress_dialog = QProgressDialog(
            (
                "Progresso"
                if self.menu_bar.get_selected_language() == "pt"
                else "Progress"
            ),
            "Cancelar" if self.menu_bar.get_selected_language() == "pt" else "Cancel",
            0,
            100,
            self.mainwindow,
        )

        self.progress_dialog.setWindowTitle(
            "Fazendo os slides..."
            if self.menu_bar.get_selected_language() == "pt"
            else "Making the slides..."
        )

        self.progress_dialog.setValue(0)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setAutoClose(False)

        self.worker.progress_signal.connect(self.progress_dialog.setValue)

        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.show()

    def on_thread_finished(self) -> None:
        """
        Called when the thread is finished.
        """

        if self.worker_thread and self.progress_dialog:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.progress_dialog.close()


class WorkerPageMany(QObject):
    """Worker class for page many."""

    progress_signal = Signal(int)
    finished = Signal()

    def __init__(
        self,
        confirm_function: Callable,
        confirm_button: QPushButton,
        active_page: QWidget,
    ) -> None:
        """
        Constructor of the worker class.

        :param confirm_function (Callable): The function executed when confirm button is clicked.
        :param confirm_button (QPushButton): The confirm button.
        :param active_page (QWidget): The active page.
        """
        super().__init__()

        self.confirm_function = confirm_function
        self.confirm_button = confirm_button
        self.active_page = active_page

    def run(
        self,
        musics: List[str],
        singers: List[str],
        progress_dialog: QProgressDialog | None = None,
        language: Literal["pt", "en"] = "pt",
    ) -> None:
        """
        Runs the worker, which will update the progress bar in a separate thread.
        Executes the confirm function for each music in the list.

        :param musics (List[str]): The list of music names.
        :param singers (List[str]): The list of singer names.
        :param progress_dialog (QProgressDialog, optional): The progress dialog.
        :param language (Literal["pt", "en"], optional): The language. Defaults to "pt".
        """

        if self.canceled(progress_dialog, language):
            return

        for i, music in enumerate(musics):

            if self.canceled(progress_dialog, language):
                break

            self.confirm_function(
                self.confirm_button, self.active_page, music, singers[i]
            )

            if self.canceled(progress_dialog, language):
                break

            current_percentage = (i + 1) * 100 // len(musics)

            self.progress_signal.emit(current_percentage)

        time.sleep(1)

        self.finished.emit()

    def canceled(
        self,
        progress_dialog: QProgressDialog | None = None,
        language: Literal["pt", "en"] = "pt",
    ) -> bool:
        """
        Called when the thread is canceled.

        :param progress_dialog (QProgressDialog, optional): The progress dialog.
        :param language (Literal["pt", "en"], optional): The language. Defaults to "pt".

        :return (bool): True if the thread was canceled, False otherwise.
        """
        time.sleep(1)

        QApplication.processEvents()

        if progress_dialog:
            if progress_dialog.wasCanceled():
                QMessageBox.warning(
                    self.active_page,
                    "Atenção" if language == "pt" else "Attention",
                    (
                        "A operação foi cancelada."
                        if language == "pt"
                        else "The operation was canceled."
                    ),
                )
                return True
        return False
