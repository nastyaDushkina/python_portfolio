from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from chat import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {
                     'message': {
                         'date': 1611001482,
                         'from_id': 388092344,
                         'id': 83, 'out': 0,
                         'peer_id': 388092344,
                         'text': 'привет',
                         'conversation_message_id': 69,
                         'fwd_messages': [],
                         'important': False,
                         'random_id': 0,
                         'attachments': [],
                         'is_hidden': False
                     },
                     'client_info': {
                         'button_actions': ['text', 'vkpay', 'open_app', 'location',
                                            'open_link', 'intent_subscribe', 'intent_unsubscribe'],
                         'keyboard': True,
                         'inline_keyboard': True,
                         'carousel': False, 'lang_id': 0
                     }
                 },
                 'group_id': 201386370,
                 'event_id': '9bec51d44075e4f9af662c864331f052a319a84e'}

    def test_ok(self):
        count = 5
        object = {}
        events = [object] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('chat.vk_api.VkApi'):
            with patch('chat.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.print_event = Mock()
                bot.run()

                bot.print_event.assert_called()
                bot.print_event.assert_called_with({})
                bot.print_event.assert_any_call({})
                assert bot.print_event.call_count == 5

    def test_print_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        send_mock = Mock()
        with patch('chat.vk_api.VkApi'):
            with patch('chat.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock

                bot.print_event(event)

        send_mock.assert_called_once_with(
            message=event.object.message['text'][-1::-1],
            peer_id=event.object.message['peer_id'],
            random_id=ANY
        )
