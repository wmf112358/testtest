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