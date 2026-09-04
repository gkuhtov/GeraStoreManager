import os
from datetime import datetime, timezone

import customtkinter as ctk
from tkinter import filedialog

from core.ipa_reader import read_ipa
from core.icon_extractor import extract_icon
from core.app_database import add_app
from core.plist_generator import write_plist
from core.github_release import GitHubRelease
from core.settings import APP_CATEGORIES, get_github_settings


class AddApp(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.ipa_data = None
        self.icon_path = None
        self.ipa_file = None

        self.create_interface()

    def create_interface(self):

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.form = self.scroll_frame

        title = ctk.CTkLabel(
            self.form,
            text="Добавление IPA",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=(10, 3)
        )

        subtitle = ctk.CTkLabel(
            self.form,
            text="Выберите IPA-файл для добавления в GeraStore",
            text_color="gray"
        )

        subtitle.pack(
            pady=(0, 15)
        )

        self.select_button = ctk.CTkButton(
            self.form,
            text="📦  Выбрать IPA",
            height=42,
            command=self.select_ipa
        )

        self.select_button.pack(
            pady=8
        )

        self.preview = ctk.CTkFrame(
            self.form,
            corner_radius=14
        )

        self.preview.pack(
            fill="x",
            padx=10,
            pady=15
        )

        self.preview.grid_columnconfigure(
            1,
            weight=1
        )

        self.icon_label = ctk.CTkLabel(
            self.preview,
            text="📱",
            width=100,
            height=100,
            font=("Arial", 48)
        )

        self.icon_label.grid(
            row=0,
            column=0,
            rowspan=5,
            padx=(20, 15),
            pady=20
        )

        self.name_label = ctk.CTkLabel(
            self.preview,
            text="Приложение не выбрано",
            font=("Arial", 21, "bold"),
            anchor="w"
        )

        self.name_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 20),
            pady=(20, 3)
        )

        self.developer_preview = ctk.CTkLabel(
            self.preview,
            text="Разработчик не указан",
            text_color="gray",
            anchor="w"
        )

        self.developer_preview.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 20),
            pady=2
        )

        self.version_preview = ctk.CTkLabel(
            self.preview,
            text="Версия: •",
            anchor="w"
        )

        self.version_preview.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(0, 20),
            pady=2
        )

        self.bundle_preview = ctk.CTkLabel(
            self.preview,
            text="Bundle ID: •",
            text_color="gray",
            anchor="w"
        )

        self.bundle_preview.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(0, 20),
            pady=2
        )

        self.minimum_ios_preview = ctk.CTkLabel(
            self.preview,
            text="Минимальная iOS: •",
            text_color="gray",
            anchor="w"
        )

        self.minimum_ios_preview.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=(0, 20),
            pady=(2, 20)
        )

        self.info = ctk.CTkTextbox(
            self.form,
            height=140,
            corner_radius=10
        )

        self.info.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        self.developer = self.create_field(
            "Разработчик",
            "Например: Alfa-Bank"
        )

        self.subtitle_field = self.create_field(
            "Subtitle",
            "Краткое описание приложения"
        )

        self.category_field = self.create_combo_field(
            "Категория",
            APP_CATEGORIES
        )

        self.category_field.set(
            "Приложения"
        )

        self.description = self.create_text_field(
            "Описание",
            "Полное описание приложения"
        )

        self.add_button = ctk.CTkButton(
            self.form,
            text="✓  Добавить приложение",
            height=45,
            font=("Arial", 14, "bold"),
            command=self.save
        )

        self.add_button.pack(
            pady=(20, 30)
        )

    def create_field(
        self,
        title,
        placeholder=""
    ):

        container = ctk.CTkFrame(
            self.form,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=10,
            pady=7
        )

        label = ctk.CTkLabel(
            container,
            text=title,
            font=("Arial", 13, "bold")
        )

        label.pack(
            anchor="w",
            pady=(0, 4)
        )

        field = ctk.CTkEntry(
            container,
            height=38,
            placeholder_text=placeholder
        )

        field.pack(
            fill="x"
        )

        return field

    def create_text_field(
        self,
        title,
        placeholder=""
    ):

        container = ctk.CTkFrame(
            self.form,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=10,
            pady=7
        )

        label = ctk.CTkLabel(
            container,
            text=title,
            font=("Arial", 13, "bold")
        )

        label.pack(
            anchor="w",
            pady=(0, 4)
        )

        field = ctk.CTkTextbox(
            container,
            height=120,
            corner_radius=8
        )

        field.pack(
            fill="x"
        )

        return field

    def create_combo_field(
        self,
        title,
        values
    ):

        container = ctk.CTkFrame(
            self.form,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=10,
            pady=7
        )

        label = ctk.CTkLabel(
            container,
            text=title,
            font=("Arial", 13, "bold")
        )

        label.pack(
            anchor="w",
            pady=(0, 4)
        )

        combo = ctk.CTkComboBox(
            container,
            values=values,
            height=38
        )

        combo.pack(
            fill="x"
        )

        return combo

    def select_ipa(self):

        file = filedialog.askopenfilename(
            title="Выберите IPA",
            filetypes=[
                ("IPA files", "*.ipa")
            ]
        )

        if not file:
            return

        try:

            self.ipa_file = file

            self.ipa_data = read_ipa(
                file
            )

            print(
                "========================================"
            )

            print(
                "IPA DEBUG"
            )

            print(
                "IPA:",
                file
            )

            print(
                "BUNDLE ID:",
                self.ipa_data.get(
                    "bundle_id"
                )
            )

            print(
                "NAME:",
                self.ipa_data.get(
                    "name"
                )
            )

            print(
                "VERSION:",
                self.ipa_data.get(
                    "version"
                )
            )

            print(
                "MINIMUM iOS:",
                self.ipa_data.get(
                    "minimum_ios"
                )
            )

            print(
                "SIZE:",
                self.ipa_data.get(
                    "size"
                )
            )

            print(
                "========================================"
            )

            try:

                self.icon_path = extract_icon(
                    file,
                    self.ipa_data["bundle_id"]
                )

                print(
                    "ICON RESULT:",
                    self.icon_path
                )

                print(
                    "ICON EXISTS:",
                    os.path.isfile(
                        self.icon_path
                    )
                    if self.icon_path
                    else False
                )

                if (
                    self.icon_path
                    and os.path.isfile(
                        self.icon_path
                    )
                ):

                    print(
                        "ICON SIZE:",
                        os.path.getsize(
                            self.icon_path
                        )
                    )

            except Exception as icon_error:

                import traceback

                print(
                    "========================================"
                )

                print(
                    "ICON EXTRACTION ERROR"
                )

                print(
                    type(icon_error).__name__,
                    ":",
                    icon_error
                )

                traceback.print_exc()

                print(
                    "========================================"
                )

                raise

            if not self.icon_path:

                self.ipa_data = None
                self.ipa_file = None
                self.icon_path = None

                raise Exception(
                    "Не удалось извлечь иконку из IPA.\n"
                    "Публикация без иконки запрещена.\n"
                    "Попробуй другой IPA или проверь, "
                    "что в архиве есть PNG."
                )

            name = self.ipa_data.get(
                "name",
                ""
            )

            if not name:
                name = "Без названия"

            self.name_label.configure(
                text=name
            )

            version = self.ipa_data.get(
                "version",
                ""
            )

            if not version:
                version = "не указана"

            self.version_preview.configure(
                text=f"Версия: {version}"
            )

            bundle_id = self.ipa_data.get(
                "bundle_id",
                ""
            )

            if not bundle_id:
                bundle_id = "не указан"

            self.bundle_preview.configure(
                text=f"Bundle ID: {bundle_id}"
            )

            minimum_ios = self.ipa_data.get(
                "minimum_ios",
                ""
            )

            if not minimum_ios:
                minimum_ios = "не указана"

            self.minimum_ios_preview.configure(
                text=f"Минимальная iOS: {minimum_ios}"
            )

            developer = self.ipa_data.get(
                "developer",
                ""
            )

            if developer:

                self.developer.delete(
                    0,
                    "end"
                )

                self.developer.insert(
                    0,
                    developer
                )

                self.developer_preview.configure(
                    text=developer
                )

            size = self.ipa_data.get(
                "size",
                0
            )

            size_mb = round(
                size / 1024 / 1024,
                2
            )

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"IPA выбран.\n\n"
                f"Размер: {size_mb} MB\n"
                f"Минимальная iOS: {minimum_ios}\n"
                f"Иконка: {self.icon_path}\n\n"
            )

            self.select_button.configure(
                text="✓  IPA выбрано"
            )

        except Exception as error:

            print(
                "SELECT IPA ERROR:",
                repr(error)
            )

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"Ошибка чтения IPA:\n\n{error}"
            )

    def make_release_tag(self):

        bundle = self.ipa_data.get(
            "bundle_id",
            "app"
        )

        version = self.ipa_data.get(
            "version",
            "unknown"
        )

        safe_bundle = "".join(
            char
            if char.isalnum() or char in ".-_"
            else "-"
            for char in bundle
        )

        safe_version = "".join(
            char
            if char.isalnum() or char in ".-_"
            else "-"
            for char in version
        )

        return (
            f"gerastore-{safe_bundle}-{safe_version}"
        )

    def make_asset_name(self):

        name = self.ipa_data.get(
            "name",
            "app"
        )

        version = self.ipa_data.get(
            "version",
            "unknown"
        )

        safe_name = "".join(
            char
            if char.isalnum() or char in " .-_"
            else "_"
            for char in name
        ).strip()

        safe_name = safe_name.replace(
            " ",
            "_"
        )

        safe_version = "".join(
            char
            if char.isalnum() or char in ".-_"
            else "-"
            for char in version
        )

        return (
            f"{safe_name}_{safe_version}.ipa"
        )

    def upload_to_github(self):

        settings = get_github_settings()

        if not settings.get(
            "token"
        ):

            raise Exception(
                "GitHub Token не указан в settings.json"
            )

        github = GitHubRelease(
            settings["owner"],
            settings["repo"],
            settings["token"]
        )

        tag = self.make_release_tag()

        name = self.ipa_data.get(
            "name",
            "GeraStore App"
        )

        version = self.ipa_data.get(
            "version",
            ""
        )

        release_name = name

        if version:
            release_name += f" {version}"

        description = (
            self.subtitle_field.get().strip()
        )

        release = github.create_release(
            tag=tag,
            name=release_name,
            description=description
        )

        asset_name = self.make_asset_name()

        asset = github.upload_file(
            release,
            self.ipa_file
        )

        download_url = github.get_download_url(
            asset
        )

        return (
            release,
            asset,
            download_url
        )

    def save(self):

        if not self.ipa_data:

            self.show_error(
                "Сначала выберите IPA."
            )

            return

        if not self.ipa_file:

            self.show_error(
                "Файл IPA не выбран."
            )

            return

        if not self.icon_path:

            self.show_error(
                "Иконка не извлечена из IPA.\n"
                "Публикация отменена.\n"
                "Выбери IPA заново."
            )

            return

        self.add_button.configure(
            text="⏳  Добавление приложения...",
            state="disabled"
        )

        self.select_button.configure(
            state="disabled"
        )

        self.info.delete(
            "1.0",
            "end"
        )

        self.info.insert(
            "end",
            "Проверка данных приложения...\n\n"
        )

        self.update()

        try:

            name = self.ipa_data.get(
                "name",
                "GeraStore App"
            )

            version = self.ipa_data.get(
                "version",
                "unknown"
            )

            bundle_id = self.ipa_data.get(
                "bundle_id",
                "app"
            )

            size = self.ipa_data.get(
                "size",
                0
            )

            minimum_ios = self.ipa_data.get(
                "minimum_ios",
                ""
            )

            self.info.insert(
                "end",
                "Минимальная iOS: "
                f"{minimum_ios or 'не указана'}\n\n"
            )

            self.info.insert(
                "end",
                "Подготовка GitHub Release...\n"
            )

            self.update()

            release, asset, download_url = (
                self.upload_to_github()
            )

            self.info.insert(
                "end",
                "✓ GitHub Release создан/найден.\n"
            )

            self.info.insert(
                "end",
                f"✓ IPA загружен: "
                f"{asset.get('name', '')}\n"
            )

            self.info.insert(
                "end",
                "✓ Download URL получен.\n\n"
            )

            self.info.insert(
                "end",
                f"{download_url}\n\n"
            )

            self.update()

            self.info.insert(
                "end",
                "Создание appPlist...\n"
            )

            self.update()

            app_plist = write_plist(
                name=name,
                bundle_id=bundle_id,
                version=version,
                download_url=download_url,
                size=size,
                minimum_ios=minimum_ios
            )

            self.info.insert(
                "end",
                f"✓ Plist: {app_plist}\n"
            )

            self.info.insert(
                "end",
                f"✓ Minimum iOS: "
                f"{minimum_ios or 'не указана'}\n\n"
            )

            self.update()

            description = self.description.get(
                "1.0",
                "end"
            ).strip()

            app = {
                "name": name,
                "bundleIdentifier": bundle_id,
                "developerName": self.developer.get().strip(),
                "category": self.category_field.get(),
                "subtitle": self.subtitle_field.get().strip(),
                "localizedDescription": description,
                "iconURL": self.icon_path,
                "versions": [
                    {
                        "version": version,
                        "date": datetime.now(
                            timezone.utc
                        ).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "downloadURL": download_url,
                        "size": size,
                        "minimumOSVersion": minimum_ios,
                        "appPlist": app_plist
                    }
                ]
            }

            self.info.insert(
                "end",
                "Сохранение приложения...\n"
            )

            self.update()

            add_app(app)

            self.info.insert(
                "end",
                "✓ Приложение добавлено "
                "в GeraStore Manager.\n\n"
            )

            self.info.insert(
                "end",
                "GitHub Release:\n"
            )

            self.info.insert(
                "end",
                f"{release.get('html_url', '')}\n\n"
            )

            self.info.insert(
                "end",
                "Download URL:\n"
            )

            self.info.insert(
                "end",
                f"{download_url}\n\n"
            )

            self.info.insert(
                "end",
                f"Минимальная iOS: "
                f"{minimum_ios or 'не указана'}\n\n"
            )

            self.info.insert(
                "end",
                f"Размер IPA: "
                f"{round(size / 1024 / 1024, 2)} MB\n\n"
            )

            self.info.insert(
                "end",
                "✓ IPA автоматически загружен "
                "в GitHub Release."
            )

            self.add_button.configure(
                text="✓  Приложение добавлено"
            )

        except Exception as error:

            print(
                "SAVE ERROR:",
                repr(error)
            )

            self.info.insert(
                "end",
                "\n\nОШИБКА:\n"
                f"{error}"
            )

            self.add_button.configure(
                text="❌  Ошибка"
            )

        finally:

            self.select_button.configure(
                state="normal"
            )

            self.add_button.configure(
                state="normal"
            )

    def show_error(
        self,
        message
    ):

        self.info.delete(
            "1.0",
            "end"
        )

        self.info.insert(
            "end",
            f"Ошибка:\n\n{message}"
        )

        self.add_button.configure(
            text="✓  Добавить приложение",
            state="normal"
        )

        self.select_button.configure(
            state="normal"
        )