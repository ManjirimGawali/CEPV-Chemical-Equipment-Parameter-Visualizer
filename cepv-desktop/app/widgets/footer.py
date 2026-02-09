from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt


class Footer(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(120)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }
            QLabel#title {
                font-size: 14px;
                font-weight: 600;
                color: #475569;
            }
            QLabel#subtitle {
                font-size: 11px;
                color: #94a3b8;
            }
            QLabel#copyright {
                font-size: 12px;
                font-weight: 600;
                color: #334155;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 16, 24, 12)
        root.setSpacing(8)

        # -------- Top Section --------
        top = QVBoxLayout()
        top.setAlignment(Qt.AlignCenter)

        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Data analytics & visualization for chemical equipment"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        top.addWidget(title)
        top.addWidget(subtitle)

        root.addLayout(top)

        # -------- Divider --------
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #cbd5e1;")
        root.addWidget(divider)

        # -------- Bottom Section --------
        bottom = QHBoxLayout()
        bottom.setAlignment(Qt.AlignCenter)

        credit = QLabel("Created by Manjiri Gawali (VIT Bhopal)")
        credit.setObjectName("copyright")
        credit.setAlignment(Qt.AlignCenter)

        bottom.addWidget(credit)
        root.addLayout(bottom)
