import zipfile
import os


def extract_icon(ipa_path):

    output = "assets/icons/app_icon.png"

    with zipfile.ZipFile(ipa_path, "r") as ipa:

        icons = []

        for file in ipa.namelist():

            if file.endswith(".png") and ".app/" in file:
                icons.append(file)

        if not icons:
            raise Exception("Иконка не найдена")


        icon = max(
            icons,
            key=lambda x: ipa.getinfo(x).file_size
        )


        data = ipa.read(icon)


    with open(output, "wb") as f:
        f.write(data)


    return output
