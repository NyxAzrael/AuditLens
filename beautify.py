from PyQt5.QtWidgets import qApp
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QPixmap, QColor, QIcon, QPainter
from PyQt5.QtCore import Qt

def create_colored_icon(color: QColor) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, 16, 16)
    painter.end()
    return QIcon(pixmap)

def apply_global_styles():
    qApp.setStyleSheet("""
        QWidget {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 14px;
        }
        QPushButton {
            background-color: #f5f5f7;
            border-radius: 8px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QComboBox, QLineEdit, QTextEdit {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 4px;
            background-color: #fff;
        }
        QTableWidget {
            border: none;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            padding: 6px;
            border: none;
            font-weight: bold;
        }
    """)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#ffffff"))
    qApp.setPalette(palette)


def show_with_fade(dialog):
    animation = QPropertyAnimation(dialog, b"windowOpacity")
    animation.setDuration(300)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    dialog.setWindowOpacity(0.0)
    animation.start()
    dialog.show()
    dialog.animation = animation  # 防止GC清除动画
