import os
from datetime import datetime
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
            height=90,
            corner_radius=10
        )

        self.info.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        self.developer = self.create_field(
            "Разработчик",
            "Например: Radarbot"
        )

        self.subtitle_field = self.create_field(
            "Subtitle",
            "Краткое описание приложения"
        )

        self.description = self.create_text_field(
            "Описание",
            "Полное описание приложения"
        )

        self.download_label = ctk.CTkLabel(
            self.form,
            text="Download URL",
            font=("Arial", 13, "bold")
        )

        self.download_label.pack(
            anchor="w",
            padx=10,
            pady=(7, 4)
        )

        self.download = ctk.CTkEntry(
            self.form,
            height=38,
            state="disabled"
        )

        self.download.pack(
            fill="x",
            padx=10,
            pady=(0, 7)
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

            name = self.ipa_data["name"]

            if not name:
                name = "Без названия"

            self.name_label.configure(
                text=name
            )

            version = self.ipa_data["version"]

            if not version:
                version = "не указана"

            self.version_preview.configure(
                text=f"Версия: {version}"
            )

            bundle_id = self.ipa_data["bundle_id"]

            if not bundle_id:
                bundle_id = "не указан"

            self.bundle_preview.configure(
                text=f"Bundle ID: {bundle_id}"
            )

            size_mb = round(
                self.ipa_data["size"] / 1024 / 1024,
                2
            )

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"Размер IPA: {size_mb} MB\n\n"
                f"Файл иконки: {self.icon_path}\n\n"
                "Download URL будет создан автоматически "
                "после загрузки IPA в GitHub Release."
            )

            self.download.configure(
                state="normal"
            )

            self.download.delete(
                0,
                "end"
            )

            self.download.configure(
                state="disabled"
            )

            self.select_button.configure(
                text="✓  IPA выбрано"
            )

        except Exception as error:

            self.ipa_data = None
            self.ipa_file = None

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"Ошибка чтения IPA:\n\n{error}"
            )

    def set_download_url(
        self,
        url
    ):

        self.download.configure(
            state="normal"
        )

        self.download.delete(
            0,
            "end"
        )

        self.download.insert(
            0,
            url
        )

        self.download.configure(
            state="disabled"
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
            f"gerastore-"
            f"{safe_bundle}-"
            f"{safe_version}"
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
            f"{safe_name}_"
            f"{safe_version}.ipa"
        )

    def upload_to_github(self):

        settings = get_github_settings()

        if not settings.get("token"):
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
            release_name += (
                f" {version}"
            )

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

            self.info.insert(
                "end",
                "\n\nСначала выберите IPA."
            )

            return

        if not self.ipa_file:

            self.info.insert(
                "end",
                "\n\nIPA-файл не выбран."
            )

            return

        description = self.description.get(
            "1.0",
            "end"
        ).strip()

