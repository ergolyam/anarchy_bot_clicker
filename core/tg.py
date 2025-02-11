import asyncio
from config.config import Config
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, EditedMessageHandler

from modes.chasemute import chasemute_func
from modes.antimute import antimute_func

from config import logging_config
logging = logging_config.setup_logging(__name__)

USER_SESSIONS = Config.usersmain or [Config.usernames[0]]

async def handle_messages(client, message):
    mode = Config.mode
    if mode == 'chasemute':
        if not Config.userchase:
            logging.error('Env userchase is not set')
            return
        await chasemute_func(client, message)
    elif mode == 'antimute':
        if not Config.usernames:
            logging.error('Env usernames is not set')
            return
        await antimute_func(client, message)
    else:
        logging.error('Env mode is not set')
        return

def create_app(session_name: str) -> Client:
    app = Client(
        name=f"{Config.sessions_path}/{session_name.strip(' ').strip('@')}",
        api_id=Config.tg_id,
        api_hash=Config.tg_hash
    )
    app.add_handler(MessageHandler(handle_messages, filters.group))
    app.add_handler(EditedMessageHandler(handle_messages, filters.group))
    
    return app

clients = [create_app(sess) for sess in USER_SESSIONS]

async def start_bot():
    logging.info("Launching all clients...")
    for client in clients:
        logging.info(f"Starting client: {client.name}")
        await client.start()
    logging.info("All clients have been started.")

async def stop_bot():
    logging.info("Stopping all clients...")
    for client in clients:
        logging.info(f"Stopping client: {client.name}")
        await client.stop()
    logging.info("All clients have been stopped.")

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
