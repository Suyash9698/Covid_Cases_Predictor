import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
import math


class AnimatedWheel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animated Wheel")
        self.setGeometry(100, 100, 400, 400)

        self.angle = 0  # Initial angle of rotation

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(20)  # Update every 20 milliseconds

    def update_angle(self):
        self.angle += 2  # Increment the rotation angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)  # Translate to the center of the widget
        painter.rotate(self.angle)  # Rotate the painter

        # Draw the wheel
        wheel_radius = 100
        wheel_width = 20
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.red)
        painter.drawEllipse(QPointF(0, 0), wheel_radius, wheel_radius)
        painter.setBrush(Qt.white)
        painter.drawEllipse(QPointF(0, 0), wheel_radius - wheel_width, wheel_radius - wheel_width)

        # Draw virus-like structures
        virus_radius = 5
        virus_count = 10
        virus_spacing = 20
        for i in range(virus_count):
            angle = i * (360 / virus_count)
            x = (wheel_radius - virus_spacing) * math.cos(angle * math.pi / 180)
            y = (wheel_radius - virus_spacing) * math.sin(angle * math.pi / 180)
            painter.setBrush(Qt.red)
            painter.drawEllipse(QPointF(x, y), virus_radius, virus_radius)

        painter.resetTransform()  # Reset painter transformation


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedWheel()
    window.show()
    sys.exit(app.exec_())
