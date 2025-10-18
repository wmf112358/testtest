import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy,
    QLineEdit, QComboBox, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from GUI.commonStyle import CommonStyle
from GUI.sectionSelectDialog import SectionSelectDialog
from commond import ExtractHeaderThread
from section_extractor import SectionExtractThread
from GUI.caseListPage import CaseListPage

class InfoEditPage(QWidget):
    def __init__(self, on_back, path="基本情報設定", pattern_type=None):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 60)
        layout.setSpacing(36)
        self.section_thread = None
        self.threads = []  # 保存所有线程对象，防止被回收

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
        icon1.setPixmap(QPixmap("../images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        self.file_edit = file_edit
        self.file_btn = file_btn

        self.extract_thread = None  # 保存线程对象，防止被回收        
        file_btn.clicked.connect(self.select_ipo_file)
        
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
        self.pgmid_edit = pgmid_edit

        group1_grid.addWidget(QLabel("ＰＧＭ名称"), 2, 0)
        label_pgmname = group1_grid.itemAtPosition(2, 0).widget()
        label_pgmname.setFixedWidth(70)
        pgmname_edit = QLineEdit()
        pgmname_edit.setFixedHeight(25)
        pgmname_edit.setFixedWidth(500)
        pgmname_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        pgmname_edit.setStyleSheet(CommonStyle.TEXT_BOX)
        group1_grid.addWidget(pgmname_edit, 2, 1)
        self.pgmname_edit = pgmname_edit

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
        self.skeleton_combo = skeleton_combo
        
        def set_skeleton_items(pattern_type):
            skeleton_combo.clear()
            if pattern_type == "オンライン":
                skeleton_combo.addItems([""] + [f"UZ0C{str(i).zfill(2)}" for i in range(1, 11)])
            elif pattern_type == "部品":
                skeleton_combo.addItems(["", "UZ8K01", "UZ2B01"])
            elif pattern_type == "バッチ":
                skeleton_combo.addItems([""] + [f"UZ0Q{str(i).zfill(2)}" for i in range(1, 12)] + ["UZ1Q01"])
            elif pattern_type == "DBI":
                skeleton_combo.addItems(["", "UZ9U01"])
            else:
                skeleton_combo.addItems([""])

        set_skeleton_items(pattern_type)

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
        icon2.setPixmap(QPixmap("../images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        icon3.setPixmap(QPixmap("../images/icon1.jpg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        self.btn_ipo = btn_ipo
        btn_area.addWidget(btn_ipo)
        form_layout.addLayout(btn_area)
        btn_ipo.clicked.connect(self.show_section_select)
        form_area.setLayout(form_layout)
        layout.addWidget(form_area)
        layout.addStretch()
        self.setLayout(layout)

    def select_ipo_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "IPOファイル選択",
            "",
            "IPO Files (*.ipo);;All Files (*)"
        )
        if file_path:
            self.file_edit.setText(file_path)
            pgm_id = os.path.splitext(os.path.basename(file_path))[0]
            # 先关闭旧线程
            for t in self.threads:
                if t.isRunning():
                    t.quit()
                    t.wait()
            self.threads.clear()
            self.file_btn.setEnabled(False)  # 禁用按钮
            # 启动新线程
            thread = ExtractHeaderThread(file_path, pgm_id)
            thread.finished.connect(self.on_extract_finished)
            thread.start()
            self.threads.append(thread)


    def on_extract_finished(self, result, error):
        self.file_btn.setEnabled(True)  # 恢复按钮
        if error:
            QMessageBox.warning(self, "解析エラー", f"IPOファイル解析に失敗しました。\n{error}")
        else:
            self.pgmid_edit.setText(result.program_id)
            self.pgmname_edit.setText(result.program_name)
            self.skeleton_combo.setCurrentText(result.pattern_id)
        self.extract_thread = None  # 释放线程对象

    # IPO解析按钮点击事件，只弹窗和处理数据
    def show_section_select(self):
        file_path = self.file_edit.text()
        pgmid = self.pgmid_edit.text()
        if not file_path or not pgmid:
            QMessageBox.warning(self, "入力エラー", "IPOファイルとPGMIDを入力してください。")
            return

        # 先关闭旧线程
        if self.section_thread is not None and self.section_thread.isRunning():
            self.section_thread.quit()
            self.section_thread.wait()
        self.btn_ipo.setEnabled(False)  # 禁用按钮

        # 1. 启动线程解析
        self.section_thread = SectionExtractThread(file_path, pgmid)
        self.section_thread.finished.connect(self.on_section_extracted)
        self.section_thread.start()

    def on_section_extracted(self, section_ids, error):
        self.btn_ipo.setEnabled(True)  # 恢复按钮
        self.section_thread = None
        if error:
            QMessageBox.warning(self, "解析エラー", f"セクション抽出に失敗しました。\n{error}")
            return
        # 2. 解析完成后再弹出对话框
        dlg = SectionSelectDialog(section_ids, self)
        if dlg.exec_() == QDialog.Accepted:
            selected_sections = dlg.get_selected_sections()
            self.update_case_list_by_sections(selected_sections)

    def update_case_list_by_sections(self, selected_sections):
        case_list = self.get_case_list(selected_sections)
        pgmid = self.pgmid_edit.text()
        pgmname = self.pgmname_edit.text()
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

    def closeEvent(self, event):
        for t in getattr(self, 'threads', []):
            if t.isRunning():
                t.quit()
                t.wait()
        self.threads = []
        event.accept()
