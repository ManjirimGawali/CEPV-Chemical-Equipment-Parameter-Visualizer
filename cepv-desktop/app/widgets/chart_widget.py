from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class ChartWidget(QWidget):
    def __init__(self, charts):
        super().__init__()

        layout = QVBoxLayout(self)

        fig = Figure(figsize=(6, 4))
        canvas = Canvas(fig)
        ax = fig.add_subplot(111)

        x = range(1, len(charts["flowrate"]) + 1)

        ax.plot(x, charts["flowrate"], label="Flowrate", linewidth=2)
        ax.plot(x, charts["pressure"], label="Pressure", linewidth=2)
        ax.plot(x, charts["temperature"], label="Temperature", linewidth=2)

        ax.set_xlabel("Record Index")
        ax.set_ylabel("Measured Value")
        ax.legend()
        ax.grid(True)

        layout.addWidget(canvas)
