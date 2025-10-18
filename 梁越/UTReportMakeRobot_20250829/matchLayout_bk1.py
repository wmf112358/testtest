import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from getInfo import CobolSelector, FileCopyFinder

file_path = 'C:/Users/9511554/Desktop/LHL/01_jishudasai/IPOソース参照/MAET8600.ipo'
with open(file_path, "r", encoding="Shift_JIS") as f:
    content = f.read()

selector = CobolSelector(content)
selects = selector.find_select_assign()

finder = FileCopyFinder(content)
copy_results = [(file_name, finder.find_copy_for(file_name)) for file_name, _ in selects]

class ResultWindow(QWidget):
    def __init__(self, selects, copy_results):
        super().__init__()
        self.setWindowTitle("COBOL文件分析结果")
        self.setGeometry(300, 100, 700, 400)
        self.init_ui(selects, copy_results)

    def init_ui(self, selects, copy_results):
        layout = QVBoxLayout()
        # 设置整体背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e6f2ff"))
        self.setPalette(palette)

        # 标题
        title = QLabel("COBOL文件 SELECT/ASSIGN 及 COPY句分析")
        title.setFont(QFont("微软雅黑", 16, QFont.Bold))
        title.setStyleSheet("color: #003366; margin-bottom: 10px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # SELECT/ASSIGN结果
        group1 = QGroupBox("SELECT/ASSIGN结果")
        group1.setStyleSheet("QGroupBox { font-weight: bold; color: #003366; border: 1px solid #99ccff; background: #f7fbff; }")
        table1 = QTableWidget(len(selects), 2)
        table1.setHorizontalHeaderLabels(["文件名", "ASSIGN TO"])
        table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, (file_name, assign_to) in enumerate(selects):
            table1.setItem(i, 0, QTableWidgetItem(file_name))
            table1.setItem(i, 1, QTableWidgetItem(assign_to))
        group1_layout = QVBoxLayout()
        group1_layout.addWidget(table1)
        group1.setLayout(group1_layout)
        layout.addWidget(group1)

        # COPY句结果
        group2 = QGroupBox("各文件的COPY句")
        group2.setStyleSheet("QGroupBox { font-weight: bold; color: #003366; border: 1px solid #99ccff; background: #f7fbff; }")
        table2 = QTableWidget(len(copy_results), 2)
        table2.setHorizontalHeaderLabels(["文件名", "COPY句"])
        table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, (file_name, copy_name) in enumerate(copy_results):
            table2.setItem(i, 0, QTableWidgetItem(file_name))
            table2.setItem(i, 1, QTableWidgetItem(copy_name if copy_name else "未找到"))
        group2_layout = QVBoxLayout()
        group2_layout.addWidget(table2)
        group2.setLayout(group2_layout)
        layout.addWidget(group2)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow(selects, copy_results)
    window.show()
    sys.exit(app.exec_())