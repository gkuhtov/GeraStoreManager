import zipfile
import os
import re


def extract_icon(ipa_path, bundle_id=None):

    output_dir = "assets/icons"

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    if bundle_id:

        safe_name = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            bundle_id
        )

    else:

        safe_name = os.path.splitext(
            os.path.basename(ipa_path)
        )[0]

        safe_name = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            safe_name
        )

    output = os.path.join(
        output_dir,
        safe_name + ".png"
    )

    with zipfile.ZipFile(
        ipa_path,
        "r"
    ) as ipa:

        icons = []

        for file in ipa.namelist():

            if (
                file.endswith(".png")
                and ".app/" in file
            ):

                icons.append(file)

        if not icons:

            raise Exception(
                "Иконка не найдена"
            )

        icon = max(
            icons,
            key=lambda x:
            ipa.getinfo(x).file_size
        )

        data = ipa.read(
            icon
        )

    with open(
        output,
        "wb"
    ) as f:

        f.write(
            data
        )

    return output
