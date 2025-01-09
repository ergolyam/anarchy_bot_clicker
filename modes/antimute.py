from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

async def antimute_func(main_client, clients, message):
    try:
        if message.from_user.username == Config.bot_username:
            logging.debug(f"Processing antimute request from {message.from_user.username} with text: {message.text}")

            lines = message.text.split("\n")
            mute_target = lines[0].split(' ')[1].rstrip('?')

            logging.debug(f"Target user for antimute: {mute_target}")

            buttons_callback_data = []
            buttons = message.reply_markup.inline_keyboard if message.reply_markup else []

            if not buttons:
                logging.warning("No inline buttons found in the message.")
            else:
                logging.debug(f"Found {len(buttons)} inline button rows.")

                for row in buttons:
                    for button in row:
                        callback_data = button.callback_data
                        buttons_callback_data.append(callback_data)

            if any(user in mute_target for user in Config.usernames):
                logging.debug(f"Target {mute_target} is in the allowed list for antimute.")
                await main_client.request_callback_answer(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    callback_data=buttons_callback_data[1]
                )
                for client in clients:
                    await client.request_callback_answer(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        callback_data=buttons_callback_data[1]
                    )
                return
            else:
                logging.warning(f"Target {mute_target} is not in the allowed list for antimute.")

    except Exception as e:
        logging.error(f"An error occurred in antimute_func: {e}", exc_info=True)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
