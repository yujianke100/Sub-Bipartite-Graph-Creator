import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QMessageBox, QSplashScreen
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from Ui_design import Ui_Form
from crawler import get_datasets, downloader
from unpacker import unpacker
from data_cut import data_cal
from get_data import get_data

class main_window(QMainWindow,Ui_Form):
    def __init__(self,parent = None):
        super(main_window, self).__init__(parent)
        self.setupUi(self)
        self.next.clicked.connect(self.on_click_next)
        self.quit.clicked.connect(self.on_click_quit)
        self.fresh_scroll()

    def on_click_next(self):
        self.next.setEnabled(False)
        self.quit.setEnabled(False)
        selected_list = list(self.selected_set)
        for i in selected_list:
            print('downloading {}'.format(i))
            downloader(i)
        for i in selected_list:
            print('unpacking {}'.format(i))
            unpacker(i)
        data_cal(selected_list)
        get_data()
        sys.exit()


    def on_click_quit(self):
        sys.exit()

    def fresh_scroll(self):
        lh = QHBoxLayout()
        lv = QVBoxLayout()
        w = QWidget()
        self.setCentralWidget(w)
        w.setLayout(lv)
        self.check_box = []
        self.selected_set = set()
        self.data_list, self.data_len, self.useful_dataset_num = get_datasets()
        for i in self.data_list:
            self.check_box.append(QCheckBox("{:<5}| {:<25}| n:{:^10}| e:{:^10}".format(i[0], i[1], i[2], i[3]), self))
            self.check_box[-1].stateChanged.connect(self.check_box_select)
            lv.addWidget(self.check_box[-1])
        self.scrollArea.setWidget(w)

    def check_box_select(self):
        for i in range(len(self.check_box)):
            if(self.check_box[i].isChecked()):
                self.selected_set.update([self.data_list[i][4]])
            else:
                try:
                    self.selected_set.remove(self.data_list[i][4])
                except:
                    pass

def gui():
    #启动界面https://blog.csdn.net/weixin_41259130/article/details/88736136
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(r"splash.png"))
    splash.show()
    app.processEvents()
    gui = main_window()
    gui.show()
    splash.finish(gui)
    sys.exit(app.exec_())

if __name__ =='__main__':
    gui()
    