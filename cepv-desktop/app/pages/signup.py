# app/pages/signup.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from app.services.api import signup
from app.widgets.loading_spinner import LoadingSpinner


class SignupPage(QWidget):
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
        title = QLabel("Create account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:700;")

        subtitle = QLabel("Join us and start analyzing your data")
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

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm password")
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setStyleSheet(self.input_style())

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm)

        # ---------- Buttons ----------
        self.signup_btn = QPushButton("Create account")
        self.signup_btn.setStyleSheet(self.primary_btn())
        self.signup_btn.clicked.connect(self.handle_signup)

        back_btn = QPushButton("Back to login")
        back_btn.setStyleSheet(self.link_btn())
        back_btn.clicked.connect(self.app.show_login)

        layout.addWidget(self.signup_btn)
        layout.addWidget(back_btn)
        
        # ---------- Loading Spinner ----------
        self.loading_spinner = LoadingSpinner("Creating account...")
        self.loading_spinner.hide()
        layout.addWidget(self.loading_spinner)

        root.addWidget(card)
        
        # Signup thread
        self.signup_thread = None

    # ---------- Logic ----------
    def handle_signup(self):
        if self.password.text() != self.confirm.text():
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter all fields")
            return

        # Disable signup button and show loader
        self.signup_btn.setEnabled(False)
        self.signup_btn.setText("Creating account...")
        self.loading_spinner.show()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.confirm.setEnabled(False)
        
        # Start signup in background thread
        self.signup_thread = SignupThread(username, password)
        self.signup_thread.signup_success.connect(self.on_signup_success)
        self.signup_thread.signup_error.connect(self.on_signup_error)
        self.signup_thread.start()
    
    def on_signup_success(self):
        """Handle successful signup"""
        QMessageBox.information(self, "Success", "Account created successfully")
        self.app.show_login()
        self.reset_ui()
    
    def on_signup_error(self, error_msg):
        """Handle signup error"""
        QMessageBox.critical(self, "Signup Failed", str(error_msg))
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI after signup attempt"""
        self.signup_btn.setEnabled(True)
        self.signup_btn.setText("Create account")
        self.loading_spinner.hide()
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.confirm.setEnabled(True)

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


class SignupThread(QThread):
    """Background thread for signup API call"""
    signup_success = pyqtSignal()
    signup_error = pyqtSignal(str)
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
    
    def run(self):
        try:
            signup(self.username, self.password)
            self.signup_success.emit()
        except Exception as e:
            self.signup_error.emit(str(e))
