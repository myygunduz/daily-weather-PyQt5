from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QPoint
class CustomTitleBar(QWidget):
    def __init__(self,parent, title):
        super(CustomTitleBar,self).__init__()
        self.parent = parent

        self.Title = QLabel(self, text = title)
        self.Title.setFont(QFont('Times', 15))
        self.Title.setFixedHeight(35)

        self.MinimizeWindowButton = QPushButton(self, text = "▁")
        self.MinimizeWindowButton.clicked.connect(self.btn_min_clicked)
        self.MinimizeWindowButton.setFixedSize(35,28)

        self.CloseWindowButton = QPushButton(self, text = "✖")
        self.CloseWindowButton.clicked.connect(self.btn_close_clicked)
        self.CloseWindowButton.setFixedSize(35,28)


        self.Layout = QHBoxLayout()
        self.Layout.setAlignment(Qt.AlignCenter)
        self.Layout.setContentsMargins(0,0,0,0)
        self.Layout.addWidget(self.Title)
        self.Layout.addWidget(self.MinimizeWindowButton)
        self.Layout.addWidget(self.CloseWindowButton)
        self.Layout.addSpacing(10)

        self.setLayout(self.Layout)
        self.start = QPoint(0, 0)
        self.pressing = False
    def resizeEvent(self, QResizeEvent):
        super(CustomTitleBar, self).resizeEvent(QResizeEvent)
        self.Title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()