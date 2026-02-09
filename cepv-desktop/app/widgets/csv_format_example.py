from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CSVFormatExample(QWidget):
    def __init__(self):
        super().__init__()

        headers = [
            "Equipment Name",
            "Type",
            "Flowrate",
            "Pressure",
            "Temperature",
        ]

        rows = [
            ["Pump-1", "Pump", 120, 5.2, 110],
            ["Compressor-1", "Compressor", 95, 8.4, 95],
            ["Valve-1", "Valve", 60, 4.1, 105],
            ["HeatExchanger-1", "HeatExchanger", 150, 6.2, 130],
            ["Pump-2", "Pump", 132, 5.6, 118],
            ["Reactor-1", "Reactor", 140, 7.5, 140],
        ]

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------- Header ----------
        title = QLabel("Expected CSV Format *")
        title.setStyleSheet(
            "color:#dc2626; font-size:16px; font-weight:600;"
        )

        subtitle = QLabel(
            "Your CSV file should follow this structure and column naming"
        )
        subtitle.setStyleSheet("color:#64748b; font-size:12px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------- Table ----------
        table = QTableWidget(len(rows), len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Fixed height (as requested)
        table.setMinimumHeight(420)
        table.setMaximumHeight(420)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # ----- Header handling (IMPORTANT) -----
        h_header = table.horizontalHeader()
        v_header = table.verticalHeader()

        h_header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        h_header.setFixedHeight(48)

        h_header.setSectionResizeMode(QHeaderView.Stretch)
        h_header.setHighlightSections(False)

        header_font = QFont()
        header_font.setBold(True)
        table.horizontalHeader().setFont(header_font)

        # ----- Vertical header -----
        v_header.setVisible(False)
        v_header.setDefaultSectionSize(36)

        # ----- Table behavior -----
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setFocusPolicy(Qt.NoFocus)

        # ----- Populate data -----
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                table.setItem(r, c, item)

        layout.addWidget(table)

        # ---------- Footer Notes ----------
        note = QLabel(
            "• Column names are case-insensitive\n"
            "• Numeric fields must contain valid numbers\n"
            "• Extra columns will be ignored"
        )
        note.setStyleSheet("color:#64748b; font-size:11px;")
        layout.addWidget(note)

        self.setStyleSheet(self.card_style())

    def card_style(self):
        return """
            QWidget {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 14px;
            }
            QHeaderView::section {
                background: #f1f5f9;
                padding-left: 8px;
                border: none;
            }
        """
