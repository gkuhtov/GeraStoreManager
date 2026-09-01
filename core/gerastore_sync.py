from datetime import datetime

import json
import os
import subprocess
import plistlib

from urllib.request import Request, urlopen
from datetime import timezone
from pathlib import Path


def normalize_compare_value(value, field=""):

    if value is None:
        return ""

    value = str(value).strip()

    if field in [
        "size",
        "fileSize"
    ]:

        try:
            return str(int(value))

        except Exception:
            return value


    if field == "iconURL":

        if "icons/" in value:
            return value.split("icons/")[-1]

        if "assets/icons/" in value:
            return value.split("assets/icons/")[-1]

        return value


    if field in [
        "localizedDescription",
        "appDescription"
    ]:

        lines = []

        for line in value.splitlines():

            line = line.strip()

            while line.endswith(
                (".", "!", "?")
            ):

                line = line[:-1]

            lines.append(line)

        return "\n".join(lines)


    return value



def normalize_value(value):

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return value



def normalize_time(value):

    if not value:
        return ""

    try:

        value = value.replace(
            "Z",
            "+00:00"
        )

        dt = datetime.fromisoformat(
            value
        )

        return dt.strftime(
            "%Y-%m-%dT%H:%M"
        )

    except Exception:

        return value



MANAGER_APPS = "data/apps.json"


