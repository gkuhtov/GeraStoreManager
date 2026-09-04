import zipfile
import os
import plistlib


def read_ipa(path):

    result = {
        "name": "",
        "bundle_id": "",
        "version": "",
        "minimum_ios": "",
        "size": 0
    }

    result["size"] = os.path.getsize(path)

    with zipfile.ZipFile(path, "r") as ipa:

        plist_file = None

        for file in ipa.namelist():
            if file.endswith(".app/Info.plist"):
                plist_file = file
                break

        if not plist_file:
            raise Exception("Info.plist не найден")

        plist_data = ipa.read(plist_file)

    plist = plistlib.loads(plist_data)

    result["name"] = (
        plist.get("CFBundleDisplayName")
        or plist.get("CFBundleName")
        or ""
    )

    result["bundle_id"] = plist.get(
        "CFBundleIdentifier",
        ""
    )

    result["version"] = plist.get(
        "CFBundleShortVersionString",
        ""
    )

    result["minimum_ios"] = (
        plist.get("MinimumOSVersion")
        or plist.get("CFBundleMinimumOSVersion")
        or ""
    )

    return result