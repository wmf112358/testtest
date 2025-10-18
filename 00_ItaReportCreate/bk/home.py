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

def icon_with_bg(path, size=(20, 20), bg="#d6e7f4", icon_color=None):
    pixmap = QPixmap(path)
    image = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
    bg_color = QColor(bg)
    for y in range(image.height()):
        for x in range(image.width()):
            color = QColor(image.pixel(x, y))
            # 替换白色为底色
            if color.red() > 240 and color.green() > 240 and color.blue() > 240:
                image.setPixelColor(x, y, bg_color)
            # 只替换黑色为icon_color，其它颜色不变
            elif icon_color and color.red() < 30 and color.green() < 30 and color.blue() < 30:
                image.setPixelColor(x, y, QColor(icon_color))
            # 其它颜色保持不变
    result = QPixmap(size[0], size[1])
    result.fill(bg_color)
    scaled = QPixmap.fromImage(image).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    painter = QPainter(result)
    x = (size[0] - scaled.width()) // 2
    y = (size[1] - scaled.height()) // 2
    painter.drawPixmap(x, y, scaled)
    painter.end()
    return QIcon(result)

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

class PatternSelectPage(QWidget):
    def __init__(self, on_pattern_selected):
        super().__init__()
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
                btn = QPushButton(btn_text)
                btn.setFont(QFont("Meiryo", 12))
                btn.setStyleSheet(CommonStyle.PATTERN_SELECT_BUTTON)
                btn.clicked.connect(lambda _, g=group_title, b=btn_text: on_pattern_selected(g, b))
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

