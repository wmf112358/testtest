import sys
from getInfo import CobolSelector, FileCopyFinder

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QCheckBox, QFrame, QPushButton
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class MatchWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFont(QFont("Meiryo", 60))
        self.setWindowTitle("ITa仕様書作成")
        self.setGeometry(300, 100, 700, 400)
        self.init_ui()

    def init_ui(self):
        # 主布局
        layout = QVBoxLayout()
        #layout.setSpacing(2)  # 控件之间的间距缩小为2像素
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e6f2ff"))
        self.setPalette(palette)

        # 标题
        title = QLabel("MAES5100 ― マッチング 1：1")
        title.setFont(QFont("Meiryo", 12, QFont.Bold))
        title.setStyleSheet("color: #003366; margin: 10px 0;")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        # 说明
        desc = QLabel("下記条件を満たす場合、出力対象を選択してください。")
        desc.setFont(QFont("Meiryo", 11))
        desc.setStyleSheet("color: #333; padding-left: 32px;")
        layout.addWidget(desc, alignment=Qt.AlignLeft)

        # 条件列表
        conditions = [
            ("HAEW21RのKEY　＞　HAEW24RのKEY",),
            ("HAEW21RのKEY　＜　HAEW24RのKEY",),
            ("HAEW21RのKEY　＝　HAEW24RのKEY",)
        ]

        for cond in conditions:
            group = QGroupBox()
            group.setStyleSheet("QGroupBox { border: 1px solid #99ccff; background: #f7fbff; margin-top: 8px; }")
            vbox = QVBoxLayout()
            # 条件表达式
            cond_label = QLabel(f"・ {cond[0]}")
            cond_label.setFont(QFont("Meiryo", 11))
            vbox.addWidget(cond_label)
            # 选择区
            hbox = QHBoxLayout()
            hbox.setContentsMargins(32, 0, 0, 0)  # 整体向右移动约两个日文汉字
            cb1 = QCheckBox("HAEW25W")
            cb2 = QCheckBox("何も出力しない")
            cb1.setFont(QFont("Meiryo", 10))
            cb2.setFont(QFont("Meiryo", 10))
            hbox.addWidget(cb1)
            hbox.addSpacing(24)  # cb1和cb2之间增加间距（数值可调整）
            hbox.addWidget(cb2)
            hbox.addStretch()
            vbox.addLayout(hbox)
            group.setLayout(vbox)
            layout.addWidget(group)
            layout.addSpacing(8)  # 每个条件之间增加间隔（数值可调整）

        layout.addSpacing(30)  # 在条件列表和按钮之间添加间隔

        # 下一步按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        next_btn = QPushButton("次へ")
        next_btn.setFont(QFont("Meiryo", 11))
        next_btn.setStyleSheet("padding: 6px 24px; background: #99ccff; color: #003366; border-radius: 6px;")
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        # 在主布局和按钮之间插入一个垂直间隔
        layout.addSpacing(8)  # 数值可调整，单位为像素
        layout.addLayout(btn_layout)

        # 边框
        frame = QFrame()
        frame.setLayout(layout)
        frame.setStyleSheet("QFrame { background: #e6f2ff; }")

        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatchWindow()
    window.show()
    sys.exit(app.exec_())