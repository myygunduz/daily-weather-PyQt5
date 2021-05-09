from PyQt5.QtWidgets import (QPushButton,
                                QApplication,
                                QWidget,
                                QGridLayout,
                                QLineEdit,
                                QVBoxLayout,
                                QHBoxLayout,
                                QLabel,
                                QCompleter,
                                QGroupBox)
from PyQt5.QtGui import (QCursor,
                        QMovie,
                        QPainter,
                        QFont,
                        QIcon,
                        QPixmap)
from PyQt5.QtCore import Qt,QSize
from Modules.customwidgets import ImageBox
from Modules.jsonHelper import writeJ, readJ
from Modules.weather import weather
class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 50, 1200, 680)
        self.setFixedSize(1200,680)
        
        self.css = readJ("Databases/Jsons/css.json")
        self.citiesJson = readJ("Databases/Jsons/cities.json")

        self.movie = QMovie("Databases/Images/weather.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        self.showLayouts()
        
    def showLayouts(self):
        self.East_Area_Layout = self.eastArea()
        self.West_Area_Layout = self.westArea()

        self.SouthLayout = QGridLayout()
        self.SouthLayout.addWidget(self.West_Area_Layout,0,0)
        self.SouthLayout.addWidget(self.East_Area_Layout,0,1)

        self.setLayout(self.SouthLayout)
    def eastArea(self):
        self.icon = ImageBox(source = "")  
        self.icon.setFixedSize(120,120)

        self.degree = QLabel(self)
        self.degree.setFont(QFont('Times', 15))

        self.date = QLabel(self)
        self.date.setFont(QFont('Times', 15))


        self.northeastLayout = QHBoxLayout()
        self.northeastLayout.setAlignment(Qt.AlignLeft)
        self.northeastLayout.addWidget(self.icon)
        self.northeastLayout.addSpacing(20)
        self.northeastLayout.addWidget(self.degree)
        self.northeastLayout.addSpacing(300)
        self.northeastLayout.addWidget(self.date)


        self.cityname = QLabel(self,text="Şehir Seçmeniz Gerekiyor")
        self.cityname.setAlignment(Qt.AlignCenter)
        self.cityname.setFont(QFont('Times', 30))

        self.favoritebutton = QPushButton(self)
        self.favoritebutton.clicked.connect(self.settingFavoriteCity)
        self.favoritebutton.setFixedSize(50,50)
        self.favoritebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.favoritebutton.setIconSize(QSize(50,50))

        self.eastLayout = QVBoxLayout()
        self.eastLayout.addWidget(self.cityname)
        self.eastLayout.addLayout(self.northeastLayout)
        self.eastLayout.addSpacing(600)
        self.eastLayout.addWidget(self.favoritebutton)
        

        self.eastGroupBox = QGroupBox()
        self.eastGroupBox.setLayout(self.eastLayout)

        self.eastGroupBox.setStyleSheet("".join(i for i in self.css['eastGroupBox']))
        self.cityname.setStyleSheet("".join(i for i in self.css['cityname']))
        self.icon.setStyleSheet("".join(i for i in self.css['icon']))
        self.degree.setStyleSheet("".join(i for i in self.css['degree']))
        self.date.setStyleSheet("".join(i for i in self.css['date']))
        self.favoritebutton.setStyleSheet("".join(i for i in self.css['favoritebutton']))
        
        

        return self.eastGroupBox

    def westArea(self):
        self.westGroupBox = QGroupBox()
        self.westLayout = QVBoxLayout()
        self.westGroupBox.setFixedWidth(300)
        
        Completer = QCompleter(self.citiesJson['cities'])
        Completer.popup().setFont(QFont('Times', 15))
        self.searchbar = QLineEdit(self)
        self.searchbar.setCompleter(Completer)
        self.searchbar.setFixedHeight(50)
        self.searchbar.setFont(QFont('Times', 15))
        self.searchbar.setPlaceholderText("Şehir İsmi Girin")
        self.searchbar.textChanged.connect(self.searchFavorite)
        self.searchbar.setAlignment(Qt.AlignCenter)


        self.searchbutton = QPushButton()
        self.searchbutton.clicked.connect(lambda: self.getWeatherInfo(self.searchbar.text()))
        self.searchbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.searchbutton.setFixedSize(50,50)

        self.searchGroupBox = QGroupBox()
        self.searchLayout= QHBoxLayout()

        self.searchLayout.addWidget(self.searchbar)
        self.searchLayout.addWidget(self.searchbutton)


        self.searchGroupBox.setLayout(self.searchLayout)
        self.westLayout.addWidget(self.searchGroupBox)

        self.buttons = []
        if len(self.citiesJson['favorite_cities']):
            for i in self.citiesJson['favorite_cities']:
                self.createbutton(i)

        self.westLayout.setAlignment(Qt.AlignTop)
        self.westGroupBox.setLayout(self.westLayout)
        Completer.popup().setStyleSheet("".join(i for i in self.css['Completer']))
        self.westGroupBox.setStyleSheet("".join(i for i in self.css['westGroupBox']))
        self.searchbar.setStyleSheet("".join(i for i in self.css['searchbar']))
        self.searchbutton.setStyleSheet("".join(i for i in self.css['searchbutton']))
        self.searchGroupBox.setStyleSheet("".join(i for i in self.css['searchGroupBox']))

        return self.westGroupBox

    def getWeatherInfo(self, city_name:str):
        self.searchbar.setText("")
        if self.cityname.text().lower() != city_name.lower():
            try:
                self.weather = weather(city_name)['result'][0]
                print(self.weather)

                self.cityname.setText(city_name.capitalize())
                self.icon.setSource(self.weather['icon'])
                self.degree.setText(f"Hava {self.weather['description'].capitalize()} {self.weather['degree']}°C\nEn Az: {self.weather['min']} En Fazla: {self.weather['max']} Nem: {self.weather['humidity']}")
                self.date.setText(f"{self.weather['date']}\n{self.weather['day']}")
                
                heart_mode = "heartFalse"
                if city_name.lower() in self.citiesJson['favorite_cities']: heart_mode = "heartTrue"
                
                self.favoritebutton.setIcon(QIcon(f"Databases/Images/{heart_mode}.png"))
            except IndexError:
                self.searchbar.setText("Şehir Bulunamadı")
    
    def settingFavoriteCity(self):
        cityname=self.cityname.text().lower()
        if cityname.strip() in self.citiesJson['favorite_cities'] :
            index = self.citiesJson['favorite_cities'].index(cityname)
            self.citiesJson['favorite_cities'].pop(index)
            self.buttons[index].destroy()
            self.westLayout.removeWidget(self.buttons[index])
            self.buttons.pop(index)
            self.favoritebutton.setIcon(QIcon(f"Databases/Images/heartFalse.png"))
            print(cityname+" silindi")
        else:
            self.citiesJson['favorite_cities'].append(cityname.strip())
            self.createbutton(cityname)
            self.favoritebutton.setIcon(QIcon(f"Databases/Images/heartTrue.png"))
        writeJ(self.citiesJson,"Databases/Jsons/cities.json")

    def createbutton(self,text):
        button = QPushButton(self,text=text.capitalize())
        button.clicked.connect(lambda ch, text=text : self.getWeatherInfo(text))
        button.setStyleSheet("".join(i for i in self.css['fovorite_buttons']))
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setFixedHeight(50)
        button.setFont(QFont('Times', 15))
        self.buttons.append(button)
        self.westLayout.addWidget(button)
    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
    def searchFavorite(self,text):
        x = 0
        for button in self.buttons:
            if text.lower() not in button.text().lower():
                x+=1   
            if text.lower() in button.text().lower():
                button.show()
            else:
                if x == len(self.buttons):
                    for button in self.buttons:
                        button.show()
                    return
                button.hide()
if __name__ == '__main__':
    app = QApplication([])
    Interface = Interface()

    Interface.show()
    app.exec_()
