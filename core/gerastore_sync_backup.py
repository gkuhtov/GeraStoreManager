import json
import os
import subprocess
from datetime import datetime, timezone


MANAGER_APPS = "data/apps.json"

GERASTORE_DIR = os.path.expanduser(
    "~/GeraStore"
)

GERASTORE_REPO = os.path.join(
    GERASTORE_DIR,
    "repo.json"
)

BASE_URL = (
    "https://gkuhtov.github.io/"
    "GeraStore/"
)


def now_time():

    return datetime.now(
        timezone.utc
    ).astimezone().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )


def absolute_icon_url(icon):

    if not icon:
        return ""

    icon = icon.replace(
        "\\",
        "/"
    )

    if icon.startswith(
        "http://"
    ) or icon.startswith(
        "https://"
    ):
        return icon

    if icon.startswith(
        "assets/icons/"
    ):

        icon = icon.replace(
            "assets/icons/",
            "icons/"
        )

    if icon.startswith(
        "icons/"
    ):

        return BASE_URL + icon

    return BASE_URL + "icons/" + icon



class GeraStoreSync:


    def __init__(self):

        if not os.path.isdir(
            GERASTORE_DIR
        ):

            raise Exception(
                "GeraStore репозиторий не найден: "
                + GERASTORE_DIR
            )



    def load_json(
        self,
        path
    ):

        if not os.path.exists(
            path
        ):
            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def load_manager_apps(self):

        return self.load_json(
            MANAGER_APPS
        )



    def load_old_repo(self):

        return self.load_json(
            GERASTORE_REPO
        )



    def find_old_app(
        self,
        apps,
        bundle
    ):

        for app in apps:

            if app.get(
                "bundleIdentifier"
            ) == bundle:

                return app

        return None



    def build_repo(self):

        data = self.load_manager_apps()

        old = self.load_old_repo()

        old_apps = old.get(
            "appRepositories",
            []
        )

        repo_time = now_time()

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

                size = version.get(
                    "size",
                    0
                )


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
                    size,

                    "fileSize":
                    size

                })



            latest = (
                versions[-1]
                if versions
                else {}
            )


            bundle = app.get(
                "bundleIdentifier",
                ""
            )


            old_app = self.find_old_app(
                old_apps,
                bundle
            )


            size = latest.get(
                "size",
                0
            )


            icon = absolute_icon_url(
                app.get(
                    "iconURL",
                    ""
                )
            )


            changed = False


            if not old_app:

                changed = True


            else:

                changed = (

                    old_app.get(
                        "version",
                        ""
                    )
                    != latest.get(
                        "version",
                        ""
                    )

                    or

                    old_app.get(
                        "downloadURL",
                        ""
                    )
                    != latest.get(
                        "downloadURL",
                        ""
                    )

                    or

                    old_app.get(
                        "size",
                        0
                    )
                    != size

                    or

                    old_app.get(
                        "iconURL",
                        ""
                    )
                    != icon

                    or

                    old_app.get(
                        "localizedDescription",
                        ""
                    )
                    != app.get(
                        "localizedDescription",
                        ""
                    )

                    or

                    old_app.get(
                        "subtitle",
                        ""
                    )
                    != app.get(
                        "subtitle",
                        ""
                    )

                    or

                    old_app.get(
                        "developerName",
                        ""
                    )
                    != app.get(
                        "developerName",
                        ""
                    )

                    or

                    old_app.get(
                        "category",
                        ""
                    )
                    != app.get(
                        "category",
                        "Utilities"
                    )

                )


            update_time = repo_time


            if old_app and not changed:

                update_time = old_app.get(
                    "appUpdateTime",
                    repo_time
                )



            apps.append({

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
                icon,


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
                bundle,


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
                icon,


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
                size,


                "appSize":
                size,


                "fileSize":
                size,


                "versions":
                versions

            })



        return {

            "version":
            "1.0",


            "sourceName":
            data.get(
                "name",
                "GeraStore"
            ),


            "sourceAuthor":
            "ГЕРЫЧ",


            "sourceDescription":
            "Каталог IPA приложений для GBox.",


            "sourceUpdateTime":
            repo_time,


            "appRepositories":
            apps

        }



    def write_repo(self):

        repo = self.build_repo()

        with open(
            GERASTORE_REPO,
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



    def git(
        self,
        *args
    ):

        result = subprocess.run(
            [
                "git",
                *args
            ],
            cwd=GERASTORE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode != 0:

            raise Exception(
                result.stderr
            )

        return result.stdout.strip()



    def publish(
        self,
        commit_message="GeraStore update"
    ):

        self.git(
            "add",
            "repo.json"
        )


        staged = self.git(
            "diff",
            "--cached",
            "--name-only"
        )


        if not staged:

            return {
                "changed": False,
                "message": "Нет изменений"
            }


        self.git(
            "commit",
            "-m",
            commit_message
        )


        self.git(
            "push",
            "origin",
            "main"
        )


        return {
            "changed": True,
            "message": "Опубликовано"
        }



    def sync(
        self,
        commit_message="GeraStore update"
    ):

        self.write_repo()

        return self.publish(
            commit_message
        )