from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatCard(QWidget):
    def __init__(self, label, value):
        super().__init__()
        layout = QVBoxLayout(self)

        l = QLabel(label)
        l.setStyleSheet("color: #666; font-size: 12px;")
        v = QLabel(str(value))
        v.setStyleSheet("font-size: 18px; font-weight: 600;")

        layout.addWidget(l)
        layout.addWidget(v)
