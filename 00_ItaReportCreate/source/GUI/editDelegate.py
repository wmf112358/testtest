from PyQt5.QtWidgets import  QStyledItemDelegate
from PyQt5 import QtGui

class EditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("""
            background: #e3f0fa;
            border: 1px solid #00B0F0;
        """)
        return editor

class NoColumnDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 0:
            painter.save()
            pen = painter.pen()
            pen.setColor(QtGui.QColor("#b5d1e8"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(option.rect.left(), option.rect.top(), option.rect.left(), option.rect.bottom())
            painter.restore()
    