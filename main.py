# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QSplashScreen, QLabel, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QTextCursor
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, Qt, QTimer
from gui.Ui_design import Ui_Form
from utils.crawler import get_datasets, downloader
from utils.unpacker import unpacker
from utils.data_cut import data_cal
from utils.data_generate import data_generate

from time import strftime, localtime


splash_img = './gui/splash.png'


class EmittingStream(QObject):
    # https://blog.csdn.net/william_munch/article/details/89425038
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec_()


class main_window(Ui_Form):
    def __init__(self, splash):
        super(main_window, self).__init__()
        self.data_list_len = 0
        self.data_num = 0
        self.splash = splash

    def change_init_status(self, info):
        self.splash.showMessage(info, Qt.AlignHCenter |
                                Qt.AlignBottom, Qt.black)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def ui_init(self):
        self.generate.clicked.connect(self.on_click_generate)
        self.quit.clicked.connect(self.on_click_quit)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
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
        timestamp = strftime('%Y-%m-%d_%H-%M-%S', localtime())
        for i in selected_list:
            print('downloading {}...'.format(i), end='')
            downloader(i)
            print('finished')
        for i in selected_list:
            print('unpacking {}...'.format(i), end='')
            unpacker(i)
            print('finished')
        data_cal(selected_list, self.gap_num.value(),
                 self.min_box.value(), self.max_box.value(), timestamp)
        data_generate(timestamp)

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
        self.data_list = get_datasets(self)
        self.data_list_len = len(self.data_list)
        self.data_num = 0
        for i in self.data_list:
            style = """padding:10px; font-size:28px; font-family:"Times New Roman";"""
            if(self.data_num % 2):
                style += 'background-color:rgb(240,240,240);'
            else:
                style += 'background-color:rgb(220,220,220);'
            lh = QHBoxLayout()
            lh.setSpacing(0)
            btn = QCheckBox('{:<5}'.format(i[0]))
            btn.setStyleSheet(style)
            self.check_box.append(btn)
            lh.addWidget(self.check_box[-1], stretch=1)
            self.check_box[-1].stateChanged.connect(self.check_box_select)
            # https://blog.csdn.net/Nin7a/article/details/104533138
            lh.addWidget(self.generate_label(i[1], style), stretch=3)
            lh.addWidget(self.generate_label(i[2], style), stretch=1)
            lh.addWidget(self.generate_label(i[3], style), stretch=1)
            lv.addLayout(lh)

            self.data_num += 1
            self.change_init_status(
                'Loading datasets...({}/{})'.format(self.data_num, self.data_list_len))
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


def main():
    # 启动界面https://blog.csdn.net/ye281842_/article/details/109637580
    app = QApplication(sys.argv)
    splash = MySplashScreen()
    splash.setPixmap(QPixmap(splash_img))  # 设置背景图片
    splash.setFont(QFont('Times New Roman', 12))
    splash.show()
    app.processEvents()
    Dialog = QDialog()
    ui = main_window(splash)
    ui.setupUi(Dialog)
    ui.ui_init()
    Dialog.show()
    splash.finish(Dialog)
    splash.deleteLater()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
