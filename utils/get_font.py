"""
This module contains the get_available_fonts_name function.
"""

from pptx.text.fonts import FontFiles


def get_available_fonts_name() -> list:
    """
    Retrieves the names of the available fonts.

    Returns:
        list: A list of strings containing the names of the available fonts.
    """
    available_fonts = FontFiles._installed_fonts()

    available_fonts_name = [font[0] for font, _ in available_fonts.items()]

    # remove duplicates transforming it in set and convert to set and back to list
    available_fonts_name = list(set(available_fonts_name))

    available_fonts_name.sort()

    return available_fonts_name
