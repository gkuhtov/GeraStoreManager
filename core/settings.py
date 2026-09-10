import json
import os


SETTINGS_FILE = "data/settings.json"
GITHUB_TOKEN_ENV = "GERAKSTORE_GITHUB_TOKEN"


def load_settings():

    with open(
        SETTINGS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_github_settings():

    settings = load_settings()

    github = settings.get(
        "github",
        {}
    )

    token = github.get(
        "token",
        ""
    ).strip()

    if not token:
        token = os.getenv(
            GITHUB_TOKEN_ENV,
            ""
        ).strip()

    return {
        "owner": github.get(
            "owner",
            ""
        ),
        "repo": github.get(
            "repo",
            ""
        ),
        "token": token
    }


# ==================================================
# GeraKStore Categories
# ==================================================

APP_CATEGORIES = [
    "Игры",
    "Приложения",
    "Утилиты",
    "Эмуляторы",
    "Социальные сети",
    "Развлечения",
    "Медиа",
    "Фото и видео",
    "Музыка",
    "Образование",
    "Работа",
    "Финансы",
    "Здоровье",
    "Навигация",
    "Другое"
]
