from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.commonStyle import CommonStyle

class PatternSelectPage(QWidget):
    def __init__(self, on_pattern_selected):
        super().__init__()
        self.on_pattern_selected = on_pattern_selected
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 30)
        layout.setSpacing(36)
        nav_bar = QLabel("パターン選択")
        nav_bar.setFont(QFont("Meiryo", 11))
        nav_bar.setStyleSheet(CommonStyle.NAV_BAR)
        layout.addWidget(nav_bar)
        groups = [
            ("ＡＣＰ", ["バッチ", "オンライン"]),
            ("部品", ["共通部品", "業務部品"]),
            ("ＤＢＩ", ["更新", "参照"]),
        ]
        for group_title, btns in groups:
            card = QWidget()
            card.setStyleSheet(CommonStyle.PATTERN_SELECT_CARD)
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(32, 24, 32, 24)
            card_layout.setSpacing(6)
            title_label = QLabel(group_title)
            title_label.setFont(QFont("Meiryo", 13, QFont.Bold))
            title_label.setStyleSheet("color: #222; margin-bottom: 8px; border: none;")
            card_layout.addWidget(title_label, alignment=Qt.AlignLeft)
            btn_layout = QHBoxLayout()
            for btn_text in btns:
                if group_title == "ＡＣＰ":
                    pattern_type = btn_text  # "バッチ" or "オンライン"
                elif group_title == "部品":
                    pattern_type = "部品"
                elif group_title == "ＤＢＩ":
                    pattern_type = "DBI"
                btn = QPushButton(btn_text)
                btn.setFont(QFont("Meiryo", 12))
                btn.setStyleSheet(CommonStyle.PATTERN_SELECT_BUTTON)
                btn.clicked.connect(lambda _, g=group_title, b=btn_text, p=pattern_type: on_pattern_selected(g, b, p))
                btn_layout.addWidget(btn)
            btn_layout.addStretch()
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            btn_widget.setContentsMargins(36, 0, 0, 0)
            btn_widget.setStyleSheet("border: none; background: transparent;")
            card_layout.addWidget(btn_widget)
            card.setLayout(card_layout)
            layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)
        
