import customtkinter as ctk

from core.app_database import load_apps, save_apps


class AppEditor(ctk.CTkToplevel):

    def __init__(self, parent, index, refresh_callback):

        super().__init__(parent)

        self.index = index
        self.refresh_callback = refresh_callback


        self.title("Редактор приложения")
        self.geometry("600x650")


        data = load_apps()

        self.app = data["apps"][index]


        ctk.CTkLabel(
            self,
            text="Редактирование",
            font=("Arial", 24)
        ).pack(
            pady=20
        )


        self.name = self.create_field(
            "Название",
            self.app["name"]
        )


        self.developer = self.create_field(
            "Разработчик",
            self.app["developerName"]
        )


        self.subtitle = self.create_field(
            "Subtitle",
            self.app["subtitle"]
        )


        self.description = self.create_field(
            "Описание",
            self.app["localizedDescription"]
        )


        self.icon = self.create_field(
            "Icon URL",
            self.app["iconURL"]
        )


        self.download = self.create_field(
            "Download URL",
            self.app["versions"][0]["downloadURL"]
        )


        self.save_button = ctk.CTkButton(
            self,
            text="Сохранить",
            command=self.save
        )

        self.save_button.pack(
            pady=20
        )



    def create_field(self, title, value):

        ctk.CTkLabel(
            self,
            text=title
        ).pack()


        entry = ctk.CTkEntry(
            self,
            width=500
        )


        entry.insert(
            0,
            value
        )


        entry.pack(
            pady=5
        )


        return entry



    def save(self):

        data = load_apps()


        app = data["apps"][self.index]


        app["name"] = self.name.get()

        app["developerName"] = self.developer.get()

        app["subtitle"] = self.subtitle.get()

        app["localizedDescription"] = self.description.get()

        app["iconURL"] = self.icon.get()

        app["versions"][0]["downloadURL"] = self.download.get()


        save_apps(data)


        self.refresh_callback()


        self.destroy()
