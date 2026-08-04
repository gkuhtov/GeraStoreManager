import customtkinter as ctk

from core.app_database import load_apps, save_apps
from ui.app_editor import AppEditor


class AppList(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=850,
            height=650
        )


        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.cards = []

        self.refresh()



    def refresh(self):

        for card in self.cards:
            card.destroy()


        self.cards.clear()


        data = load_apps()

        apps = data.get(
            "apps",
            []
        )


        if not apps:

            label = ctk.CTkLabel(
                self,
                text="Приложений пока нет"
            )

            label.pack(
                pady=30
            )

            self.cards.append(label)

            return



        for index, app in enumerate(apps):

            self.create_card(
                app,
                index
            )



    def create_card(self, app, index):

        frame = ctk.CTkFrame(
            self
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=10
        )


        title = ctk.CTkLabel(
            frame,
            text=app.get("name", "Без названия"),
            font=("Arial", 18)
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=5
        )



        version = "Нет версии"

        if app.get("versions"):

            version = app["versions"][0].get(
                "version",
                "Нет версии"
            )



        info = ctk.CTkLabel(
            frame,
            text=
            f"""
Версия: {version}

Bundle ID:
{app.get('bundleIdentifier','')}

Разработчик:
{app.get('developerName','')}
"""
        )


        info.pack(
            anchor="w",
            padx=15,
            pady=5
        )



        buttons = ctk.CTkFrame(
            frame
        )

        buttons.pack(
            pady=10
        )



        edit_button = ctk.CTkButton(
            buttons,
            text="Редактировать",
            command=lambda:
            self.open_editor(index)
        )

        edit_button.pack(
            side="left",
            padx=5
        )



        delete_button = ctk.CTkButton(
            buttons,
            text="Удалить",
            fg_color="#aa3333",
            command=lambda:
            self.delete_app(index)
        )

        delete_button.pack(
            side="left",
            padx=5
        )


        self.cards.append(frame)



    def open_editor(self, index):

        AppEditor(
            self,
            index,
            self.refresh
        )



    def delete_app(self, index):

        data = load_apps()


        if index < len(data.get("apps", [])):

            del data["apps"][index]


            save_apps(data)


        self.refresh()
