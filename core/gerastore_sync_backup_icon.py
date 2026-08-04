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


def now_time():

    return datetime.now(
        timezone.utc
    ).astimezone().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )


class GeraStoreSync:


    def __init__(self):

        if not os.path.isdir(GERASTORE_DIR):

            raise Exception(
                "GeraStore репозиторий не найден: "
                + GERASTORE_DIR
            )


    def load_json(self, path):

        if not os.path.exists(path):

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
        old_apps,
        bundle_id
    ):

        for app in old_apps:

            if app.get(
                "bundleIdentifier"
            ) == bundle_id:

                return app

        return None



    def app_changed(
        self,
        old_app,
        new_app
    ):

        if not old_app:

            return True


        fields = [

            "version",

            "downloadURL",

            "size",

            "localizedDescription",

            "iconURL"

        ]


        for field in fields:

            if old_app.get(field) != new_app.get(field):

                return True


        return False



    def build_repo(self):

        data = self.load_manager_apps()

        old_repo = self.load_old_repo()

        old_apps = old_repo.get(
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


            size = latest.get(
                "size",
                0
            )


            bundle_id = app.get(
                "bundleIdentifier",
                ""
            )


            old_app = self.find_old_app(
                old_apps,
                bundle_id
            )


            changed = self.app_changed(

                old_app,

                {

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

                    "localizedDescription":
                    app.get(
                        "localizedDescription",
                        ""
                    ),

                    "iconURL":
                    app.get(
                        "iconURL",
                        ""
                    )

                }

            )


            if changed:

                update_time = repo_time

            else:

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
                bundle_id,


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



    def git(self, *args):

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

                "changed":
                False,

                "message":
                "Нет изменений"

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

            "changed":
            True,

            "message":
            "Опубликовано"

        }



    def sync(
        self,
        commit_message="GeraStore update"
    ):

        self.write_repo()

        return self.publish(
            commit_message
        )