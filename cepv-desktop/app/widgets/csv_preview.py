from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CSVPreview(QWidget):
    def __init__(self, rows):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------- Header ----------
        title = QLabel("CSV Preview")
        title.setStyleSheet("font-size:18px; font-weight:600;")

        subtitle = QLabel(
            f"Showing first {len(rows)} rows from uploaded dataset"
        )
        subtitle.setStyleSheet("color:#64748b; font-size:12px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------- Table ----------
        headers = list(rows[0].keys())

        table = QTableWidget(len(rows), len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Height & size policy
        table.setMinimumHeight(420)
        table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # ----- Header handling (MATCHES CSVFormatExample) -----
        h_header = table.horizontalHeader()
        v_header = table.verticalHeader()

        h_header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        h_header.setFixedHeight(100)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        h_header.setHighlightSections(False)

        header_font = QFont()
        header_font.setBold(True)
        h_header.setFont(header_font)

        # ----- Vertical header -----
        v_header.setVisible(False)
        v_header.setDefaultSectionSize(34)

        # ----- Table behavior -----
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setFocusPolicy(Qt.NoFocus)

        # ----- Populate data -----
        for r, row in enumerate(rows):
            for c, key in enumerate(headers):
                item = QTableWidgetItem(str(row[key]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                table.setItem(r, c, item)

        layout.addWidget(table)

        # ---------- Styling ----------
        self.setStyleSheet("""
            QHeaderView::section {
                background-color: #f1f5f9;
                padding-left: 8px;
                border: none;
            }
            QTableWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
            }
        """)
