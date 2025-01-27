from typing import AsyncGenerator
from config.config import Config
import asyncio
from pyrogram.client import Client
from pyrogram.types import Message
from main import logging, auto_mute_interval
from modes import chasemute

reply_from_bot_flag = False
command_id: int = 0
reply_id: int = 0

class Timer:
    def __init__(self, timeout, callback, **args):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())
        self._args = args

    async def _job(self):
        await asyncio.sleep(self._timeout)
        logging.debug('Timer tick')
        await self._callback(self._args['main_client'], self._args['clients'])

    def cancel(self):
        self._task.cancel()

def parse_interval() -> int:
    ret = 0
    interval_exception = ValueError('Auto mute interval was not specified correctly.')
    if 'h' not in Config.auto_mute_interval and 'm' not in Config.auto_mute_interval:
        raise interval_exception
    buf = ''
    hour_encountered = False
    minute_encountered = False
    for c in Config.auto_mute_interval:
        if c.isdigit():
            buf += c
            continue
        elif c == 'h':
            if not hour_encountered:
                hour_encountered = True
                ret += (int(buf) * 3600)
                buf = ''
                continue
            else:
                raise interval_exception
        elif c == 'm':
            if not minute_encountered:
                minute_encountered = True
                ret += (int(buf) * 60)
                buf = ''
                continue
            else:
                raise interval_exception
        else:
            raise interval_exception
    return ret

async def mute(main_client: Client, clients: list[Client]):
    global reply_from_bot_flag
    global command_id
    global reply_id
    for target in Config.auto_mute_targets:
        generator = main_client.search_messages(chat_id=Config.auto_mute_target_chat,
                                                from_user=target,
                                                limit=1)
        assert isinstance(generator, AsyncGenerator)
        async for msg in generator:
            assert isinstance(msg, Message)
            command = await main_client.send_message(chat_id=msg.chat.id,
                                                     text='/m',
                                                     disable_notification=True,
                                                     reply_to_message_id=msg.id)
            command_id = command.id
            reply_from_bot_flag = True
            while reply_from_bot_flag:
                pass
            bot_reply = await main_client.get_messages(msg.chat.id, reply_id)
            assert isinstance(bot_reply, Message)
            await chasemute.chasemute_func(main_client, clients, bot_reply, True)
    Timer(auto_mute_interval, mute, main_client=main_client, clients=clients)

