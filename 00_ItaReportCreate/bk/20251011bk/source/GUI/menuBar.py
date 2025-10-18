import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy,
    QStackedWidget, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QFileDialog,
    QDialog, QCheckBox, QHeaderView, QStyledItemDelegate, QTextEdit,QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QImage, QFontMetrics
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QEvent
from datetime import datetime
from PyQt5.QtCore import QSize

class MenuBar(QWidget):
    def __init__(self, on_menu_clicked, highlight_idx=0):
        super().__init__()
        self.on_menu_clicked = on_menu_clicked
        self.highlight_idx = highlight_idx
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            border-top: 1px solid #ccc;
            border-right: 1px solid #ccc;
        """)
        self.init_ui()

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#204366"))
        super().paintEvent(event)

    def init_ui(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        menu_items = [
            "PGMパターン選択",
            "基本情報設定",
            "テストケース編集",
        ]
        for idx, text in enumerate(menu_items):
            label = QLabel(text)
            label.setFont(QFont("Meiryo", 11, QFont.Bold if idx == self.highlight_idx else QFont.Normal))
            if idx == self.highlight_idx:
                label.setStyleSheet("color: #00B0F0; padding: 0 0 0 20px; margin: -1px -1px 0px -1px;")
            else:
                label.setStyleSheet("color: white; padding: 0 0 0 24px; margin: -1px -1px 0px -1px;")
            label.setFixedHeight(48)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.mousePressEvent = lambda e, i=idx: self.on_menu_clicked(i)
            self.layout.addWidget(label)
        self.layout.addStretch()