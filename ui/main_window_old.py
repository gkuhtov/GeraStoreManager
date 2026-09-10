import customtkinter as ctk
from tkinter import filedialog

from core.ipa_reader import read_ipa
from core.icon_extractor import extract_icon
from core.app_database import add_app
from core.repo_exporter import export_repo

from ui.app_list import AppList


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("GeraKStore Manager")
        self.geometry("1100x900")


        self.ipa_data = None
        self.icon_path = None



        ctk.CTkLabel(
            self,
            text="GeraKStore Manager",
            font=("Arial", 32)
        ).pack(
            pady=20
        )



        self.tabs = ctk.CTkTabview(
            self,
            width=1000,
            height=760
        )

        self.tabs.pack(
            padx=20,
            pady=10
        )


        self.add_tab = self.tabs.add(
            "Добавить приложение"
        )


        self.list_tab = self.tabs.add(
            "Приложения"
        )


        self.create_add_tab()


        self.app_list = AppList(
            self.list_tab
        )



    def create_add_tab(self):


        container = ctk.CTkScrollableFrame(
            self.add_tab,
            width=900,
            height=700
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )



        self.open_button = ctk.CTkButton(
            container,
            text="📦 Выбрать IPA файл",
            height=40,
            command=self.open_ipa
        )

        self.open_button.pack(
            pady=15
        )



        self.info = ctk.CTkTextbox(
            container,
            width=800,
            height=170
        )

        self.info.pack(
            pady=10
        )



        ctk.CTkLabel(
            container,
            text="Информация приложения",
            font=("Arial",20)
        ).pack(
            pady=10
        )



        self.developer = self.create_field(
            container,
            "Разработчик"
        )


        self.category = ctk.CTkComboBox(
            container,
            values=[
                "Games",
                "Utilities",
                "Photo",
                "Video",
                "Music",
                "Social",
                "Other"
            ],
            width=700
        )

        self.category.set(
            "Other"
        )


        ctk.CTkLabel(
            container,
            text="Категория"
        ).pack()


        self.category.pack(
            pady=8
        )



        self.subtitle = self.create_field(
            container,
            "Subtitle"
        )



        self.description = self.create_field(
            container,
            "Описание"
        )



        self.download_url = self.create_field(
            container,
            "Download URL"
        )



        buttons = ctk.CTkFrame(
            container
        )

        buttons.pack(
            pady=20
        )



        ctk.CTkButton(
            buttons,
            text="Добавить приложение",
            command=self.add_application
        ).pack(
            side="left",
            padx=10
        )


        ctk.CTkButton(
            buttons,
            text="Очистить",
            command=self.clear_form
        ).pack(
            side="left",
            padx=10
        )


        ctk.CTkButton(
            buttons,
            text="Экспорт repo.json",
            command=self.export_repository
        ).pack(
            side="left",
            padx=10
        )



    def create_field(
        self,
        parent,
        title
    ):

        ctk.CTkLabel(
            parent,
            text=title
        ).pack()


        entry = ctk.CTkEntry(
            parent,
            width=700
        )


        entry.pack(
            pady=8
        )


        return entry



    def open_ipa(self):

        file = filedialog.askopenfilename(
            filetypes=[
                ("IPA files","*.ipa")
            ]
        )


        if not file:

            return



        try:

            self.ipa_data = read_ipa(file)


            self.icon_path = extract_icon(file)



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
{self.ipa_data['size'] / 1024 / 1024:.2f} MB

Иконка:
{self.icon_path}
"""
            )



        except Exception as e:

            self.info.insert(
                "end",
                f"Ошибка:\n{e}"
            )



    def add_application(self):

        if not self.ipa_data:

            return



        app = {

            "name":
            self.ipa_data["name"],


            "bundleIdentifier":
            self.ipa_data["bundle_id"],


            "developerName":
            self.developer.get(),


            "category":
            self.category.get(),


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
                    self.download_url.get(),


                    "size":
                    self.ipa_data["size"]

                }
            ]

        }


        add_app(app)


        self.app_list.refresh()



        self.info.insert(
            "end",
            "\n\nПриложение добавлено"
        )



    def clear_form(self):

        self.developer.delete(
            0,
            "end"
        )


        self.subtitle.delete(
            0,
            "end"
        )


        self.description.delete(
            0,
            "end"
        )


        self.download_url.delete(
            0,
            "end"
        )


        self.info.delete(
            "1.0",
            "end"
        )


        self.ipa_data = None

        self.icon_path = None



    def export_repository(self):

        result = export_repo()


        self.info.insert(
            "end",
            f"\nСоздан файл:\n{result}"
        )
