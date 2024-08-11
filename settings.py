from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    AIR_CONDITIONING_SEARCH: bool = True
    IGNORE_OTODOM_REDIRECTS: bool = False


settings = Settings()
