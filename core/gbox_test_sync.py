import json
import os
from datetime import datetime, timezone


MANAGER_APPS = "data/apps.json"

TEST_REPO = os.path.expanduser(
    "~/Projects/GeraStore-Test"
)

REPO_FILE = os.path.join(
    TEST_REPO,
    "repo.json"
)


def now_time():

    return datetime.now(
        timezone.utc
    ).astimezone().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )


def load_apps():

    with open(
        MANAGER_APPS,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_repo():

    data = load_apps()

    update_time = now_time()

    apps = []


    for app in data.get(
        "apps",
        []
    ):

        versions = []

        for version in app.get(
            "versions",
            []
        ):

            versions.append({

                "version":
                version.get(
                    "version",
                    ""
                ),

                "date":
                version.get(
                    "date",
                    ""
                ),

                "downloadURL":
                version.get(
                    "downloadURL",
                    ""
                ),

                "size":
                version.get(
                    "size",
                    0
                )

            })


        latest = (
            versions[-1]
            if versions
            else {}
        )


        app_data = {

            "appType":
            "SELF_SIGN",


            "appUpdateTime":
            update_time,


            "versionDate":
            latest.get(
                "date",
                ""
            ),


            "appName":
            app.get(
                "name",
                ""
            ),


            "appVersion":
            latest.get(
                "version",
                ""
            ),


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
            latest.get(
                "version",
                ""
            ),


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
            app_data
        )


    return {

        "version":
        "1.0",


        "sourceName":
        "GeraStore Test",


        "sourceAuthor":
        "ГЕРЫЧ",


        "sourceDescription":
        "Тестовый репозиторий GBox",


        "sourceUpdateTime":
        update_time,


        "appRepositories":
        apps

    }



def write_repo():

    os.makedirs(
        TEST_REPO,
        exist_ok=True
    )


    repo = build_repo()


    with open(
        REPO_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            repo,
            f,
            indent=2,
            ensure_ascii=False
        )


    return repo



if __name__ == "__main__":

    repo = write_repo()


    print(
        "Тестовый repo.json создан:"
    )

    print(
        REPO_FILE
    )


    for app in repo["appRepositories"]:

        print(
            app["appName"],
            "|",
            app["appUpdateTime"]
        )
