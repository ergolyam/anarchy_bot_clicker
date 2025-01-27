from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

async def chasemute_func(main_client, clients, message, auto_mute=False):
    try:
        if message.from_user.username == Config.bot_username:
            lines = message.text.split("\n")
            votes_for_mute = []
            votes_against_mute = []
            collect_votes_for = False
            collect_votes_against = False

            logging.debug(f"Processing message from {message.from_user.username} with text: {message.text}")

            if not auto_mute:
                for item in lines:
                    if item == 'votes for mute:':
                        collect_votes_for = True
                        continue
                    elif item == 'votes against mute:':
                        collect_votes_for = False
                        collect_votes_against = True
                        continue

                    if collect_votes_for and item != '':
                        votes_for_mute.append(item)
                    elif collect_votes_against and item != '':
                        votes_against_mute.append(item)

            buttons_callback_data = []
            buttons = message.reply_markup.inline_keyboard if message.reply_markup else []

            if not buttons:
                logging.warning("No inline buttons found in the message")
            else:
                logging.debug(f"Found {len(buttons)} inline button rows")

                for row in buttons:
                    for button in row:
                        callback_data = button.callback_data
                        buttons_callback_data.append(callback_data)

            if Config.userchase in votes_for_mute or auto_mute:
                if not auto_mute:
                    logging.debug(f"User {Config.userchase} voted for mute")
                await main_client.request_callback_answer(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    callback_data=buttons_callback_data[0]
                )
                for client in clients:
                    await client.request_callback_answer(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        callback_data=buttons_callback_data[0]
                    )
                await main_client.request_callback_answer(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    callback_data=buttons_callback_data[2])
                return

            if Config.userchase in votes_against_mute:
                logging.debug(f"User {Config.userchase} voted against mute")
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

    except Exception as e:
        logging.error(f"An error occurred in chasemute_func: {e}", exc_info=True)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
