import customtkinter as ctk
from tkinter import filedialog

from core.ipa_reader import read_ipa
from core.icon_extractor import extract_icon
from core.app_database import add_app


class AddApp(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent
        )

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.ipa_data = None
        self.icon_path = None


        self.create_interface()



    def create_interface(self):


        title = ctk.CTkLabel(
            self,
            text="Добавление IPA",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=20
        )


        self.select_button = ctk.CTkButton(
            self,
            text="📦 Выбрать IPA",
            command=self.select_ipa
        )

        self.select_button.pack(
            pady=10
        )


        self.info = ctk.CTkTextbox(
            self,
            height=200
        )

        self.info.pack(
            fill="x",
            pady=15
        )


        self.developer = self.create_field(
            "Разработчик"
        )


        self.subtitle = self.create_field(
            "Subtitle"
        )


        self.description = self.create_field(
            "Описание"
        )


        self.download = self.create_field(
            "Download URL"
        )



        self.add_button = ctk.CTkButton(
            self,
            text="Добавить приложение",
            command=self.save
        )

        self.add_button.pack(
            pady=20
        )



    def create_field(self, text):

        ctk.CTkLabel(
            self,
            text=text
        ).pack()


        field = ctk.CTkEntry(
            self,
            width=700
        )


        field.pack(
            pady=5
        )


        return field



    def select_ipa(self):

        file = filedialog.askopenfilename(
            filetypes=[
                ("IPA files", "*.ipa")
            ]
        )


        if not file:

            return


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


        self.info.insert(
            "end",
            f"""
Название:
{self.ipa_data['name']}

Bundle ID:
{self.ipa_data['bundle_id']}

Версия:
{self.ipa_data['version']}

Размер:
{round(self.ipa_data['size']/1024/1024,2)} MB

Иконка:
{self.icon_path}
"""
        )



    def save(self):

        if not self.ipa_data:

            return



        app = {

            "name":
            self.ipa_data["name"],


            "bundleIdentifier":
            self.ipa_data["bundle_id"],


            "developerName":
            self.developer.get(),


            "subtitle":
            self.subtitle.get(),


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
            "\n\nПриложение добавлено"
        )
