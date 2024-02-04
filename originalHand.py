import sys
from math import cos, sin, radians
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import QTimer, QTime, Qt


roman_numerals = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
    7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
}

class AnalogWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analog Watch")
        self.setGeometry(300, 300, 200, 200)  # Adjust size as needed
        self.resize(400, 400)  # Make the window bigger

        # Update the display every second
        timer = QTimer(self)
        timer.timeout.connect(self.update)  # Triggers the paintEvent
        timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw watch face
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(10, 10, 380, 380)  # Adjust for the window size

        # Get current time
        currentTime = QTime.currentTime()
        hour = currentTime.hour() if currentTime.hour() <= 12 else currentTime.hour() - 12
        minute = currentTime.minute()
        second = currentTime.second()

        # Calculate angles for each hand
        hour_angle = (hour + minute / 60.0) * 30 - 90  # 360 degrees / 12 hours
        minute_angle = (minute + second / 60.0) * 6 - 90  # 360 degrees / 60 minutes
        second_angle = second * 6 - 90  # 360 degrees / 60 seconds

        # Center of the watch face
        center = self.rect().center()

        # Draw hour hand
        painter.setPen(QPen(Qt.black, 8))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 50 * cos(radians(hour_angle)),
                         center.y() + 50 * sin(radians(hour_angle)))

        # Draw minute hand
        painter.setPen(QPen(Qt.black, 6))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 70 * cos(radians(minute_angle)),
                         center.y() + 70 * sin(radians(minute_angle)))

        # Draw second hand
        painter.setPen(QPen(Qt.red, 4))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 90 * cos(radians(second_angle)),
                         center.y() + 90 * sin(radians(second_angle)))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    watch = AnalogWatch()
    watch.show()
    sys.exit(app.exec())
