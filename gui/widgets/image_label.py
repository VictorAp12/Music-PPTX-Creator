"""
This module contains the code for the Imagelabel widget (which inherits from a QLabel).
"""

from io import BytesIO
from pathlib import Path

from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QMouseEvent,
    QPixmap,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
)


class ImageLabel(QLabel):
    """
    This class is used to create the image label.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            QLabel{
                border: 4px dashed #aaa;
            }
            QToolTip {background-color: dark; color: white;border: black solid 1px}
        """
        )

        self.setScaledContents(True)
        self.setMaximumSize(500, 300)

        self.img_path = None
        self.image_data = None

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        If the drag event contains an image, accept the event.

        :param event (QDragEnterEvent): the event.
        """
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        """
        If the drag event contains an image, accept the event.

        :param event (QDragMoveEvent): the event.
        """
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """
        If the drop event contains an image, set the image and accept the event.

        :param event (QDropEvent): the event.
        """
        if event.mimeData().hasImage:
            event.setDropAction(Qt.DropAction.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()

            self.img_path = Path(file_path)

        else:
            event.ignore()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        If the right mouse button is pressed, show the full screen image.

        :param event (QMouseEvent): the event.
        """
        if event.button() == Qt.MouseButton.RightButton:
            if not self.pixmap().isNull():
                self.show_fullscreen_image()
        else:
            self.open_file_dialog()

        return super().mousePressEvent(event)

    def set_image(self, file_path: str) -> None:
        """
        Sets the image of the label using the path.

        :param file_path (str): the path of the image.
        """
        self.setPixmap(QPixmap(file_path))

    def set_image_data(self, image_data: bytes | BytesIO) -> None:
        """
        Sets the image data of the label on a variable.
        """
        self.image_data = image_data

    def show_fullscreen_image(self) -> None:
        """
        Shows the full screen image of the label.
        """
        fullscreen_window = QDialog()
        layout = QVBoxLayout()

        label = QLabel()
        label.setPixmap(self.pixmap())
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(True)

        layout.addWidget(label)

        fullscreen_window.setLayout(layout)
        fullscreen_window.setWindowState(Qt.WindowState.WindowMaximized)
        fullscreen_window.setWindowTitle("Visualizando imagem em Tela Inteira")
        fullscreen_window.exec_()

    def open_file_dialog(self) -> None:
        """
        Opens a file dialog to select an image.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", filter="*.png *.jpg *.jpeg *gif"
        )

        if file_path:
            self.set_image(file_path)
            self.img_path = Path(file_path)
