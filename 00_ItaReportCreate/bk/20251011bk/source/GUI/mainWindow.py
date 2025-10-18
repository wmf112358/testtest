from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit
)
from PyQt5.QtCore import Qt
from GUI.titleBar import TitleBar
from GUI.menuBar import MenuBar
from GUI.patternSelectPage import PatternSelectPage
from GUI.infoEditPage import InfoEditPage
from GUI.caseListPage import CaseListPage
from GUI.caseDetailEditPage import CaseDetailEditPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 900)
        self.page2 = None
        self.page_detail = None
        self.init_ui()
        self.info_edit_page = None

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

    def on_pattern_selected(self, group, btn_text, pattern_type):
        path = f"基本情報設定／{group}／{btn_text}"
        if self.page2:
            idx = self.stack.indexOf(self.page2)
            if idx != -1:
                self.stack.removeWidget(self.page2)
            self.page2.deleteLater()
        self.page2 = InfoEditPage(self.on_info_back, path=path, pattern_type=pattern_type)
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
    
    def closeEvent(self, event):
        # 检查所有页面的线程对象
        for page_attr in ['page1', 'page2', 'page3']:
            page = getattr(self, page_attr, None)
            if page is not None:
                for thread_attr in ['extract_thread', 'section_thread']:
                    thread = getattr(page, thread_attr, None)
                    if thread is not None and hasattr(thread, 'isRunning') and thread.isRunning():
                        thread.quit()
                        thread.wait()
        event.accept()
