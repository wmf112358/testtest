from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QCheckBox, QHeaderView,QMessageBox
)
from PyQt5.QtCore import Qt
from GUI.commonStyle import CommonStyle
from GUI.editDelegate import NoColumnDelegate

class SectionSelectDialog(QDialog):
    def __init__(self, sections=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("セクション選択")
        self.setFixedSize(800, 600)
        self.section_table = QTableWidget(0, 1)
        self.section_table.setHorizontalHeaderLabels(["セクションID"])
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

        if sections:
            self.set_sections(sections)

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
        # 返回用户勾选的 section id 列表
        selected = []
        for i, cb in enumerate(self.checkboxes):
            if cb.isChecked():
                section_id = self.table.item(i, 1).text()
                selected.append(section_id)
        return selected
    
    def set_sections(self, section_ids):
        self.table.setRowCount(len(section_ids))
        self.checkboxes = []
        def create_center_checkbox():
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            checkbox = QCheckBox()
            layout.addWidget(checkbox)
            return widget, checkbox

        for i, sec in enumerate(section_ids):
            self.table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i, 1, QTableWidgetItem(sec))
            cb_widget, cb = create_center_checkbox()
            self.checkboxes.append(cb)
            self.table.setCellWidget(i, 2, cb_widget)
            self.table.setRowHeight(i, 28)
    