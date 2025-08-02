# anarchy_bot_clicker
A clicker bot for automatically pressing inline buttons in Telegram bots.

## Usage

### Deploy

- Run the bot:
    ```bash
    uv run main.py
    ```

- Other working env's:
    ```env
    LOG_LEVEL="INFO"
    MODE="antimute" # antimute, chasemute, mixed
    TG_ID="your_telegram_api_id"
    TG_HASH="your_telegram_api_hash"
    PROTECT_USERS="@user1, @user2, @user3" # first user is the main one
    CLICK_USERS="@mainuser1, @mainuser2, @mainuser3"
    CHASE_USER="@chaseuser"
    BOT_USERNAME="anarchy_bot_username"
    SESSIONS_PATH="/path/to/dir"
    ```

- Pull container:
    ```bash
    podman pull ghcr.io/ergolyam/anarchy_bot_clicker:latest
    ```

- Create dir:
    ```bash
    mkdir -p $HOME/sessions/
    ```

- Deploy in container as antimute:
    ```bash
    export BOT_USER="user1" && \
    podman run \
    --name anarchy_bot_clicker_antimute-$BOT_USER \
    -v $HOME/sessions/:/app/sessions/:z \
    -e MODE="antimute" \
    -e TG_ID="your_telegram_api_id" \
    -e TG_HASH="your_telegram_api_hash" \
    -e BOT_USERNAME="anarchy_bot_username" \
    -e PROTECT_USERS="@$BOT_USER, @user2, @user3" \
    ghcr.io/ergolyam/anarchy_bot_clicker:latest
    ```

- Deploy in container as chasemute:
    ```bash
    podman run \
    --name anarchy_bot_clicker_chasemute \
    -v $HOME/sessions/:/app/sessions/:z \
    -e MODE="chasemute" \
    -e TG_ID="your_telegram_api_id" \
    -e TG_HASH="your_telegram_api_hash" \
    -e BOT_USERNAME="anarchy_bot_username" \
    -e CLICK_USERS="@mainuser1, @mainuser2, @mainuser3" \
    -e CHASE_USER="@chaseuser" \
    ghcr.io/ergolyam/anarchy_bot_clicker:latest
    ```

- Deploy in container as mixed:
    ```bash
    podman run \
    --name anarchy_bot_clicker \
    -v $HOME/sessions/:/app/sessions/:z \
    -e MODE="mixed" \
    -e TG_ID="your_telegram_api_id" \
    -e TG_HASH="your_telegram_api_hash" \
    -e BOT_USERNAME="anarchy_bot_username" \
    -e PROTECT_USERS="@user1, @user2, @user3" \
    -e CLICK_USERS="@mainuser1, @mainuser2, @mainuser3" \
    -e CHASE_USER="@chaseuser" \
    ghcr.io/ergolyam/anarchy_bot_clicker:latest
    ```

   The bot listens for votes in Telegram groups and acts on behalf of the specified users to either mute or protect them during "mute votes" initiated by other bots (e.g., [anarchy_bot](https://github.com/gmankab/anarchy_bot)).

#### Designed for use with [anarchy_bot](https://github.com/gmankab/anarchy_bot)