class InfoEditPage(QWidget):
    def __init__(self, on_back, path="基本情報設定"):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 60)
        layout.setSpacing(36)

        # 顶部导航栏
        nav_bar = QWidget()
        nav_bar.setStyleSheet(CommonStyle.NAV_BAR)
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        nav_label = QLabel(path)
        nav_label.setFont(QFont("Meiryo", 11))
        nav_layout.addWidget(nav_label, alignment=Qt.AlignVCenter)
        nav_layout.addStretch()
        btn_back = QPushButton("<< 返回")
        btn_back.setFont(QFont("Meiryo", 10))
        btn_back.setStyleSheet(CommonStyle.BACK_BUTTON)
        btn_back.clicked.connect(on_back)
        nav_layout.addWidget(btn_back, alignment=Qt.AlignVCenter)
        nav_bar.setLayout(nav_layout)
        layout.addWidget(nav_bar)

        form_area = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 24, 40, 24)
        form_layout.setSpacing(10)

        # IPO情報区
        group1_title_widget = QWidget()
        group1_title_layout = QHBoxLayout()
        group1_title_layout.setContentsMargins(0, 0, 0, 0)
        group1_title_layout.setSpacing(0)
        icon1 = QLabel()
        icon1.setPixmap(QPixmap("./images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon1.setFixedSize(24, 32)
        icon1.setAlignment(Qt.AlignTop)
        group1_title_layout.addWidget(icon1, alignment=Qt.AlignTop)
        group1_title = QLabel("ＩＰＯ情報")
        group1_title.setFont(QFont("Meiryo", 12, QFont.Bold))
        group1_title.setStyleSheet("color: #222; margin-bottom: 8px;")
        group1_title.setFixedHeight(28)
        group1_title_layout.addWidget(group1_title, alignment=Qt.AlignVCenter)
        group1_title_layout.addStretch()
        group1_title_widget.setLayout(group1_title_layout)
        form_layout.addWidget(group1_title_widget, alignment=Qt.AlignLeft)

        group1_grid = QGridLayout()
        group1_grid.setHorizontalSpacing(8)
        group1_grid.setVerticalSpacing(14)
        group1_grid.setColumnStretch(0, 0)
        group1_grid.setColumnStretch(1, 1)

        group1_grid.addWidget(QLabel("ＩＰＯファイル"), 0, 0)
        label_ipo_file = group1_grid.itemAtPosition(0, 0).widget()
        label_ipo_file.setFixedWidth(70)  # 与作業者区一致
        file_widget = QWidget()
        file_layout = QHBoxLayout()
        file_layout.setSpacing(0)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_edit = QLineEdit()
        file_edit.setFixedHeight(25)
        file_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        file_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        file_btn = QPushButton("選択")
        file_btn.setFixedHeight(25)
        file_btn.setFixedWidth(60)
        file_btn.setStyleSheet(CommonStyle.FILE_PATH_SELECT_BUTTON)

        def select_ipo_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "IPOファイル選択",
                "",
                "IPO Files (*.ipo);;All Files (*)"
            )
            if file_path:
                file_edit.setText(file_path)

        file_btn.clicked.connect(select_ipo_file)

        file_layout.addWidget(file_edit)
        file_layout.addWidget(file_btn)
        file_widget.setLayout(file_layout)
        group1_grid.addWidget(file_widget, 0, 1)

        group1_grid.addWidget(QLabel("ＰＧＭＩＤ"), 1, 0)
        label_pgmid = group1_grid.itemAtPosition(1, 0).widget()
        label_pgmid.setFixedWidth(70)
        pgmid_edit = QLineEdit()
        pgmid_edit.setFixedHeight(25)
        pgmid_edit.setFixedWidth(200)
        pgmid_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        pgmid_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        group1_grid.addWidget(pgmid_edit, 1, 1)

        group1_grid.addWidget(QLabel("ＰＧＭ名称"), 2, 0)
        label_pgmname = group1_grid.itemAtPosition(2, 0).widget()
        label_pgmname.setFixedWidth(70)
        pgmname_edit = QLineEdit()
        pgmname_edit.setFixedHeight(25)
        pgmname_edit.setFixedWidth(500)
        pgmname_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        pgmname_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        group1_grid.addWidget(pgmname_edit, 2, 1)

        group1_grid.addWidget(QLabel("スケルトン"), 3, 0)
        label_skeleton = group1_grid.itemAtPosition(3, 0).widget()
        label_skeleton.setFixedWidth(70)
        skeleton_combo = QComboBox()         
        skeleton_combo.setFixedHeight(25)
        skeleton_combo.setFixedWidth(200)
        skeleton_combo.setEditable(True)
        skeleton_combo.lineEdit().setStyleSheet(CommonStyle.SKELETON_COMBO_QLINE_EDIT)
        #skeleton_combo.setStyleSheet("border: 1px solid #888; background: #fff;")
        skeleton_combo.setStyleSheet(CommonStyle.COMBO_BOX)
        skeleton_combo.addItems(["", "バッチ", "オンライン", "その他"])
        group1_grid.addWidget(skeleton_combo, 3, 1)

        group1_grid_widget = QWidget()
        group1_grid_widget.setLayout(group1_grid)
        group1_grid_widget.setContentsMargins(15, 0, 0, 0)  # 右缩进15px
        form_layout.addWidget(group1_grid_widget)

        form_layout.addSpacing(28)

        # 作業者情報区
        group2_title_widget = QWidget()
        group2_title_layout = QHBoxLayout()
        group2_title_layout.setContentsMargins(0, 0, 0, 0)
        group2_title_layout.setSpacing(0)
        icon2 = QLabel()
        icon2.setPixmap(QPixmap("./images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon2.setFixedSize(24, 32)
        icon2.setAlignment(Qt.AlignTop)
        group2_title_layout.addWidget(icon2, alignment=Qt.AlignTop)
        group2_title = QLabel("作業者情報")
        group2_title.setFont(QFont("Meiryo", 12, QFont.Bold))
        group2_title.setStyleSheet("color: #222; margin-bottom: 8px;")
        group2_title.setFixedHeight(28)
        group2_title_layout.addWidget(group2_title, alignment=Qt.AlignVCenter)
        group2_title_layout.addStretch()
        group2_title_widget.setLayout(group2_title_layout)
        form_layout.addWidget(group2_title_widget, alignment=Qt.AlignLeft)

        group2_grid = QGridLayout()
        group2_grid.setHorizontalSpacing(8)
        group2_grid.setVerticalSpacing(14)

        # 控制每列宽度分配
        group2_grid.setColumnStretch(0, 0)  # 标签
        group2_grid.setColumnStretch(1, 0)  # 编辑框
        group2_grid.setColumnStretch(2, 0)  # 会社略称标签
        group2_grid.setColumnStretch(3, 0)  # 会社略称编辑框

        worker_edit = QLineEdit()        
        updater_edit = QLineEdit()        
        approver_edit = QLineEdit()
        company1_edit = QLineEdit()
        company2_edit = QLineEdit()
        company3_edit = QLineEdit()

        row_index = 0        
        for row in [
            ("担当者", worker_edit, "会社略称", company1_edit),
            ("最終更新者", updater_edit, "会社略称", company2_edit),
            ("最終承認者", approver_edit, "会社略称", company3_edit),
        ]:
            hbox = QHBoxLayout()
            label1 = QLabel(row[0])
            label1.setFixedWidth(70)  # 标签宽度
            hbox.addWidget(label1)
            hbox.addSpacing(8)        # 标签和编辑框间距
            edit1 = row[1]
            edit1.setFixedHeight(25)
            edit1.setFixedWidth(400)
            edit1.setStyleSheet(CommonStyle.TEXT_BOX)
            hbox.addWidget(edit1)
            hbox.addSpacing(32)       # 左右编辑框间距
            label2 = QLabel(row[2])
            label2.setFixedWidth(60)
            hbox.addWidget(label2)
            hbox.addSpacing(8)
            edit2 = row[3]
            edit2.setFixedHeight(25)
            edit2.setFixedWidth(150)
            edit2.setStyleSheet(CommonStyle.TEXT_BOX)
            hbox.addWidget(edit2)
            hbox.addStretch()
            group2_grid.addLayout(hbox, row_index, 0, 1, 4)
            row_index += 1

        group2_grid_widget = QWidget()
        group2_grid_widget.setLayout(group2_grid)
        group2_grid_widget.setContentsMargins(15, 0, 0, 0)
        form_layout.addWidget(group2_grid_widget)

        form_layout.addSpacing(28)

        # 成果物情報区
        group3_title_widget = QWidget()
        group3_title_layout = QHBoxLayout()
        group3_title_layout.setContentsMargins(0, 0, 0, 0)
        group3_title_layout.setSpacing(0)
        icon3 = QLabel()
        icon3.setPixmap(QPixmap("./images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon3.setFixedSize(24, 32)
        icon3.setAlignment(Qt.AlignTop)
        group3_title_layout.addWidget(icon3, alignment=Qt.AlignTop)
        group3_title = QLabel("成果物情報")
        group3_title.setFont(QFont("Meiryo", 12, QFont.Bold))
        group3_title.setStyleSheet("color: #222; margin-bottom: 8px;")
        group3_title.setFixedHeight(28)
        group3_title_layout.addWidget(group3_title, alignment=Qt.AlignVCenter)
        group3_title_layout.addStretch()
        group3_title_widget.setLayout(group3_title_layout)
        form_layout.addWidget(group3_title_widget, alignment=Qt.AlignLeft)

        group3_grid = QGridLayout()
        group3_grid.setHorizontalSpacing(8)
        group3_grid.setVerticalSpacing(12)
        group3_grid.setColumnStretch(0, 0)
        group3_grid.setColumnStretch(1, 1)

        group3_grid.addWidget(QLabel("成果物パス"), 0, 0)
        label_output = group3_grid.itemAtPosition(0, 0).widget()
        label_output.setFixedWidth(70)
        output_widget = QWidget()
        output_layout = QHBoxLayout()
        output_layout.setSpacing(0)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_edit = QLineEdit()
        output_edit.setFixedHeight(25)
        output_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        output_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        output_btn = QPushButton("選択")
        output_btn.setFixedHeight(25)
        output_btn.setFixedWidth(60)
        output_btn.setStyleSheet(CommonStyle.FILE_PATH_SELECT_BUTTON)
        def select_output_folder():
            folder_path = QFileDialog.getExistingDirectory(
                self,
                "成果物フォルダ選択",
                "",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            if folder_path:
                output_edit.setText(folder_path)

        output_btn.clicked.connect(select_output_folder)
        
        output_layout.addWidget(output_edit)
        output_layout.addWidget(output_btn)
        output_widget.setLayout(output_layout)
        group3_grid.addWidget(output_widget, 0, 1)

        group3_grid_widget = QWidget()
        group3_grid_widget.setLayout(group3_grid)
        group3_grid_widget.setContentsMargins(15, 0, 0, 0)
        form_layout.addWidget(group3_grid_widget)

        form_layout.addSpacing(50)

        # 右下按钮
        btn_area = QHBoxLayout()
        btn_area.addStretch()
        btn_ipo = QPushButton("IPO解析")
        btn_ipo.setFixedWidth(100)
        btn_ipo.setStyleSheet(CommonStyle.BUTTON)
        btn_area.addWidget(btn_ipo)
        form_layout.addLayout(btn_area)
        btn_ipo.clicked.connect(self.show_section_select)
        form_area.setLayout(form_layout)
        layout.addWidget(form_area)
        layout.addStretch()
        self.setLayout(layout)

    # IPO解析按钮点击事件，只弹窗和处理数据
    def show_section_select(self):
        sections = ["1000-SECTION", "1200-SECTION", "2000-SECTION"]
        dlg = SectionSelectDialog(sections, self)
        if dlg.exec_() == QDialog.Accepted:
            selectedSections = dlg.get_selected_sections()
            case_list = self.get_case_list(selectedSections)
            pgmid = self.findChild(QLineEdit, "pgmid_edit").text() if self.findChild(QLineEdit, "pgmid_edit") else "xxxxxx"
            pgmname = self.findChild(QLineEdit, "pgmname_edit").text() if self.findChild(QLineEdit, "pgmname_edit") else "xxxxxxxxxx"
            main_window = self.window()
            main_window.page3.update_case_list(case_list, pgmid, pgmname)
            main_window.menu_bar.highlight_idx = 2
            main_window.menu_bar.init_ui()
            main_window.stack.setCurrentWidget(main_window.page3)

    def get_case_list(self, selected_sections):
        # 这里模拟后台调用，实际可替换为API或数据库查询
        # 返回格式：[{"no": 1, "name": "XXX", ...}, ...]
        return [
            {"no": 1, "name": "X X X X X", "time": "2025/08/10", "edit": "編集", "delete": "削除"},
            {"no": 2, "name": "Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y", "time": "2025/08/09", "edit": "編集", "delete": "削除"},
        ]

class CaseListPage(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 顶部导航栏
        self.nav_bar = QWidget()
        self.nav_bar.setStyleSheet(CommonStyle.NAV_BAR)
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(0)
        self.nav_label = QLabel()
        self.nav_label.setFont(QFont("Meiryo", 11))
        self.nav_label.setStyleSheet("color: #222; padding: 12px 0 12px 24px;")
        self.nav_layout.addWidget(self.nav_label, alignment=Qt.AlignVCenter)
        self.nav_layout.addStretch()
        
        self.btn_add = QPushButton()
        self.btn_add.setFont(QFont("Meiryo", 10))
        self.btn_add.setIcon(icon_with_bg("./images/icon4.jpg", (16, 16)))
        self.btn_add.setIconSize(QSize(16, 16))
        self.btn_add.setText("ケース追加")
        self.btn_add.setLayoutDirection(Qt.LeftToRight)
        self.btn_add.setStyleSheet(CommonStyle.BACK_BUTTON)

        self.btn_add.clicked.connect(self.add_case_row)
        # 用于保存当前case列表
        self.case_list_data = []

        self.nav_layout.addWidget(self.btn_add) 

        self.btn_create = QPushButton()
        self.btn_create.setFont(QFont("Meiryo", 10))
        self.btn_create.setIcon(icon_with_bg("./images/icon5.jpg", (20, 20)))
        self.btn_create.setIconSize(QSize(20, 20))
        self.btn_create.setText("Ita仕様書作成")
        self.btn_create.setLayoutDirection(Qt.LeftToRight)
        self.btn_create.setStyleSheet(CommonStyle.BACK_BUTTON)
        self.nav_layout.addWidget(self.btn_create)

        self.btn_back = QPushButton("<< 返回")
        self.btn_back.setFont(QFont("Meiryo", 10))
        self.btn_back.setStyleSheet(CommonStyle.BACK_BUTTON)
        self.btn_back.clicked.connect(on_back)
        self.nav_layout.addWidget(self.btn_back, alignment=Qt.AlignVCenter)
        self.nav_bar.setLayout(self.nav_layout)
        self.layout.addWidget(self.nav_bar)

        self.nav_layout.setSpacing(16)

        # case表格
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["No.","ケース一覧", "更新時間", "操作"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)  # 不显示自带行号
        # 禁止点击表头选中整列
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setHighlightSections(False)

        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.verticalHeader().setMinimumWidth(60)
        self.table.verticalHeader().setMaximumWidth(60)
        self.table.verticalHeader().setStyleSheet(CommonStyle.CASE_LIST_TABLE_HEADER)
        self.table.setStyleSheet(CommonStyle.CASE_LIST_TABLE)
        # 列宽设置
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # No.
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # ケース一覧
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)  # 更新時間
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)  # 操作
        self.table.setColumnWidth(2, 200)  # 更新时间列宽度加大
        self.table.setColumnWidth(3, 200)  # 操作列宽度加大
        self.table.viewport().installEventFilter(self)

        self.table.setEditTriggers(QTableWidget.DoubleClicked)
        self.table.itemChanged.connect(self.on_item_changed)

        self.table.setItemDelegateForColumn(1, EditDelegate())  # 只对ケース一覧列设置

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def add_case_row(self):
        # 新增一行数据
        no = len(self.case_list_data) + 1
        new_case = {"no": no, "name": "", "time": datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
        self.case_list_data.append(new_case)
        self.update_case_table()

        # 光标定位到新行的ケース一覧列
        row = self.table.rowCount() - 1
        self.table.setCurrentCell(row, 1)
        self.table.editItem(self.table.item(row, 1))

    def update_case_list(self, case_list, pgmid, pgmname):
        # 设置导航栏PGMID和PGM名称，固定宽度，超长用省略号
        max_pgmid_len = 12
        max_pgmname_len = 16
        fm = self.nav_label.fontMetrics()
        pgmid_disp = fm.elidedText(pgmid, Qt.ElideRight, max_pgmid_len * fm.averageCharWidth())
        pgmname_disp = fm.elidedText(pgmname, Qt.ElideRight, max_pgmname_len * fm.averageCharWidth())
        self.nav_label.setText(f"PGMID　{pgmid_disp}　　PGM名称　{pgmname_disp}")

        # 同步数据
        self.case_list_data = []
        for case in case_list:
            self.case_list_data.append({
                "no": case["no"],
                "name": case["name"],
                "time": case.get("time", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            })

        self.update_case_table()

    def update_case_table(self):
        self.table.setRowCount(len(self.case_list_data))
        for i, case in enumerate(self.case_list_data):
            # No.列
            item_no = QTableWidgetItem(str(case["no"]))
            item_no.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item_no)
            # ケース一覧列
            item_name = QTableWidgetItem(case["name"])
            self.table.setItem(i, 1, item_name)
            # 更新时间列居中
            item_time = QTableWidgetItem(case["time"])
            item_time.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, item_time)
            # 操作列居中
            op_widget = QWidget()
            op_layout = QHBoxLayout(op_widget)
            op_layout.setContentsMargins(0, 0, 0, 0)
            op_layout.setSpacing(34)
            op_layout.setAlignment(Qt.AlignCenter)
            btn_edit = QPushButton("編集")
            btn_edit.setFont(QFont("Meiryo", 10))
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setStyleSheet(CommonStyle.BACK_BUTTON)
            btn_edit.clicked.connect(lambda _, idx=i: self.edit_case(idx))
            btn_delete = QPushButton("削除")
            btn_delete.setFont(QFont("Meiryo", 10))
            btn_delete.setCursor(Qt.PointingHandCursor)
            btn_delete.setStyleSheet(CommonStyle.BACK_BUTTON)
            btn_delete.clicked.connect(lambda _, idx=i: self.delete_case(idx))
            op_layout.addWidget(btn_edit)
            op_layout.addWidget(btn_delete)
            self.table.setCellWidget(i, 3, op_widget)

    def on_item_changed(self, item):
        # 只处理ケース一覧列（第1列）
        if item.column() == 1:
            row = item.row()
            now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            self.case_list_data[row]["name"] = item.text()
            self.case_list_data[row]["time"] = now_str
            # 更新时间列刷新
            time_item = self.table.item(row, 2)
            if time_item is None:
                time_item = QTableWidgetItem(now_str)
                time_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, time_item)
            else:
                time_item.setText(now_str)

    def edit_case(self, idx):
        # 获取当前行的数据
        case_data = self.case_list_data[idx].copy()
        # 获取当前显示的 PGMID 和 PGM名称
        nav_text = self.nav_label.text()
        # 假设格式为 "PGMID　xxxxxx　　PGM名称　yyyyyyyy"
        pgmid = ""
        pgmname = ""
        if "PGMID" in nav_text and "PGM名称" in nav_text:
            try:
                pgmid = nav_text.split("PGMID")[1].split("PGM名称")[0].strip("　 :")
                pgmname = nav_text.split("PGM名称")[1].strip("　 :")
            except Exception:
                pass
        case_data["pgmid"] = pgmid
        case_data["pgmname"] = pgmname
        # 调用主窗口方法切换到详细编辑页面
        main_window = self.window()
        if hasattr(main_window, "show_case_detail"):
            main_window.show_case_detail(case_data)

    def delete_case(self, idx):
        # 弹出确认对话框
        if 0 <= idx < len(self.case_list_data):
            case_no = self.case_list_data[idx]["no"]
            reply = QMessageBox.question(
                self,
                "削除確認",
                f"ケースNo.{case_no} を削除しますか？",
                QMessageBox.Ok | QMessageBox.Cancel
            )
            if reply == QMessageBox.Ok:
                del self.case_list_data[idx]
                # 重新编号
                for i, case in enumerate(self.case_list_data):
                    case["no"] = i + 1
                self.update_case_table()

    def eventFilter(self, obj, event):
        if obj == self.table.viewport() and event.type() == event.MouseButtonRelease:
            pos = event.pos()
            index = self.table.indexAt(pos)
            # 如果点击的是空白区域（没有单元格）
            if not index.isValid():
                self.table.clearSelection()
                self.table.setCurrentCell(-1, -1)  # 清除当前焦点单元格，虚线框消失
        return super().eventFilter(obj, event)
    
class EditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("""
            background: #e3f0fa;
            border: 1px solid #00B0F0;
        """)
        return editor
    
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
        pgmid = case_data.get("pgmid", "")
        pgmname = case_data.get("pgmname", "")
        max_pgmid_len = 12
        max_pgmname_len = 16
        fm = self.nav_label.font()
        metrics = QFontMetrics(fm)
        pgmid_disp = metrics.elidedText(pgmid, Qt.ElideRight, max_pgmid_len * metrics.averageCharWidth())
        pgmname_disp = metrics.elidedText(pgmname, Qt.ElideRight, max_pgmname_len * metrics.averageCharWidth())
        self.nav_label.setText(f"PGMID　{pgmid_disp}　　PGM名称　{pgmname_disp}")
        self.nav_layout.addWidget(self.nav_label, alignment=Qt.AlignVCenter)
        self.nav_layout.addStretch()        
        
        self.btn_add = QPushButton()
        self.btn_add.setFont(QFont("Meiryo", 10))
        # 生成灰色图标
        # 顶部导航栏色
        NAV_BG = "#d6e7f4"

        #gray_icon_add = icon_with_bg("./images/icon4.jpg", (16, 16), bg=NAV_BG, icon_color="#bfbfbf")
        self.btn_add.setIcon(icon_with_bg("./images/icon4.jpg", (16, 16), bg="#d6e7f4", icon_color="#bfbfbf"))
        self.btn_add.setIconSize(QSize(16, 16))
        self.btn_add.setText("ケース追加")
        self.btn_add.setLayoutDirection(Qt.LeftToRight)
        self.btn_add.setStyleSheet(CommonStyle.GRAY_BUTTON)
        self.btn_add.setEnabled(False)

        self.nav_layout.addWidget(self.btn_add) 

        self.btn_create = QPushButton()
        self.btn_create.setFont(QFont("Meiryo", 10))
        #gray_icon_create = icon_with_bg("./images/icon5.jpg", (20, 20), bg=NAV_BG, icon_color="#bfbfbf")
        self.btn_create.setIcon(icon_with_bg("./images/icon5.jpg", (20, 20), bg="#d6e7f4", icon_color="#bfbfbf"))
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

class MultiHeaderView(QHeaderView):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setSectionsClickable(False)
        self.setFixedHeight(44 + 28)
        self.setAttribute(Qt.WA_Hover, False)

    def event(self, event):
        if event.type() in (QEvent.HoverEnter, QEvent.HoverMove, QEvent.HoverLeave):
            return False
        return super().event(event)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        border_color = QColor("#b5d1e8")
        bg_color = QColor("#e3f0fa")
        col_count = self.model().columnCount()
        is_last_col = logicalIndex == col_count - 1

        # 合并单元格宽度
        if logicalIndex == 0:
            width = self.sectionSize(0) + self.sectionSize(1)
            # 上半部分（合并单元格）
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.setPen(border_color)
            # 外框
            painter.drawRect(rect.x(), rect.y(), width, 44)
            # 右侧竖线（只画到上半部分，避免和下半部分重叠）
            painter.drawLine(rect.x() + width - 1, rect.y(), rect.x() + width - 1, rect.y() + 44)
            # 左侧竖线
            painter.drawLine(rect.x(), rect.y(), rect.x(), rect.y() + 44)
            # 下分割线（上半部分底部）
            painter.drawLine(rect.x(), rect.y() + 44 - 1, rect.x() + width, rect.y() + 44 - 1)
            # 文本
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y(), width, 44, Qt.AlignCenter, "条件")
            # 下半部分（条件項目）
            painter.setFont(QFont("Meiryo", 10))
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            # 右侧竖线（只画右边，左边不用画）
            painter.drawLine(rect.x() + rect.width() - 1, rect.y()+44, rect.x() + rect.width() - 1, rect.y()+44 + 28)
            # 下分割线
            painter.drawLine(rect.x(), rect.y() + 44 + 28 - 1, rect.x() + rect.width(), rect.y() + 44 + 28 - 1)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y()+44, rect.width(), 28, Qt.AlignCenter, self.model().headerData(logicalIndex, Qt.Horizontal))
        elif logicalIndex == 1:
            # 只画下半部分（判定値）
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            # 右侧竖线（判定値右边）
            painter.drawLine(rect.x() + rect.width() - 1, rect.y()+44, rect.x() + rect.width() - 1, rect.y()+44 + 28)
            # 下分割线
            painter.drawLine(rect.x(), rect.y() + 44 + 28 - 1, rect.x() + rect.width(), rect.y() + 44 + 28 - 1)
            painter.setFont(QFont("Meiryo", 10))
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y()+44, rect.width(), 28, Qt.AlignCenter, self.model().headerData(logicalIndex, Qt.Horizontal))
        elif logicalIndex == 2:
            width = 0
            for i in range(2, 9):
                width += self.sectionSize(i)
            # 上半部分（合并单元格）
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.setPen(border_color)
            # 外框
            painter.drawRect(rect.x(), rect.y(), width, 44)
            # 左侧竖线（只画到上半部分，避免和下半部分重叠）
            painter.drawLine(rect.x(), rect.y(), rect.x(), rect.y() + 44)
            # 右侧竖线
            painter.drawLine(rect.x() + width - 1, rect.y(), rect.x() + width - 1, rect.y() + 44)
            # 下分割线（上半部分底部）
            painter.drawLine(rect.x(), rect.y() + 44 - 1, rect.x() + width, rect.y() + 44 - 1)
            # 文本
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y(), width, 44, Qt.AlignCenter, "処理")
            # 下半部分（ステータス）
            painter.setFont(QFont("Meiryo", 10))
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            # 左侧竖线（只画左边，右边不用画）
            painter.drawLine(rect.x(), rect.y()+44, rect.x(), rect.y()+44 + 28)
            # 右侧竖线（只画最后一列右边）
            if logicalIndex == 8:
                painter.drawLine(rect.x() + rect.width() - 1, rect.y()+44, rect.x() + rect.width() - 1, rect.y()+44 + 28)
            # 下分割线
            painter.drawLine(rect.x(), rect.y() + 44 + 28 - 1, rect.x() + rect.width(), rect.y() + 44 + 28 - 1)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y()+44, rect.width(), 28, Qt.AlignCenter, self.model().headerData(logicalIndex, Qt.Horizontal))
        else:
            # 只画下半部分（其它列）
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
            # 右侧竖线（只画最后一列右边）
            if is_last_col:
                painter.drawLine(rect.x() + rect.width() - 1, rect.y()+44, rect.x() + rect.width() - 1, rect.y()+44 + 28)
            # 左侧竖线（只画左边）
            painter.drawLine(rect.x(), rect.y()+44, rect.x(), rect.y()+44 + 28)
            # 下分割线
            painter.drawLine(rect.x(), rect.y() + 44 + 28 - 1, rect.x() + rect.width(), rect.y() + 44 + 28 - 1)
            painter.setFont(QFont("Meiryo", 10))
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y()+44, rect.width(), 28, Qt.AlignCenter, self.model().headerData(logicalIndex, Qt.Horizontal))
        painter.restore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 900)
        self.page2 = None
        self.page_detail = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        self.menu_bar = MenuBar(self.on_menu_clicked, highlight_idx=0)
        body_layout.addWidget(self.menu_bar)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: #fff;")
        self.page1 = PatternSelectPage(self.on_pattern_selected)
        self.page3 = CaseListPage(self.on_case_back)
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page3)
        body_layout.addWidget(self.stack)
        main_layout.addLayout(body_layout)
        self.setLayout(main_layout)

    def on_menu_clicked(self, idx):
        self.menu_bar.highlight_idx = idx
        self.menu_bar.init_ui()
        if idx == 0:
            self.stack.setCurrentIndex(0)
        elif idx == 1:
            if self.page2:
                self.stack.setCurrentIndex(1)
        elif idx == 2:
            self.stack.setCurrentIndex(self.stack.indexOf(self.page3))

    def on_pattern_selected(self, group, btn_text):
        path = f"基本情報設定／{group}／{btn_text}"
        if self.page2:
            idx = self.stack.indexOf(self.page2)
            if idx != -1:
                self.stack.removeWidget(self.page2)
            self.page2.deleteLater()
        self.page2 = InfoEditPage(self.on_info_back, path=path)
        self.stack.insertWidget(1, self.page2)
        self.menu_bar.highlight_idx = 1
        self.menu_bar.init_ui()
        self.stack.setCurrentIndex(1)

    def on_info_back(self):
        # 基本情報編集画面返回到パターン選択画面
        self.menu_bar.highlight_idx = 0
        self.menu_bar.init_ui()
        self.stack.setCurrentWidget(self.page1)

    def on_case_back(self):
        # ケース編集画面返回到基本情報編集画面
        self.menu_bar.highlight_idx = 1
        self.menu_bar.init_ui()
        if self.page2:
            self.stack.setCurrentWidget(self.page2)

    def mousePressEvent(self, event):
        # 清除所有 QLineEdit 的焦点
        for edit in self.findChildren(QLineEdit):
            edit.clearFocus()
        super().mousePressEvent(event)

    def show_case_detail(self, case_data):
        # 假设 get_case_detail_data 和 get_section_list 为后台接口
        #detail_data = get_case_detail_data(case_data["no"])
        #section_list = get_section_list()
        detail_data = []
        section_list = []
        if self.page_detail:
            idx = self.stack.indexOf(self.page_detail)
            if idx != -1:
                self.stack.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
        self.page_detail = CaseDetailEditPage(self.on_case_detail_back, case_data, detail_data, section_list)
        self.stack.addWidget(self.page_detail)
        self.stack.setCurrentWidget(self.page_detail)

    def on_case_detail_back(self):
        self.stack.setCurrentWidget(self.page3)

