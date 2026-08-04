import os
import io
import customtkinter as ctk
import requests

from PIL import Image

from core.app_database import load_apps


CACHE_DIR = "data/icon_cache"


class AppList(ctk.CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )

        self.all_apps = []
        self.icon_images = []

        os.makedirs(
            CACHE_DIR,
            exist_ok=True
        )

        self.create_interface()
        self.load_data()

    # --------------------------------------------------
    # INTERFACE
    # --------------------------------------------------

    def create_interface(self):

        self.search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍  Поиск приложения...",
            height=40,
            corner_radius=10
        )

        self.search_entry.pack(
            fill="x"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.on_search
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True
        )

    # --------------------------------------------------
    # DATA
    # --------------------------------------------------

    def load_data(self):

        data = load_apps()

        self.all_apps = data.get(
            "apps",
            []
        )

        self.render_apps(
            self.all_apps
        )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def on_search(self, event=None):

        query = self.search_entry.get().strip().lower()

        if not query:

            filtered = self.all_apps

        else:

            filtered = []

            for app in self.all_apps:

                name = str(
                    app.get(
                        "name",
                        ""
                    )
                ).lower()

                bundle = str(
                    app.get(
                        "bundleIdentifier",
                        ""
                    )
                ).lower()

                developer = str(
                    app.get(
                        "developerName",
                        ""
                    )
                ).lower()

                if (
                    query in name
                    or query in bundle
                    or query in developer
                ):

                    filtered.append(
                        app
                    )

        self.render_apps(
            filtered
        )

    # --------------------------------------------------
    # RENDER
    # --------------------------------------------------

    def render_apps(
        self,
        apps
    ):

        for widget in self.scroll_frame.winfo_children():

            widget.destroy()

        self.icon_images.clear()

        if not apps:

            empty = ctk.CTkFrame(
                self.scroll_frame,
                corner_radius=12
            )

            empty.pack(
                fill="x",
                pady=10
            )

            label = ctk.CTkLabel(
                empty,
                text="Приложения не найдены",
                font=(
                    "Arial",
                    16
                ),
                text_color="gray"
            )

            label.pack(
                pady=40
            )

            return

        for app in apps:

            self.create_app_card(
                app
            )

    # --------------------------------------------------
    # APP CARD
    # --------------------------------------------------

    def create_app_card(
        self,
        app
    ):

        card = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=6
        )

        # ICON

        icon_frame = ctk.CTkFrame(
            card,
            width=80,
            height=80,
            fg_color="transparent"
        )

        icon_frame.pack(
            side="left",
            padx=15,
            pady=15
        )

        icon_frame.pack_propagate(
            False
        )

        image = self.load_icon(
            app
        )

        if image:

            icon_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(64, 64)
            )

            self.icon_images.append(
                icon_image
            )

            icon_label = ctk.CTkLabel(
                icon_frame,
                text="",
                image=icon_image
            )

            icon_label.pack(
                expand=True
            )

        else:

            self.create_default_icon(
                icon_frame
            )

        # INFORMATION

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=15
        )

        name = app.get(
            "name",
            "Без названия"
        )

        name_label = ctk.CTkLabel(
            info,
            text=name,
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        name_label.pack(
            anchor="w"
        )

        developer = app.get(
            "developerName",
            ""
        )

        bundle = app.get(
            "bundleIdentifier",
            ""
        )

        details = developer

        if bundle:

            if details:

                details += "  •  "

            details += bundle

        details_label = ctk.CTkLabel(
            info,
            text=details,
            text_color="gray",
            font=(
                "Arial",
                12
            )
        )

        details_label.pack(
            anchor="w",
            pady=(3, 0)
        )

        versions = app.get(
            "versions",
            []
        )

        version = ""
        size = ""

        if versions:

            latest = versions[-1]

            version = latest.get(
                "version",
                ""
            )

            size_value = latest.get(
                "size",
                0
            )

            size = self.format_size(
                size_value
            )

        meta = []

        if version:

            meta.append(
                f"v{version}"
            )

        if size:

            meta.append(
                size
            )

        meta_label = ctk.CTkLabel(
            info,
            text="  •  ".join(meta),
            text_color="#3B82F6",
            font=(
                "Arial",
                12,
                "bold"
            )
        )

        meta_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        # BUTTONS

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            side="right",
            padx=15
        )

        edit_button = ctk.CTkButton(
            buttons,
            text="Редактировать",
            width=120,
            height=34,
            command=lambda a=app: self.edit_app(a)
        )

        edit_button.pack(
            pady=3
        )

        delete_button = ctk.CTkButton(
            buttons,
            text="Удалить",
            width=120,
            height=34,
            fg_color="transparent",
            border_width=1,
            command=lambda a=app: self.delete_app(a)
        )

        delete_button.pack(
            pady=3
        )

    # --------------------------------------------------
    # ICON LOADING
    # --------------------------------------------------

    def load_icon(
        self,
        app
    ):

        icon_url = app.get(
            "iconURL",
            ""
        )

        if not icon_url:

            return None

        # LOCAL FILE

        if os.path.exists(
            icon_url
        ):

            try:

                return Image.open(
                    icon_url
                ).convert(
                    "RGBA"
                )

            except Exception:

                return None

        # CACHE NAME

        cache_name = self.make_cache_name(
            icon_url
        )

        cache_path = os.path.join(
            CACHE_DIR,
            cache_name
        )

        # CACHE

        if os.path.exists(
            cache_path
        ):

            try:

                return Image.open(
                    cache_path
                ).convert(
                    "RGBA"
                )

            except Exception:

                try:

                    os.remove(
                        cache_path
                    )

                except Exception:

                    pass

        # DOWNLOAD

        if icon_url.startswith(
            "http://"
        ) or icon_url.startswith(
            "https://"
        ):

            try:

                response = requests.get(
                    icon_url,
                    timeout=10
                )

                response.raise_for_status()

                image_data = io.BytesIO(
                    response.content
                )

                image = Image.open(
                    image_data
                ).convert(
                    "RGBA"
                )

                image.save(
                    cache_path,
                    "PNG"
                )

                return image

            except Exception as error:

                print(
                    f"Не удалось загрузить иконку: {error}"
                )

                return None

        return None

    def make_cache_name(
        self,
        url
    ):

        import hashlib

        name = hashlib.md5(
            url.encode(
                "utf-8"
            )
        ).hexdigest()

        return name + ".png"

    # --------------------------------------------------
    # DEFAULT ICON
    # --------------------------------------------------

    def create_default_icon(
        self,
        parent
    ):

        label = ctk.CTkLabel(
            parent,
            text="📱",
            font=(
                "Arial",
                35
            )
        )

        label.pack(
            expand=True
        )

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def format_size(
        self,
        size
    ):

        try:

            size = int(
                size
            )

        except Exception:

            return ""

        if size <= 0:

            return ""

        mb = size / (
            1024 * 1024
        )

        if mb < 1024:

            return f"{mb:.1f} MB"

        gb = mb / 1024

        return f"{gb:.2f} GB"

    # --------------------------------------------------
    # ACTIONS
    # --------------------------------------------------

    def edit_app(
        self,
        app
    ):

        print(
            "Редактирование:",
            app.get(
                "name"
            )
        )

    def delete_app(
        self,
        app
    ):

        print(
            "Удаление:",
            app.get(
                "name"
            )
        )
