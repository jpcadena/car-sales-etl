"""
Config script for Core module
"""
import datetime
from typing import Optional, Any

# pylint: disable=no-name-in-module
from pydantic import BaseSettings, PostgresDsn, validator, EmailStr


class Settings(BaseSettings):
    """
    Settings class that inherited from Pydantic BaseSettings
    """
    ENCODING: str
    NUM_BINS: int
    MAX_COLUMNS: int
    CHUNK_SIZE: int
    WIDTH: int
    PALETTE: str
    FONT_SIZE: int
    RE_PATTERN: str
    RE_REPL: str
    COLORS: list[str]
    LABELS: list[str]

    FIG_SIZE: tuple[int, int] = (15, 8)
    NUMERICS: list[str] = [
        'uint8', 'uint16', 'uint32', 'uint64',
        'int8', 'int16', 'int32',
        'int64',
        'float16', 'float32', 'float64']
    RANGES: list[tuple] = [
        (0, 255), (0, 65535), (0, 4294967295), (0, 18446744073709551615),
        (-128, 127), (-32768, 32767), (-2147483648, 2147483647),
        (-18446744073709551616, 18446744073709551615)]

    TS_PRECISION: int
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn = None

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

    CURRENT_YEAR: int = datetime.date.today().year

    class Config:
        """
        Config class for Settings
        """
        env_file: str = ".env"
        env_file_encoding: str = 'utf-8'
        arbitrary_types_allowed = True


settings = Settings()
