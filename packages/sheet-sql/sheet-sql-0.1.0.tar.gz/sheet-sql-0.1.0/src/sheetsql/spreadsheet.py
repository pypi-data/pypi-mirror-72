"""Spreadsheet interface."""

from gspread import Client
from gspread import Spreadsheet as GSpreadSpreadsheet

from .worksheet import Worksheet  # type: ignore


class Spreadsheet(GSpreadSpreadsheet):
    """Class inheriting the gspread.Spreadsheet class to represent a spreadsheet."""

    def __init__(self, client: Client, properties: dict) -> None:
        """Init method for the Spreadsheet class."""
        super().__init__(client, properties)
        spreadsheet_metadata = self.fetch_sheet_metadata()
        self._worksheets = {
            worksheet["properties"]["title"]: Worksheet(self, worksheet["properties"])
            for worksheet in spreadsheet_metadata["sheets"]
        }

    def __len__(self) -> int:
        """Return number of worksheets."""
        return len(self._worksheets)

    @property
    def worksheets(self) -> list:
        """List the worksheets in the current spreadsheet."""
        return list(self._worksheets.keys())

    def __getitem__(self, worksheet_name: str) -> Worksheet:
        """Make worksheets subscriptable."""
        return self.get_worksheet(worksheet_name)

    def get_worksheet(self, worksheet_name: str) -> Worksheet:
        """Get specific worksheet by name."""
        return self._worksheets[worksheet_name]
