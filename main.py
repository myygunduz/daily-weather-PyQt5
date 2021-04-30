from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.showLayouts()
        
    def showLayouts(self):
        # self.East_Area_Layout = self.eastArea()
        self.mainLayout = QGridLayout()
        # self.mainLayout.addLayout(self.East_Area_Layout,0,1)
        self.setLayout(self.mainLayout)

    def eastArea(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    Interface = Interface()

    Interface.show()
    app.exec_()
