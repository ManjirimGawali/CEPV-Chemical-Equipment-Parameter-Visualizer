# app/pages/login.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox,
    QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from app.services.api import login
from app.state import AppState
from app.widgets.loading_spinner import LoadingSpinner


class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setStyleSheet("background:#f8fafc;")

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        # ---------- Card ----------
        card = QWidget()
        card.setFixedWidth(420)
        card.setStyleSheet(self.card_style())

        layout = QVBoxLayout(card)
        layout.setSpacing(16)

        # ---------- Header ----------
        title = QLabel("Sign in")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:700;")

        subtitle = QLabel("Welcome back. Please login to your account.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#64748b; font-size:13px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------- Inputs ----------
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet(self.input_style())

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.input_style())

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        # ---------- Buttons ----------
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet(self.primary_btn())
        self.login_btn.clicked.connect(self.handle_login)

        signup_btn = QPushButton("Create account")
        signup_btn.setStyleSheet(self.link_btn())
        signup_btn.clicked.connect(self.app.show_signup)

        layout.addWidget(self.login_btn)
        layout.addWidget(signup_btn)
        
        # ---------- Loading Spinner ----------
        self.loading_spinner = LoadingSpinner("Logging in...")
        self.loading_spinner.hide()
        layout.addWidget(self.loading_spinner)

        root.addWidget(card)
        
        # Login thread
        self.login_thread = None

    # ---------- Logic ----------
    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        # Disable login button and show loader
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        self.loading_spinner.show()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        
        # Start login in background thread
        self.login_thread = LoginThread(username, password)
        self.login_thread.login_success.connect(self.on_login_success)
        self.login_thread.login_error.connect(self.on_login_error)
        self.login_thread.start()
    
    def on_login_success(self, data):
        """Handle successful login"""
        AppState.set_token(data["token"])
        self.app.show_dashboard()
        self.reset_ui()
    
    def on_login_error(self, error_msg):
        """Handle login error"""
        QMessageBox.critical(self, "Login Failed", str(error_msg))
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI after login attempt"""
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Login")
        self.loading_spinner.hide()
        self.username.setEnabled(True)
        self.password.setEnabled(True)

    # ---------- Styles ----------
    def card_style(self):
        return """
            QWidget {
                background:white;
                border-radius:14px;
                padding:28px;
            }
        """

    def input_style(self):
        return """
            QLineEdit {
                padding:12px;
                border-radius:8px;
                border:1px solid #cbd5e1;
                font-size:14px;
            }
        """

    def primary_btn(self):
        return """
            QPushButton {
                background:#0f172a;
                color:white;
                padding:12px;
                border-radius:8px;
                font-weight:600;
            }
            QPushButton:hover { background:#020617; }
        """

    def link_btn(self):
        return """
            QPushButton {
                background:transparent;
                color:#0f172a;
                font-weight:600;
                border:none;
            }
        """


class LoginThread(QThread):
    """Background thread for login API call"""
    login_success = pyqtSignal(dict)
    login_error = pyqtSignal(str)
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
    
    def run(self):
        try:
            data = login(self.username, self.password)
            self.login_success.emit(data)
        except Exception as e:
            self.login_error.emit(str(e))
