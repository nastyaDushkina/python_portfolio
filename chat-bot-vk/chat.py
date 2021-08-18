#!usr/bin/env python3
import random

try:
    import settings
except IndexError:
    exit('Do cp settings.py.default settings.py and set token')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from log_config import log_config
import logging.config

logging.config.dictConfig(log_config)
console_log = logging.getLogger('console_logger')
file_log = logging.getLogger('file_logger')


class Bot:
    """
    Echo-reverse bot для vk.com.
    Use python3.8
    """

    def __init__(self, group_id, token):
        """

        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """Запуск бота."""
        for event in self.long_poller.listen():
            file_log.debug(f'получено событие!')
            try:
                self.print_event(event)
            except Exception:
                file_log.exception('возникла ошибка')

    def print_event(self, event):
        """
        Отправляет перевёрнутое сообщение назад, если это текст.
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message['text'][-1::-1]
            self.api.messages.send(message=message,
                                   peer_id=event.object.message['peer_id'],
                                   random_id=random.randint(0, 2 ** 20))
            file_log.debug(f'отправлено {message}')
        else:
            console_log.info(f'мы ещё не умеем такое обрабатывать {event.type}')


if __name__ == '__main__':
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
