import json
import os
from datetime import datetime, timezone


MANAGER_APPS = "data/apps.json"

OLD_REPO = os.path.expanduser(
    "~/Projects/GeraStore/repo.json"
)

TEST_REPO = os.path.expanduser(
    "~/Projects/GeraStore-Test/repo.json"
)


def now_time():

    return datetime.now(
        timezone.utc
    ).astimezone().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )


def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def build_repo():

    apps_data = load_json(
        MANAGER_APPS
    )

    old_repo = load_json(
        OLD_REPO
    )


    old_apps = {}

    for app in old_repo.get(
        "appRepositories",
        []
    ):

        old_apps[
            app.get("bundleIdentifier")
        ] = app


    apps = []


    for app in apps_data.get(
        "apps",
        []
    ):

        bundle = app.get(
            "bundleIdentifier"
        )


        old = old_apps.get(
            bundle,
            {}
        )


        versions = app.get(
            "versions",
            []
        )


        latest = (
            versions[-1]
            if versions
            else {}
        )


        old_version = old.get(
            "appVersion"
        )


        new_version = latest.get(
            "version"
        )


        if old_version != new_version:

            update_time = now_time()

        else:

            update_time = old.get(
                "appUpdateTime",
                now_time()
            )


        apps.append({

            "appName":
            app.get("name"),

            "bundleIdentifier":
            bundle,

            "appVersion":
            new_version,

            "appUpdateTime":
            update_time

        })


    return {

        "sourceName":
        "GeraStore Test",

        "sourceUpdateTime":
        now_time(),

        "appRepositories":
        apps

    }


if __name__ == "__main__":

    repo = build_repo()

    save_json(
        TEST_REPO,
        repo
    )

    print(
        "Готово:"
    )

    for app in repo["appRepositories"]:

        print(
            app["appName"],
            "|",
            app["appUpdateTime"]
        )
