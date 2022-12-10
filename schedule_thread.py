import os
import subprocess
import time
import requests
from datetime import datetime, timedelta
from threading import Thread, Event

is_windows = os.name == "nt"
use_shell = is_windows


def binary_search(arr, target):
    l = 0
    r = len(arr) - 1
    while l <= r:
        m = (l + r) // 2
        if arr[m] < target:
            l = m + 1
        elif arr[m] == target:
            return m
        else:
            r = m - 1
    if l == len(arr):
        l = 0
    return l


class Task:
    def __init__(self, items, main=None):
        self.items = items
        day = items[0]
        hour = items[1]
        minute = items[2]
        self.command = ' '.join(items[3:])
        self.main = main
        if day == '*':
            self.days = list(range(7))
        else:
            self.days = list(map(int, day.split(",")))
            self.days = [x - 1 for x in self.days]
            self.days.sort()
        if hour == '*':
            self.hours = list(range(24))
        else:
            self.hours = list(map(int, hour.split(",")))
            self.hours.sort()
        if minute == '*':
            self.minutes = list(range(60))
        else:
            self.minutes = list(map(int, minute.split(",")))
            self.minutes.sort()

        self.next_minutes = self.get_next_minutes()

        self.message_pusher_url = None
        self.title = self.main.config["titleText"]
        if self.main:
            self.message_pusher_url = self.main.config["messagePusherURL"]

    def get_next_time(self):
        now = datetime.now()
        cur_day = now.weekday()
        cur_hour = now.hour
        cur_minute = now.minute
        day_idx = binary_search(self.days, cur_day)
        hour_idx = binary_search(self.hours, cur_hour)
        minute_idx = binary_search(self.minutes, cur_minute)
        day_delta = self.days[day_idx] - cur_day
        if day_delta < 0:
            day_delta += 7
        if day_delta == 0:
            hour_delta = self.hours[hour_idx] - cur_hour
            if hour_delta < 0:
                hour_delta += 24
        else:
            hour_delta = self.hours[0] - cur_hour
            # if hour_delta < 0:
            #     hour_delta += 24
            #     day_delta -= 1
        if hour_delta == 0:
            minute_delta = self.minutes[minute_idx] - cur_minute
            if minute_delta < 0:
                minute_delta += 60
        else:
            minute_delta = self.minutes[0] - cur_minute
        next_time = now + timedelta(days=day_delta, hours=hour_delta, minutes=minute_delta)
        return next_time

    def get_next_minutes(self):
        now = datetime.now()
        next_time = self.get_next_time()
        delta = next_time - now
        return delta.days * 24 * 60 + delta.seconds // 60

    def execute(self):
        if self.items[3] == '@tray':
            if self.main:
                self.main.tray_message_signal.emit(self.title, " ".join(self.items[4:]))
        elif self.items[3] == '@msg':
            if self.message_pusher_url:
                url = self.message_pusher_url
                url = url.replace('$title', self.title)
                url = url.replace('$description', ' '.join(self.items[4:]))
                requests.get(url, verify=False)
        else:
            now = datetime.now()
            cur_day = now.day
            cur_weekday = now.weekday()
            command = self.command.replace("$day", str(cur_day))
            command = command.replace("$weekday", str(cur_weekday))
            subprocess.Popen(command.split(' '), shell=use_shell, cwd="./")
        print(f'[{datetime.now()}]: command \"{self.command}\" executed')


def parse_tasks(cron: str, main=None):
    if not cron:
        return []
    task_strs = cron.split('\n')
    tasks = []
    for task in task_strs:
        if task.startswith('#'):  # ignore comments
            continue
        items = task.split(' ')
        if len(items) < 4:
            continue  # illegal cron expressions
        tasks.append(Task(items, main))
    return tasks


class ScheduleThread(Thread):
    def __init__(self, main, debug=False):
        super().__init__()
        self.main = main
        self.debug = debug
        self._stop_event = Event()
        self.tasks = parse_tasks(self.main.config['schedule'], self.main)
        if self.debug:
            print(self.main.config['schedule'])
            now = datetime.now()
            print(now)
            for t in self.tasks:
                print(t.get_next_time(), " ", t.get_next_minutes())
                t.execute()

    def run(self):
        if len(self.tasks) == 0:
            return
        while not self.should_stop():
            min_next_minutes = 24 * 60
            for task in self.tasks:
                task.next_minutes = task.get_next_minutes()
                min_next_minutes = min(min_next_minutes, task.next_minutes)
                if task.next_minutes <= 0:
                    task.execute()
            min_next_minutes = max(min_next_minutes, 1)
            time.sleep(min_next_minutes * 60)
            if self.should_stop():
                break

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()


if __name__ == '__main__':
    print(datetime.now())
    task = Task(["1", "12", "*", "python ./script.py"])
    print(task.get_next_time())
    task = Task(["*", "*", "*", "python ./script.py"])
    print(task.get_next_time())
    task = Task(["5", "12", "*", "python ./script.py"])
    print(task.get_next_time())
    task = Task(["6", "12", "*", "python ./script.py"])
    print(task.get_next_time())
    task = Task(["5", "9", "*", "python ./script.py"])
    print(task.get_next_time())
