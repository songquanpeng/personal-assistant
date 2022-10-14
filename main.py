from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
import requests
from ui import Ui_MainWindow
from threading import Thread
import subprocess
import sys
import os
import configparser
import socket
import resource

filename = "go-file.exe"
exec_filename = filename
config_file = "gofile-launcher.ini"
is_windows = os.name == "nt"
use_shell = is_windows
if sys.platform == 'darwin':
    filename = "go-file-macos"
    exec_filename = "./" + filename
    dir_path = os.path.dirname(sys.argv[0])
    os.chdir(dir_path)
elif sys.platform == 'linux':
    filename = "go-file"
    exec_filename = "./" + filename

os.environ["SESSION_SECRET"] = socket.gethostname() + os.getcwd()


def get_latest_version(repository, username="songquanpeng"):
    try:
        data = requests.get(f"https://api.github.com/repos/{username}/{repository}/releases/latest").json()
    except:
        return None
    latest_version = data["tag_name"]
    return latest_version


def get_ips():
    return socket.gethostbyname_ex(socket.gethostname())[2]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.gofile = None
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.ips = get_ips()
        self.ips.insert(0, "localhost")
        for ip in self.ips:
            self.hostComboBox.addItem(ip, ip)
        if 'host' in self.config['DEFAULT']:
            host = self.config['DEFAULT']['host']
            if host in self.ips:
                idx = self.ips.index(host)
            else:
                idx = 0
            self.hostComboBox.setCurrentIndex(idx)
        self.hostComboBox.currentIndexChanged.connect(lambda v: self.update_config("host", self.ips[v]))
        if 'port' in self.config['DEFAULT']:
            self.portSpinBox.setValue(int(self.config['DEFAULT']['port']))
        self.portSpinBox.textChanged.connect(lambda v: self.update_config("port", v))
        if 'file' in self.config['DEFAULT']:
            self.fileLineEdit.setText(self.config['DEFAULT']['file'])
        self.fileLineEdit.textChanged.connect(lambda v: self.update_config("file", v))
        if 'video' in self.config['DEFAULT']:
            self.videoLineEdit.setText(self.config['DEFAULT']['video'])
        self.videoLineEdit.textChanged.connect(lambda v: self.update_config("video", v))
        self.aboutMsgBox = QMessageBox()
        self.aboutMsgBox.setFont(self.font())
        self.aboutMsgBox.setWindowIcon(QIcon(":/icon.png"))
        self.aboutMsgBox.setIcon(QMessageBox.Information)
        self.aboutMsgBox.setWindowTitle("关于")
        self.aboutMsgBox.setText(
            f"Gofile Launcher 由 JustSong 构建，<a href='https://github.com/songquanpeng/gofile-launcher'>源代码</a>遵循 MIT 协议")
        self.NotFoundMsgBox = QMessageBox()
        self.NotFoundMsgBox.setFont(self.font())
        self.NotFoundMsgBox.setWindowIcon(QIcon(":/icon.png"))
        self.NotFoundMsgBox.setIcon(QMessageBox.Information)
        self.NotFoundMsgBox.setWindowTitle(f"未能找到 {filename}")
        self.NotFoundMsgBox.setText("请点击更新按钮进行下载或者手动下载后放到本启动器相同目录下")

    def closeEvent(self, event):
        with open(config_file, 'w') as cfg:
            self.config.write(cfg)
        if self.gofile is not None:
            self.on_startBtn_clicked()
        event.accept()

    def update_config(self, key, value):
        self.config['DEFAULT'][key] = value

    @pyqtSlot()
    def on_startBtn_clicked(self):
        if self.gofile is None:
            if os.path.exists(f"./{filename}"):
                port = self.portSpinBox.text()
                host = self.hostComboBox.currentText()
                file_path = self.fileLineEdit.text()
                video_path = self.videoLineEdit.text()
                self.gofile = subprocess.Popen(
                    [f"{exec_filename}", "--port", f"{port}", "--host", f"{host}", "--path", f"{file_path}", "--video",
                     f"{video_path}"], shell=use_shell, cwd="./")
                self.statusbar.showMessage("服务已启动")
                self.startBtn.setText("终止")
            else:
                self.NotFoundMsgBox.show()
        else:
            if os.name == "nt":
                subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.gofile.pid), shell=True)
            else:
                # Not tested.
                # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
                self.gofile.kill()
            self.gofile = None
            self.statusbar.showMessage("服务已终止")
            self.startBtn.setText("启动")

    @pyqtSlot()
    def on_fileChooseBtn_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "选择要分享的文件的目录", ".")
        self.fileLineEdit.setText(path)
        self.statusbar.showMessage(f"已选择：{path}")

    @pyqtSlot()
    def on_videoChooseBtn_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "选择要分享的视频的目录", ".")
        self.videoLineEdit.setText(path)
        self.statusbar.showMessage(f"已选择：{path}")

    @pyqtSlot()
    def on_aboutBtn_clicked(self):
        self.aboutMsgBox.show()

    @pyqtSlot()
    def on_updateBtn_clicked(self):
        if os.path.exists(f"./{filename}"):
            process = subprocess.Popen([f"{exec_filename}", '--version'], stdout=subprocess.PIPE, shell=use_shell,
                                       cwd="./")
            output = process.communicate()[0]
            current_version = output.decode('utf-8')
            current_version = current_version.rstrip("\n")
            self.statusbar.showMessage(f"正在请求 GitHub 服务器查询当前最新版本 ...")
            latest_version = get_latest_version("go-file")
            if latest_version is None:
                self.statusbar.showMessage(f"无法连接到 GitHub 服务器")
            if latest_version == current_version:
                self.statusbar.showMessage(f"已是最新版：{latest_version}")
                return
        worker = ThreadDownloader(self.statusbar, self.updateBtn)
        worker.start()


class ThreadDownloader(Thread):
    def __init__(self, statusbar, updateBtn):
        super().__init__()
        self.statusbar = statusbar
        self.updateBtn = updateBtn

    def run(self):
        self.updateBtn.setEnabled(False)
        self.statusbar.showMessage("正在从 GitHub 上获取最新版 ...")
        res = requests.get(f"https://github.com/songquanpeng/go-file/releases/latest/download/{filename}")
        if res.status_code != 200:
            self.statusbar.showMessage(f"下载失败：{res.text}")
        else:
            with open(f"./{filename}", "wb") as f:
                f.write(res.content)
            self.statusbar.showMessage(f"下载完成")
            if os.name != "nt":
                subprocess.run(["chmod", "u+x", f"./{filename}"])
        self.updateBtn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = MainWindow()
    Dialog.show()
    sys.exit(app.exec_())
