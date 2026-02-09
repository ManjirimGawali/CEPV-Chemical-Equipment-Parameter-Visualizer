# app/pages/history.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QHBoxLayout, QMessageBox, QFileDialog
)



from app.widgets.footer import Footer
# from PyQt5.QtCore import Qt
from app.widgets.csv_preview import CSVPreview
from app.widgets.navbar import Navbar
from app.widgets.stat_card import StatCard
from app.widgets.chart_widget import ChartWidget
from app.services.api import get_history, analyze_dataset, download_pdf
from app.state import AppState

class HistoryPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setStyleSheet("background: #f8fafc;")

        # ---------- Scroll Wrapper ----------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)  # Remove border/frame
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 24, 24, 24)
        # self.layout.setSpacing(24)

        scroll.setWidget(container)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)  # Remove margins to eliminate border
        root.addWidget(scroll)

        # ---------- Navbar ----------
        self.layout.addWidget(Navbar(app, active="history"))

        # ---------- Header ----------
        self.render_header()

        # ---------- History List ----------
        self.history_card = self.card()
        self.history_layout = QVBoxLayout(self.history_card)
        self.history_layout.setSpacing(14)

        self.layout.addWidget(self.history_card)

        # ---------- Analysis Section ----------
        self.analysis_card = self.card()
        self.analysis_layout = QVBoxLayout(self.analysis_card)
        self.analysis_layout.setSpacing(16)

        self.layout.addWidget(self.analysis_card)
        self.analysis_card.hide()  # hidden until Analyze

        self.load_history()
        self.layout.addStretch()
        
        # after all content
        self.layout.addStretch()
        self.layout.addWidget(Footer())

    # ================= HEADER ================= #

    def render_header(self):
        title = QLabel("Upload History")
        title.setStyleSheet("font-size: 32px; font-weight: 800;")

        subtitle = QLabel("Previously uploaded datasets and analysis")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

    # ================= HISTORY LIST ================= #

    def load_history(self):
        try:
            datasets = get_history()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.history_layout.addWidget(
            QLabel("Recent Datasets")
        )

        for d in datasets:
            self.history_layout.addWidget(self.history_row(d))

    def history_row(self, dataset):
        row_card = QWidget()
        row_card.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                padding: 12px;
            }
        """)

        row = QHBoxLayout(row_card)

        label = QLabel(f"{dataset['name']}  •  {dataset['filename']}")
        label.setStyleSheet("font-size: 14px; font-weight: 500;")

        analyze_btn = QPushButton("Analyze")
        analyze_btn.setStyleSheet(self.primary_btn())
        analyze_btn.clicked.connect(
            lambda _, id=dataset["id"]: self.analyze(id)
        )

        pdf_btn = QPushButton("Download PDF")
        pdf_btn.setStyleSheet(self.secondary_btn())
        pdf_btn.clicked.connect(
            lambda _, id=dataset["id"]: self.save_pdf(id)
        )

        row.addWidget(label)
        row.addStretch()
        row.addWidget(analyze_btn)
        row.addWidget(pdf_btn)

        return row_card

    # ================= ANALYSIS ================= #

    def analyze(self, dataset_id):
        self.clear_analysis()

        try:
            data = analyze_dataset(dataset_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        summary = data["summary"]
        charts = data["charts"]

        # ---- Title ----
        title = QLabel("Dataset Analysis")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        self.analysis_layout.addWidget(title)

        # ---- Summary Cards ----
        stats = QHBoxLayout()
        stats.addWidget(StatCard("Total Equipment", summary["total_equipment"]))
        stats.addWidget(StatCard("Avg Flowrate", round(summary["average_flowrate"], 3)))
        stats.addWidget(StatCard("Avg Pressure", round(summary["average_pressure"], 3)))
        stats.addWidget(StatCard("Avg Temperature", round(summary["average_temperature"], 3)))

        self.analysis_layout.addLayout(stats)

        # ---- Analytics ----
        analytics_title = QLabel("Analytics")
        analytics_title.setStyleSheet("font-size: 18px; font-weight: 600;")
        self.analysis_layout.addWidget(analytics_title)

        chart = ChartWidget(charts)
        chart.setMinimumHeight(420)  # 👈 prevents cramped charts
        self.analysis_layout.addWidget(chart)

        self.analysis_card.show()

        # Auto-scroll down to analysis
        self.analysis_card.scrollTo = True

         # ---- Cache in AppState ----
        AppState.last_analyzed_id = dataset_id
        AppState.last_analyzed_summary = data["summary"]
        AppState.last_analyzed_charts = data["charts"]
        AppState.last_analyzed_preview = data["preview"]

        self.render_analysis(
            data["summary"],
            data["charts"],
            data["preview"]
        )

    def restore_cached_analysis(self):
        if AppState.last_analyzed_summary:
            self.render_analysis(
                AppState.last_analyzed_summary,
                AppState.last_analyzed_charts,
                AppState.last_analyzed_preview
            )

    def render_analysis(self, summary, charts, preview):
        header = QHBoxLayout()

        # title = QLabel("Dataset Analysis")
        # title.setStyleSheet("font-size:20px; font-weight:700;")

        # clear_btn = QPushButton("Clear Analysis")
        # clear_btn.clicked.connect(self.clear_analysis)

        # header.addWidget(title)
        # header.addStretch()
        # header.addWidget(clear_btn)

        self.analysis_layout.addLayout(header)

        # ---- Stats ----
        stats = QHBoxLayout()
        stats.addWidget(StatCard("Total Equipment", summary["total_equipment"]))
        stats.addWidget(StatCard("Avg Flowrate", round(summary["average_flowrate"], 3)))
        stats.addWidget(StatCard("Avg Pressure", round(summary["average_pressure"], 3)))
        stats.addWidget(StatCard("Avg Temperature", round(summary["average_temperature"], 3)))
        # self.analysis_layout.addLayout(stats)

        # ---- Charts ----
        # self.analysis_layout.addWidget(ChartWidget(charts))

        # ---- CSV Preview (NEW) ----
        self.analysis_layout.addWidget(CSVPreview(preview))    

    # ================= PDF ================= #

    def save_pdf(self, dataset_id):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "dataset_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            download_pdf(dataset_id, file_path)
            QMessageBox.information(self, "Success", "PDF downloaded successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ================= UTILS ================= #

    def clear_analysis(self):
        while self.analysis_layout.count():
            child = self.analysis_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # ================= STYLES ================= #

    def card(self):
        w = QWidget()
        w.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 14px;
                padding: 18px;
            }
        """)
        return w

    def primary_btn(self):
        return """
            QPushButton {
                background: #0f172a;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background: #020617; }
        """

    def secondary_btn(self):
        return """
            QPushButton {
                background: #e2e8f0;
                color: #0f172a;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: 500;
            }
        """
