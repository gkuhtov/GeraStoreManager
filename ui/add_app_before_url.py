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
        # HEADER
        # ==================================================

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

        # ==================================================
        # SELECT
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
        # APP PREVIEW
        # ==================================================

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

        # Icon

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

        # Name

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

        # Developer

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

        # Version

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

        # Bundle ID

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

        # ==================================================
        # IPA DETAILS
        # ==================================================

        self.info = ctk.CTkTextbox(
            self.form,
            height=110,
            corner_radius=10
        )

        self.info.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        # ==================================================
        # USER FIELDS
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
            font=("Arial", 14, "bold"),
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

            self.ipa_data = read_ipa(file)

            self.icon_path = extract_icon(file)

            # ------------------------------------------
            # PREVIEW
            # ------------------------------------------

            name = self.ipa_data["name"]

            if not name:
                name = "Без названия"

            self.name_label.configure(
                text=name
            )

            self.version_preview.configure(
                text=f"Версия: {self.ipa_data['version'] or 'не указана'}"
            )

            self.bundle_preview.configure(
                text=f"Bundle ID: {self.ipa_data['bundle_id'] or 'не указан'}"
            )

            # ------------------------------------------
            # DEVELOPER
            # ------------------------------------------

            self.developer_preview.configure(
                text="Разработчик будет указан ниже"
            )

            # ------------------------------------------
            # INFO
            # ------------------------------------------

            size_mb = round(
                self.ipa_data["size"] /
                1024 /
                1024,
                2
            )

            self.info.delete(
                "1.0",
                "end"
            )

            self.info.insert(
                "end",
                f"Размер IPA: {size_mb} MB\n\n"
                f"Файл иконки: {self.icon_path}"
            )

            # ------------------------------------------
            # BUTTON
            # ------------------------------------------

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

        add_app(app)

        self.info.insert(
            "end",
            "\n\n✓ Приложение добавлено."
        )