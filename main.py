from PyQt5.QtWidgets import (QPushButton,
                                QApplication,
                                QWidget,
                                QGridLayout,
                                QLineEdit,
                                QVBoxLayout,
                                QHBoxLayout,
                                QLabel,
                                QGroupBox)
from PyQt5.QtGui import (QCursor,QMovie,QPainter,QFont)
from PyQt5.QtCore import Qt
from Modules.jsonHelper import writeJ, readJ
from Modules.weather import weather
class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 50, 1200, 680)
        self.setFixedSize(1200, 680)
        self.movie = QMovie("Databases/weather.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.showLayouts()
        
    def showLayouts(self):
        self.East_Area_Layout = self.eastArea()
        self.West_Area_Layout = self.westArea()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.West_Area_Layout,0,0)
        self.mainLayout.addWidget(self.East_Area_Layout,0,1)
        self.setLayout(self.mainLayout)

    def eastArea(self):
        self.eastGroupBox = QGroupBox()
        self.eastLayout = QVBoxLayout()
        self.northeastLayout = QHBoxLayout()

        self.icon = QPushButton(self)  
        self.northeastLayout.addWidget(self.icon)

        self.degree = QLabel(self)
        self.northeastLayout.addWidget(self.degree)

        self.northeastLayout.addSpacing(300)

        
        self.date = QLabel(self)
        self.northeastLayout.addWidget(self.date)
        self.northeastLayout.setAlignment(Qt.AlignTop)
        self.eastLayout.addLayout(self.northeastLayout)
        self.eastGroupBox.setLayout(self.eastLayout)
        return self.eastGroupBox

    def westArea(self):
        self.westGroupBox = QGroupBox()
        self.westLayout = QVBoxLayout()
        self.westGroupBox.setFixedWidth(300)

        self.searchbar = QLineEdit(self)
        self.westLayout.addWidget(self.searchbar)
        self.favorite_cities = readJ("Databases/favorite_cities.json")

        if not (not self.favorite_cities['names_of_cities']):
            for i in self.favorite_cities['names_of_cities']:
                button = QPushButton(self,text=i.capitalize())
                text = button.text()
                button.clicked.connect(lambda ch, text=text : self.havadurumu(text))
                button.setStyleSheet("""background-color: #aad8d3;
                                        color: #222222;
                                        border:2px solid #aad8d3;
                                        border-radius: 25px;""")
                button.setCursor(QCursor(Qt.PointingHandCursor))
                button.setFixedHeight(50)
                button.setFont(QFont('Times', 15))
                self.westLayout.addWidget(button)

        self.westLayout.setAlignment(Qt.AlignTop)
        self.westGroupBox.setLayout(self.westLayout)
        self.westGroupBox.setStyleSheet("border:2px solid #079096;border-top-left-radius: 30px;border-bottom-left-radius: 30px;background-color: #079096;")
        return self.westGroupBox

    def havadurumu(self, city_name:str):
        self.weather = weather(city_name)['result'][0]
        print(self.weather)
        #self.icon.setStyleSheet(f"background-image: url({self.weather['icon']});")
        self.degree.setText(f"Hava {self.weather['description'].capitalize()} {self.weather['degree']}°C\nEn Az: {self.weather['min']} En Fazla: {self.weather['max']} Nem: {self.weather['humidity']}")
        self.date.setText(f"{self.weather['date']}\n{self.weather['day']}")

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
