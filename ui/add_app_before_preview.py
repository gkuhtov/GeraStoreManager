import customtkinter as ctk
from tkinter import filedialog

from core.ipa_reader import read_ipa
from core.icon_extractor import extract_icon
from core.app_database import add_app


class AddApp(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.ipa_data = None
        self.icon_path = None

        self.create_interface()

    # ==================================================
    # INTERFACE
    # ==================================================

    def create_interface(self):

        # Прокручиваемая область

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

        # ==================================================
        # TITLE
        # ==================================================

        title = ctk.CTkLabel(
            self.form,
            text="Добавление IPA",
            font=(
                "Arial",
                26,
                "bold"
            )
        )

        title.pack(
            pady=(10, 5)
        )

        subtitle = ctk.CTkLabel(
            self.form,
            text="Выберите IPA-файл для автоматического чтения информации",
            text_color="gray"
        )

        subtitle.pack(
            pady=(0, 15)
        )

        # ==================================================
        # SELECT IPA
        # ==================================================

        self.select_button = ctk.CTkButton(
            self.form,
            text="📦  Выбрать IPA",
            height=42,
            command=self.select_ipa
        )

        self.select_button.pack(
            pady=8
        )

        # ==================================================
        # IPA INFO
        # ==================================================

        self.info = ctk.CTkTextbox(
            self.form,
            height=180,
            corner_radius=10
        )

        self.info.pack(
            fill="x",
            padx=10,
            pady=12
        )

        # ==================================================
        # FIELDS
        # ==================================================

        self.developer = self.create_field(
            "Разработчик",
            "Например: Radarbot"
        )

        self.subtitle_field = self.create_field(
            "Subtitle",
            "Краткое описание приложения"
        )

        self.description = self.create_field(
            "Описание",
            "Полное описание приложения"
        )

        self.download = self.create_field(
            "Download URL",
            "https://..."
        )

        # ==================================================
        # SAVE
        # ==================================================

        self.add_button = ctk.CTkButton(
            self.form,
            text="✓  Добавить приложение",
            height=45,
            font=(
                "Arial",
                14,
                "bold"
            ),
            command=self.save
        )

        self.add_button.pack(
            pady=(20, 30)
        )

    # ==================================================
    # FIELD
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
            font=(
                "Arial",
                13,
                "bold"
            )
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

            self.ipa_data = read_ipa(
                file
            )

            self.icon_path = extract_icon(
                file
            )

            self.info.delete(
                "1.0",
                "end"
            )

            size_mb = round(
                self.ipa_data["size"] /
                1024 /
                1024,
                2
            )

            self.info.insert(
                "end",
                f"""Название:
{self.ipa_data["name"]}

Bundle ID:
{self.ipa_data["bundle_id"]}

Версия:
{self.ipa_data["version"]}

Размер:
{size_mb} MB

Иконка:
{self.icon_path}
"""
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

            self.info.insert(
                "end",
                "\n\nСначала выберите IPA."
            )

            return

        app = {

            "name":
            self.ipa_data["name"],

            "bundleIdentifier":
            self.ipa_data["bundle_id"],

            "developerName":
            self.developer.get(),

            "subtitle":
            self.subtitle_field.get(),

            "localizedDescription":
            self.description.get(),

            "iconURL":
            self.icon_path,

            "versions":
            [
                {

                    "version":
                    self.ipa_data["version"],

                    "date":
                    "2026-07-29",

                    "downloadURL":
                    self.download.get(),

                    "size":
                    self.ipa_data["size"]

                }
            ]

        }

        add_app(
            app
        )

        self.info.insert(
            "end",
            "\n\n✓ Приложение добавлено."
        )