import os
import sys

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QMessageBox

from config import Config
from rest_thread import RestThread
from ui import Ui_MainWindow

config_file = "personal-assistant.ini"
is_windows = os.name == "nt"
use_shell = is_windows


class MainWindow(QMainWindow, Ui_MainWindow):
    notify_message_box_signal = pyqtSignal(str)
    update_work_progress_signal = pyqtSignal(int)
    update_rest_progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.debug = os.getenv('PA_DEBUG') == "true"
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(":/icon.png"))
        self.tray.setVisible(True)
        self.menu = QMenu()
        self.menu.setFont(self.centralwidget.font())
        show_action = self.menu.addAction("设置")
        show_action.triggered.connect(self.show)
        quit_action = self.menu.addAction("退出")
        quit_action.triggered.connect(self.quit)
        self.tray.setContextMenu(self.menu)
        self.restStopBtn.setDisabled(True)
        self.config = Config(config_file)
        if 'workInterval' in self.config:
            self.workSpinBox.setValue(int(self.config['workInterval'].split(' ')[0]))
        else:
            self.config['workInterval'] = '20'
        self.workSpinBox.textChanged.connect(lambda v: self.update_config("workInterval", v))
        if 'restInterval' in self.config:
            self.restSpinBox.setValue(int(self.config['restInterval'].split(' ')[0]))
        else:
            self.config['restInterval'] = '60'
        self.restSpinBox.textChanged.connect(lambda v: self.update_config("restInterval", v))
        self.remind_methods = ['消息提醒', '弹窗提醒', '全屏覆盖', '显示桌面']
        if 'remindMethod' in self.config:
            remind_method = self.config['remindMethod']
            if remind_method in self.remind_methods:
                idx = self.remind_methods.index(remind_method)
            else:
                idx = 0
            self.methodComboBox.setCurrentIndex(idx)
        else:
            self.config['remindMethod'] = '消息提醒'
        self.methodComboBox.currentIndexChanged.connect(
            lambda v: self.update_config("remindMethod", self.remind_methods[v]))
        if 'microblogServer' in self.config:
            self.microblogServerLineEdit.setText(self.config['microblogServer'])
        self.microblogServerLineEdit.textChanged.connect(lambda v: self.update_config("microblogServer", v))
        if 'microblogToken' in self.config:
            self.microblogTokenLineEdit.setText(self.config['microblogToken'])
        self.microblogTokenLineEdit.textChanged.connect(lambda v: self.update_config("microblogToken", v))
        if 'messageServer' in self.config:
            self.messageServerLineEdit.setText(self.config['messageServer'])
        self.messageServerLineEdit.textChanged.connect(lambda v: self.update_config("messageServer", v))
        if 'messageToken' in self.config:
            self.messageTokenLineEdit.setText(self.config['messageToken'])
        self.messageTokenLineEdit.textChanged.connect(lambda v: self.update_config("messageToken", v))
        if 'schedule' in self.config:
            self.scheduleTextEdit.setPlainText(self.config['schedule'])
        if 'todo' in self.config:
            self.todoTextEdit.setPlainText(self.config['todo'])

        self.notify_message_box = QMessageBox()
        self.notify_message_box.setFont(self.centralwidget.font())
        self.notify_message_box.setWindowIcon(QIcon(":/icon.png"))
        self.notify_message_box.setIcon(QMessageBox.Information)
        self.notify_message_box.setWindowTitle("个人助理")
        self.notify_message_box.resize(520, 230)
        self.notify_message_box.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.notify_message_box_signal.connect(self.show_notify_message_box)
        self.update_work_progress_signal.connect(self.workProgressBar.setValue)
        self.update_rest_progress_signal.connect(self.restProgressBar.setValue)
        # threads
        self.rest_thread = None

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def quit(self):
        self.rest_thread = None
        app.quit()

    def update_config(self, key, value):
        self.config[key] = value

    def show_notify_message_box(self, msg):
        self.notify_message_box.setText(msg)
        self.notify_message_box.show()

    @pyqtSlot()
    def on_restStartBtn_clicked(self):
        self.restStopBtn.setEnabled(True)
        if self.rest_thread is None:
            self.restStartBtn.setText("暂停")
            self.rest_thread = RestThread(self, self.debug)
            self.rest_thread.start()
            self.statusbar.showMessage("休息提醒已启动")
        else:
            if self.rest_thread.should_pause():
                self.restStartBtn.setText("暂停")
                self.rest_thread.resume()
                self.statusbar.showMessage("休息提醒已恢复")
            else:
                self.restStartBtn.setText("继续")
                self.rest_thread.pause()
                self.statusbar.showMessage("休息提醒已暂停")

    @pyqtSlot()
    def on_restStopBtn_clicked(self):
        if self.rest_thread is not None:
            self.restStopBtn.setDisabled(True)
            self.rest_thread.stop()
            # self.rest_thread.join()
            self.rest_thread = None
            self.workProgressBar.setValue(0)
            self.restProgressBar.setValue(0)
            self.statusbar.showMessage("休息提醒已终止")
            self.restStartBtn.setText("开始")

    @pyqtSlot()
    def on_scheduleSaveBtn_clicked(self):
        value = self.scheduleTextEdit.toPlainText()
        self.config['schedule'] = value
        self.statusbar.showMessage("配置已保存")

    @pyqtSlot()
    def on_todoSaveBtn_clicked(self):
        value = self.todoTextEdit.toPlainText()
        self.config['todo'] = value
        self.statusbar.showMessage("配置已保存")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = MainWindow()
    Dialog.show()
    sys.exit(app.exec_())
