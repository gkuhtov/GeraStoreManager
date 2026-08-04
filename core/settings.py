import json


SETTINGS_FILE = "data/settings.json"


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

    return {
        "owner": github.get(
            "owner",
            ""
        ),
        "repo": github.get(
            "repo",
            ""
        ),
        "token": github.get(
            "token",
            ""
        )
    }
