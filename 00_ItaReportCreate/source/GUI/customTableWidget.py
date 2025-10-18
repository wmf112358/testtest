from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette
from PyQt5.QtCore import QModelIndex

class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hover_row = None           # 左侧加号/双线悬停行
        self._hover_row_right = None     # 右侧高亮悬停行

    def set_hover_row(self, row):
        self._hover_row = row
        self.viewport().update()

    def set_hover_row_right(self, row):
        self._hover_row_right = row
        self.viewport().update()
    
    def paintEvent(self, event):
        # 右侧悬停高亮（仅未选中时），要在super()之前绘制
        if self._hover_row_right is not None and self._hover_row_right >= 0:
            if not self.selectionModel().isRowSelected(self._hover_row_right, QModelIndex()):
                painter = QPainter(self.viewport())
                color = QColor("#e3f0fa")  # 浅蓝色
                for col in range(self.columnCount()):
                    rect = self.visualRect(self.model().index(self._hover_row_right, col))
                    painter.fillRect(rect, color)
                painter.end()
        # 选中行自定义深蓝色
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            painter = QPainter(self.viewport())
            color = QColor("#1976d2")  # 深蓝色
            for index in selected_rows:
                row = index.row()
                for col in range(self.columnCount()):
                    rect = self.visualRect(self.model().index(row, col))
                    painter.fillRect(rect, color)
            painter.end()
        super().paintEvent(event)
        # 左侧画双线
        if self._hover_row is not None and self._hover_row >= 0:
            painter = QPainter(self.viewport())
            pen = QPen(QColor("#3399ff"), 2)
            painter.setPen(pen)
            rect = self.visualRect(self.model().index(self._hover_row, 0))
            x1 = rect.left()
            x2 = self.viewport().width()
            y = rect.top()
            painter.drawLine(x1, y, x2, y)
            painter.drawLine(x1, y+2, x2, y+2)
            painter.end()
        
        # 画第一列左边框线
        painter = QPainter(self.viewport())
        # 颜色和粗细与 gridline 保持一致        
        pen = QPen(QColor(self.palette().color(QPalette.Mid)), 1)  # 1像素，和gridline一致
        painter.setPen(pen)
        for row in range(self.rowCount()):
            rect = self.visualRect(self.model().index(row, 0))
            x = rect.left()
            y1 = rect.top()
            y2 = rect.bottom()
            painter.drawLine(x, y1, x, y2)
        painter.end()
            