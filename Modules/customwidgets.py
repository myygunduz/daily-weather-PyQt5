#                PyQt5 Custom Widgets                 #
#                    Kadir Aksoy                      #
#   https://github.com/kadir014/pyqt5-custom-widgets  #


import time
import os
from math import ceil, sin, pi, sqrt, atan2, pow
import requests

from PyQt5.QtCore import Qt, QEvent, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QAbstractButton, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPainter, QPixmap, QPen, QBrush, QMovie, QImage



class Animation:
    easeOutSine  = lambda x: sin((x * pi) / 2)
    easeOutCubic = lambda x: 1 - ((1 - x)**3)
    easeOutQuart = lambda x: 1 - pow(1 - x, 4)
    easeOutCirc  = lambda x: sqrt(1 - pow(x - 1, 2))



class AnimationHandler:
    def __init__(self, widget, startv, endv, type):
        self.widget = widget
        self.type = type

        self.startv = startv
        self.endv = endv

        self.value = 0.0001

        self.reverse = False
        self.start_time = None
        self.interval = 20 / 1000

    def start(self, reverse=False):
        self.start_time = time.time()
        self.reverse = reverse
        self.value = 0.01

    def done(self):
        return self.start_time is None

    def update(self):
        if not self.done():
            if time.time() - self.start_time < self.interval:
                return

            self.start_time = time.time()
            self.value = self.type(self.value)

            if self.reverse:
                if ceil(self.current()) <= self.startv: self.start_time = None
            else:
                if self.current() >= self.endv: self.start_time = None

    def current(self):
        if self.reverse:
            return self.endv - (self.value * (self.endv-self.startv))
        else:
            return self.value * (self.endv-self.startv)



class ImageBox(QLabel):
    def __init__(self, source, keepAspectRatio=True, smoothScale=True):
        super().__init__()

        self.source = source
        self.animated = False

        self.keepAspectRatio = keepAspectRatio
        self.smoothScale = smoothScale

        if self.source is not None: self.setSource(self.source)

    def setSource(self, source):
        self.source = source

        if self.source.startswith("http"):

            if self.source.endswith(".gif"):
                r = requests.get(self.source)

                with open("temp.gif", "wb") as f:
                    f.write(r.content)

                self.animated = True
                self.orgmovie = QMovie("temp.gif")
                self.movie = self.orgmovie
                self.setMovie(self.movie)
                self.movie.start()

            else:
                r = requests.get(self.source)

                self.animated = False
                self.orgpixmap = QPixmap.fromImage(QImage.fromData(r.content))
                self.pixmap = self.orgpixmap
                self.setPixmap(self.pixmap)

        else:
            if source.endswith(".gif"):
                self.animated = True
                self.movie = QMovie(source)
                self.setMovie(self.movie)
                self.movie.start()

            else:
                self.animated = False
                self.orgpixmap = QPixmap(source)
                self.pixmap = QPixmap(source)
                self.setPixmap(self.pixmap)

        self.resizeEvent(None)
    
    def resizeEvent(self, event):
        w, h = self.width(), self.height()

        t = (Qt.FastTransformation, Qt.SmoothTransformation)[self.smoothScale]
        k = (Qt.IgnoreAspectRatio, Qt.KeepAspectRatio)[self.keepAspectRatio]

        if self.animated:
            self.movie.setScaledSize(QSize(w, h))

        else:
            self.pixmap = self.orgpixmap.scaled(w, h, transformMode=t, aspectRatioMode=k)
            self.setPixmap(self.pixmap)



