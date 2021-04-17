import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox
from Ui_design import Ui_Form

class main_window(QMainWindow,Ui_Form):
    def __init__(self,parent = None):
        super(main_window, self).__init__(parent)
        self.setupUi(self)
        self.next.clicked.connect(self.on_click_next)
        self.quite.clicked.connect(self.on_click_quite)
        self.fresh_scroll()

    def on_click_next(self):
        print(self.selected_idx)

    def on_click_quite(self):
        sys.exit()

    def fresh_scroll(self):
        lh = QHBoxLayout()
        lv = QVBoxLayout()
        w = QWidget()
        self.setCentralWidget(w)
        w.setLayout(lv)
        self.check_box = []
        self.selected_idx = []
        for i in range(10):
            self.selected_idx.append(False)
            self.check_box.append(QCheckBox(str(i), self))
            self.check_box[-1].stateChanged.connect(self.check_box_select)
            lv.addWidget(self.check_box[-1])
        self.scrollArea.setWidget(w)

    def check_box_select(self):
        for i in self.check_box:
            if(i.isChecked()):
                self.selected_idx[int(i.text())] = True
            else:
                self.selected_idx[int(i.text())] = False

if __name__ =='__main__':
    app = QApplication(sys.argv)
    gui = main_window()
    gui.show()
    sys.exit(app.exec_())