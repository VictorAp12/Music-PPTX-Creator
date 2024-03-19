"""
This module contains the code for the TreeView class.
"""

from typing import List

from PySide6.QtWidgets import QTreeWidget, QWidget, QTreeWidgetItem, QHeaderView
from PySide6.QtCore import Qt


class TreeView(QTreeWidget):
    """
    This class is used to create the UI for the TreeView.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            QToolTip {background-color: dark; color: white; border: black solid 1px}
        """
        )
        self.setMaximumHeight(500)

        self._config_style()

        self.is_sorted_1 = True
        self.is_sorted_2 = True

    def add_headers(self, checked_header_name: str, list_headers: List[str]) -> None:
        """
        Adds the headers to the TreeView.

        :param list_headers (List[str]): the list of headers to add.
        """
        self.setColumnCount(len(list_headers) + 1)
        self.setHeaderLabels([f"{checked_header_name}"] + list_headers)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionsClickable(True)
        self.header().sectionClicked.connect(self.header_clicked)

    def add_values(self, list_values: List[List[str]] | List[str]):
        """
        Adds the values to the TreeView.

        :param list_values (List[List[str]], List[str]): the list of values to add.
        """
        if isinstance(list_values[0], list):
            for value in list_values:
                child_item = QTreeWidgetItem(self)
                child_item.setFlags(
                    child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable
                )
                child_item.setCheckState(0, Qt.CheckState.Checked)
                for i, item in enumerate(value):
                    child_item.setText(i + 1, item)

        elif isinstance(list_values[0], str):
            for value in list_values:
                child_item = QTreeWidgetItem(self)
                child_item.setFlags(
                    child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable
                )
                child_item.setCheckState(0, Qt.CheckState.Checked)
                child_item.setText(1, value)  # type: ignore

    def toggle_check_all(self, check: bool) -> None:
        """
        Toggles the check state of all items in the TreeView.

        :param check (bool): the check state to set.
        """
        check_state = Qt.CheckState.Checked if check else Qt.CheckState.Unchecked

        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).setCheckState(0, check_state)

    def header_clicked(self, index: int) -> None:
        """
        This method is called when the header is clicked.
        It sorts the TreeView and toggle the check state of all items
            if the header is the first one.

        :param index (int): the index of the header clicked.
        """
        if index == 0:

            try:
                self.toggle_check_all(
                    not self.topLevelItem(0).checkState(0) == Qt.CheckState.Checked
                )

            except AttributeError:
                pass

        elif index == 1:

            if self.is_sorted_1:
                self.sortByColumn(index, Qt.SortOrder.AscendingOrder)
                self.is_sorted_1 = False

            else:
                self.sortByColumn(index, Qt.SortOrder.DescendingOrder)
                self.is_sorted_1 = True

        elif index == 2:

            if self.is_sorted_2:
                self.sortByColumn(index, Qt.SortOrder.AscendingOrder)
                self.is_sorted_2 = False

            else:
                self.sortByColumn(index, Qt.SortOrder.DescendingOrder)
                self.is_sorted_2 = True

    def _config_style(self) -> None:
        """
        This method configures the style of the TreeView.
        """
        self.setStyleSheet(
            "QTreeView {margin-top: 4px; margin-bottom: 4px; border: 0px;}"
        )
