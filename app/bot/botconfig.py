from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    @property
    def Token(self):
        return self.TOKEN

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
