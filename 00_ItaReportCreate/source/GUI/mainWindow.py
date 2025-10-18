from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit
)
from PyQt5.QtCore import Qt,QPoint
from GUI.titleBar import TitleBar
from GUI.menuBar import MenuBar
from GUI.patternSelectPage import PatternSelectPage
from GUI.infoEditPage import InfoEditPage
from GUI.caseListPage import CaseListPage
from GUI.caseDetailEditPage import CaseDetailEditPage
from PyQt5.QtGui import QPainter, QPolygon, QColor

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self._resize_margin = 1
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 900)
        self.page2 = None
        self.page_detail = None
        self.init_ui()
        self.info_edit_page = None

        # 拖拽缩放相关变量
        self._resize_margin = 6
        self._resizing = False
        self._resize_dir = None
        self._mouse_press_pos = None
        self._mouse_press_geom = None
        self.setMouseTracking(True)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        #main_layout.setContentsMargins(self._resize_margin, self._resize_margin, self._resize_margin, self._resize_margin)
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

        # 添加右下角拖拽控件
        self.resize_handle = ResizeHandle(self)
        self.resize_handle.raise_()
        self._update_resize_handle_pos()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_resize_handle_pos()

    def _update_resize_handle_pos(self):
        # 将拖拽控件放在右下角
        if hasattr(self, "resize_handle"):
            x = self.width() - self.resize_handle.width()
            y = self.height() - self.resize_handle.height()
            self.resize_handle.move(x, y)

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
        for t in getattr(self, 'threads', []):
            if t.isRunning():
                t.quit()
                if not t.wait(3000):  # 最多等3秒
                    t.terminate()
                    t.wait()
        event.accept()

    def _get_resize_direction(self, pos):
        w = self.width()
        h = self.height()
        x = pos.x()
        y = pos.y()
        m = self._resize_margin

        left = x <= m
        right = x >= w - m
        top = y <= m
        bottom = y >= h - m

        if left and top:
            return 'top-left'
        if right and top:
            return 'top-right'
        if left and bottom:
            return 'bottom-left'
        if right and bottom:
            return 'bottom-right'
        if top:
            return 'top'
        if bottom:
            return 'bottom'
        if left:
            return 'left'
        if right:
            return 'right'
        return None

    def _update_cursor_by_pos(self, pos):
        dir = self._get_resize_direction(pos)
        if dir in ('left', 'right'):
            self.setCursor(Qt.SizeHorCursor)
        elif dir in ('top', 'bottom'):
            self.setCursor(Qt.SizeVerCursor)
        elif dir in ('top-left', 'bottom-right'):
            self.setCursor(Qt.SizeFDiagCursor)
        elif dir in ('top-right', 'bottom-left'):
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            dir = self._get_resize_direction(event.pos())
            if dir:
                self._resizing = True
                self._resize_dir = dir
                self._mouse_press_pos = event.globalPos()
                self._mouse_press_geom = self.geometry()
                event.accept()
                return
        # 清除所有 QLineEdit 的焦点
        for edit in self.findChildren(QLineEdit):
            edit.clearFocus()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.globalPos() - self._mouse_press_pos
            geom = self._mouse_press_geom
            x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()
            min_w = self.minimumWidth() if self.minimumWidth() > 0 else 200
            min_h = self.minimumHeight() if self.minimumHeight() > 0 else 120

            dx = delta.x()
            dy = delta.y()

            nx, ny, nw, nh = x, y, w, h

            if 'left' in self._resize_dir:
                nx = x + dx
                nw = w - dx
                if nw < min_w:
                    nx = x + (w - min_w)
                    nw = min_w
            if 'right' in self._resize_dir:
                nw = w + dx
                if nw < min_w:
                    nw = min_w
            if 'top' in self._resize_dir:
                ny = y + dy
                nh = h - dy
                if nh < min_h:
                    ny = y + (h - min_h)
                    nh = min_h
            if 'bottom' in self._resize_dir:
                nh = h + dy
                if nh < min_h:
                    nh = min_h

            self.setGeometry(int(nx), int(ny), int(nw), int(nh))
            event.accept()
            return
        else:
            self._update_cursor_by_pos(event.pos())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._resizing:
            self._resizing = False
            self._resize_dir = None
            self._mouse_press_pos = None
            self._mouse_press_geom = None
            self.setCursor(Qt.ArrowCursor)  # 拖拽结束后恢复鼠标指针
            event.accept()
            return
        super().mouseReleaseEvent(event)

class ResizeHandle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(18, 18)
        self.setCursor(Qt.SizeFDiagCursor)
        self._dragging = False
        self._drag_pos = None
        self._start_geom = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 底色白色
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        points = [QPoint(0, self.height()), QPoint(self.width(), self.height()), QPoint(self.width(), 0)]
        painter.drawPolygon(QPolygon(points))

        # 画斜纹（与三角斜边平行）
        stripe_color = QColor("#b5d1e8")
        painter.setPen(stripe_color)
        step = 4
        w, h = self.width(), self.height()
        # 从右下到左上画斜线
        for i in range(0, w, step):
            painter.drawLine(w - i, h, w, h - i)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = event.globalPos()
            self._start_geom = self.window().geometry()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.globalPos() - self._drag_pos
            geom = self._start_geom
            min_w = self.window().minimumWidth() if self.window().minimumWidth() > 0 else 200
            min_h = self.window().minimumHeight() if self.window().minimumHeight() > 0 else 120
            nw = max(min_w, geom.width() + delta.x())
            nh = max(min_h, geom.height() + delta.y())
            self.window().resize(nw, nh)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()