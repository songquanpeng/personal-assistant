import os
import subprocess
import time
from datetime import datetime, timedelta
from threading import Thread, Event

import pyautogui
import pyperclip

is_windows = os.name == "nt"
use_shell = is_windows
windows_start_microsoft_todo_cmd = r"explorer.exe shell:appsFolder\Microsoft.Todos_8wekyb3d8bbwe!App"

target_hour = 3


class TodoThread(Thread):
    def __init__(self, main, debug=False):
        super().__init__()
        self.main = main
        self.debug = debug
        self._stop_event = Event()
        self.todo_config = self.main.config['todo']
        if self.debug:
            print(self.main.config['todo'])

    def add_todos(self):
        if not self.todo_config:
            return
        todo_strs = self.todo_config.split('\n')
        now = datetime.now()
        today = now.weekday() + 1
        todos = []
        for todo_str in todo_strs:
            if todo_str.startswith('#'):  # ignore comments
                continue
            items = todo_str.split(' ')
            if len(items) < 2:
                continue  # illegal expression
            if items[0] == '*' or items[0] == str(today):
                todos.append(' '.join(items[1:]))
        if len(todos) == 0:
            return
        if is_windows:
            subprocess.Popen(windows_start_microsoft_todo_cmd, shell=use_shell)
        time.sleep(5)
        try_times = 3
        while len(pyautogui.getWindowsWithTitle("Microsoft To Do")) == 0 and try_times > 0:
            try_times -= 1
            time.sleep(5)
        if len(pyautogui.getWindowsWithTitle("Microsoft To Do")) == 0:
            print("cannot get handler for Microsoft To Do")
            return
        todo_app = pyautogui.getWindowsWithTitle("Microsoft To Do")[0]
        todo_app.activate()
        for todo in todos:
            print(f"adding todo: {todo}")
            pyperclip.copy(todo)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            time.sleep(1)
        todo_app.close()

    def run(self):
        while not self.should_stop():
            now = datetime.now()
            if abs(now.hour - target_hour) <= 1:
                self.add_todos()
            # prepare next run
            hours_delta = target_hour - now.hour
            if hours_delta <= 0:
                hours_delta += 24
            next_run_time = now + timedelta(hours=hours_delta)
            delta = next_run_time - now
            next_run_minutes = delta.days * 24 * 60 + delta.seconds // 60
            time.sleep(next_run_minutes * 60)
            if self.should_stop():
                break

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()


if __name__ == '__main__':
    print(datetime.now())
