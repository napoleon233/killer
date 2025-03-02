import sys
import random
import asyncio
import threading
import webbrowser
from PyQt5 import QtWidgets, uic
from twitchio import Client

# Данные ботов
BOTS = [
    {"nickname": "pip_licer", "oauth": "oauth:2fvcf515wt707zlrt4ws4hkma9u3m7"},
    {"nickname": "vasyok_di", "oauth": "oauth:xhx9vxmepeyffrmzt2z41i0sj6jv1y"},
    {"nickname": "olesha_popka", "oauth": "oauth:0iaa5fmj6y46i63d7z15ygxgj3rp4p"},
    {"nickname": "judifruct", "oauth": "oauth:8tfyp8nn62b7pomv1gx323af56jyyw"}
]


class TwitchBot(Client):
    def __init__(self, bot_data, message, channel):
        super().__init__(token=bot_data["oauth"], initial_channels=[f"#{channel}"])
        self.bot_nickname = bot_data["nickname"]
        self.message = message
        self.channel = f"#{channel}"

    async def event_ready(self):
        print(f"{self.bot_nickname} подключился к чату {self.channel}")
        await asyncio.sleep(2)  # Задержка перед отправкой
        ws = self._connection
        await ws.send(f"PRIVMSG {self.channel} :{self.message}")
        print(f"{self.bot_nickname}: {self.message}")


async def run_bot_async(bot):
    await bot.start()


def send_message(message, channel):
    if not message or not channel:
        print("Ошибка: пустое сообщение или канал")
        return

    bot_data = random.choice(BOTS)  # Выбираем случайного бота
    print(f"Выбран бот: {bot_data['nickname']}")

    def run_in_thread():
        async def inner_run():
            bot = TwitchBot(bot_data, message, channel)  # Создаём 1 бота
            await run_bot_async(bot)  # Запускаем его

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(inner_run())

    bot_thread = threading.Thread(target=run_in_thread)
    bot_thread.start()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)  # Загружаем UI
        self.pushButton.clicked.connect(self.handle_send)
        self.pushButton_2.clicked.connect(self.open_streamer_channel)

    def handle_send(self):
        message = self.plainTextEdit_2.toPlainText().strip()
        channel = self.plainTextEdit.toPlainText().strip()
        send_message(message, channel)

    def open_streamer_channel(self):
        channel = self.plainTextEdit.toPlainText().strip()
        if channel:
            url = f"https://www.twitch.tv/{channel}"
            webbrowser.open(url)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