class SectionSelectDialog(QDialog):
    def __init__(self, sections, parent=None):
        super().__init__(parent)
        self.setWindowTitle("セクション選択")
        self.setFixedSize(800, 600)
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 40)
        # 三列：No, セクション名, 复选框
        self.table = QTableWidget(len(sections), 3)
        self.table.setHorizontalHeaderLabels(["No", "セクション名", ""])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 行号列宽度与网格线
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.verticalHeader().setMinimumWidth(40)
        self.table.verticalHeader().setMaximumWidth(40)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.verticalHeader().setVisible(False)  # 不显示自带行号

        # 列宽设置
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 60)   # 复选框

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 标题底色与按钮一致
        self.table.setStyleSheet(CommonStyle.SECTION_SELECT_TABLE)
        self.table.setItemDelegate(NoColumnDelegate())

        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 28)

        def create_center_checkbox():
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 水平居中
            checkbox = QCheckBox()
            layout.addWidget(checkbox)
            return widget, checkbox

        self.checkboxes = []
        for i, sec in enumerate(sections):
            self.table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i, 1, QTableWidgetItem(sec))
            cb_widget, cb = create_center_checkbox()
            self.checkboxes.append(cb)
            self.table.setCellWidget(i, 2, cb_widget)

        # 标题复选框也居中
        self.header_checkbox = QCheckBox(self.table)
        self.header_checkbox.stateChanged.connect(self.toggle_all)
        self.update_header_checkbox_pos()  # 这里调用类方法
        self.table.horizontalHeader().sectionResized.connect(self.update_header_checkbox_pos)
        self.table.horizontalHeader().sectionMoved.connect(self.update_header_checkbox_pos)
        layout.addWidget(self.table)

        layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("キャンセル")
        btn_ok = QPushButton("OK")
        btn_cancel.setStyleSheet(CommonStyle.BUTTON)
        btn_ok.setStyleSheet(CommonStyle.BUTTON)
        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.on_ok_clicked)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def on_ok_clicked(self):
        if any(self.get_selected_sections()):
            self.accept()
        else:
            QMessageBox.warning(self, "選択エラー", "少なくとも1つのセクションを選択してください。")

    def update_header_checkbox_pos(self):
        header = self.table.horizontalHeader()
        # 复选框居中于第三列
        #x = header.sectionViewportPosition(2) + (header.sectionSize(2) - self.header_checkbox.sizeHint().width()) // 2
        x = header.sectionPosition(2)+135  # 135px是为了让复选框居中
        y = 6 
        self.header_checkbox.move(x, y)

    def toggle_all(self, state):
        for cb in self.checkboxes:
            cb.setChecked(state == 2)

    def get_selected_sections(self):
        return [cb.isChecked() for cb in self.checkboxes]
    
class NoColumnDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 0:
            painter.save()
            pen = painter.pen()
            pen.setColor(QtGui.QColor("#b5d1e8"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(option.rect.left(), option.rect.top(), option.rect.left(), option.rect.bottom())
            painter.restore()
    
class CommonStyle:
    BUTTON = """
        QPushButton {
            background: #e3f0fa;
            color: #222;
            border: 1px solid #b5d1e8;
            border-radius: 0px;
            min-width: 80px;
            min-height: 32px;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """
    PATTERN_SELECT_CARD ="""
        background: #f7f8fa;
        border: 1px solid #ccc;
        border-radius: 0px;
        margin-left: 40px;
        margin-right: 320px;
    """
    PATTERN_SELECT_BUTTON = """
        QPushButton {
            background: #e3f0fa;
            color: #222;
            border: 1px solid #b5d1e8;
            border-radius: 0px;
            min-width: 160px;
            min-height: 40px;
            margin: 0 28px;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """

    FILE_PATH_SELECT_BUTTON = """
        QPushButton {
            border: 1px solid #888;
            background: #e3f0fa;
            padding: 0 8px;
            border-left: none;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """

    SECTION_SELECT_TABLE = """
        QTableWidget {
            gridline-color: #b5d1e8;
            border: none;
        }
        QHeaderView::section {
            background: #e3f0fa;
            border-top: 1px solid #b5d1e8;
            border-bottom: 1px solid #b5d1e8;
            border-right: 1px solid #b5d1e8;
            color: #222;
            font-weight: bold;
        }
        QHeaderView::section:first {
            border-left: 1px solid #b5d1e8;
        }
    """

    TEXT_BOX = """
        QLineEdit {
            border: 1px solid #888;
            background: #fff;
        }
        QLineEdit:focus {
            border: 1px solid #00B0F0;
            background: #e3f0fa;
        }
    """

    COMBO_BOX = """
        QComboBox {
            border: 1px solid #888;
            background: #fff;
        }
        QComboBox::drop-down {
            border-left: 1px solid #888;
            width: 24px;
        }
        QComboBox::down-arrow {
            image: url(./images/icon3.jpg);
            width: 12px;
            height: 12px;
        }
    """
    SKELETON_COMBO_QLINE_EDIT = """
        QLineEdit:focus {
            border: 1px solid #00B0F0;
            background: #e3f0fa;
        }
    """

    NAV_BAR = """
        background: #d6e7f4;
        color: #222;
        padding: 12px 0 12px 24px;
        border-bottom: 1px solid #ccc;
    """

    TITLE = """
        color: white;
        background-color: #111;
        min-height: 44px;
        max-height: 44px;
        padding-left: 0px;
        padding-right: 0px;
    """

    TITLE_BUTTON = """
        QPushButton {
            background: #111;
            color: #fff;
            border: none;
            min-height: 44px;
            max-height: 44px;
            margin: 0;
            padding: 0;
        }
    """
    BACK_BUTTON = """
        QPushButton {
            background: transparent;
            color: #222;
            border: none; 
            padding: 0 16px 0 0;
        }
        QPushButton:hover {
            color: #00B0F0; 
            text-decoration: underline;
        }
    """
    GRAY_BUTTON = """
        QPushButton {
            background: transparent;
            color: #BFBFBF;
            border: none; 
            padding: 0 16px 0 0;
        }
    """

    CASE_LIST_TABLE_HEADER = """
        QHeaderView { background: #F2F2F2; color: #222; font-weight: bold; }
    """

    CASE_LIST_TABLE = """
        QTableWidget {
            border: none;
            gridline-color: #BFBFBF;
            font-family: Meiryo;
            font-size: 10pt;
        }
        QHeaderView::section {
            background: #F2F2F2;
            color: #222;
            border-width: 0px 1px 1px 0px;  /* 上右下左 */
            border-style: solid;
            border-color: transparent #BFBFBF #BFBFBF transparent;
            font-size: 11pt;
            height: 44px;
        }
        QHeaderView::section:hover, QHeaderView::section:pressed, QHeaderView::section:focus {
            background: #F2F2F2 !important;
        }
        QHeaderView::section:checked {
            background: #F2F2F2 !important;
        }
        QHeaderView {
            background: #F2F2F2;
        }
    """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())