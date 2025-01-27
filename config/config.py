import os

class Config:
    log_level: str = "DEBUG"
    mode: str = 'chasemute'
    tg_id: str = ''
    tg_hash: str = ''
    usermain: str = ''
    userchase: str = ''
    usernames: list = []
    bot_username: str = 'g_anarchy_bot'
    sessions_path: str = './'
    clients_usernames: list = ['']
    auto_mute_enabled: bool = True
    auto_mute_aggressive: bool = True
    auto_mute_aggressive_ignore: list = []
    auto_mute_interval: str = '1m'
    auto_mute_targets: list = []
    auto_mute_target_chat: str = ''

    @classmethod
    def load_from_env(cls):
        for key in cls.__annotations__:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                current_value = getattr(cls, key)
                if isinstance(current_value, int):
                    setattr(cls, key, int(env_value))
                elif isinstance(current_value, list):
                    setattr(cls, key, env_value.split(","))
                else:
                    setattr(cls, key, env_value)

Config.load_from_env()

if not os.path.exists(Config.sessions_path):
    os.makedirs(Config.sessions_path)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
