import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QSplashScreen, QLabel, QDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from Ui_design import Ui_Form
from crawler import get_datasets, downloader
from unpacker import unpacker
from data_cut import data_cal
from get_data import get_data
import time
import threading

class main_window(Ui_Form):
    def __init__(self):
        super(main_window, self).__init__()
        self.load_flag = 1
    
    def ui_init(self):
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
        data_cal(selected_list, self.gap_num.value(), self.min_box.value(), self.max_box.value())
        get_data()
        sys.exit()

    def on_click_quit(self):
        sys.exit()

    def generate_label(self, name):
        temp_label = QLabel()
        temp_label.setText(name)
        temp_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        return temp_label

    def fresh_scroll(self):
        lv = QVBoxLayout()
        v = QWidget()
        v.setLayout(lv)
        self.check_box = []
        self.selected_set = set()
        self.data_list, self.data_len, self.useful_dataset_num = get_datasets()
        for i in self.data_list:
            lh = QHBoxLayout()
            self.check_box.append(QCheckBox('{:<5}'.format(i[0])))
            lh.addWidget(self.check_box[-1],stretch=5)
            self.check_box[-1].stateChanged.connect(self.check_box_select)
            #https://blog.csdn.net/Nin7a/article/details/104533138
            temp_label1 = QLabel()
            temp_label1.setLineWidth(5)
            lh.addWidget(self.generate_label(i[1]),stretch=30)
            lh.addWidget(self.generate_label(i[2]),stretch=10)
            lh.addWidget(self.generate_label(i[3]),stretch=10)

            lv.addLayout(lh)
        self.scrollArea.setWidget(v)
        self.load_flag = 0

    def check_box_select(self):
        for i in range(len(self.check_box)):
            if(self.check_box[i].isChecked()):
                self.selected_set.update([self.data_list[i][4]])
            else:
                try:
                    self.selected_set.remove(self.data_list[i][4])
                except:
                    pass
    

class MySplashScreen(QSplashScreen):
    def mousePressEvent(self, event):
        pass

class MyThread(threading.Thread):
    #https://www.jianshu.com/p/ebecd0667aee
    def __init__(self , threadName, splash):
        super(MyThread,self).__init__(name=threadName)
        self.splash = splash
    def run(self):
        global count
        for i in range(100):
            try:
                self.splash.showMessage("正在读取数据集，已经过{}秒".format(i), Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
                time.sleep(1)
            except:
                break
            
            

def main():
    #启动界面https://blog.csdn.net/ye281842_/article/details/109637580
    app = QApplication(sys.argv)
    splash = MySplashScreen()
    splash.setPixmap(QPixmap('./splash.png'))  # 设置背景图片
    splash.setFont(QFont('微软雅黑', 10))
    splash.show()
    MyThread("waiting", splash).start()
    app.processEvents()
    Dialog = QDialog()
    ui = main_window()
    ui.setupUi(Dialog)
    ui.ui_init()
    Dialog.show()
    splash.finish(Dialog)
    splash.deleteLater()
    sys.exit(app.exec_())

if __name__ =='__main__':
    main()
    