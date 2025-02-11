from config.config import Config
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, EditedMessageHandler

from modes.chasemute import chasemute_func
from modes.antimute import antimute_func
from modes.automute import automute_func

from config import logging_config
logging = logging_config.setup_logging(__name__)

def gen_sessions(mode: str):
    if mode == 'chasemute' and Config.click_users:
        users = Config.click_users
        if Config.automute:
            users = users + [Config.chase_user + "_automute"]
        return users
    elif mode == 'antimute' and Config.protect_users:
        return [Config.protect_users[0]]
    elif mode == 'mixed' and Config.protect_users and Config.click_users:
        users = [Config.protect_users[0]] + Config.click_users
        if Config.automute:
            users = users + [Config.chase_user + "_automute"]
        return users
    else:
        return

first_protect_user = False

def create_app(session_name: str, mode: str) -> Client:
    global first_protect_user
    app = Client(
        name=f"{Config.sessions_path}/{session_name.strip(' ').strip('@')}",
        api_id=Config.tg_id,
        api_hash=Config.tg_hash
    )
    if mode == 'chasemute' and Config.chase_user:
        logging.info(f'Apply {mode} handlers.')
        if session_name == Config.chase_user and Config.automute:
            logging.debug(f'Apply {session_name} as automute session.')
            app.add_handler(EditedMessageHandler(automute_func, filters.group))
        else:
            logging.debug(f'Apply {session_name} as chasemute session.')
            app.add_handler(MessageHandler(chasemute_func, filters.group))
            app.add_handler(EditedMessageHandler(chasemute_func, filters.group))
    elif mode == 'antimute' and Config.protect_users:
        logging.info(f'Apply {mode} handlers.')
        logging.debug(f'Apply {session_name} as antimute session.')
        app.add_handler(MessageHandler(antimute_func, filters.group))
    elif Config.mode == "mixed":
        logging.info(f'Apply {mode} handlers.')
        if Config.protect_users and session_name == Config.protect_users[0] and not first_protect_user:
            logging.debug(f'Apply {session_name} as antimute session.')
            app.add_handler(MessageHandler(antimute_func, filters.group))
            first_protect_user = True
        else:
            if session_name == Config.chase_user and Config.automute:
                logging.debug(f'Apply {session_name} as automute session.')
                app.add_handler(EditedMessageHandler(automute_func, filters.group))
            else:
                logging.debug(f'Apply {session_name} as chasemute session.')
                app.add_handler(MessageHandler(chasemute_func, filters.group))
                app.add_handler(EditedMessageHandler(chasemute_func, filters.group))
    else:
        logging.error('Env is not set or config is incomplete.')
    return app

mode = Config.mode
sessions = gen_sessions(mode)
if not sessions:
    raise ValueError(f'gen_sessions returned {sessions}. Stopped.')
clients = [create_app(sess, mode) for sess in sessions]

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
