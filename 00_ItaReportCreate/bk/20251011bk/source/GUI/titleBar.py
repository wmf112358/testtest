from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.commonStyle import CommonStyle

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(44)
        self.setStyleSheet("background-color: #111;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.title = QLabel("　Ita仕様書自動作成")
        self.title.setFont(QFont("Meiryo", 12, QFont.Bold))
        self.title.setStyleSheet(CommonStyle.TITLE)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.title)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(spacer)
        btn_width = 48
        btn_height = 44
        self.btn_min = QPushButton("―")
        self.btn_min.setFixedSize(btn_width, btn_height)
        self.btn_min.setStyleSheet(self.btn_style())
        self.btn_min.setToolTip("最小化")
        self.btn_min.clicked.connect(self.on_min)
        layout.addWidget(self.btn_min)
        self.btn_max = QPushButton("□")
        self.btn_max.setFixedSize(btn_width, btn_height)
        self.btn_max.setStyleSheet(self.btn_style())
        self.btn_max.setToolTip("最大化")
        self.btn_max.clicked.connect(self.on_max)
        layout.addWidget(self.btn_max)
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(btn_width, btn_height)
        self.btn_close.setStyleSheet(self.btn_style(close=True))
        self.btn_close.setToolTip("閉じる")
        self.btn_close.clicked.connect(self.on_close)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)
        self.startPos = None

    def btn_style(self, close=False):
        if close:
            return CommonStyle.TITLE_BUTTON + """
                QPushButton:hover {background: #e81123; color: #fff;}
            """
        else:
            return CommonStyle.TITLE_BUTTON + """
                QPushButton:hover {background: #444; color: #fff;}
            """

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPos()
            self.clickPos = self.mapToParent(event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.startPos:
            delta = event.globalPos() - self.startPos
            self.parent.move(self.parent.pos() + delta)
            self.startPos = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        super().mouseReleaseEvent(event)

    def on_min(self):
        self.parent.showMinimized()

    def on_max(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_max.setText("□")
            self.btn_max.setToolTip("最大化")
        else:
            self.parent.showMaximized()
            self.btn_max.setText("❐")
            self.btn_max.setToolTip("回復")

    def on_close(self):
        self.parent.close()