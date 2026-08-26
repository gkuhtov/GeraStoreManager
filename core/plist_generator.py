import os
from pathlib import Path
from xml.sax.saxutils import escape

GERASTORE_DIR = os.path.expanduser("~/Projects/GeraStore")
PLIST_DIR = os.path.join(GERASTORE_DIR, "plist")
PLIST_BASE_URL = "https://gkuhtov.github.io/GeraStore/plist/"


def build_plist_xml(name, bundle_id, version, download_url, size):
    size = int(size or 0)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>items</key>
\t<array>
\t\t<dict>
\t\t\t<key>assets</key>
\t\t\t<array>
\t\t\t\t<dict>
\t\t\t\t\t<key>kind</key>
\t\t\t\t\t<string>software-package</string>
\t\t\t\t\t<key>url</key>
\t\t\t\t\t<string>{escape(download_url)}</string>
\t\t\t\t</dict>
\t\t\t</array>
\t\t\t<key>metadata</key>
\t\t\t<dict>
\t\t\t\t<key>bundle-identifier</key>
\t\t\t\t<string>{escape(bundle_id)}</string>
\t\t\t\t<key>bundle-version</key>
\t\t\t\t<string>{escape(str(version))}</string>
\t\t\t\t<key>kind</key>
\t\t\t\t<string>software</string>
\t\t\t\t<key>title</key>
\t\t\t\t<string>{escape(name)}</string>
\t\t\t\t<key>file-size</key>
\t\t\t\t<integer>{size}</integer>
\t\t\t</dict>
\t\t</dict>
\t</array>
</dict>
</plist>
"""


def plist_filename(bundle_id: str) -> str:
    safe = "".join(c if c.isalnum() or c in ".-_" else "_" for c in bundle_id)
    return f"{safe}.plist"


def plist_url(bundle_id: str) -> str:
    return PLIST_BASE_URL + plist_filename(bundle_id)


def write_plist(name, bundle_id, version, download_url, size) -> str:
    """
    Пишет файл в ~/Projects/GeraStore/plist/ и возвращает публичный URL.
    """
    os.makedirs(PLIST_DIR, exist_ok=True)

    filename = plist_filename(bundle_id)
    path = os.path.join(PLIST_DIR, filename)

    xml = build_plist_xml(name, bundle_id, version, download_url, size)
    Path(path).write_text(xml, encoding="utf-8")

    print(f"Plist записан: {path}")
    return plist_url(bundle_id)