class ColorPreview(QWidget):
    def __init__(self):
        super().__init__()

        self.color = QColor(0, 0, 0)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("#000000")
        self.layout.addWidget(self.label, alignment=Qt.AlignBottom|Qt.AlignHCenter)

        self.setFixedSize(90, 65)

    def setColor(self, color):
        self.color = color
        self.label.setText(self.color.name())

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing)

        pt.setPen(QPen(QColor(0, 0, 0, 0)))
        pt.setBrush(QBrush(QColor(225, 225, 225)))

        pt.drawRoundedRect(0, 0, self.width(), self.height(), 9, 9)

        pt.setBrush(QBrush(self.color))

        pt.drawRoundedRect(15, 15, self.width()-30, self.height()-45, 4, 4)

        pt.end()



class ColorPicker(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self):
        super().__init__()

        self.color = None

        self.radius = 110
        self.setFixedSize(self.radius*2, self.radius*2)

        self.mouse_x, self.mouse_y = 0, 0

    def mouseMoveEvent(self, event):
        self.mouse_x, self.mouse_y = event.x(), event.y()

        dist = sqrt(pow(self.mouse_x-self.radius, 2)+pow(self.mouse_y-self.radius, 2))

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing)

        # TODO: Complete optimized color wheel & picker are and cursor

        for i in range(self.width()):
            for j in range(self.height()):
                color = QColor(255, 255, 255, 255)
                h = (atan2(i-self.radius, j-self.radius)+pi)/(2.*pi)
                s = sqrt(pow(i-self.radius, 2)+pow(j-self.radius, 2))/self.radius
                v = 1.0

                rr = 0.65

                ww = self.width()/(rr*5.72)
                hh = self.height()/(rr*5.72)

                if rr < s < 1.0:
                    color.setHsvF(h, s, v, 1.0)
                    pt.setPen(color)
                    pt.drawPoint(i, j)


                elif ww < i < self.width()-ww and hh < j < self.height()-hh:
                    h = 0.8
                    s = (i - ww) / (self.width()-ww*2)
                    v = 1-((j - hh) / (self.height()-hh*2))

                    hh = int(h*360)
                    ss = int(s*255)
                    vv = int(v*255)
                    color.setHsv(hh, ss, vv)
                    pt.setPen(color)
                    pt.drawPoint(i, j)

        # center = QPointF(self.width()/2, self.height()/2)
        # p = QPainter(self)
        # hsv_grad = QConicalGradient(center, 90)
        # for deg in range(360):
        #     col = QColor.fromHsvF(deg / 360, 1, self.v)
        #     hsv_grad.setColorAt(deg / 360, col)
        #
        # val_grad = QRadialGradient(center, self.radius)
        # val_grad.setColorAt(0.0, QColor.fromHsvF(0.0, 0.0, self.v, 1.0))
        # val_grad.setColorAt(1.0, Qt.transparent)
        #
        # p.setPen(Qt.transparent)
        # p.setBrush(hsv_grad)
        # p.drawEllipse(self.rect())
        # p.setBrush(val_grad)
        # p.drawEllipse(self.rect())

        pt.end()



