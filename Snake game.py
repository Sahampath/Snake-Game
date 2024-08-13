import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QKeyEvent, QBrush, QFont, QLinearGradient
from PyQt5.QtCore import QTimer, QRect, Qt
import random

class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Snake Game')
        self.setGeometry(100, 100, 620, 420)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.game_area = GameArea()
        self.layout.addWidget(self.game_area)

        self.show()

class GameArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)

        self.init_game()
        self.dark_mode = True
        self.set_dark_mode()

    def init_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.random_food()
        self.direction = Qt.Key_Right
        self.score = 0
        self.game_over = False

    def random_food(self):
        return (random.randint(0, 29) * 20, random.randint(0, 19) * 20)

    def keyPressEvent(self, event: QKeyEvent):
        if self.game_over:
            if event.key() == Qt.Key_R:
                self.init_game()
                self.game_over = False
            elif event.key() == Qt.Key_Q:
                QApplication.quit()
        else:
            if event.key() == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = Qt.Key_Up
            elif event.key() == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = Qt.Key_Down
            elif event.key() == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = Qt.Key_Left
            elif event.key() == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = Qt.Key_Right

    def update_game(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        if self.direction == Qt.Key_Up:
            head_y -= 20
        elif self.direction == Qt.Key_Down:
            head_y += 20
        elif self.direction == Qt.Key_Left:
            head_x -= 20
        elif self.direction == Qt.Key_Right:
            head_x += 20

        new_head = (head_x, head_y)
        if new_head in self.snake or head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 400:
            self.game_over = True
            self.update()
        else:
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.score += 1
                self.food = self.random_food()
            else:
                self.snake.pop()
            self.update()

    def set_dark_mode(self):
        if self.dark_mode:
            self.bg_color = QColor(30, 30, 30)
            self.snake_color = QColor(0, 255, 0)
            self.food_color = QColor(255, 0, 0)
            self.text_color = QColor(255, 255, 255)
        else:
            self.bg_color = QColor(255, 255, 255)
            self.snake_color = QColor(0, 0, 0)
            self.food_color = QColor(255, 0, 0)
            self.text_color = QColor(0, 0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setBrush(QBrush(self.bg_color))
        painter.drawRect(self.rect())
        
        border_color = QColor(0, 0, 0)
        border_width = 5
        painter.setPen(QColor(border_color))
        painter.drawRect(border_width // 2, border_width // 2, self.width() - border_width, self.height() - border_width)
        
        if self.game_over:
            font = QFont()
            font.setBold(True)
            font.setPointSize(20)
            painter.setFont(font)
            painter.setPen(self.text_color)
            message = f"Game Over!\nScore: {self.score}\nPress 'R' to Retry\nPress 'Q' to Quit"
            painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignCenter, message)
        else:
            painter.setBrush(QBrush(self.snake_color))
            for segment in self.snake:
                self.draw_3d_rect(painter, segment[0], segment[1], 20, 20)

            self.draw_3d_rect(painter, self.food[0], self.food[1], 20, 20, is_food=True)

            painter.setPen(self.text_color)
            painter.drawText(10, 20, f"Score: {self.score}")

    def draw_3d_rect(self, painter, x, y, width, height, is_food=False):
        gradient = QLinearGradient(x, y, x + width, y + height)
        if is_food:
            gradient.setColorAt(0.0, self.food_color.darker(150))
            gradient.setColorAt(1.0, self.food_color)
        else:
            gradient.setColorAt(0.0, self.snake_color.darker(150))
            gradient.setColorAt(1.0, self.snake_color)

        painter.setBrush(QBrush(gradient))
        painter.drawRect(QRect(x, y, width, height))

        shadow_color = QColor(0, 0, 0, 80)
        painter.setBrush(QBrush(shadow_color))
        painter.drawRect(QRect(x + 2, y + 2, width, height))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    sys.exit(app.exec_())
