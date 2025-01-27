from pyrogram.types import Message
from config.config import Config
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.sync import compose

from modes.chasemute import chasemute_func
from modes.antimute import antimute_func

from core import auto_mute as am

from config import logging_config
logging = logging_config.setup_logging(__name__)

app = Client(f"{Config.sessions_path}/{Config.usermain.strip('@')}", api_id=Config.tg_id, api_hash=Config.tg_hash)
clients: list = []

@app.on_message(filters.group)
@app.on_edited_message(filters.group)
async def handle_messages(client: Client, message: Message):
    global clients
    if am.reply_from_bot_flag and message.reply_to_message.id == am.command_id:
        am.reply_id = message.id
        am.reply_from_bot_flag = False
    mode = Config.mode
    if mode == 'chasemute':
        if not Config.userchase:
            logging.error('Env userchase is not set')
            return
        await chasemute_func(client, clients, message)
    elif mode == 'antimute':
        if not Config.usernames:
            logging.error('Env usernames is not set')
            return
        await antimute_func(client, clients, message)
    else:
        logging.error('Env mode is not set')
        return

async def start_bot():
    global clients
    logging.info("Launching the bot...")
    clients = [None] * len(Config.clients_usernames)
    logging.info(clients)
    for i in range(len(clients)):
        logging.info(Config.clients_usernames[i])
        clients[i] = Client(f"{Config.sessions_path}/{Config.clients_usernames[i].strip('@')}", api_id=Config.tg_id, api_hash=Config.tg_hash)
        logging.info(clients[i])

    await app.start()
    await compose(clients)

async def stop_bot():
    global clients
    logging.info("Stopping the bot...")
    try:
        await app.stop()
    except ConnectionError:
        pass
    for i in range(len(clients)):
        try:
            await clients[i].stop()
        except ConnectionError:
            continue


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
