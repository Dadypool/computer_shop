from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TOKEN: str

    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+psycopg://postgres:postgres@localhost:5432/shop
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def Token(self):
        return self.TOKEN

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
