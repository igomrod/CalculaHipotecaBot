from datetime import datetime
from unittest import mock

from telegram import Update, User, MessageEntity, Chat, Message
from telegram.constants import MessageEntityType, ChatType
from telegram.ext import Application


class TelegramTestClient:
    def __init__(self, telegram_app: Application):
        self._message = None
        self._update = None
        self._application = telegram_app

    async def initialize(self):
        await self._application.initialize()

    async def type(self, message: str):
        self._message = \
            Message(**{
                'bot': self._application.bot,
                'chat': Chat(**{'id': 706760768, 'type': ChatType.PRIVATE, 'first_name': 'Iván'}),
                'text': message,
                'group_chat_created': False,
                'entities': [
                    MessageEntity(**{'length': 19, 'type': MessageEntityType.BOT_COMMAND, 'offset': 0})
                ],
                'new_chat_members': [], 'new_chat_photo': [],
                'message_id': 1501,
                'delete_chat_photo': False,
                'caption_entities': [],
                'date': datetime.now(),
                'supergroup_chat_created': False,
                'photo': [],
                'channel_chat_created': False,
                'from_user': User(**{'is_bot': False, 'first_name': 'Iván', 'id': 706760768, 'language_code': 'en'})
            })

        self._update = Update(
            **{
                'update_id': 434670121,
                'message': self._message
            }
        )

    async def assert_bot_reply_with(self, message: str):
        with mock.patch.object(self._message._bot, 'send_message',
                               wraps=self._message._bot.send_message) as monkey:
            await self._application.process_update(self._update)

            args, kwargs = monkey.call_args

            monkey.assert_called()
            assert kwargs.get('text') == message, f"bot reply message must be {message}"
