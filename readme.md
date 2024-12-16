# anarchy_bot_clicker
A clicker bot for automatically pressing inline buttons in Telegram bots.

## Usage

### Deploy

- Run the bot:
    ```bash
    python main.py
    ```

- Other working env's:
    ```env
    LOG_LEVEL="INFO"
    MODE="antimute" or "chasemute"
    TG_ID="your_telegram_api_id"
    TG_HASH="your_telegram_api_hash"
    USERMAIN="@mainuser"
    USERCHASE="@chaseuser"
    USERNAMES="@user1, @user2, @user3"
    BOT_USERNAME="anarchy_bot_username"
    SESSIONS_PATH="/path/to/dir"
    ```

- Deploy in container:
    ```bash
    export BOT_MODE="chasemute" && \ # or export BOT_MODE="antimute"
    export BOT_USER="mainuser" && \
    podman pull ghcr.io/grisha765/anarchy_bot_clicker:latest && \
    mkdir -p $HOME/sessions/ && \
    podman run \
    --name anarchy_bot_clicker_$BOT_MODE-$BOT_USER \
    -v $HOME/sessions/:/app/sessions/:z \
    -e MODE=$BOT_MODE \
    -e TG_ID="your_telegram_api_id" \
    -e TG_HASH="your_telegram_api_hash" \
    -e BOT_USERNAME="anarchy_bot_username" \
    -e USERMAIN="@$BOT_USER" \
    -e USERCHASE="@chaseuser" \ # if BOT_MODE is equal to chasemute
    -e USERNAMES="@user1, @user2, @user3" # if BOT_MODE is equal to antimute
    ghcr.io/grisha765/anarchy_bot_clicker:latest
    ```

   The bot listens for votes in Telegram groups and acts on behalf of the specified users to either mute or protect them during "mute votes" initiated by other bots (e.g., [anarchy_bot](https://github.com/gmankab/anarchy_bot)).

#### Designed for use with [anarchy_bot](https://github.com/gmankab/anarchy_bot)