GERASTORE_DIR = os.path.expanduser(
    "~/Projects/GeraStore"
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



def get_plist_file_size(plist_url):

    if not plist_url:
        return 0

    try:

        request = Request(
            plist_url,
            headers={
                "User-Agent": "GeraStoreManager/1.0"
            }
        )

        with urlopen(
            request,
            timeout=15
        ) as response:

            plist_data = response.read()


        data = plistlib.loads(
            plist_data
        )


        items = data.get(
            "items",
            []
        )


        if not items:
            return 0


        metadata = items[0].get(
            "metadata",
            {}
        )


        file_size = metadata.get(
            "file-size",
            metadata.get(
                "size",
                0
            )
        )


        try:

            return int(
                file_size
            )

        except Exception:

            return 0


    except Exception as e:

        print(
            "Не удалось получить размер из appPlist:",
            plist_url,
            "|",
            e
        )

        return 0



def get_download_file_size(download_url):

    if not download_url:
        return 0

    try:

        request = Request(
            download_url,
            method="HEAD",
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )


        with urlopen(
            request,
            timeout=20
        ) as response:

            content_length = response.headers.get(
                "Content-Length"
            )


            if content_length:

                return int(
                    content_length
                )


    except Exception as e:

        print(
            "Не удалось получить размер IPA:",
            download_url,
            "|",
            e
        )


    return 0



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



def human_file_size(size):
    try:
        size = int(size or 0)
    except (TypeError, ValueError):
        return ""

    if size <= 0:
        return ""

    return f"{size / (1024 * 1024):.1f} MB"


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


        old_source_time = old.get(
            "sourceUpdateTime",
            ""
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


                plist_url = version.get(
                    "appPlist",
                    ""
                )


                plist_size = get_plist_file_size(
                    plist_url
                )


                if plist_size:

                    size = plist_size


                else:

                    download_url = version.get(
                        "downloadURL",
                        ""
                    )


                    download_size = get_download_file_size(
                        download_url
                    )


                    if download_size:

                        size = download_size


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


                    "appSize":
                    size,


                    "fileSize":
                    size,


                    "appFileSize":
                    size,


                    "human_file_size":
                    human_file_size(size),


                    "appPlist":
                    version.get(
                        "appPlist",
                        ""
                    ),


                    "category":
                    app.get(
                        "category",
                        ""
                    ),


                    "localizedDescription":
                    app.get(
                        "localizedDescription",
                        ""
                    ).strip(),


                    "iconURL":
                    app.get(
                        "iconURL",
                        ""
                    )

                })



            latest = (

                versions[-1]

                if versions

                else {

                    "version":
                    app.get(
                        "version",
                        ""
                    ),

                    "downloadURL":
                    app.get(
                        "downloadURL",
                        ""
                    ),

                    "size":
                    app.get(
                        "size",
                        0
                    ),

                    "fileSize":
                    app.get(
                        "fileSize",
                        0
                    ),

                    "category":
                    app.get(
                        "category",
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
                    )

                }
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

                fields = [

                    "version",

                    "downloadURL",

                    "size",

                    "fileSize",

                    "category",

                    "subtitle",

                    "localizedDescription",

                    "iconURL"

                ]


                for field in fields:

                    old_value = old_app.get(
                        field,
                        ""
                    )


                    if field in [

                        "version",

                        "downloadURL",

                        "size",

                        "fileSize"

                    ]:

                        new_value = latest.get(
                            field,
                            ""
                        )

                    else:

                        new_value = app.get(
                            field,
                            ""
                        )


                    if (
                        normalize_compare_value(
                            old_value,
                            field
                        )
                        !=
                        normalize_compare_value(
                            new_value,
                            field
                        )
                    ):

                        if field in [

                            "category",

                            "localizedDescription",

                            "iconURL"

                        ]:

                            continue


                        print(
                            "DIFFER:",
                            field,
                            "\n OLD:",
                            old_value,
                            "\n NEW:",
                            new_value
                        )


                old_version = old_app.get(
                    "version",
                    ""
                )


                new_version = latest.get(
                    "version",
                    ""
                )


                old_download = old_app.get(
                    "downloadURL",
                    ""
                )


                new_download = latest.get(
                    "downloadURL",
                    ""
                )


                old_size = old_app.get(
                    "size",
                    0
                )


                new_size = latest.get(
                    "size",
                    0
                )


                old_file_size = old_app.get(
                    "fileSize",
                    0
                )


                new_file_size = latest.get(
                    "fileSize",
                    0
                )


                old_icon = old_app.get(
                    "iconURL",
                    ""
                )


                new_icon = app.get(
                    "iconURL",
                    ""
                )


                if new_icon.startswith(
                    "assets/icons/"
                ):

                    new_icon = (

                        "https://gkuhtov.github.io/"
                        "GeraStore/icons/"
                        +
                        new_icon.replace(
                            "assets/icons/",
                            ""
                        )

                    )


                changed = any([

                    old_version != new_version,

                    old_download != new_download,

                    old_size != new_size,

                    old_file_size != new_file_size

                ])


            if changed:

                print(
                    "Изменено:",
                    app.get(
                        "name"
                    )
                )


            update_time = repo_time


            if old_app and not changed:

                update_time = old_app.get(
                    "appUpdateTime",
                    repo_time
                )


            category = app.get(
                "category",
                "Утилиты"
            )


            if category == "БАНК":

                category = "Финансы"


            category_map = {

                "Игры": 0,

                "Приложения": 1,

                "Утилиты": 2,

                "Эмуляторы": 3,

                "Социальные сети": 4,

                "Развлечения": 5,

                "Медиа": 6,

                "Фото и видео": 7,

                "Музыка": 8,

                "Образование": 9,

                "Работа": 10,

                "Финансы": 11,

                "Здоровье": 12,

                "Навигация": 13,

                "Другое": 14

            }


            apps.append({

                "appType":
                "SELF_SIGN",


                "category":
                category,


                "appCateIndex":
                category_map.get(
                    category,
                    1
                ),


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
                ).strip(),


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
                ).strip(),


                "iconURL":
                icon,


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


                "appFileSize":
                size,


                "human_file_size":
                human_file_size(size),


                "versions":
                versions

            })



        source_update_time = old_source_time


        for app in apps:

            if app.get(
                "appUpdateTime"
            ) == repo_time:

                source_update_time = repo_time

                break


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


            "sourceExportEnable":
            True,


            "sourceLinkTitle":
            "GitHub",


            "sourceLinkUrl":
            "https://github.com/gkuhtov/GeraStore",


            "sourceImage":
            "https://gkuhtov.github.io/GeraStore/icons/app_icon.png",


            "sourceDescription":
            "Каталог IPA приложений для GBox.",


            "sourceUpdateTime":
            source_update_time,


            "appCategories":
            [

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

            ],

            "appRepositories":
            apps

        }



    def write_repo(self):

        """
        Пишет ТОЛЬКО в опубликованный файл:
        ~/Projects/GeraStore/repo.json

        Локальное состояние менеджера
        (data/repo.json) обновляется
        только после успешного publish.
        """

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



    def save_manager_repo(
        self,
        repo
    ):

        """
        Обновляет локальное состояние
        менеджера после успешной публикации.
        """



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

        repo_file = Path(
            GERASTORE_DIR
        ) / "repo.json"


        if not repo_file.is_file():

            raise Exception(
                f"Не найден repo.json: {repo_file}"
            )


        # ==================================================
        # ДОБАВЛЯЕМ repo.json
        # ==================================================

        self.git(
            "add",
            "repo.json"
        )


        # ==================================================
        # ДОБАВЛЯЕМ PLIST
        # ==================================================

        self.git(
            "add",
            "plist"
        )


        # ==================================================
        # ДОБАВЛЯЕМ ICONS
        # ==================================================

        self.git(
            "add",
            "icons"
        )


        # ==================================================
        # ПРОВЕРЯЕМ STAGED-ФАЙЛЫ
        # ==================================================

        staged = self.git(
            "diff",
            "--cached",
            "--name-only"
        )


        if not staged.strip():

            return {
                "changed": False,
                "message": "Нет изменений"
            }


        # ==================================================
        # ПОКАЗЫВАЕМ ФАЙЛЫ
        # ==================================================

        print(
            "\n===== FILES TO PUBLISH ====="
        )


        print(
            staged
        )


        print(
            "============================"
        )


        # ==================================================
        # ПОКАЗЫВАЕМ DIFF
        # ==================================================

        diff = self.git(
            "diff",
            "--cached"
        )


        print(
            "\n===== GIT CHANGE ====="
        )


        print(
            diff[:5000]
        )


        print(
            "======================\n"
        )


        # ==================================================
        # COMMIT
        # ==================================================

        self.git(
            "commit",
            "-m",
            commit_message
        )


        # ==================================================
        # PUSH
        # ==================================================

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

        # 1. Собираем новый repo
        #    и пишем только в
        #    ~/Projects/GeraStore/repo.json

        repo = self.write_repo()


        # 2. Публикуем

        result = self.publish(
            commit_message
        )


        # 3. Только после успешной публикации
        #    обновляем локальное состояние
        #    менеджера

        if result.get(
            "changed"
        ):

            self.save_manager_repo(
                repo
            )


        return result