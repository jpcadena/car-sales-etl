"""
Config script for Core module
"""
from functools import lru_cache
from typing import Optional, Any

from numpy import float16
# pylint: disable=no-name-in-module
from pydantic import BaseSettings, PostgresDsn, validator, EmailStr, \
    root_validator


@root_validator(pre=True)
def validate_mail_credentials(values):
    """
    Validate email credentials before reading the env file
    :param values:
    :type values:
    :return:
    :rtype:
    """
    mail_credentials = values.get('MAIL_CREDENTIALS')
    if mail_credentials:
        username, password = mail_credentials.split(':')
        values['MAIL_CREDENTIALS'] = (username, password)
    return values


class Settings(BaseSettings):
    """
    Settings class that inherited from Pydantic BaseSettings
    """
    MAX_COLUMNS: int
    WIDTH: int
    CHUNK_SIZE: int
    ENCODING: str

    PALETTE: str
    FONT_SIZE: int
    FIG_SIZE: tuple[int, int] = (15, 8)
    COLORS: list[str] = ['lightskyblue', 'coral', 'palegreen']

    converters: dict = {
        'TotalCharges': lambda x: float16(x.replace(' ', '0.0'))}
    NUMERICS: list[str] = [
        'uint8', 'uint16', 'uint32', 'uint64',
        'int8', 'int16', 'int32',
        'int64',
        'float16', 'float32', 'float64']
    RANGES: list[tuple] = [
        (0, 255), (0, 65535), (0, 4294967295), (0, 18446744073709551615),
        (-128, 127), (-32768, 32767), (-2147483648, 2147483647),
        (-18446744073709551616, 18446744073709551615)]

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str],
                               values: dict[str, Any]) -> Any:
        """
        Construct for creating a database connection
        :param v: SQLAlchemy database URI
        :type v: str
        :param values: Dictionary with elements to validate
        :type values: dict
        :return: Database connection
        :rtype: PostgresDsn
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    MAIL_SERVER: str
    MAIL_FROM: EmailStr
    MAIL_TO: EmailStr
    MAIL_SUBJECT: str
    MAIL_CREDENTIALS: list[str]
    MAIL_TIMEOUT: float

    class Config:
        """
        Config class for Settings
        """
        env_file: str = ".env"
        env_file_encoding: str = 'utf-8'
        arbitrary_types_allowed = True


settings = Settings()


@lru_cache()
def get_setting() -> Settings:
    """
    Get settings cached
    :return: settings object
    :rtype: Settings
    """
    return Settings()