class StyledButton(QAbstractButton):

    defaultStyles = ("flat", "hyper")

    def __init__(self, text="", style="flat", icon=None, fixedBottom=False):
        super().__init__()

        self.text = text

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if self.text:
            self.textLbl = QLabel(self.text)
            self.layout.addWidget(self.textLbl, alignment=Qt.AlignCenter)

        self._icon = None
        if icon is not None:
            self.setIcon(icon)

        # TODO: find a better way for opacity
        self.opacity = QGraphicsOpacityEffect(self)
        self.opacity.setOpacity(1.00)
        self.setGraphicsEffect(self.opacity)

        if style not in StyledButton.defaultStyles:
            raise Exception(f"'{style}' is not a default style.")
        self.style = style

        self.dropShadow = False
        self.shadow = None

        self.width = 135
        self.height = 45

        self.rounded = True
        self.borderRadius = 6

        if self.style == "flat":
            self.anim = AnimationHandler(self, 0, 5, Animation.easeOutCubic)
            self.animcirc = AnimationHandler(self, 0, 100, Animation.easeOutSine)
            self.animcirc.interval = 25 / 1000

            self.borderColor = QColor(52, 189, 235)
            self.borderWidth = 2
            self.backgroundColor = QColor(255, 255, 255)

            self.hoverLighter = False
            self.hoverFactor = 1

        elif self.style == "hyper":
            self.animline = AnimationHandler(self, 0, 1, Animation.easeOutCubic)
            self.animline.value = 0

            self.borderColor = QColor(235, 52, 91)
            self.borderWidth = 4

            self.fixedBottom = fixedBottom

        self.circleColor = self.borderColor.lighter(166)

        self._press_reset = False
        self.mouse_x, self.mouse_y = 0, 0

        self.setMinimumSize(self.width+2, self.height+2)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.setFixedSize(self.width+2, self.height+2)
        self._icon.resize(self.width/2, self.height/2)
        self.update()

    def setIcon(self, filepath):
        self._icon = ImageBox(filepath)
        self._icon.resize(18, 18)
        if self.text:
            self.layout.insertWidget(0, self._icon, alignment=Qt.AlignVCenter|Qt.AlignRight)
            self.layout.addSpacing(30)
        else:
            self.layout.insertWidget(0, self._icon, alignment=Qt.AlignCenter)

    def setDropShadow(self, bshad):
        if bshad:
            self.dropShadow = True
            if self.shadow is None:
                self.shadow = QGraphicsDropShadowEffect(self)
                self.shadow.setBlurRadius(6)
                self.shadow.setColor(QColor(0, 0, 0, 100))
                self.shadow.setOffset(0, 2)
                self.setGraphicsEffect(self.shadow)

        else:
            self.dropShadow = False
            self.shadow.setColor(QColor(0, 0, 0, 0))

    def update(self, *args, **kwargs):
        if self.style == "flat":
            self.anim.update()
            self.animcirc.update()
        elif self.style == "hyper":
            self.animline.update()
        super().update(*args, **kwargs)

    def enterEvent(self, event):
        if self.style == "flat": self.anim.start()
        elif self.style == "hyper": self.animline.start()

    def leaveEvent(self, event):
        if not self._press_reset and self.style == "flat":
            self.anim.start(reverse=True)
        if self.style == "hyper":
            self.animline.start(reverse=True)
        self._press_reset = False

    def mousePressEvent(self, event):
        self.mouse_x, self.mouse_y = event.x(), event.y()
        if self.style == "flat":
            self.animcirc.start()
            if not self._press_reset:
                self.anim.start(reverse=True)
                self._press_reset = True
        super().mousePressEvent(event)

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing)

        if self.style == "flat":
            if self.isEnabled():
                pen = QPen(self.borderColor, self.borderWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                if self.hoverLighter: brush = QBrush(self.backgroundColor.lighter(100+self.anim.current()*self.hoverFactor))
                else: brush = QBrush(self.backgroundColor.darker(100+self.anim.current()*self.hoverFactor))
            else:
                pen = QPen(self.borderColor.darker(106), self.borderWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                brush = QBrush(self.backgroundColor.darker(103))
            pt.setPen(pen)
            pt.setBrush(brush)

            if self.rounded:
                pt.drawRoundedRect(1, 1, self.width, self.height, self.borderRadius, self.borderRadius)

            pt.setPen(QPen(QColor(0, 0, 0, 0), 0))
            c = QColor(self.circleColor.red(), self.circleColor.green(), self.circleColor.blue(), 255-(self.animcirc.current()*2.5))
            pt.setBrush(QBrush(c, Qt.SolidPattern))

            pt.drawEllipse(self.mouse_x-self.animcirc.current()/1,
                                self.mouse_y-self.animcirc.current()/1,
                                self.animcirc.current()*2,
                            self.animcirc.current()*2)

        elif self.style == "hyper":
            if self.isEnabled():
                pen = QPen(self.borderColor, self.borderWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            else:
                pen = QPen(self.borderColor.darker(110), self.borderWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            pt.setPen(pen)

            if self.fixedBottom: a = 1
            else: a = self.animline.current()

            pt.drawLine(self.width//2, self.height, self.width//2+(a*(self.width//2)), self.height)
            pt.drawLine(self.width//2, self.height, self.width//2+(a*(self.width//-2)), self.height)

        pt.end()
        if self.style == "flat":
            if not self.anim.done(): self.update()
            if not self.animcirc.done(): self.update()
        elif self.style == "hyper":
            if not self.animline.done(): self.update()



class ToggleSwitch(QWidget):

    defaultStyles = ("win10", "ios", "android")
    toggled = pyqtSignal(name="toggled")

    def __init__(self, text="", style="win10", on=False):
        super().__init__()

        self.text = text

        self.on = on

        # TODO: find a better way for opacity
        self.opacity = QGraphicsOpacityEffect(self)
        self.opacity.setOpacity(1.00)
        self.setGraphicsEffect(self.opacity)

        if style not in ToggleSwitch.defaultStyles:
            raise Exception(f"'{style}' is not a default style.")
        self.style = style


        if self.style == "win10":
            self.onColor  = QColor(0, 116, 208)
            self.offColor = QColor(0, 0, 0)

            self.handleAlpha = True
            self.handleColor = QColor(255, 255, 255)

            self.width = 35
            self.radius = 26

        elif self.style == "ios":
            self.onColor  = QColor(73, 208, 96)
            self.offColor = QColor(250, 250, 250)

            self.handleAlpha = False
            self.handleColor = QColor(255, 255, 255)

            self.width = 21
            self.radius = 29

        elif self.style == "android":
            self.onColor  = QColor(0, 150, 136)
            self.offColor = QColor(255, 255, 255)

            self.handleAlpha = True
            self.handleColor = QColor(255, 255, 255)

            self.width = 35
            self.radius = 26

        self.setMinimumSize(self.width + (self.radius*2) + (len(self.text)*10), self.radius+2)

        self.anim = AnimationHandler(self, 0, self.width, Animation.easeOutCirc)
        if self.on: self.anim.value = 1

    def desaturate(self, color):
        cc = getattr(self, color)
        h = cc.hue()
        if h < 0: h = 0
        s = cc.saturation()//4
        if s > 255: s = 255
        c = QColor.fromHsv(h, s, cc.value())
        setattr(self, color, c)

    def saturate(self, color):
        cc = getattr(self, color)
        h = cc.hue()
        if h < 0: h = 0
        s = cc.saturation()*4
        if s > 255: s = 255
        c = QColor.fromHsv(h, s, cc.value())
        setattr(self, color, c)

    def update(self, *args, **kwargs):
        self.anim.update()
        super().update(*args, **kwargs)

    def mousePressEvent(self, event):
        if self.isEnabled():
            if self.on:
                self.on = False
                self.anim.start(reverse=True)
            else:
                self.on = True
                self.anim.start()
            self.update()

            self.toggled.emit()

    def changeEvent(self, event):
        if event.type() == QEvent.EnabledChange:
            if self.isEnabled():
                self.saturate("onColor")
                self.saturate("offColor")
                self.saturate("handleColor")
                self.opacity.setOpacity(1.00)
            else:
                self.desaturate("onColor")
                self.desaturate("offColor")
                self.desaturate("handleColor")
                self.opacity.setOpacity(0.4)

            self.update()

        else:
            super().changeEvent(event)

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing)

        if self.style == "win10":

            if self.on:
                pen = QPen(self.onColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)
                brush = QBrush(self.onColor)
                pt.setBrush(brush)


                r = self.radius
                w = self.width

                pt.drawChord(r, 1, r, r, 90*16, 180*16)
                pt.drawChord(r+w, 1, r, r, -90*16, 180*16)
                pt.drawRect(r+r//2, 1, w, r)

                if self.handleAlpha: pt.setBrush(pt.background())
                else: pt.setBrush(QBrush(self.handleColor))
                offset = r*0.4
                pt.drawEllipse(r+offset/2+self.anim.current() , 1+offset/2 , r-offset , r-offset)

            else:
                pen = QPen(self.offColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)

                r = self.radius
                w = self.width

                pt.drawArc(r, 1, r, r, 90*16, 180*16)
                pt.drawArc(r+w, 1, r, r, -90*16, 180*16)
                pt.drawLine(r+r//2, 1, r+w+r//2, 1)
                pt.drawLine(r+r//2, r+1, r+w+r//2, r+1)

                brush = QBrush(self.offColor)
                pt.setBrush(brush)
                offset = r*0.4
                pt.drawEllipse(r+offset/2+self.anim.current() , offset/2+1 , r-offset , r-offset)

        elif self.style == "ios":

            if self.on:
                pen = QPen(self.onColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)
                brush = QBrush(self.onColor)
                pt.setBrush(brush)

                r = self.radius
                w = self.width

                pt.drawChord(r, 1, r, r, 90*16, 180*16)
                pt.drawChord(r+w, 1, r, r, -90*16, 180*16)
                pt.drawRect(r+r//2, 1, w, r)

                if self.handleAlpha: pt.setBrush(pt.background())
                else: pt.setBrush(QBrush(self.handleColor))
                offset = r*0.025
                pt.drawEllipse(r+offset/2+self.anim.current() , 1+offset/2 , r-offset , r-offset)

            else:
                pen = QPen(self.offColor.darker(135), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)
                brush = QBrush(self.offColor)
                pt.setBrush(brush)

                r = self.radius
                w = self.width

                pt.drawChord(r, 1, r, r, 90*16, 180*16)
                pt.drawChord(r+w, 1, r, r, -90*16, 180*16)
                pt.drawRect(r+r//2, 1, w, r)
                pt.setPen(QPen(self.offColor))
                pt.drawRect(r+r//2-2, 2, w+4, r-2)

                if self.handleAlpha: pt.setBrush(pt.background())
                else: pt.setBrush(QBrush(self.handleColor))
                pt.setPen(QPen(self.handleColor.darker(160)))
                offset = r*0.025
                pt.drawEllipse(r+offset/2+self.anim.current() , 1+offset/2 , r-offset , r-offset)

        elif self.style == "android":

            if self.on:
                pen = QPen(self.onColor.lighter(145), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)
                brush = QBrush(self.onColor.lighter(145))
                pt.setBrush(brush)

                r = self.radius
                w = self.width

                pt.drawChord(r+r//4, 1+r//4, r//2, r//2, 90*16, 180*16)
                pt.drawChord(r+w+r//4, 1+r//4, r//2, r//2, -90*16, 180*16)
                pt.drawRect(r+r//2, 1+r//4, w, r//2)

                pt.setBrush(QBrush(self.onColor))
                pt.setPen(QPen(self.onColor))
                pt.drawEllipse(r+self.anim.current(), 1 , r, r)

            else:
                pen = QPen(self.offColor.darker(130), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                pt.setPen(pen)
                brush = QBrush(self.offColor.darker(130))
                pt.setBrush(brush)

                r = self.radius
                w = self.width

                pt.drawChord(r+r//4, 1+r//4, r//2, r//2, 90*16, 180*16)
                pt.drawChord(r+w+r//4, 1+r//4, r//2, r//2, -90*16, 180*16)
                pt.drawRect(r+r//2, 1+r//4, w, r//2)

                pt.setBrush(QBrush(self.offColor))
                pt.setPen(QPen(self.offColor.darker(140)))
                pt.drawEllipse(r+self.anim.current(), 1 , r, r)

        font = pt.font()
        pt.setFont(font)
        pt.setPen(QPen(Qt.black))

        pt.drawText(w+r*2+10, r//2+r//4, self.text)

        pt.end()

        if not self.anim.done(): self.update()
