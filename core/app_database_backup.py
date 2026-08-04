import json
import os


DATABASE = "data/apps.json"


def load_apps():

    if not os.path.exists(DATABASE):

        return {
            "name": "GeraStore",
            "identifier": "com.gkuhtov.gerastore",
            "apps": []
        }


    with open(
        DATABASE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_apps(data):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        DATABASE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )



def add_app(app):

    data = load_apps()


    # удаляем старую версию этого приложения
    data["apps"] = [
        x for x in data["apps"]
        if x["bundleIdentifier"] != app["bundleIdentifier"]
    ]


    data["apps"].append(app)


    save_apps(data)
