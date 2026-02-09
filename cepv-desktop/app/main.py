# app/main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from app.app_window import AppWindow
from app.utils.util import resource_path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env from project root (parent directory of app/)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env
    pass

def main():
    app = QApplication(sys.argv)
    
    # Set application icon
    try:
        icon_path = resource_path("app/assets/logo.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
    except Exception:
        # Icon is optional, don't crash if it fails
        pass
    
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
