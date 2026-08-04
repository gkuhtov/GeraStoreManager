import json
import os


def export_repo():

    source = "data/apps.json"
    output = "export/repo.json"


    if not os.path.exists(source):

        raise Exception(
            "Файл apps.json не найден"
        )


    with open(
        source,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    os.makedirs(
        "export",
        exist_ok=True
    )


    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


    return output
