import os
import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QMessageBox

from config import Config
from rest_thread import RestThread
from schedule_thread import ScheduleThread
from ui import Ui_MainWindow
from utils import get_latest_version
from websocket_thread import WebSocketThread

config_file = os.path.join(os.path.dirname(sys.argv[0]), "personal-assistant.json")
is_windows = os.name == "nt"
use_shell = is_windows
hide_when_start = False
version = "v0.0.0"

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"


class MainWindow(QMainWindow, Ui_MainWindow):
    notify_message_box_signal = pyqtSignal(str)
    tray_message_signal = pyqtSignal(str, str)
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

        def activate_tray(reason):
            if reason == QSystemTrayIcon.Trigger:
                self.show()

        self.tray.activated.connect(activate_tray)
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
        self.remind_methods = ['消息提醒', '弹窗提醒', '显示桌面', '强制锁屏']
        if 'remindMethod' in self.config:
            remind_method = self.config['remindMethod']
            if remind_method in self.remind_methods:
                idx = self.remind_methods.index(remind_method)
            else:
                idx = 0
                self.config['remindMethod'] = self.remind_methods[idx]
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
        if 'messagePusherURL' in self.config:
            self.messagePusherURLLineEdit.setText(self.config['messagePusherURL'])
        self.messagePusherURLLineEdit.textChanged.connect(lambda v: self.update_config("messagePusherURL", v))
        if 'schedule' in self.config:
            self.scheduleTextEdit.setPlainText(self.config['schedule'])
        if 'todo' in self.config:
            self.todoTextEdit.setPlainText(self.config['todo'])
        if 'remindWorkText' in self.config:
            self.workTextLineEdit.setText(self.config['remindWorkText'])
        else:
            self.config['remindWorkText'] = self.workTextLineEdit.text()
        self.workTextLineEdit.textChanged.connect(lambda v: self.update_config("remindWorkText", v))
        if 'remindRestText' in self.config:
            self.restTextLineEdit.setText(self.config['remindRestText'])
        else:
            self.config['remindRestText'] = self.restTextLineEdit.text()
        self.restTextLineEdit.textChanged.connect(lambda v: self.update_config("remindRestText", v))
        if 'titleText' in self.config:
            self.titleTextLineEdit.setText(self.config['titleText'])
        else:
            self.config['titleText'] = self.titleTextLineEdit.text()
        self.titleTextLineEdit.textChanged.connect(lambda v: self.update_config("titleText", v))
        self.setWindowTitle(self.config['titleText'])
        if 'messagePusherServerAddress' in self.config:
            self.messagePusherServerAddressLineEdit.setText(self.config['messagePusherServerAddress'])
        else:
            self.config['messagePusherServerAddress'] = self.messagePusherServerAddressLineEdit.text()
        self.messagePusherServerAddressLineEdit.textChanged.connect(
            lambda v: self.update_config("messagePusherServerAddress", v))
        if 'messagePusherClientToken' in self.config:
            self.messagePusherClientTokenLineEdit.setText(self.config['messagePusherClientToken'])
        else:
            self.config['messagePusherClientToken'] = self.messagePusherClientTokenLineEdit.text()
        self.messagePusherClientTokenLineEdit.textChanged.connect(
            lambda v: self.update_config("messagePusherClientToken", v))
        if 'messagePusherUsername' in self.config:
            self.messagePusherUsernameLineEdit.setText(self.config['messagePusherUsername'])
        else:
            self.config['messagePusherUsername'] = self.messagePusherUsernameLineEdit.text()
        self.messagePusherUsernameLineEdit.textChanged.connect(lambda v: self.update_config("messagePusherUsername", v))
        if 'messagePusher' in self.config:
            self.messagePusherCheckBox.setCheckState(int(self.config['messagePusher']))
        self.messagePusherCheckBox.stateChanged.connect(lambda v: self.update_config("messagePusher", str(v)))
        if self.messagePusherCheckBox.isChecked():
            self.websocket_thread = WebSocketThread(self, self.debug)
            self.websocket_thread.setDaemon(True)
            self.websocket_thread.start()
        if 'bootStart' in self.config:
            self.bootStartCheckBox.setCheckState(int(self.config['bootStart']))
        self.bootStartCheckBox.stateChanged.connect(lambda v: self.update_config("bootStart", str(v)))
        if 'hideStart' in self.config:
            self.hideStartCheckBox.setCheckState(int(self.config['hideStart']))
            if self.config['hideStart'] == '2':
                global hide_when_start
                hide_when_start = True
        self.hideStartCheckBox.stateChanged.connect(lambda v: self.update_config("hideStart", str(v)))
        start_rest_remind = False
        if 'beginStart' in self.config:
            self.beginStartCheckBox.setCheckState(int(self.config['beginStart']))
            if self.config['beginStart'] == '2':
                start_rest_remind = True
        self.beginStartCheckBox.stateChanged.connect(lambda v: self.update_config("beginStart", str(v)))
        if is_windows:
            self.settings = QSettings(RUN_PATH, QSettings.NativeFormat)

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
        self.tray_message_signal.connect(self.show_tray_message)
        # threads
        self.schedule_thread = ScheduleThread(self, self.debug)
        self.schedule_thread.setDaemon(True)
        self.schedule_thread.start()
        # TODO: todo_thread
        # self.todo_thread = TodoThread(self, self.debug)
        # self.todo_thread.setDaemon(True)
        # self.todo_thread.start()
        self.rest_thread = None
        if start_rest_remind:
            self.on_restStartBtn_clicked()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def quit(self):
        self.rest_thread = None
        app.quit()

    def update_config(self, key, value):
        self.config[key] = value
        if key == "bootStart":
            if is_windows:
                if value == '2':
                    self.settings.setValue("PersonalAssistant", sys.argv[0])
                else:
                    self.settings.remove("PersonalAssistant")
            else:
                self.statusbar.showMessage("开机启动选项仅支持 Windows 系统")
        elif key == "messagePusher":
            pass

    def show_notify_message_box(self, msg):
        self.notify_message_box.setText(msg)
        self.notify_message_box.show()

    def show_tray_message(self, title, msg):
        self.tray.showMessage(title, msg)

    @pyqtSlot()
    def on_restStartBtn_clicked(self):
        self.restStopBtn.setEnabled(True)
        if self.rest_thread is None:
            self.restStartBtn.setText("暂停")
            self.rest_thread = RestThread(self, self.debug)
            self.rest_thread.setDaemon(True)
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
        current_time = datetime.now().strftime("%H:%M:%S")
        self.statusbar.showMessage(f"配置已保存（{current_time}）")
        self.schedule_thread.stop()
        self.schedule_thread = ScheduleThread(self, self.debug)
        self.schedule_thread.setDaemon(True)
        self.schedule_thread.start()

    @pyqtSlot()
    def on_todoSaveBtn_clicked(self):
        value = self.todoTextEdit.toPlainText()
        self.config['todo'] = value
        current_time = datetime.now().strftime("%H:%M:%S")
        self.statusbar.showMessage(f"配置已保存（{current_time}）")
        # TODO: todo_thread
        # self.todo_thread.stop()
        # self.todo_thread = TodoThread(self, self.debug)
        # self.todo_thread.setDaemon(True)
        # self.todo_thread.start()

    @pyqtSlot()
    def on_updateBtn_clicked(self):
        self.updateBtn.setDisabled(True)
        self.statusbar.showMessage(f"正在从 GitHub 获取信息 ...")
        latest_version = get_latest_version()
        if latest_version is None:
            self.statusbar.showMessage(f"无法连接至 GitHub 服务器")
        elif latest_version != version:
            self.statusbar.showMessage(f"更新可用：{version} -> {latest_version}")
        else:
            self.statusbar.showMessage(f"已是最新版：{latest_version}")
        self.updateBtn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = MainWindow()
    if not hide_when_start:
        Dialog.show()
    sys.exit(app.exec_())
