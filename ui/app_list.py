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

    def refresh(self):

        self.load_data()

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def on_search(self, event=None):

        query = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

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

    def render_apps(self, apps):

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

    def create_app_card(self, app):

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

        name_label = ctk.CTkLabel(
            info,
            text=app.get(
                "name",
                "Без названия"
            ),
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

            size = self.format_size(
                latest.get(
                    "size",
                    0
                )
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
    # ICON
    # --------------------------------------------------

    def load_icon(self, app):

        icon_url = app.get(
            "iconURL",
            ""
        )

        if not icon_url:

            return None

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

        cache_name = self.make_cache_name(
            icon_url
        )

        cache_path = os.path.join(
            CACHE_DIR,
            cache_name
        )

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

        if (
            icon_url.startswith("http://")
            or icon_url.startswith("https://")
        ):

            try:

                response = requests.get(
                    icon_url,
                    timeout=10
                )

                response.raise_for_status()

                image = Image.open(
                    io.BytesIO(
                        response.content
                    )
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

    def make_cache_name(self, url):

        import hashlib

        name = hashlib.md5(
            url.encode(
                "utf-8"
            )
        ).hexdigest()

        return name + ".png"

    def create_default_icon(self, parent):

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
    # ACTIONS
    # --------------------------------------------------

    def edit_app(self, app):

        from ui.app_editor import AppEditor

        AppEditor(
            self,
            app,
            on_saved=self.on_app_saved
        )

    # --------------------------------------------------
    # APP SAVED
    # --------------------------------------------------

    def on_app_saved(self):

        print()
        print("=" * 60)
        print("GeraKStore Manager: приложение сохранено")
        print("=" * 60)

        self.refresh()

        try:

            from core.gerastore_sync import GeraKStoreSync

            print("Запускаем синхронизацию с GitHub...")

            sync = GeraKStoreSync()

            result = sync.sync(
                commit_message="Update application from GeraKStore Manager"
            )

            print(
                "Результат синхронизации:",
                result
            )

            if result.get("changed"):

                self.show_info(
                    "Изменения опубликованы.\n\n"
                    "repo.json и иконки обновлены на GitHub."
                )

            else:

                self.show_info(
                    "Изменений для публикации нет."
                )

        except Exception as error:

            print()
            print("ОШИБКА СИНХРОНИЗАЦИИ:")
            print(error)

            self.show_error(
                "Приложение сохранено локально,\n"
                "но опубликовать изменения не удалось.\n\n"
                f"Ошибка:\n{error}"
            )

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    def delete_app(self, app):

        name = app.get(
            "name",
            "это приложение"
        )

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Удаление приложения"
        )

        dialog.geometry(
            "420x200"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog,
            text=f"Удалить «{name}»?",
            font=(
                "Arial",
                16,
                "bold"
            )
        )

        label.pack(
            pady=(35, 20)
        )

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack()

        cancel = ctk.CTkButton(
            buttons,
            text="Отмена",
            width=110,
            command=dialog.destroy
        )

        cancel.pack(
            side="left",
            padx=5
        )

        confirm = ctk.CTkButton(
            buttons,
            text="Удалить",
            width=110,
            fg_color="#C62828",
            hover_color="#A91F1F",
            command=lambda: self.confirm_delete(
                app,
                dialog
            )
        )

        confirm.pack(
            side="left",
            padx=5
        )

    def confirm_delete(
        self,
        app,
        dialog
    ):

        data = load_apps()

        bundle_id = app.get(
            "bundleIdentifier"
        )

        name = app.get(
            "name",
            "приложение"
        )

        data["apps"] = [
            item
            for item in data.get(
                "apps",
                []
            )
            if item.get(
                "bundleIdentifier"
            ) != bundle_id
        ]

        from core.app_database import save_apps

        save_apps(
            data
        )

        dialog.destroy()

        self.load_data()

        try:

            from core.gerastore_sync import GeraKStoreSync

            print()
            print("=" * 60)
            print("GeraKStore Manager: приложение удалено")
            print("=" * 60)
            print("Запускаем синхронизацию с GitHub...")

            sync = GeraKStoreSync()

            result = sync.sync(
                commit_message=f"Remove {name} from GeraKStore Manager"
            )

            print(
                "Результат синхронизации:",
                result
            )

            if result.get("changed"):

                self.show_info(
                    "Приложение удалено.\n\n"
                    "GeraKStore опубликован."
                )

            else:

                self.show_info(
                    "Приложение удалено.\n\n"
                    "Изменений для публикации нет."
                )

        except Exception as error:

            print()
            print("ОШИБКА СИНХРОНИЗАЦИИ:")
            print(error)

            self.show_error(
                "Приложение удалено локально,\n"
                "но опубликовать удаление не удалось.\n\n"
                f"Ошибка:\n{error}"
            )

    # --------------------------------------------------
    # DIALOGS
    # --------------------------------------------------

    def show_info(self, message):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "GeraKStore Manager"
        )

        dialog.geometry(
            "430x190"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=360
        )

        label.pack(
            expand=True,
            padx=20
        )

        button = ctk.CTkButton(
            dialog,
            text="ОК",
            width=100,
            command=dialog.destroy
        )

        button.pack(
            pady=(0, 20)
        )

        dialog.update_idletasks()

        x = (
            self.winfo_rootx()
            + (
                self.winfo_width()
                - dialog.winfo_width()
            ) // 2
        )

        y = (
            self.winfo_rooty()
            + (
                self.winfo_height()
                - dialog.winfo_height()
            ) // 2
        )

        dialog.geometry(
            f"+{x}+{y}"
        )

    def show_error(self, message):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Ошибка"
        )

        dialog.geometry(
            "450x260"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=390,
            justify="left"
        )

        label.pack(
            expand=True,
            padx=20
        )

        button = ctk.CTkButton(
            dialog,
            text="ОК",
            width=100,
            command=dialog.destroy
        )

        button.pack(
            pady=(0, 20)
        )

        dialog.update_idletasks()

        x = (
            self.winfo_rootx()
            + (
                self.winfo_width()
                - dialog.winfo_width()
            ) // 2
        )

        y = (
            self.winfo_rooty()
            + (
                self.winfo_height()
                - dialog.winfo_height()
            ) // 2
        )

        dialog.geometry(
            f"+{x}+{y}"
        )

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def format_size(self, size):

        try:

            size = int(size)

        except Exception:

            return ""

        if size <= 0:

            return ""

        mb = size / (
            1024 * 1024
        )

        if mb < 1024:

            return f"{mb:.1f} MB"

        return f"{mb / 1024:.2f} GB"
