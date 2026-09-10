import os
from pathlib import Path
from xml.sax.saxutils import escape


GERASTORE_DIR = os.path.expanduser(
    "~/Projects/GeraKStore"
)

PLIST_DIR = os.path.join(
    GERASTORE_DIR,
    "plist"
)

PLIST_BASE_URL = (
    "https://gkuhtov.github.io/GeraKStore/plist/"
)


def build_plist_xml(
    name,
    bundle_id,
    version,
    download_url,
    size,
    minimum_ios=""
):
    size = int(size or 0)

    minimum_ios = str(
        minimum_ios or ""
    ).strip()

    minimum_ios_block = ""

    if minimum_ios:
        minimum_ios_block = f"""
                <key>MinimumOSVersion</key>
                <string>{escape(minimum_ios)}</string>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{escape(download_url)}</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{escape(bundle_id)}</string>
                <key>bundle-version</key>
                <string>{escape(str(version))}</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{escape(name)}</string>
                <key>file-size</key>
                <integer>{size}</integer>{minimum_ios_block}
            </dict>
        </dict>
    </array>
</dict>
</plist>
"""


def plist_filename(bundle_id: str) -> str:
    safe = "".join(
        c if c.isalnum() or c in ".-_" else "_"
        for c in bundle_id
    )

    return f"{safe}.plist"


def plist_url(bundle_id: str) -> str:
    return (
        PLIST_BASE_URL
        + plist_filename(bundle_id)
    )


def write_plist(
    name,
    bundle_id,
    version,
    download_url,
    size,
    minimum_ios=""
) -> str:
    """
    Пишет файл в ~/Projects/GeraKStore/plist/
    и возвращает публичный URL.
    """

    os.makedirs(
        PLIST_DIR,
        exist_ok=True
    )

    filename = plist_filename(
        bundle_id
    )

    path = os.path.join(
        PLIST_DIR,
        filename
    )

    xml = build_plist_xml(
        name=name,
        bundle_id=bundle_id,
        version=version,
        download_url=download_url,
        size=size,
        minimum_ios=minimum_ios
    )

    Path(path).write_text(
        xml,
        encoding="utf-8"
    )

    print(
        f"Plist записан: {path}"
    )

    if minimum_ios:
        print(
            f"Minimum iOS: {minimum_ios}"
        )

    return plist_url(bundle_id)