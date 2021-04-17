import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from Ui_design import Ui_Form
 
class MyMainWindow(QMainWindow,Ui_Form):
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.next.clicked.connect(self.onClick_Next)
        self.quite.clicked.connect(self.onClick_Quite)

    def onClick_Next(self):
        pass

    def onClick_Quite(self):
        sys.exit()
    
if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())