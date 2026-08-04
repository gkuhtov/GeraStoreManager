import os
from datetime import date
import customtkinter as ctk
from tkinter import filedialog

from core.ipa_reader import read_ipa
from core.icon_extractor import extract_icon
from core.app_database import add_app
from core.github_release import GitHubRelease
from core.settings import get_github_settings


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

    # ==================================================
    # INTERFACE
    # ==================================================

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
            rowspan=4,
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
            pady=(2, 20)
        )

        self.info = ctk.CTkTextbox(
            self.form,
            height=120,
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

    # ==================================================
    # FIELDS
    # ==================================================

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

    # ==================================================
    # SELECT IPA
    # ==================================================

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

            self.icon_path = extract_icon(
                file,
                self.ipa_data["bundle_id"]
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
                f"Иконка: {self.icon_path}\n\n"
                f"После заполнения данных нажмите "
                f"«Добавить приложение»."
            )

            self.select_button.configure(
                text="✓  IPA выбрано"
            )

        except Exception as error:

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"Ошибка чтения IPA:\n\n{error}"
            )

    # ==================================================
    # SAVE
    # ==================================================

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

        self.add_button.configure(
            text="⏳  Загрузка IPA...",
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
            "Создание GitHub Release...\n"
        )

        self.update()

        try:

            settings = get_github_settings()

            github = GitHubRelease(
                settings["owner"],
                settings["repo"],
                settings["token"]
            )

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

            safe_bundle = (
                bundle_id
                .replace(
                    " ",
                    "-"
                )
                .replace(
                    "/",
                    "-"
                )
            )

            safe_version = (
                version
                .replace(
                    " ",
                    "-"
                )
                .replace(
                    "/",
                    "-"
                )
            )

            tag = (
                f"gerastore-"
                f"{safe_bundle}-"
                f"{safe_version}"
            )

            release = github.create_release(
                tag=tag,
                name=f"{name} {version}",
                description=(
                    f"{name}\n\n"
                    f"Bundle ID: {bundle_id}\n"
                    f"Version: {version}"
                )
            )

            self.info.insert(
                "end",
                "✓ Release создан.\n"
            )

            self.update()

            self.info.insert(
                "end",
                "Загрузка IPA в Release...\n"
            )

            self.update()

            asset = github.upload_file(
                release,
                self.ipa_file
            )

            download_url = github.get_download_url(
                asset
            )

            self.info.insert(
                "end",
                "✓ IPA загружен.\n\n"
            )

            self.info.insert(
                "end",
                f"Download URL:\n"
                f"{download_url}\n\n"
            )

            self.update()

            description = self.description.get(
                "1.0",
                "end"
            ).strip()

            app = {

                "name":
                name,

                "bundleIdentifier":
                bundle_id,

                "developerName":
                self.developer.get().strip(),

                "subtitle":
                self.subtitle_field.get().strip(),

                "localizedDescription":
                description,

                "iconURL":
                self.icon_path,

                "versions":
                [
                    {
                        "version":
                        version,

                        "date":
                        date.today().isoformat(),

                        "downloadURL":
                        download_url,

                        "size":
                        self.ipa_data.get(
                            "size",
                            0
                        )
                    }
                ]
            }

            add_app(
                app
            )

            self.info.insert(
                "end",
                "✓ Приложение добавлено "
                "в GeraStore Manager."
            )

            self.add_button.configure(
                text="✓  Приложение добавлено"
            )

        except Exception as error:

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

    # ==================================================
    # ERROR
    # ==================================================

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
