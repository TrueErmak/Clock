import sys
from math import cos, sin, radians
from PySide6.QtCore import QTimer, QTime, Qt, QRect
from PySide6.QtGui import QPainter, QPen, QPainterPath, QFont, QColor, QMovie
from PySide6.QtWidgets import QApplication, QWidget

class AnalogWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analog Watch")
        self.setGeometry(300, 300, 400, 400)  # Window size adjusted for visibility

        # Load the animated GIF background
        self.movie = QMovie('background.gif')
        self.movie.frameChanged.connect(self.repaint)  # Repaint on each frame change
        if self.movie.loopCount() != -1:
            # If the GIF has a finite number of loops, restart it when it finishes
            self.movie.finished.connect(self.movie.start)
        self.movie.start()  # Start the animation

        # Update the display every second
        timer = QTimer(self)
        timer.timeout.connect(self.update)  # Triggers the paintEvent
        timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the current frame of the background animation
        currentFrame = self.movie.currentPixmap()
        targetRect = QRect(0, 0, self.width(), self.height())
        sourceRect = currentFrame.rect()
        painter.drawPixmap(targetRect, currentFrame, sourceRect)

        static_roman_numerals = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
            7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
        }

        # Center of the clock and radius calculation
        center = self.rect().center()
        radius = min(center.x(), center.y()) * 0.9

        # Set the color for the Roman numerals
        painter.setPen(QColor("red"))  # Replace "your_color_here" with your desired color

        # Draw Roman numerals
        painter.setFont(QFont('Times New Roman', 24))
        for hour, numeral in static_roman_numerals.items():
            angle = radians((hour / 12.0) * 360 - 90)
            x = center.x() + (radius - 40) * cos(angle) - painter.fontMetrics().boundingRect(numeral).width() / 2
            y = center.y() + (radius - 40) * sin(angle) + painter.fontMetrics().height() / 4
            painter.drawText(x, y, numeral)

        # Get current time
        currentTime = QTime.currentTime()
        hour = currentTime.hour() % 12 + currentTime.minute() / 60.0
        hour_angle = (hour / 12.0) * 360 - 10 #90
        print(f"Current Time: {currentTime.toString()}")

        # Custom shape for the hour hand
        painter.save()  # Save the painter's current state
        painter.translate(center)  # Move the origin to the center of the clock
        painter.rotate(hour_angle)  # Rotate the painter to the hour angle

        hourHandPath = QPainterPath()
        hourHandPath.moveTo(-5, -10)  # Starting point at the base of the hand
        hourHandPath.lineTo(0, -radius * 0.5)  # Tip of the hand
        hourHandPath.lineTo(5, -10)  # Completing the triangular shape of the hand
        hourHandPath.closeSubpath()

        painter.setPen(QPen(Qt.green, 1))  # Set the pen for the hour hand outline
        painter.setBrush(Qt.green)  # Set the brush for filling the hour hand
        painter.drawPath(hourHandPath)  # Draw the custom shaped hour hand

        painter.restore()  # Restore the painter's state

        # Custom shape for the minute hand
        minute_angle = (currentTime.minute() / 60.0) * 360 - 10
        painter.save()
        painter.translate(center)
        painter.rotate(minute_angle)
        minuteHandPath = QPainterPath()
        minuteHandPath.moveTo(-5, -10)  # Adjust as per your design
        minuteHandPath.lineTo(0, -radius * 0.7)  # Length of the minute hand
        minuteHandPath.lineTo(5, -10)  # Completing the shape
        minuteHandPath.closeSubpath()
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setBrush(Qt.gray)
        painter.drawPath(minuteHandPath)
        painter.restore()

        # Custom shape for the second hand
        second_angle = (currentTime.second() / 60.0) * 360 - 0
        painter.save()
        painter.translate(center)
        painter.rotate(second_angle)
        secondHandPath = QPainterPath()
        secondHandPath.moveTo(-3, -10)  # Slimmer design for the second hand
        secondHandPath.lineTo(0, -radius * 0.8)  # Length of the second hand
        secondHandPath.lineTo(3, -10)  # Completing the shape
        secondHandPath.closeSubpath()
        painter.setPen(QPen(Qt.red, 1))  # Color of the second hand
        painter.setBrush(Qt.red)  # Color of the second hand
        painter.drawPath(secondHandPath)
        painter.restore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    watch = AnalogWatch()
    watch.show()
    sys.exit(app.exec_())