import zipfile
import plistlib
import os
import tempfile
import shutil


class IPAParser:

    def __init__(self, ipa_path):
        self.ipa_path = ipa_path


    def extract_info(self):

        temp_dir = tempfile.mkdtemp()

        try:
            with zipfile.ZipFile(self.ipa_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)


            payload = os.path.join(
                temp_dir,
                "Payload"
            )

            app_folder = None

            for item in os.listdir(payload):
                if item.endswith(".app"):
                    app_folder = os.path.join(
                        payload,
                        item
                    )
                    break


            if not app_folder:
                raise Exception(
                    "APP внутри IPA не найден"
                )


            plist_path = os.path.join(
                app_folder,
                "Info.plist"
            )


            with open(
                plist_path,
                "rb"
            ) as f:

                plist = plistlib.load(f)


            return {

                "name":
                plist.get(
                    "CFBundleDisplayName",
                    plist.get(
                        "CFBundleName",
                        ""
                    )
                ),

                "bundleIdentifier":
                plist.get(
                    "CFBundleIdentifier",
                    ""
                ),

                "version":
                plist.get(
                    "CFBundleShortVersionString",
                    ""
                ),

                "build":
                plist.get(
                    "CFBundleVersion",
                    ""
                ),

                "size":
                os.path.getsize(
                    self.ipa_path
                )

            }


        finally:

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )
