from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QComboBox, QHeaderView, QTextEdit
)
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from GUI.commonStyle import CommonStyle
from GUI.multiHeaderView import MultiHeaderView
from GUI.utils import icon_with_bg

class CaseDetailEditPage(QWidget):
    def __init__(self, on_back, case_data, detail_data, section_list):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部导航栏
        self.nav_bar = QWidget()
        self.nav_bar.setStyleSheet(CommonStyle.NAV_BAR)
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(0)
        self.nav_label = QLabel()
        self.nav_label.setFont(QFont("Meiryo", 11))
        self.nav_label.setStyleSheet("color: #222; padding: 12px 0 12px 24px;")
        pgmid = case_data.get("pgmid", "").replace(":", "").replace("：", "").strip()
        pgmname = case_data.get("pgmname", "").replace(":", "").replace("：", "").strip()
        max_pgmid_len = 12
        max_pgmname_len = 20
        fm = self.nav_label.font()
        metrics = QFontMetrics(fm)
        pgmid_disp = metrics.elidedText(pgmid, Qt.ElideRight, max_pgmid_len * metrics.averageCharWidth())
        pgmname_disp = metrics.elidedText(pgmname, Qt.ElideRight, max_pgmname_len * metrics.averageCharWidth())
        self.nav_label.setText(f"PGMID：{pgmid_disp}　　PGM名称：{pgmname_disp}")
        self.nav_layout.addWidget(self.nav_label, alignment=Qt.AlignVCenter)
        self.nav_layout.addStretch()        
        
        self.btn_add = QPushButton()
        self.btn_add.setFont(QFont("Meiryo", 10))
        # 生成灰色图标
        # 顶部导航栏色
        NAV_BG = "#d6e7f4"

        #gray_icon_add = icon_with_bg("./images/icon4.jpg", (16, 16), bg=NAV_BG, icon_color="#bfbfbf")
        self.btn_add.setIcon(icon_with_bg("../images/icon4.jpg", (16, 16), bg="#d6e7f4", icon_color="#bfbfbf"))
        self.btn_add.setIconSize(QSize(16, 16))
        self.btn_add.setText("ケース追加")
        self.btn_add.setLayoutDirection(Qt.LeftToRight)
        self.btn_add.setStyleSheet(CommonStyle.GRAY_BUTTON)
        self.btn_add.setEnabled(False)

        self.nav_layout.addWidget(self.btn_add) 

        self.btn_create = QPushButton()
        self.btn_create.setFont(QFont("Meiryo", 10))
        #gray_icon_create = icon_with_bg("./images/icon5.jpg", (20, 20), bg=NAV_BG, icon_color="#bfbfbf")
        self.btn_create.setIcon(icon_with_bg("../images/icon5.jpg", (20, 20), bg="#d6e7f4", icon_color="#bfbfbf"))
        self.btn_create.setIconSize(QSize(20, 20))
        self.btn_create.setText("Ita仕様書作成")
        self.btn_create.setLayoutDirection(Qt.LeftToRight)
        self.btn_create.setStyleSheet(CommonStyle.GRAY_BUTTON)
        self.btn_create.setEnabled(False)
        self.nav_layout.addWidget(self.btn_create)

        self.btn_back = QPushButton("<< 返回")
        self.btn_back.setFont(QFont("Meiryo", 10))
        self.btn_back.setStyleSheet(CommonStyle.BACK_BUTTON)
        self.btn_back.clicked.connect(on_back)
        self.nav_layout.addWidget(self.btn_back, alignment=Qt.AlignVCenter)
        self.nav_bar.setLayout(self.nav_layout)
        main_layout.addWidget(self.nav_bar)

        # 灰色导航栏
        gray_bar = QWidget()
        gray_bar.setStyleSheet("background: #f2f2f2; border-bottom: 1px solid #ccc;")
        gray_layout = QHBoxLayout()
        gray_layout.setContentsMargins(24, 0, 24, 0)
        gray_layout.setSpacing(0)

        gray_label = QLabel("詳細ケース編集")
        gray_label.setFont(QFont("Meiryo", 11))
        gray_label.setStyleSheet("color: #222;padding: 8px 0 8px 0;")
        gray_layout.addWidget(gray_label, alignment=Qt.AlignVCenter)

        gray_layout.addStretch()

        btn_add = QPushButton("追加")
        btn_add.setFont(QFont("Meiryo", 10))
        btn_add.setStyleSheet(CommonStyle.BACK_BUTTON)
        gray_layout.addWidget(btn_add)

        btn_save = QPushButton("保存")
        btn_save.setFont(QFont("Meiryo", 10))
        btn_save.setStyleSheet(CommonStyle.BACK_BUTTON)
        gray_layout.addWidget(btn_save)

        gray_bar.setLayout(gray_layout)
        main_layout.addWidget(gray_bar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 24, 40, 0)
        content_layout.setSpacing(0)

        # ケース説明
        desc_layout = QHBoxLayout()
        desc_layout.setSpacing(6)
        desc_label = QLabel("ケース説明")
        desc_label.setFixedWidth(80)
        desc_edit = QTextEdit()
        desc_edit.setMaximumHeight(40)
        desc_edit.setMinimumWidth(700)
        desc_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        desc_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(desc_edit)
        desc_layout.addStretch()
        content_layout.addLayout(desc_layout)

        content_layout.addSpacing(10)

        # セクション
        section_layout = QHBoxLayout()
        section_layout.setSpacing(6)
        section_label = QLabel("セクション")
        section_label.setFixedWidth(80)
        section_combo = QComboBox()
        section_combo.setMinimumWidth(200)
        section_combo.setFixedHeight(24)
        section_combo.setStyleSheet(CommonStyle.COMBO_BOX)
        section_layout.addWidget(section_label)
        section_layout.addWidget(section_combo)
        section_layout.addStretch()
        content_layout.addLayout(section_layout)

        content_layout.addSpacing(15)

        # ケース詳細标签和按钮
        detail_bar_layout = QHBoxLayout()
        detail_bar_layout.setSpacing(25)

        detail_label = QLabel("ケース詳細")
        detail_label.setFont(QFont("Meiryo", 9))
        detail_bar_layout.addWidget(detail_label)
        btn_extract = QPushButton("抽出")
        btn_extract.setStyleSheet(CommonStyle.BUTTON)
        btn_extract.setFixedHeight(20)
        btn_extract.setMinimumWidth(40)
        btn_extract.setFont(QFont("Meiryo", 9))
        detail_bar_layout.addWidget(btn_extract, alignment=Qt.AlignVCenter)
        btn_add_detail = QPushButton("追加　✚")
        btn_add_detail.setStyleSheet(CommonStyle.BUTTON)
        btn_add_detail.setFixedHeight(20)
        btn_add_detail.setMinimumWidth(40)
        btn_add_detail.setFont(QFont("Meiryo", 9))
        detail_bar_layout.addWidget(btn_add_detail, alignment=Qt.AlignVCenter)
        detail_bar_layout.addStretch()
        content_layout.addLayout(detail_bar_layout)

        content_layout.addSpacing(10)

        # 详细case表格
        detail_case_layout = QVBoxLayout()

        self.table = QTableWidget(len(detail_data), 9)
        self.table.setHorizontalHeaderLabels([
            "条件項目", "判定値", "ステータス", "設定項目", "設定値",
            "ファイル出力", "スナップ出力", "コンソール出力", "ERRMSG出力"
        ])
        header = MultiHeaderView(self.table)
        header.setAttribute(Qt.WA_Hover, False)
        self.table.setHorizontalHeader(header)
        self.table.setStyleSheet(CommonStyle.CASE_LIST_TABLE)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFixedHeight(220)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置所有列宽度自适应（随窗口变化）
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        detail_case_layout.addWidget(self.table)
        content_layout.addLayout(detail_case_layout)

        # 让内容靠上，底部加一个addStretch()
        content_layout.addStretch()

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
