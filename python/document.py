import os
from odf.opendocument import load, OpenDocumentSpreadsheet
from odf.table import Table, TableCell, TableColumn, TableRow
from odf.text import P
from odf.style import ParagraphProperties, Style, TextProperties

class GhostDocument:
    def __init__(self, source: str) -> None:
        self.sheets = {}
        self.source = source
        self.metadata_available = False
        self.document = OpenDocumentSpreadsheet()
        self.table_styles = Style(
            parent=self.document.styles,
            name='Table Contents',
            family='paragraph'
        )
        ParagraphProperties(parent=self.table_styles, numberlines='true', linenumber='0')
        TextProperties(parent=self.table_styles, fontweight='bold')
        if (os.path.exists(source)):
            self.document = load(source)
            self.sync_sheets()
        else:
            self.setup_metadata()
            self.document.save(source)

    def sync_sheets(self):
        self.sheets = {}
        for sheet in self.document.spreadsheet.getElementsByType(Table):
            sheet_name = sheet.getAttribute('name')
            if not sheet_name.startswith('ghostdb_'):
                self.sheets[sheet.getAttribute('name')] = {
                    "sheet": sheet,
                    "cells": []
                }
            if sheet_name == 'ghostdb_metadata':
                self.metadata_available = True
        if not self.metadata_available:
            self.setup_metadata()

    def setup_metadata(self):
        self._write_dict({ "version": ["0.0.1"], "name": ["ghostdb"] }, 'ghostdb_metadata')
        self.metadata_available = True

    def _write_dict(self, data: dict, table_name: str):
        t = Table(parent=self.document.spreadsheet, name=table_name)
        headers = data.keys()
        header_row = TableRow(parent=t)
        max_row_index = 0
        for header in headers:
            TableColumn(parent=t)
            cell = TableCell(parent=header_row)
            max_row_index = max(max_row_index, len(data[header]))
            P(parent=cell, text=header, stylename=self.table_styles)

        for row_index in range(max_row_index):
            row = TableRow(parent=t)
            for key in data.keys():
                cell = TableCell(parent=row)
                P(parent=cell, text=data[key][row_index])
        self.document.save(self.source)

    def create_row(self, table_name: str, values: list):
        sheet = self.sheets[table_name]["sheet"]
        row = TableRow(parent=sheet)
        for value in values:
            cell = TableCell(parent=row)
            P(parent=cell, text=value)
        self.document.save(self.source)

    def has_table(self, table_name: str) -> bool:
        for sheet in self.document.spreadsheet.getElementsByType(Table):
            sheet_name = sheet.getAttribute('name')
            if sheet_name == table_name:
                return True
        return False

    def create_table(self, table_name: str, columns: list):
        data = {}
        for column in columns:
            data[column] = []
        self._write_dict(data, table_name)

    def close(self):
        pass
        
if __name__ == "__main__":
    con = GhostDocument("test.ods")
    con.create_table("peoples", ["id", "name", "age"])
    con.create_row("peoples", [1, "John Doe", 30])
    con.create_row("peoples", [2, "Jane Doe", 29])
    con.close()