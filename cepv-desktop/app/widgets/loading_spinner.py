from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor


class LoadingSpinner(QWidget):
    def __init__(self, text="Loading..."):
        super().__init__()
        self.text = text
        self.dots = 0
        self.max_dots = 3
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        
        # Spinner dots
        self.spinner_label = QLabel()
        self.spinner_label.setAlignment(Qt.AlignCenter)
        self.spinner_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #0f172a;
                font-weight: 600;
            }
        """)
        self.spinner_label.setText("●")
        
        # Loading text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 14px;
            }
        """)
        
        layout.addWidget(self.spinner_label)
        layout.addWidget(self.text_label)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(150)  # Update every 150ms
        
    def animate(self):
        """Animate the spinner with rotating dots"""
        self.dots = (self.dots + 1) % (self.max_dots + 1)
        dots_text = "●" * self.dots + "○" * (self.max_dots - self.dots)
        self.spinner_label.setText(dots_text)
    
    def set_text(self, text):
        """Update the loading text"""
        self.text_label.setText(text)
    
    def stop(self):
        """Stop the animation"""
        self.timer.stop()
        self.hide()

