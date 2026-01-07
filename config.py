from functools import lru_cache

from common.settings import ProjectSettings


@lru_cache()
def get_settings() -> ProjectSettings:
    settings = ProjectSettings()

    return settings


settings = get_settings()