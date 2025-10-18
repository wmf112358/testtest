from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtCore import QSize
from GUI.commonStyle import CommonStyle
from GUI.utils import icon_with_bg
from GUI.editDelegate import EditDelegate

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
        self.btn_add.setIcon(icon_with_bg("../images/icon4.jpg", (16, 16)))
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
        self.btn_create.setIcon(icon_with_bg("../images/icon5.jpg", (20, 20)))
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
        new_case = {
            "no": no,
            "name": "",
            "time": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }
        self.case_list_data.append(new_case)
        self.table.setRowCount(len(self.case_list_data))

        # 只为新行设置内容，不刷新所有行
        i = len(self.case_list_data) - 1
        # No.列
        item_no = QTableWidgetItem(str(new_case["no"]))
        item_no.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(i, 0, item_no)
        # ケース一覧列
        item_name = QTableWidgetItem(new_case["name"])
        self.table.setItem(i, 1, item_name)
        # 更新时间列
        item_time = QTableWidgetItem(new_case["time"])
        item_time.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(i, 2, item_time)
        # 操作列
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

        # 光标定位到新行的ケース一覧列
        self.table.setCurrentCell(i, 1)
        self.table.editItem(self.table.item(i, 1))

    def update_case_list(self, case_list, pgmid, pgmname):
        # 设置导航栏PGMID和PGM名称，固定宽度，超长用省略号
        max_pgmid_len = 12
        max_pgmname_len = 20
        fm = self.nav_label.fontMetrics()
        pgmid_disp = fm.elidedText(pgmid, Qt.ElideRight, max_pgmid_len * fm.averageCharWidth())
        pgmname_disp = fm.elidedText(pgmname, Qt.ElideRight, max_pgmname_len * fm.averageCharWidth())
        self.nav_label.setText(f"PGMID：{pgmid_disp}　　PGM名称：{pgmname_disp}")

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
    