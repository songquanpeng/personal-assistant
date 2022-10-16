import math
import time
from threading import Thread, Event

import pyautogui


class RestThread(Thread):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.working = True
        self.count = 0
        self.work_interval = int(self.main.config['workInterval'].split(' ')[0])
        self.rest_interval = int(self.main.config['restInterval'].split(' ')[0])
        self._stop_event = Event()
        self.method = self.main.config['remindMethod']

    def show_message(self, message):
        if self.method == "消息提醒":
            self.main.tray.showMessage("个人助理", message)
        elif self.method == "弹窗提醒":
            # TODO: 弹窗提醒
            pass
        elif self.method == "全屏覆盖":
            # TODO: 全屏覆盖
            pass
        elif self.method == "显示桌面":
            pyautogui.hotkey('win', 'd')

    def run(self):
        while not self.should_stop():
            sleep_seconds = 1
            if self.working:
                sleep_seconds *= 60
            time.sleep(sleep_seconds)
            self.count += 1
            if self.working:
                self.main.workProgressBar.setValue(math.ceil(100 * self.count / self.work_interval))
                if self.count == self.work_interval:
                    self.working = False
                    self.count = 0
                    self.show_message("开始休息！")
            else:
                self.main.restProgressBar.setValue(math.ceil(100 * self.count / self.rest_interval))
                if self.count == self.rest_interval:
                    self.working = True
                    self.count = 0
                    self.main.workProgressBar.setValue(0)
                    self.main.restProgressBar.setValue(0)
                    self.show_message("开始工作！")
        self.main.workProgressBar.setValue(0)
        self.main.restProgressBar.setValue(0)

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()
