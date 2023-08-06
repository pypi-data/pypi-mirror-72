"""Worksheet interface."""

from __future__ import annotations

import re
import string
from typing import Any, Dict, Generator, List, Tuple

import requests
from gspread import Worksheet as GSpreadWorksheet

from sheetsql import spreadsheet

from .exceptions import InvalidRowTypeException
from .utils import TQ_BASE_URL, handle_tq_response


class Worksheet(GSpreadWorksheet):
    """Class inheriting the gspread.Worksheet class to represent a worksheet."""

    def __init__(self, spreadsheet: spreadsheet.Spreadsheet, properties: dict) -> None:
        """Init method for Worksheet class."""
        super().__init__(spreadsheet, properties)
        self._default_row_type = dict

    @property
    def columns(self) -> list:
        """Get columns in the worksheet."""
        return self.row_values(1)

    @property
    def num_columns(self) -> int:
        """Get number of columns in the worksheet."""
        return len(self.columns)

    @property
    def default_row_type(self) -> Any[Dict, List, Tuple]:
        """Get default row type returned by query method if the row_type kwarg is not passed in."""
        return self._default_row_type

    @default_row_type.setter
    def default_row_type(
        self, row_type: Any[Dict, List, Tuple]
    ) -> Any[Dict, List, Tuple]:
        """Set default row type."""
        if not issubclass(row_type, (dict, list, tuple)):
            raise InvalidRowTypeException(
                f"{row_type} is an invalid row_type. "
                "Valid row_types must be subclasses of dict, list, or tuple"
            )
        self._default_row_type = row_type

    def query(
        self, tq: str, row_type: Any[Dict, List, Tuple] = None
    ) -> Generator[Any[Dict, List, Tuple], None, None]:
        """Query data in the current worksheet using Google's Table Query (tq) Language.

        See https://developers.google.com/chart/interactive/docs/querylanguage
        for more info
        """
        params = {
            "key": self.spreadsheet.id,
            "tq": self._update_tq_cols(tq),
            "gid": self.id,
        }
        response = requests.get(TQ_BASE_URL, params=params)
        result = handle_tq_response(response)
        return self._result_handler(result, row_type=row_type)

    @property
    def column_label_id_map(self) -> dict:
        """Get dictionary contaning a map of column label to column identifier."""
        return {col: string.ascii_uppercase[i] for i, col in enumerate(self.columns)}

    def _update_tq_cols(self, tq: str) -> str:
        """Replace column label with column identifier.

        This is needed for Google Sheet's table query syntax.
        """
        for k, v in self.column_label_id_map.items():
            tq = re.sub(rf"\b{k}\b", v, tq)
        return tq

    def _result_handler(
        self, result: dict, row_type: Any[Dict, List, Tuple]
    ) -> Generator[Any[Dict, List, Tuple], None, None]:
        """Handle results and convert to appropriate row_type."""
        if row_type is None:
            row_type = self.default_row_type
        if issubclass(row_type, dict):
            cols = [col["label"] for col in result["cols"]]
            return (
                row_type({col: cell["v"] for col, cell in zip(cols, row["c"])})
                for row in result["rows"]
            )
        else:
            return (
                row_type([cell["v"] for cell in row["c"]]) for row in result["rows"]
            )

    def all(self) -> Generator[Any[Dict, List, Tuple], None, None]:
        """Get generator that contains all rows in the spreadsheet."""
        return self.query("SELECT *")

    def count(self) -> int:
        """Get number of rows."""
        count = [row for row in self.query("SELECT COUNT(A)", row_type=list)][0]
        return count

    def __len__(self) -> int:
        """Make the worksheet callable with the len function."""
        return self.count()

    # def insert(self, row: list) -> None:
    #     """Insert a row to the worksheet."""
    #     num_values = len(row)
    #     if num_values != self.num_columns:
    #         raise Exception(
    #             f"Worksheet has {self.num_columns} columns, but row contains "
    #             f"{num_values} values."
    #         )
    #     self.append_row(row)

    # def insert_many(self, rows: List[list]) -> None:
    #     """Insert many rows to the worksheet."""
    #     num_rows = len(rows)
    #     for i, row in enumerate(rows):
    #         num_values = len(row)
    #         if num_values != self.num_columns:
    #             raise Exception(
    #                 f"Worksheet has {self.num_columns} columns, but row number {i + 1} "
    #                 f"contains {num_values} values."
    #             )
    #     self.append_rows(rows)
    #     print(f"Inserted {num_rows} rows")

    # def update(self) -> None:
    #     """One day..."""
    #     raise NotImplementedError

    # def delete(self) -> None:
    #     """One day..."""
    #     raise NotImplementedError

    # def distinct(self) -> None:
    #     """One day..."""
    #     raise NotImplementedError
