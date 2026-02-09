from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QMessageBox,
    QHBoxLayout, QScrollArea
)
import os
import shutil

from app.widgets.footer import Footer
from app.widgets.navbar import Navbar
from app.widgets.stat_card import StatCard
from app.widgets.csv_preview import CSVPreview
from app.widgets.chart_widget import ChartWidget
from app.widgets.csv_format_example import CSVFormatExample
from app.services.api import upload_csv, download_pdf
from app.state import AppState
from app.utils.util import resource_path


class DashboardPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.file_path = None

        self.setStyleSheet("background: #f8fafc;")

        # -------- Scroll Wrapper --------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(32, 32, 32, 32)
        self.layout.setSpacing(32)

        scroll.setWidget(container)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

        # -------- Navbar --------
        self.layout.addWidget(Navbar(app,active="dashboard"))

        # -------- Header --------
        self.render_header()

        # -------- Upload --------
        self.layout.addWidget(self.upload_card())

        # -------- Summary --------
        if AppState.summary:
            self.layout.addWidget(self.summary_card())
            self.layout.addWidget(self.section_gap())

        # -------- Analytics --------
        if AppState.charts:
            self.layout.addWidget(self.analytics_card())
            self.layout.addWidget(self.section_gap())

        # -------- CSV Preview --------
        if AppState.preview:
            self.layout.addWidget(self.preview_card())

        
        self.layout.addStretch()

        self.layout.addWidget(Footer())

    # ================= HEADER ================= #

    def render_header(self):
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 36px; font-weight: 800;")

        subtitle = QLabel(
            "Upload a CSV file to analyze equipment data and generate reports"
        )
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

    def section_gap(self, px=36):
        gap = QWidget()
        gap.setFixedHeight(px)
        return gap

    # ================= UPLOAD CARD ================= #

    def upload_card(self):
        card = self.card()
        layout = QVBoxLayout(card)
        layout.setSpacing(20)

        title = QLabel("Upload CSV File")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Dataset Name *")
        self.name_input.setStyleSheet(self.input_style())
        layout.addWidget(self.name_input)

        self.file_label = QLabel("No file chosen")
        self.file_label.setStyleSheet("color: #64748b;")

        file_row = QHBoxLayout()
        choose_btn = QPushButton("Choose CSV File")
        choose_btn.setStyleSheet(self.secondary_btn())
        choose_btn.clicked.connect(self.select_file)

        file_row.addWidget(choose_btn)
        file_row.addWidget(self.file_label)
        file_row.addStretch()

        layout.addLayout(file_row)

        btn_row = QHBoxLayout()
        upload_btn = QPushButton("Upload & Analyze")
        upload_btn.setStyleSheet(self.primary_btn())
        upload_btn.clicked.connect(self.upload)

        sample_btn = QPushButton("Download Sample CSV")
        sample_btn.setStyleSheet(self.success_btn())
        sample_btn.clicked.connect(self.download_sample)

        btn_row.addWidget(upload_btn)
        btn_row.addWidget(sample_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        layout.addSpacing(24)
        layout.addWidget(CSVFormatExample())

        return card

    # ================= SUMMARY ================= #

    def summary_card(self):
        card = self.card()
        layout = QVBoxLayout(card)
        layout.setSpacing(20)

        header = QHBoxLayout()
        title = QLabel(f"Dataset Summary — {AppState.dataset_name}")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        pdf_btn = QPushButton("Download PDF")
        pdf_btn.setStyleSheet(self.primary_btn())
        pdf_btn.clicked.connect(self.download_pdf)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(pdf_btn)

        layout.addLayout(header)

        s = AppState.summary
        stats = QHBoxLayout()
        stats.setSpacing(16)

        stats.addWidget(StatCard("Total Equipment", s["total_equipment"]))
        stats.addWidget(StatCard("Avg Flowrate", round(s["average_flowrate"], 3)))
        stats.addWidget(StatCard("Avg Pressure", round(s["average_pressure"], 3)))
        stats.addWidget(StatCard("Avg Temperature", round(s["average_temperature"], 3)))

        layout.addLayout(stats)
        return card

    # ================= ANALYTICS ================= #

    def analytics_card(self):
        card = self.card()
        layout = QVBoxLayout(card)
        layout.setSpacing(18)

        title = QLabel("Analytics")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")

        subtitle = QLabel("Trends across uploaded dataset metrics")
        subtitle.setStyleSheet("color: #64748b; font-size: 13px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        chart_container = QWidget()
        chart_container.setMinimumHeight(420)
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(8, 8, 8, 8)
        chart_layout.addWidget(ChartWidget(AppState.charts))

        layout.addWidget(chart_container)

        return card

    # ================= CSV PREVIEW ================= #

    def preview_card(self):
        card = self.card()
        layout = QVBoxLayout(card)
        layout.setSpacing(16)

        title = QLabel("CSV Preview")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        subtitle = QLabel("First 10 rows from uploaded dataset")
        subtitle.setStyleSheet("color: #64748b; font-size: 12px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(CSVPreview(AppState.preview))

        return card

    # ================= ACTIONS ================= #

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file:
            self.file_path = file
            self.file_label.setText(os.path.basename(file))

    def upload(self):
        name = self.name_input.text().strip()

        if not self.file_path or not name:
            QMessageBox.warning(self, "Error", "File and dataset name required")
            return

        try:
            data = upload_csv(self.file_path, name)

            AppState.dataset_id = data["dataset_id"]
            AppState.dataset_name = data["dataset_name"]
            AppState.summary = data["summary"]
            AppState.preview = data["preview"]
            AppState.charts = data["charts"]

            QMessageBox.information(self, "Success", "Upload successful")
            self.app.show_dashboard()  # re-render

        except Exception as e:
            QMessageBox.critical(self, "Upload Failed", str(e))

    def download_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "report.pdf", "PDF Files (*.pdf)"
        )
        if path:
            download_pdf(AppState.dataset_id, path)

    def download_sample(self):
        """Download the sample CSV file from assets"""
        try:
            # Get the source CSV file path
            source_path = resource_path("app/assets/file.csv")
            
            if not os.path.exists(source_path):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Sample CSV file not found. Please contact support."
                )
                return
            
            # Open file dialog to choose save location
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Sample CSV",
                "sample_equipment_data.csv",
                "CSV Files (*.csv)"
            )
            
            if save_path:
                # Copy the file to the selected location
                shutil.copy2(source_path, save_path)
                QMessageBox.information(
                    self,
                    "Success",
                    f"Sample CSV file downloaded successfully!\nSaved to: {os.path.basename(save_path)}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to download sample CSV:\n{str(e)}"
            )

    # ================= STYLES ================= #

    def card(self):
        w = QWidget()
        w.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                padding: 22px;
            }
        """)
        return w

    def input_style(self):
        return """
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #cbd5e1;
                font-size: 14px;
            }
        """

    def primary_btn(self):
        return """
            QPushButton {
                background: #0f172a;
                color: white;
                padding: 12px 18px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background: #020617; }
        """

    def secondary_btn(self):
        return """
            QPushButton {
                background: #0f172a;
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
            }
        """

    def success_btn(self):
        return """
            QPushButton {
                background: #166534;
                color: white;
                padding: 12px 18px;
                border-radius: 8px;
                font-weight: 600;
            }
        """
