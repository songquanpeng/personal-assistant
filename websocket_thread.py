import asyncio
import json
import ssl
import datetime
from threading import Thread, Event

import websockets


class WebSocketThread(Thread):
    def __init__(self, main, debug=False):
        super().__init__()
        self.main = main
        self._stop_event = Event()
        self.server_address = self.main.config['messagePusherServerAddress']
        self.token = self.main.config['messagePusherClientToken']
        self.username = self.main.config['messagePusherUsername']
        self.ssl_ctx = None
        if self.server_address.startswith("https"):
            self.ssl_ctx = ssl._create_unverified_context()
            scheme = "wss"
        else:
            scheme = "ws"
        if len(self.server_address.split('/')) < 3:
            self.conn_address = ""
        else:
            self.conn_address = f"{scheme}://{self.server_address.split('/')[2]}/api/register_client/{self.username}?secret={self.token}"

    def show_message(self, message):
        self.main.tray_message_signal.emit(message['title'], message['description'])
        timeVal = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msgVal =timeVal+'\n'+message['title'] +'\n'+ message['description']+'\n'
        self.main.history_message_signal.emit(msgVal)
        with open("history.txt", "a", encoding='utf-8') as file:
            file.write(msgVal+'\n')

    async def receive_message(self):
        try:
            async with websockets.connect(self.conn_address, ssl=self.ssl_ctx) as websocket:
                while not self.should_stop():
                    message = await websocket.recv()
                    message = json.loads(message)
                    self.show_message(message)
        except Exception as e:
            message = {"title": "WebSocket 连接错误", "description": str(e)}
            self.show_message(message)

    def run(self):
        asyncio.run(self.receive_message())

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()
