import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QSplashScreen, QLabel, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QTextCursor
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEventLoop, QTimer
from Ui_design import Ui_Form
from crawler import get_datasets, downloader
from unpacker import unpacker
from data_cut import data_cal
from get_data import get_data
import time
import threading


class EmittingStream(QObject):
    # https://blog.csdn.net/william_munch/article/details/89425038
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec_()


class main_window(Ui_Form):
    def __init__(self):
        super(main_window, self).__init__()

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def ui_init(self):
        self.generate.clicked.connect(self.on_click_generate)
        self.quit.clicked.connect(self.on_click_quit)
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)
        self.fresh_scroll()

    def element_switch(self, flag):
        self.generate.setEnabled(flag)
        self.quit.setEnabled(flag)
        self.max_box.setEnabled(flag)
        self.min_box.setEnabled(flag)
        self.gap_num.setEnabled(flag)

    def run(self, selected_list):
        for i in selected_list:
            print('downloading {}...'.format(i), end='')
            downloader(i)
            print('finished')
        for i in selected_list:
            print('unpacking {}...'.format(i), end='')
            unpacker(i)
            print('finished')
        data_cal(selected_list, self.gap_num.value(),
                 self.min_box.value(), self.max_box.value())
        get_data()

    def on_click_generate(self):
        self.element_switch(False)
        selected_list = []
        check_info = ''
        for i in self.selected_idx:
            selected_list.append(self.data_list[i][4])
            check_info += '{}:{}\n'.format(
                self.data_list[i][0], self.data_list[i][1])
        w = QWidget()
        reply = QMessageBox.question(w, 'Check', 'Selected datasets:\n{}'.format(
            check_info[:-1]), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            self.element_switch(True)
            return
        self.scrollArea.setEnabled(False)
        self.run(selected_list)
        self.scrollArea.setEnabled(True)
        self.element_switch(True)

    def on_click_quit(self):
        self.element_switch(False)
        sys.exit()

    def generate_label(self, name, style):
        tmp_label = QLabel()
        tmp_label.setText(name)
        tmp_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        tmp_label.setStyleSheet(style)
        return tmp_label

    def fresh_scroll(self):
        lv = QVBoxLayout()
        lv.setSpacing(0)
        v = QWidget()
        v.setLayout(lv)
        self.check_box = []
        self.selected_idx = set()
        self.data_list, self.data_len, self.useful_dataset_num = get_datasets()
        data_num = 0
        for i in self.data_list:
            if(data_num % 2):
                style = 'background-color:rgb(240,240,240); padding:5;'
            else:
                style = 'background-color:rgb(220,220,220); padding:5;'
            data_num += 1
            lh = QHBoxLayout()
            lh.setSpacing(0)
            btn = QCheckBox('{:<5}'.format(i[0]))
            btn.setStyleSheet(style)
            self.check_box.append(btn)
            lh.addWidget(self.check_box[-1], stretch=5)
            self.check_box[-1].stateChanged.connect(self.check_box_select)
            # https://blog.csdn.net/Nin7a/article/details/104533138
            lh.addWidget(self.generate_label(i[1], style), stretch=30)
            lh.addWidget(self.generate_label(i[2], style), stretch=10)
            lh.addWidget(self.generate_label(i[3], style), stretch=10)
            lv.addLayout(lh)
        self.scrollArea.setWidget(v)

    def check_box_select(self):
        for i in range(len(self.check_box)):
            if(self.check_box[i].isChecked()):
                self.selected_idx.update([i])
            else:
                try:
                    self.selected_idx.remove(i)
                except:
                    pass
        self.generate.setText('generate({})'.format(len(self.selected_idx)))


class MySplashScreen(QSplashScreen):
    def mousePressEvent(self, event):
        pass


class splash_thread(threading.Thread):
    # https://www.jianshu.com/p/ebecd0667aee
    def __init__(self, threadName, splash):
        super(splash_thread, self).__init__(name=threadName)
        self.splash = splash

    def run(self):
        for i in range(100):
            try:
                self.splash.showMessage('正在读取数据集，已经过{}秒'.format(
                    i), Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
                time.sleep(1)
            except:
                break


def main():
    # 启动界面https://blog.csdn.net/ye281842_/article/details/109637580
    app = QApplication(sys.argv)
    splash = MySplashScreen()
    splash.setPixmap(QPixmap('./splash.png'))  # 设置背景图片
    splash.setFont(QFont('微软雅黑', 10))
    splash.show()
    splash_thread('waiting', splash).start()
    app.processEvents()
    Dialog = QDialog()
    ui = main_window()
    ui.setupUi(Dialog)
    ui.ui_init()
    Dialog.show()
    splash.finish(Dialog)
    splash.deleteLater()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
