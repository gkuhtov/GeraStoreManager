import os
import zipfile
import tempfile

from core.cgbi import convert_cgbi


GERASTORE_ICONS = os.path.expanduser(
    "~/Projects/GeraStore/icons"
)


def extract_icon(
    ipa_path,
    bundle_id
):

    os.makedirs(
        GERASTORE_ICONS,
        exist_ok=True
    )

    output = os.path.join(
        GERASTORE_ICONS,
        f"{bundle_id}.png"
    )

    candidates = []

    with zipfile.ZipFile(
        ipa_path,
        "r"
    ) as ipa:

        for file in ipa.namelist():

            if not file.lower().endswith(".png"):
                continue

            if ".app/" not in file.lower():
                continue

            try:

                info = ipa.getinfo(file)

                candidates.append(
                    (
                        info.file_size,
                        file
                    )
                )

            except Exception:
                pass

        if not candidates:
            raise Exception(
                "Иконка PNG не найдена"
            )

        candidates.sort(
            reverse=True
        )

        selected = candidates[0][1]

        print(
            "Выбрана иконка:",
            selected
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

            # Проверяем, обычный ли это PNG.
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
                "Обнаружен Apple CgBI. "
                "Конвертируем..."
            )

            convert_cgbi(
                source,
                output
            )

            print(
                "CgBI PNG конвертирован:",
                output
            )

    # Возвращаем URL для GeraStore,
    # а не локальный путь Windows.
    return (
        "https://gkuhtov.github.io/"
        "GeraStore/icons/"
        f"{bundle_id}.png"
    )
