import ctypes
import math
import os
import random
import time
from threading import Thread, Event

import pyautogui

from sentences import rest_sentences, work_sentences

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
            try:
                pyautogui.hotkey('win', 'd')
            except Exception as e:
                print(e)
                self.main.statusbar.showMessage(str(e))
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
                    if self.remind_rest_text == "":
                        prompt = random.choice(rest_sentences)
                    else:
                        prompt = self.remind_rest_text
                    self.remind_user(prompt)
            else:
                self.main.update_rest_progress_signal.emit(math.ceil(100 * self.count / self.rest_interval))
                if self.count == self.rest_interval:
                    self.working = True
                    self.count = 0
                    self.main.update_work_progress_signal.emit(0)
                    self.main.update_rest_progress_signal.emit(0)
                    if self.remind_work_text == "":
                        prompt = random.choice(work_sentences)
                    else:
                        prompt = self.remind_work_text
                    self.remind_user(prompt)

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
