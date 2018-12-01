from telegram.ext import Updater


class TelegramGateway(object):
    updater = None

    def __init__(self, token: str):
        self.token = token
        if not self.updater:
            self.updater = Updater(
                token=self.token,
                request_kwargs={
                    'proxy_url': 'socks5://emc3.sharkman.ru:1080',
                    'urllib3_proxy_kwargs': {
                        'username': 'S4wu2ULFfMR2Uy68yjtonXmbD',
                        'password': 'nP39gKXDNyCdIKHvOHW4h3NwJ',
                    }
                },
            )

    def send_message(self, chat_id: int, message: str):
        self.updater.bot.send_message(chat_id=chat_id, text=message, timeout=50)
