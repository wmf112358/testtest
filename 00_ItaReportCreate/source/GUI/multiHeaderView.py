from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont,  QColor
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QStyleOptionHeader, QStyle

class MultiHeaderView(QHeaderView):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setSectionsClickable(False)
        self.setFixedHeight(44 + 28)
        self.setAttribute(Qt.WA_Hover, False)
        self.setHighlightSections(False)

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

        # 检查高亮状态，如果是合并区的第二列及之后，强制覆盖上半部分底色
        opt = QStyleOptionHeader()
        self.initStyleOption(opt)
        opt.rect = rect
        opt.section = logicalIndex
        is_highlight = opt.state & QStyle.State_On or opt.state & QStyle.State_Sunken

        # “条件”合并区，只在第0列画
        if logicalIndex == 0:
            width = self.sectionSize(0) + self.sectionSize(1)
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.drawLine(rect.x(), rect.y(), rect.x(), rect.y() + 44)
            painter.drawLine(rect.x() + width - 1, rect.y(), rect.x() + width - 1, rect.y() + 44)
            painter.drawLine(rect.x(), rect.y() + 44 - 1, rect.x() + width, rect.y() + 44 - 1)
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y(), width, 44, Qt.AlignCenter, "条件")
        # “条件”合并区的第二列（logicalIndex==1），如果高亮则强制覆盖上半部分底色
        elif logicalIndex == 1 and is_highlight:
            width = self.sectionSize(0) + self.sectionSize(1)
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x()-self.sectionSize(0), rect.y(), width, 44)
        # “処理”合并区，只在第2列画
        elif logicalIndex == 2:
            width = 0
            for i in range(2, col_count):
                width += self.sectionSize(i)
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.setPen(border_color)
            painter.drawRect(rect.x(), rect.y(), width, 44)
            painter.drawLine(rect.x(), rect.y(), rect.x(), rect.y() + 44)
            painter.drawLine(rect.x() + width - 1, rect.y(), rect.x() + width - 1, rect.y() + 44)
            painter.drawLine(rect.x(), rect.y() + 44 - 1, rect.x() + width, rect.y() + 44 - 1)
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor("#222"))
            painter.drawText(rect.x(), rect.y(), width, 44, Qt.AlignCenter, "処理")
        # “処理”合并区的后续列（logicalIndex>=3），如果高亮则强制覆盖上半部分底色
        elif logicalIndex >= 3 and is_highlight:
            width = 0
            for i in range(2, col_count):
                width += self.sectionSize(i)
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg_color)
            painter.drawRect(self.sectionPosition(2), rect.y(), width, 44)

        # 下半部分每列都画自己的内容
        painter.setFont(QFont("Meiryo", 10))
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
        painter.setPen(border_color)
        painter.drawRect(rect.x(), rect.y()+44, rect.width(), 28)
        # 补画左侧线
        painter.drawLine(rect.x(), rect.y()+44, rect.x(), rect.y()+44 + 28)
        # 右侧线
        if is_last_col or logicalIndex == 1 or logicalIndex == col_count - 1:
            painter.drawLine(rect.x() + rect.width() - 1, rect.y()+44, rect.x() + rect.width() - 1, rect.y()+44 + 28)
        # 下侧线
        painter.drawLine(rect.x(), rect.y() + 44 + 28 - 1, rect.x() + rect.width(), rect.y() + 44 + 28 - 1)
        painter.setPen(QColor("#222"))
        painter.drawText(rect.x(), rect.y()+44, rect.width(), 28, Qt.AlignCenter, self.model().headerData(logicalIndex, Qt.Horizontal))

        painter.restore()