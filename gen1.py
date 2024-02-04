import sys
from math import cos, sin, radians
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QApplication, QWidget

class AnalogWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analog Watch")
        self.setGeometry(300, 300, 400, 400)  # Window size adjusted for visibility

        # Update the display every second
        timer = QTimer(self)
        timer.timeout.connect(self.update)  # Triggers the paintEvent
        timer.start(1000)

    def paintEvent(self, event):
        static_roman_numerals = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
            7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
        }

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the clock face
        #painter.setPen(QPen(Qt.black, 2))
        #painter.drawEllipse(10, 10, 380, 380)

        # Center of the clock
        center = self.rect().center()
        radius = min(center.x(), center.y()) - 20

        # Draw Roman numerals
        painter.setFont(QFont('Times New Roman', 24))
        for hour, numeral in static_roman_numerals.items():
            angle = radians((hour / 12.0) * 360 - 90)
            x = center.x() + (radius - 40) * cos(angle) - painter.fontMetrics().boundingRect(numeral).width() / 2
            y = center.y() + (radius - 40) * sin(angle) + painter.fontMetrics().height() / 4
            painter.drawText(x, y, numeral)

        # Get current time
        currentTime = QTime.currentTime()
        hour = currentTime.hour() % 12
        minute = currentTime.minute()
        second = currentTime.second()

        # Calculate hand angles
        second_angle = (second / 60.0) * 360 - 90
        minute_angle = (minute / 60.0) * 360 - 90
        hour_angle = (hour / 12.0) * 360 + (minute / 2) - 90

        # Draw hour hand
        painter.setPen(QPen(Qt.darkGray, 8))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 0.5 * radius * cos(radians(hour_angle)),
                         center.y() + 0.5 * radius * sin(radians(hour_angle)))
    
        # Draw minute hand
        painter.setPen(QPen(Qt.gray, 6))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 0.6 * radius * cos(radians(minute_angle)),
                         center.y() + 0.6 * radius * sin(radians(minute_angle)))

        # Draw second hand
        painter.setPen(QPen(Qt.red, 4))
        painter.drawLine(center.x(), center.y(),
                         center.x() + 0.7 * radius * cos(radians(second_angle)),
                         center.y() + 0.7 * radius * sin(radians(second_angle)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    watch = AnalogWatch()
    watch.show()
    sys.exit(app.exec())
