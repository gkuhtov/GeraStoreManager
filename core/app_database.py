import json
import os
from datetime import datetime, timezone


DATABASE = "data/apps.json"


def get_now():

    return datetime.now(
        timezone.utc
    ).isoformat().replace(
        "+00:00",
        "Z"
    )


def load_apps():

    if not os.path.exists(DATABASE):

        return {
            "name": "GeraKStore",
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


def get_latest_version(app):

    versions = app.get(
        "versions",
        []
    )

    if not versions:
        return {}

    return versions[-1]


def add_app(app):

    data = load_apps()

    existing_apps = data.get(
        "apps",
        []
    )

    bundle_id = app.get(
        "bundleIdentifier",
        ""
    )

    existing = None

    for item in existing_apps:

        if item.get(
            "bundleIdentifier",
            ""
        ) == bundle_id:

            existing = item
            break

    # ==================================================
    # NEW APP
    # ==================================================

    if existing is None:

        now = get_now()

        if not app.get(
            "addedDate"
        ):

            app["addedDate"] = now

        app["appUpdateTime"] = now

        existing_apps.append(
            app
        )

    # ==================================================
    # EXISTING APP
    # ==================================================

    else:

        # --------------------------------------------------
        # Сохраняем дату первого добавления.
        # --------------------------------------------------

        if existing.get(
            "addedDate"
        ):

            app["addedDate"] = existing[
                "addedDate"
            ]

        else:

            app["addedDate"] = get_now()

        # --------------------------------------------------
        # Старые версии.
        # --------------------------------------------------

        old_versions = existing.get(
            "versions",
            []
        )

        # Делаем отдельную копию списка,
        # чтобы не менять старую запись напрямую.
        versions = list(
            old_versions
        )

        # --------------------------------------------------
        # Новая версия.
        # --------------------------------------------------

        new_versions = app.get(
            "versions",
            []
        )

        if not new_versions:

            # Защита от некорректной записи.
            app["versions"] = versions

            app["appUpdateTime"] = existing.get(
                "appUpdateTime",
                get_now()
            )

        else:

            new_version_data = new_versions[-1]

            new_version = new_version_data.get(
                "version",
                ""
            )

            new_url = new_version_data.get(
                "downloadURL",
                ""
            )

            # --------------------------------------------------
            # Проверяем, существует ли уже такая версия.
            # --------------------------------------------------

            existing_version_index = None

            for index, version_data in enumerate(
                versions
            ):

                if version_data.get(
                    "version",
                    ""
                ) == new_version:

                    existing_version_index = index
                    break

            # --------------------------------------------------
            # Новая версия.
            # --------------------------------------------------

            if existing_version_index is None:

                versions.append(
                    new_version_data
                )

                app["appUpdateTime"] = get_now()

                print()
                print(
                    f"Новая версия обнаружена: "
                    f"{new_version}"
                )

            # --------------------------------------------------
            # Версия уже существует.
            # --------------------------------------------------

            else:

                old_version_data = versions[
                    existing_version_index
                ]

                old_url = old_version_data.get(
                    "downloadURL",
                    ""
                )

                # Обновляем запись версии, если
                # изменился URL или данные версии.
                if old_version_data != new_version_data:

                    versions[
                        existing_version_index
                    ] = new_version_data

                    app["appUpdateTime"] = get_now()

                    print()
                    print(
                        f"Версия обновлена: "
                        f"{new_version}"
                    )

                else:

                    app["appUpdateTime"] = existing.get(
                        "appUpdateTime",
                        get_now()
                    )

            app["versions"] = versions

        # --------------------------------------------------
        # Сохраняем актуальные данные приложения,
        # но версии оставляем объединёнными.
        # --------------------------------------------------

        index = existing_apps.index(
            existing
        )

        existing_apps[index] = app

    data["apps"] = existing_apps

    save_apps(
        data
    )
