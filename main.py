import asyncio, signal
from config.config import Config
from config import logging_config
from core import auto_mute as am
from core.tg import app, clients
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")

auto_mute_interval: int = 0


async def main():
    global auto_mute_interval
    from core.tg import start_bot, stop_bot
    await start_bot()

    loop = asyncio.get_running_loop()

    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    if Config.auto_mute_enabled:
        auto_mute_interval = am.parse_interval()

    await am.mute(app, clients)

    try:
        await stop
    finally:
        await stop_bot()

if __name__ == '__main__':
    if Config.tg_id != 0 or Config.usermain:
        asyncio.run(main())
