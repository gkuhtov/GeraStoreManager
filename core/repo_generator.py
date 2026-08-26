import json


def create_repo(data, extra):

    repo = {
        "name": data["name"],
        "bundleIdentifier": data["bundle_id"],
        "developerName": extra["developer"],
        "subtitle": extra["subtitle"],
        "localizedDescription": extra["description"],
        "iconURL": extra["icon_url"],
        "versions": [
            {
                "version": data["version"],
                "date": data.get("date", ""),
                "downloadURL": extra["download_url"],
                "size": data["size"]
            }
        ]
    }


    with open(
        "data/repo.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            repo,
            f,
            indent=2,
            ensure_ascii=False
        )


    return "data/repo.json"
