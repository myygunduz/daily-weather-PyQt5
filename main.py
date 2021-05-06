from PyQt5.QtWidgets import (QPushButton,
                                QApplication,
                                QWidget,
                                QGridLayout,
                                QLineEdit,
                                QVBoxLayout,
                                QHBoxLayout,
                                QLabel,
                                QGroupBox)
from PyQt5.QtGui import (QMovie,QPainter)
from PyQt5.QtCore import Qt
from Modules.jsonHelper import writeJ, readJ
from Modules.weather import weather
class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 50, 1200, 680)
        self.setFixedSize(1200, 680)
        self.setStyleSheet(open("Databases/main.css","r").read())
        self.movie = QMovie("Databases/weather.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.showLayouts()
        
    def showLayouts(self):
        # self.East_Area_Layout = self.eastArea()
        self.West_Area_Layout = self.westArea()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.West_Area_Layout,0,0)
        # self.mainLayout.addLayout(self.East_Area_Layout,0,1)
        self.setLayout(self.mainLayout)

    def eastArea(self):
        self.northeastLayout = QHBoxLayout()
        

    def westArea(self):
        self.westGroupBox = QGroupBox()
        self.westLayout = QVBoxLayout()

        self.searchbar = QLineEdit(self)
        self.westLayout.addWidget(self.searchbar)
        self.favorite_cities = readJ("Databases/favorite_cities.json")

        if not (not self.favorite_cities['names_of_cities']):
            for i in self.favorite_cities['names_of_cities']:
                button = QPushButton(self,text=i)
                text = button.text()
                button.clicked.connect(lambda ch, text=text : self.havadurumu(text))
                self.westLayout.addWidget(button)

        self.westLayout.setAlignment(Qt.AlignTop)
        self.westGroupBox.setLayout(self.westLayout)
        self.westGroupBox.setObjectName("westLayout")
        return self.westGroupBox
    def havadurumu(self, city_name:str):
        #print(weather(city_name))
        pass
    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

if __name__ == '__main__':
    app = QApplication([])
    Interface = Interface()

    Interface.show()
    app.exec_()
