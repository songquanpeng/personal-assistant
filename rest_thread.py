import ctypes
import math
import os
import time
from threading import Thread, Event

import pyautogui

is_windows = os.name == "nt"


class RestThread(Thread):
    def __init__(self, main, debug=False):
        super().__init__()
        self.main = main
        self.working = True
        self.paused = False
        self.count = 0
        self.work_interval = int(self.main.config['workInterval'].split(' ')[0])
        self.rest_interval = int(self.main.config['restInterval'].split(' ')[0])
        self._stop_event = Event()
        self._pause_event = Event()
        self.method = self.main.config['remindMethod']
        self.remind_work_text = self.main.config['remindWorkText']
        self.remind_rest_text = self.main.config['remindRestText']
        self.seconds_per_minute = 60
        self.title = self.main.config["titleText"]
        if debug:
            self.seconds_per_minute = 1

    def remind_user(self, message):
        if self.method == "消息提醒":
            self.main.tray_message_signal.emit(self.title, message)
        elif self.method == "弹窗提醒":
            self.main.notify_message_box_signal.emit(message)
        elif self.method == "显示桌面":
            pyautogui.hotkey('win', 'd')
        elif self.method == "强制锁屏":
            if self.working:
                self.main.tray_message_signal.emit(self.title, message)
            else:
                if is_windows:
                    ctypes.windll.user32.LockWorkStation()
                else:
                    self.main.tray_message_signal.emit(self.title, message)

    def run(self):
        while not self.should_stop():
            while self.should_pause():
                time.sleep(1)
            sleep_seconds = 1
            if self.working:
                sleep_seconds *= self.seconds_per_minute
            time.sleep(sleep_seconds)
            if self.should_stop():
                return
            while self.should_pause():
                time.sleep(1)
            self.count += 1
            if self.working:
                self.main.update_work_progress_signal.emit(math.ceil(100 * self.count / self.work_interval))
                if self.count == self.work_interval:
                    self.working = False
                    self.count = 0
                    self.remind_user(self.remind_rest_text)
            else:
                self.main.update_rest_progress_signal.emit(math.ceil(100 * self.count / self.rest_interval))
                if self.count == self.rest_interval:
                    self.working = True
                    self.count = 0
                    self.main.update_work_progress_signal.emit(0)
                    self.main.update_rest_progress_signal.emit(0)
                    self.remind_user(self.remind_work_text)

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()

    def should_pause(self):
        return self._pause_event.is_set()
