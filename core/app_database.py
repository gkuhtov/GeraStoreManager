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

    try:

        from core.gerastore_sync import GeraStoreSync

        print()
        print("=" * 60)
        print("GeraStore Manager: база сохранена")
        print("=" * 60)
        print("Запускаем синхронизацию с GitHub...")

        sync = GeraStoreSync()

        result = sync.sync(
            commit_message="Auto update GeraStore"
        )

        print(
            "Результат синхронизации:",
            result
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("ОШИБКА АВТОПУБЛИКАЦИИ")
        print("=" * 60)
        print(error)


def add_app(app):

    data = load_apps()

    existing_apps = data.get(
        "apps",
        []
    )

    bundle_id = app.get(
        "bundleIdentifier"
    )

    existing = None

    for item in existing_apps:

        if item.get(
            "bundleIdentifier"
        ) == bundle_id:

            existing = item
            break

    # Новое приложение.
    # Сохраняем дату первого добавления.

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

    else:

        # Сохраняем старую дату добавления.

        if existing.get(
            "addedDate"
        ):

            app["addedDate"] = existing[
                "addedDate"
            ]

        elif not app.get(
            "addedDate"
        ):

            app["addedDate"] = get_now()

        old_version = existing.get(
            "version",
            ""
        )

        new_version = app.get(
            "version",
            ""
        )


        old_url = existing.get(
            "downloadURL",
            ""
        )

        new_url = app.get(
            "downloadURL",
            ""
        )


        if (
            old_version != new_version
            or old_url != new_url
        ):

            app["appUpdateTime"] = get_now()

        else:

            app["appUpdateTime"] = existing.get(
                "appUpdateTime",
                get_now()
            )


        # Заменяем старую запись
        # актуальными данными.

        index = existing_apps.index(
            existing
        )

        existing_apps[index] = app

    data["apps"] = existing_apps

    save_apps(
        data
    )
