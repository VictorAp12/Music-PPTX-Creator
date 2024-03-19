"""
This module contains the modify_image function.

The function modifies the opacity of a gived image.
"""

from io import BytesIO
from typing import Literal
from PIL import Image
from PySide6.QtWidgets import QLabel


def modify_image(
    imagem_background: bytes,
    transparencia_imagem_background: float,
    status_bar_label: QLabel | None = None,
    language: Literal["pt", "en"] = "pt",
) -> BytesIO:
    """
    Modifies the opacity of the image in the background.

    :param imagem_background (bytes): the image in bytes.
    :param transparencia_imagem_background (float): the opacity of the image.
    :param status_bar_label (QLabel): the status bar label.
    :param language (Literal["pt", "en"]): the language.
    """
    imagem_bg = Image.open(BytesIO(imagem_background))
    imagem_bg = imagem_bg.convert("RGBA")

    nivel_transparencia = int(transparencia_imagem_background * 255)

    if status_bar_label:
        status_bar_label.setText(
            "Alterando opacidade da imagem..."
            if language == "pt"
            else "Changing image opacity..."
        )

        if imagem_bg.width + imagem_bg.height > 2000:
            status_bar_label.setText(
                "Alterando opacidade da imagem... Isso pode demorar um pouco, \
                a imagem é muito grande"
                if language == "pt"
                else "Changing image opacity... It may take a while, \
                the image size is too big"
            )

    for y in range(imagem_bg.height):
        for x in range(imagem_bg.width):
            r, g, b, _ = imagem_bg.getpixel((x, y))
            imagem_bg.putpixel((x, y), (r, g, b, nivel_transparencia))

    imagem_transparente_bytes = BytesIO()
    imagem_bg.save(imagem_transparente_bytes, format="PNG")
    imagem_bg.close()
    imagem_transparente_bytes.seek(0)

    return imagem_transparente_bytes
