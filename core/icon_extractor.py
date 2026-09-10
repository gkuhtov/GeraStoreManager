import os
import zipfile
import tempfile
import plistlib

from core.cgbi import convert_cgbi


GERASTORE_ICONS = os.path.expanduser(
    "~/Projects/GeraKStore/icons"
)


def _find_app_root(files):
    """
    Находит основной .app внутри IPA.
    Исключает PlugIns/*.appex и другие вложенные приложения.
    """
    candidates = []

    for file in files:
        parts = file.split("/")

        if len(parts) >= 2 and parts[0] == "Payload":
            for i, part in enumerate(parts[1:], start=1):
                if part.lower().endswith(".app"):
                    app_root = "/".join(parts[:i + 1]) + "/"

                    if ".appex/" not in app_root.lower():
                        candidates.append(app_root)
                    break

    if not candidates:
        return None

    candidates = sorted(set(candidates), key=len)

    return candidates[0]


def _read_info_plist(ipa, app_root):
    """
    Читает Info.plist основного приложения.
    """
    plist_path = app_root + "Info.plist"

    try:
        data = ipa.read(plist_path)
        return plistlib.loads(data)
    except Exception as e:
        print(
            "Не удалось прочитать Info.plist:",
            e
        )
        return {}


def _icon_names_from_plist(plist):
    """
    Возвращает имена основной иконки из CFBundleIcons.
    """
    names = []

    for key in (
        "CFBundleIcons",
        "CFBundleIcons~ipad",
    ):
        icons = plist.get(key)

        if not isinstance(icons, dict):
            continue

        primary = icons.get(
            "CFBundlePrimaryIcon"
        )

        if not isinstance(primary, dict):
            continue

        files = primary.get(
            "CFBundleIconFiles",
            []
        )

        if isinstance(files, str):
            files = [files]

        for name in files:
            if isinstance(name, str):
                name = name.strip()

                if name and name not in names:
                    names.append(name)

    return names


def _find_icon_by_plist(files, app_root, icon_names):
    """
    Ищет PNG основной иконки по именам из Info.plist.

    Ищем только непосредственно внутри основного .app.
    PlugIns/*.appex не рассматриваем.
    """
    app_pngs = []

    for file in files:
        if not file.startswith(app_root):
            continue

        relative = file[len(app_root):]

        # Иконка должна находиться непосредственно
        # в корне основного .app.
        if "/" in relative:
            continue

        if not file.lower().endswith(".png"):
            continue

        app_pngs.append(file)

    if not app_pngs:
        return None

    # Сначала точные совпадения.
    for name in icon_names:
        expected = name.lower()

        if expected.endswith(".png"):
            expected = expected[:-4]

        for file in app_pngs:
            basename = os.path.basename(file)
            stem = os.path.splitext(basename)[0]

            if stem.lower() == expected:
                return file

    # Затем варианты @2x, @3x и т.д.
    for name in icon_names:
        expected = name.lower()

        if expected.endswith(".png"):
            expected = expected[:-4]

        matches = []

        for file in app_pngs:
            basename = os.path.basename(file)
            stem = os.path.splitext(basename)[0].lower()

            if stem.startswith(expected + "@"):
                matches.append(file)

        if matches:
            # Предпочитаем @3x, затем @2x.
            matches.sort(
                key=lambda x: (
                    "@3x" not in x.lower(),
                    "@2x" not in x.lower(),
                    len(x)
                )
            )

            return matches[0]

    return None


def _find_fallback_icon(files, app_root):
    """
    Резервный поиск иконки, если Info.plist не помог.

    Не выбираем случайную большую PNG.
    Сначала проверяем стандартные имена AppIcon.
    """
    app_pngs = []

    for file in files:
        if not file.startswith(app_root):
            continue

        relative = file[len(app_root):]

        if "/" in relative:
            continue

        if not file.lower().endswith(".png"):
            continue

        app_pngs.append(file)

    if not app_pngs:
        return None

    priority_names = (
        "AppIcon60x60@3x.png",
        "AppIcon60x60@2x.png",
        "AppIcon60x60.png",
        "AppIcon76x76@2x~ipad.png",
        "AppIcon76x76.png",
        "AppIcon@3x.png",
        "AppIcon@2x.png",
        "AppIcon.png",
    )

    lower_map = {
        os.path.basename(f).lower(): f
        for f in app_pngs
    }

    for name in priority_names:
        found = lower_map.get(name.lower())

        if found:
            return found

    # Дополнительный поиск по AppIcon.
    appicon_matches = [
        f for f in app_pngs
        if "appicon" in os.path.basename(f).lower()
    ]

    if appicon_matches:
        appicon_matches.sort(
            key=lambda x: (
                "@3x" not in x.lower(),
                "@2x" not in x.lower(),
                len(x)
            )
        )

        return appicon_matches[0]

    return None


def extract_icon(
    ipa_path,
    bundle_id
):
    """
    Извлекает иконку приложения из IPA.

    Приоритет:
    1. CFBundleIcons / CFBundleIcons~ipad.
    2. Стандартные AppIcon*.png.
    3. Если ничего не найдено, выдаём понятную ошибку.
    """

    os.makedirs(
        GERASTORE_ICONS,
        exist_ok=True
    )

    output = os.path.join(
        GERASTORE_ICONS,
        f"{bundle_id}.png"
    )

    with zipfile.ZipFile(
        ipa_path,
        "r"
    ) as ipa:

        files = ipa.namelist()

        app_root = _find_app_root(files)

        if not app_root:
            raise Exception(
                "Основное приложение .app не найдено"
            )

        print(
            "Основной .app:",
            app_root
        )

        plist = _read_info_plist(
            ipa,
            app_root
        )

        icon_names = _icon_names_from_plist(
            plist
        )

        print(
            "Имена иконок из Info.plist:",
            icon_names
        )

        selected = None

        if icon_names:
            selected = _find_icon_by_plist(
                files,
                app_root,
                icon_names
            )

        if selected:
            print(
                "Иконка найдена по Info.plist:",
                selected
            )
        else:
            selected = _find_fallback_icon(
                files,
                app_root
            )

            if selected:
                print(
                    "Иконка найдена резервным поиском:",
                    selected
                )

        if not selected:
            raise Exception(
                "Иконка приложения не найдена. "
                "Проверь CFBundleIcons, "
                "AppIcon*.png или Assets.car."
            )

        data = ipa.read(
            selected
        )

    with tempfile.TemporaryDirectory() as tmp:

        source = os.path.join(
            tmp,
            "source.png"
        )

        with open(
            source,
            "wb"
        ) as f:
            f.write(data)

        try:
            from PIL import Image

            img = Image.open(
                source
            )

            img.load()

            img = img.convert(
                "RGBA"
            )

            img.save(
                output,
                "PNG",
                optimize=True
            )

            print(
                "Обычный PNG сохранён:",
                output
            )

        except Exception:

            print(
                "PNG не открылся как обычный PNG. "
                "Пробуем Apple CgBI..."
            )

            convert_cgbi(
                source,
                output
            )

            print(
                "CgBI PNG конвертирован:",
                output
            )

    return (
        "https://gkuhtov.github.io/"
        "GeraKStore/icons/"
        f"{bundle_id}.png"
    )
