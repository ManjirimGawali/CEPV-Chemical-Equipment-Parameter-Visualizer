from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from app.utils.util import resource_path

class Navbar(QWidget):
    def __init__(self, app, active="dashboard"):
        super().__init__()
        self.app = app
        self.active = active

        self.setFixedHeight(64)
        self.setStyleSheet(self.base_style())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 8, 24, 8)
        layout.setSpacing(16)

        # ---------- Logo + Brand ----------
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(10)

        logo = QLabel()
        logo.setFixedSize(38, 38)
        logo.setScaledContents(True)

        # Try to load logo, but don't crash if it doesn't exist
        try:
            logo_path = resource_path("app/assets/logo.ico")
            if os.path.exists(logo_path):
                logo.setPixmap(QPixmap(logo_path))
        except Exception:
            pass  # Logo is optional

        text_container = QWidget()
        text_box = QVBoxLayout(text_container)
        text_box.setContentsMargins(0, 0, 0, 0)
        text_box.setSpacing(0)

        title = QLabel("CEPV")
        title.setObjectName("brand")

        subtitle = QLabel("Chemical Equipment Visualizer")
        subtitle.setObjectName("subtitle")

        text_box.addWidget(title)
        text_box.addWidget(subtitle)

        brand_layout.addWidget(logo)
        brand_layout.addWidget(text_container)

        # ---------- Nav Buttons ----------
        self.dashboard_btn = QPushButton("Dashboard")
        self.history_btn = QPushButton("History")
        logout_btn = QPushButton("Logout")

        self.dashboard_btn.clicked.connect(self.app.show_dashboard)
        self.history_btn.clicked.connect(self.app.show_history)
        logout_btn.clicked.connect(self.logout)

        self.set_active_tab()

        layout.addLayout(brand_layout)
        layout.addStretch()
        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(logout_btn)

    # ---------------- Active Tab ----------------

    def set_active_tab(self):
        if self.active == "dashboard":
            self.dashboard_btn.setObjectName("active")
            self.history_btn.setObjectName("")
        elif self.active == "history":
            self.history_btn.setObjectName("active")
            self.dashboard_btn.setObjectName("")

        self.style().unpolish(self)
        self.style().polish(self)

    # ---------------- Logout ----------------

    def logout(self):
        from app.state import AppState
        AppState.clear()
        self.app.show_login()

    # ---------------- Styles ----------------

    def base_style(self):
        return """
        QWidget {
            background: white;
            border-bottom: 1px solid #e5e7eb;
        }

        QLabel#brand {
            color: #020617;
            font-size: 18px;
            font-weight: 800;
        }

        QLabel#subtitle {
            color: #64748b;
            font-size: 11px;
        }

        QPushButton {
            color: #334155;
            background: transparent;
            border: none;
            font-size: 14px;
            padding: 8px 14px;
            border-radius: 8px;
        }

        QPushButton:hover {
            background: #f1f5f9;
        }

        QPushButton#active {
            background: #0f172a;
            color: white;
            font-weight: 600;
        }

        QPushButton:last-child {
            background: #020617;
            color: white;
            font-weight: 600;
        }

        QPushButton:last-child:hover {
            background: #020617;
        }
        """
