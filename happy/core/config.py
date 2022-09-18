"""Settings and environment variables."""

from functools import lru_cache
from typing import Dict, List

from pydantic import BaseSettings

tags_metadata: List[Dict[str, str]] = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
]


class Settings(BaseSettings):
    """Class defining the API settings.

    Attributes
    ----------
    elasticsearch_host : str
        The ElasticSearch hostname.
    elasticsearch_port : str
        The ElasticSearch port.
    elasticsearch_username : str
        The ElasticSearch username.
    elasticsearch_password : str
        The ElasticSearch user password.

    """

    elasticsearch_host: str
    elasticsearch_port: str
    elasticsearch_username: str
    elasticsearch_password: str

    class Config:
        """Configuration options."""

        env_file: str = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get the API settings.

    Returns
    -------
    Settings

    """
    return Settings()
