import json
import os
from datetime import datetime

from core.app_database import load_apps


TEST_REPO = os.path.expanduser(
    "~/Projects/GeraKStore-Test/repo.json"
)


BASE_URL = (
    "https://gkuhtov.github.io/"
    "GeraKStore-Test/"
)


def build_test_repo():

    data = load_apps()

    apps = []

    for app in data.get("apps", []):

        versions = app.get(
            "versions",
            []
        )

        latest = (
            versions[-1]
            if versions
            else {}
        )

        version = latest.get(
            "version",
            ""
        )

        date = latest.get(
            "date",
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

        item = {

            "appType":
            "SELF_SIGN",

            "appUpdateTime":
            datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S+0800"
            ),

            "versionDate":
            date,

            "appName":
            app.get(
                "name",
                ""
            ),

            "appVersion":
            version,

            "appImage":
            app.get(
                "iconURL",
                ""
            ),

            "appPackage":
            latest.get(
                "downloadURL",
                ""
            ),

            "appDescription":
            app.get(
                "localizedDescription",
                ""
            ),

            "name":
            app.get(
                "name",
                ""
            ),

            "bundleIdentifier":
            app.get(
                "bundleIdentifier",
                ""
            ),

            "developerName":
            app.get(
                "developerName",
                ""
            ),

            "subtitle":
            app.get(
                "subtitle",
                ""
            ),

            "localizedDescription":
            app.get(
                "localizedDescription",
                ""
            ),

            "iconURL":
            app.get(
                "iconURL",
                ""
            ),

            "category":
            app.get(
                "category",
                "Utilities"
            ),

            "version":
            version,

            "downloadURL":
            latest.get(
                "downloadURL",
                ""
            ),

            "size":
            latest.get(
                "size",
                0
            ),

            "versions":
            versions
        }


        apps.append(
            item
        )


    repo = {

        "version":
        "1.0",

        "sourceName":
        "GeraKStore Test",

        "sourceAuthor":
        "ГЕРЫЧ",

        "sourceDescription":
        "Тестовый репозиторий GBox",

        "sourceUpdateTime":
        datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S+0800"
        ),

        "appRepositories":
        apps
    }


    return repo



def main():

    repo = build_test_repo()


    os.makedirs(
        os.path.dirname(TEST_REPO),
        exist_ok=True
    )


    with open(
        TEST_REPO,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            repo,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        "Тестовый repo.json создан:"
    )

    print(
        TEST_REPO
    )


    for app in repo["appRepositories"]:

        print(
            app["appName"],
            "|",
            app.get(
                "appUpdateTime"
            )
        )



if __name__ == "__main__":
    main()
