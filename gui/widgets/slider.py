"""
This module contains the TransparencySlider class.
"""

from typing import TYPE_CHECKING, List, Literal
import io

from PIL import Image

from PySide6.QtWidgets import QSlider, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from utils.modify_image import modify_image


if TYPE_CHECKING:
    from gui.widgets.image_label import ImageLabel


class TransparencySlider(QSlider):
    """
    This class is used to create the transparency slider.
    """

    def __init__(self, label_with_image: "ImageLabel") -> None:
        """
        Creates the transparency slider.

        :param label_with_image (ImageLabel): the label with the image.
        """
        super().__init__()

        self.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
        """
        )

        self.label_with_image = label_with_image
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setTickInterval(10)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

    def update_tooltip(self, language: Literal["pt", "en"] = "pt") -> None:
        """
        Updates the tooltip of the slider with the current selected opacity.

        :param language (Literal["pt", "en"]): the language.
        """
        self.setToolTip(
            f"Opacidade selecionada: {self.value()}\n Role a barra para alterar"
            if language == "pt"
            else f"Opacity selected: {self.value()}\n Drag the slider to change"
        )

    def update_opacity(
        self,
        status_bar_label: QLabel | None = None,
        widgets_to_deactivate: List[QLabel] | None = None,
        language: Literal["pt", "en"] = "pt",
    ) -> None:
        """
        Updates the opacity of the image in the background.

        :param status_bar_label (QLabel): the status bar label.
        :param widgets_to_deactivate (List): List of widgets to disable during the process.
        :param language (Literal["pt", "en"]): the language.
        """
        opacity = self.value() / 100.0

        if self.label_with_image.img_path is None:
            return

        if widgets_to_deactivate:
            for widget in widgets_to_deactivate:
                widget.setDisabled(True)

        image = Image.open(self.label_with_image.img_path)

        buffer = io.BytesIO()

        image.save(buffer, format="PNG")

        image_bytes = buffer.getvalue()

        image_data = modify_image(image_bytes, opacity, status_bar_label, language)

        self.label_with_image.set_image_data(image_data)

        pixmap = QPixmap()

        pixmap.loadFromData(image_data.getvalue(), "PNG")
        self.label_with_image.setPixmap(pixmap)

        if status_bar_label:
            status_bar_label.setText(
                f"Opacidade da imagem alterada: {self.value()}%"
                if language == "pt"
                else f"Image opacity changed: {self.value()}%"
            )

        if widgets_to_deactivate:
            for widget in widgets_to_deactivate:
                widget.setEnabled(True)

        buffer.close()
