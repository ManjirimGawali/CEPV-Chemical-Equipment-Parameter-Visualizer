# app/app_window.py
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
import os
from app.utils.util import resource_path

from app.pages.login import LoginPage
from app.pages.signup import SignupPage
from app.pages.dashboard import DashboardPage
from app.pages.history import HistoryPage


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CEPV Desktop")
        self.setMinimumSize(1100, 700)
        
        # Set window icon
        self.set_window_icon()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Static pages
        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)

        self.stack.addWidget(self.login_page)   # index 0
        self.stack.addWidget(self.signup_page)  # index 1

        self.dashboard_index = None
        self.history_index = None

        self.show_login()
    
    def set_window_icon(self):
        """Set the application window icon"""
        try:
            icon_path = resource_path("app/assets/logo.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            # Icon is optional, don't crash if it fails
            pass

    # ---------------- Navigation ---------------- #

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_page)

    def show_dashboard(self):
        self._remove_dynamic_pages()

        dashboard = DashboardPage(self)
        self.dashboard_index = self.stack.addWidget(dashboard)
        self.stack.setCurrentWidget(dashboard)

    def show_history(self):
        self._remove_dynamic_pages()

        history = HistoryPage(self)
        self.history_index = self.stack.addWidget(history)
        self.stack.setCurrentWidget(history)

    # ---------------- Cleanup ---------------- #

    def _remove_dynamic_pages(self):
        """
        Remove dashboard & history pages so they are recreated fresh.
        This mimics React re-render behavior.
        """
        for i in reversed(range(self.stack.count())):
            widget = self.stack.widget(i)
            if isinstance(widget, (DashboardPage, HistoryPage)):
                self.stack.removeWidget(widget)
                widget.deleteLater()
