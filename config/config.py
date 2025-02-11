import os

class Config:
    log_level: str = "INFO"
    mode: str = 'None'
    tg_id: str = '0'
    tg_hash: str = '0'
    click_users: list = []
    chase_user: str = ''
    protect_users: list = []
    bot_username: str = 'g_anarchy_bot'
    sessions_path: str = './'

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
