"""
This module contains the search_music_lyric function.
It uses the lyricsgenius library to search for lyrics on Genius.
"""

import re
from typing import Literal, Tuple
import lyricsgenius

from PySide6.QtWidgets import QWidget, QMessageBox


def remove_square_brackets(text: str) -> str:
    """
    Removes square brackets from the text.

    :param text (str): The text to remove the square brackets from.

    :return: The text with the square brackets removed.
    """

    return re.sub(r"\[.*?\]\n", "", text)


def search_lyrics_on_genius(
    window: QWidget,
    music: str,
    singer: str,
    genius_key: str | None = None,
    language: Literal["pt", "en"] = "pt",
) -> Tuple[str, str, list[str], str] | None:
    """
    Searches for lyrics on Genius and returns the found music, singer, lyrics, and image.

    :param window: The QWidget window object.
    :param music: The name of the music to search for.
    :param singer: The name of the singer to search for.

    :raises: QtWidgets.QMessageBox if no lyrics are found or if there is an error while searching.

    :return found_music (str): The name of the found music.
    :return found_singer (str): The name of the found singer.
    :return found_lyrics (list[str]): The list of found lyrics.
    :return image (str): The URL of the found image, or None if no lyrics are found.
    """

    api_key = genius_key
    if not genius_key:
        api_key = "bxl6Q4NJ3YPaoo5xE7aBegmbEr4JLExbRyGvbcXO0Jh1JXf3Rno60Su9xkz6pPro"

    genius = lyricsgenius.Genius(api_key, timeout=10, sleep_time=1)

    try:
        search = genius.search(f"{music} {singer}")

        result = search["hits"][0]["result"]
        found_music = result["title"]
        found_singer = result["primary_artist"]["name"]
        image = result["song_art_image_thumbnail_url"]

    except IndexError:
        msg_box = QMessageBox()
        msg_box.setIcon(msg_box.Icon.Critical)
        msg_box.information(
            window,
            "Erro" if language == "pt" else "Error",
            (
                "Nenhuma letra encontrada!\nVerifique se digitou corretamente"
                if language == "pt"
                else "No lyrics found!\nCheck if you typed correctly"
            ),
        )
        return None

    if found_music != music or found_singer != singer:
        msg_box = QMessageBox()

        response = msg_box.question(
            window,
            "Divergência" if language == "pt" else "Divergence",
            (
                "O nome da música encontrada e o nome do cantor encontrado "
                "não correspondem com os digitados "
                "(houve um erro na sua digitação ou não há a letra no genius lyrics)."
                "\nO nome da música encontrada: "
                f"{found_music}\nO nome do cantor(a) encontrado: {found_singer}\n"
                "Deseja continuar?"
                if language == "pt"
                else "Found music and singer name do not match with the ones typed.\n"
                "(there was an error in your typing or the letter was not in the genius lyrics).\n"
                "\nFound music: "
                f"{found_music}\nFound singer: {found_singer}\n"
                "Do you want to continue?"
            ),
        )

        if response == QMessageBox.StandardButton.No:
            return None

    music_lyric = genius.lyrics(result["id"]).split("\n\n")  # type: ignore

    music_items = range(len(music_lyric))

    for i in music_items:
        if re.search(r"(you might also like|embed|\d{2}embed)", music_lyric[i].lower()):
            music_lyric[i] = re.sub(
                r"(you might also like|embed|\d{2}embed)",
                lambda x: "\n" if x.group() == "you might also like" else "",
                music_lyric[i].lower(),
            )

            try:
                if i < len(music_lyric):
                    result = music_lyric[i].split("\n\n")

                    bloc1 = result[0]

                    if len(result) > 1:
                        bloc2 = result[1]
                    else:
                        bloc2 = ""

                    music_lyric.remove(music_lyric[i])
                    music_lyric.insert(i, bloc1)

                    if bloc2:
                        music_lyric.insert(i + 1, bloc2)

            except Exception as exc:
                msg_box = QMessageBox()
                msg_box.setIcon(msg_box.Icon.Critical)
                msg_box.information(
                    window,
                    "Erro" if language == "pt" else "Error",
                    (
                        f"Erro na divisão dos blocos: {str(exc)}"
                        if language == "pt"
                        else f"Error in block division: {str(exc)}"
                    ),
                )

                return None

        # if its the first paragraph and it has a line break
        # and it has a number its a header of the song so it needs to be removed
        # before the line break
        if (
            i == 0
            and "\n" in music_lyric[i]
            and bool(re.search(r"\d", music_lyric[i])) is True
        ):
            music_lyric[i] = music_lyric[i].split("\n", 1)[1]

    for i, letra in enumerate(music_lyric):
        music_lyric[i] = remove_square_brackets(letra)

    # remove the [refrao] [1 verso] etc
    music_lyric = [linha for linha in music_lyric if not linha.startswith("[")]
    music_lyric = [linha for linha in music_lyric if not linha.endswith("]")]

    # the first item is a blank because its ignored on create_slides function
    music_lyric.insert(0, "")

    return found_music, found_singer, music_lyric, image
