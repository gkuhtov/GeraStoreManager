import customtkinter as ctk
from PIL import Image

from core.app_database import load_apps, save_apps
from ui.app_editor import AppEditor


class AppList(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=950,
            height=700
        )


        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.cards = []
        self.images = []


        self.refresh()



    def refresh(self):

        for card in self.cards:
            card.destroy()


        self.cards.clear()
        self.images.clear()


        data = load_apps()

        apps = data.get(
            "apps",
            []
        )


        if not apps:

            empty = ctk.CTkLabel(
                self,
                text="Приложений пока нет",
                font=("Arial",20)
            )

            empty.pack(
                pady=50
            )


            self.cards.append(empty)

            return



        for index, app in enumerate(apps):

            self.create_card(
                app,
                index
            )



    def create_card(
        self,
        app,
        index
    ):


        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )


        left = ctk.CTkFrame(
            card,
            width=130
        )

        left.pack(
            side="left",
            padx=15,
            pady=15
        )


        icon = self.load_icon(
            app.get("iconURL")
        )


        if icon:

            icon_label = ctk.CTkLabel(
                left,
                image=icon,
                text=""
            )

            icon_label.pack()


        else:

            ctk.CTkLabel(
                left,
                text="📦",
                font=("Arial",50)
            ).pack()



        right = ctk.CTkFrame(
            card
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )



        ctk.CTkLabel(
            right,
            text=app.get(
                "name",
                "Без названия"
            ),
            font=("Arial",22,"bold")
        ).pack(
            anchor="w"
        )



        version = "?"

        size = "?"

        if app.get("versions"):

            version = app["versions"][0].get(
                "version",
                "?"
            )


            size = round(
                app["versions"][0].get(
                    "size",
                    0
                ) / 1024 / 1024,
                2
            )



        info = f"""
Версия: {version}
Размер: {size} MB
Категория: {app.get('category','Other')}

Bundle ID:
{app.get('bundleIdentifier','')}
"""


        ctk.CTkLabel(
            right,
            text=info,
            justify="left"
        ).pack(
            anchor="w",
            pady=10
        )



        buttons = ctk.CTkFrame(
            right
        )

        buttons.pack(
            anchor="w"
        )



        ctk.CTkButton(
            buttons,
            text="Редактировать",
            command=lambda:
            self.edit(index)
        ).pack(
            side="left",
            padx=5
        )



        ctk.CTkButton(
            buttons,
            text="Удалить",
            fg_color="#b83232",
            command=lambda:
            self.delete(index)
        ).pack(
            side="left",
            padx=5
        )



        self.cards.append(card)



    def load_icon(
        self,
        path
    ):

        try:

            if not path:
                return None


            image = Image.open(
                path
            )


            image.thumbnail(
                (90,90)
            )


            icon = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(90,90)
            )


            self.images.append(icon)


            return icon


        except:

            return None



    def edit(
        self,
        index
    ):

        AppEditor(
            self,
            index,
            self.refresh
        )



    def delete(
        self,
        index
    ):

        data = load_apps()


        if index < len(data["apps"]):

            del data["apps"][index]


            save_apps(data)



        self.refresh()
