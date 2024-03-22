# Music PPTX Creator

Não entende inglês? [Clique aqui para ver esta página em português](https://github.com/VictorAp12/Music-PPTX-Creator/blob/main/readme.md)

"Music PPTX Creator" is an application that allows users to search for music songs typed by the user on the Genius website using the GeniusApi and convert them into PowerPoint presentations. The application is highly responsive and intuitive, with many tooltips (pop-ups that appear when you hover over an element for a short period of time) and various functions such as:

Customize the slides in any way you want by changing the styles;
Modify existing presentations made with this app;
Change the background image and adjust its transparency;
Change the destination folder for files;
Change the language;
Change the expired or unavailable Genius API key.

<h3 align="center">Music PPTX Creator</h3>

<div align="center">
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/ab401b3f-aa54-4f2d-a613-4c15aa246065" />
</div>

### O projeto tem 3 páginas:
-The first page searches for only one song;
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/2a076d16-4034-4eec-8be5-e1680c79beb0" width="500"/>

- The second page searches for multiple songs by search query or by a structured CSV file: [Example](https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/6cab8e9f-1557-40aa-861f-b222c625ee5e)
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/ec45a7c9-a748-48d9-a65b-f783ec6ba7e0" width="500"/>

- The third page does not perform the song search, as you will need to manually enter it afterwards, then create the PowerPoint presentation.
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/18a39ead-f7ea-4b4b-ad60-780835032883" width="500"/>

Content:
- [Requirements](#requirements)
- [Installation](#installation)
- [Reason](#reason)

## Requirements
- Python 3.11 ou acima.

## Installation

  - Download the project as a zip or using git clone https://github.com/VictorAp12/Music-PPTX-Creator.git

  - Create a virtual environment in the project folder:
    ```bash
    python -m venv venv
    ````

  - Activate the virtual environment in the project folder:
    ```bash
    venv\Scripts\activate
    ```

  - Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

  - Run the main.py:
    ```bash
    python -m main
    ```

## Reason
The goal of this project was to apply my knowledge of OOP (Object-Oriented Programming), PySide6 (library for user interface), python-pptx (for creating and modifying PowerPoint presentations), and the Genius API (for music searches). This is why the project has strong typing throughout and includes classes and methods.
The main focus was on the GUI part, as I am a back-end developer and needed to improve my front-end skills.
I also wanted to automate the process of creating dynamic PowerPoint presentations, which is why the project searches for user-chosen songs, each of which can have a different length, making the automation process quite challenging.
