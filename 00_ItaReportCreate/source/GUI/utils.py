from PyQt5.QtGui import  QPixmap, QIcon, QPainter, QColor, QImage
from PyQt5.QtCore import Qt

def icon_with_bg(path, size=(20, 20), bg="#d6e7f4", icon_color=None):
    pixmap = QPixmap(path)
    image = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
    bg_color = QColor(bg)
    for y in range(image.height()):
        for x in range(image.width()):
            color = QColor(image.pixel(x, y))
            # 替换白色为底色
            if color.red() > 240 and color.green() > 240 and color.blue() > 240:
                image.setPixelColor(x, y, bg_color)
            # 只替换黑色为icon_color，其它颜色不变
            elif icon_color and color.red() < 30 and color.green() < 30 and color.blue() < 30:
                image.setPixelColor(x, y, QColor(icon_color))
            # 其它颜色保持不变
    result = QPixmap(size[0], size[1])
    result.fill(bg_color)
    scaled = QPixmap.fromImage(image).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    painter = QPainter(result)
    x = (size[0] - scaled.width()) // 2
    y = (size[1] - scaled.height()) // 2
    painter.drawPixmap(x, y, scaled)
    painter.end()
    return QIcon(result)
