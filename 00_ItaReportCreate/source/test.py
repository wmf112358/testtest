from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenu
from PyQt5.QtCore import Qt, QEvent, QModelIndex
from PyQt5.QtGui import QPainter, QColor

class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hover_row = None

    def set_hover_row(self, row):
        self._hover_row = row
        self.viewport().update()

    def paintEvent(self, event):
        # 悬停高亮（仅未选中时），要在super()之前绘制
        if self._hover_row is not None and self._hover_row >= 0:
            if not self.selectionModel().isRowSelected(self._hover_row, QModelIndex()):
                painter = QPainter(self.viewport())
                color = QColor("#e3f0fa")  # 浅蓝色
                for col in range(self.columnCount()):
                    rect = self.visualRect(self.model().index(self._hover_row, col))
                    painter.fillRect(rect, color)
                painter.end()
        super().paintEvent(event)

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = CustomTableWidget(10, 5)
        for i in range(10):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(f"{i},{j}"))
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.viewport().setMouseTracking(True)
        self.table.viewport().installEventFilter(self)
        self.table.viewport().setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.table)

    def eventFilter(self, obj, event):
        if obj == self.table.viewport():
            if event.type() == QEvent.MouseMove:
                pos = event.pos()
                row = self.table.rowAt(pos.y())
                last_col_rect = self.table.visualRect(self.table.model().index(row, self.table.columnCount()-1)) if row >= 0 else None
                if row >= 0 and last_col_rect.right() <= pos.x() < last_col_rect.right() + 24:
                    self.table.viewport().setCursor(Qt.ArrowCursor)
                    self.table.set_hover_row(row)
                else:
                    self.table.viewport().setCursor(Qt.IBeamCursor)
                    self.table.set_hover_row(None)
            elif event.type() == QEvent.Leave:
                self.table.viewport().setCursor(Qt.IBeamCursor)
                self.table.set_hover_row(None)
            elif event.type() == QEvent.MouseButtonPress:
                pos = event.pos()
                row = self.table.rowAt(pos.y())
                last_col_rect = self.table.visualRect(self.table.model().index(row, self.table.columnCount()-1)) if row >= 0 else None
                if event.button() == Qt.LeftButton:
                    # 只在右侧区域选中行
                    if row >= 0 and last_col_rect.right() <= pos.x() < last_col_rect.right() + 24:
                        self.table.selectRow(row)
                    else:
                        self.table.clearSelection()
                elif event.button() == Qt.RightButton:
                    # 右键时如果在右侧区域，选中行并弹出菜单
                    if row >= 0 and last_col_rect.right() <= pos.x() < last_col_rect.right() + 24:
                        self.table.selectRow(row)
                        menu = QMenu()
                        delete_action = menu.addAction("删除当前行")
                        action = menu.exec_(event.globalPos())
                        if action == delete_action:
                            self.table.removeRow(row)
                            self.table.clearSelection()  # 删除后不选中任何行
                        return True
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())