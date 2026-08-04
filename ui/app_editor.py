import customtkinter as ctk

from core.app_database import load_apps, save_apps
from core.gerastore_sync import GeraStoreSync


class AppEditor(ctk.CTkToplevel):

    def __init__(self, parent, app, on_saved=None):

        super().__init__(parent)

        self.parent = parent
        self.app = app
        self.on_saved = on_saved

        self.title("Редактирование приложения")

        self.geometry("620x620")

        self.minsize(
            560,
            560
        )

        self.resizable(
            True,
            True
        )

        self.transient(parent)

        self.grab_set()

        self.center_window()

        self.create_interface()

        self.load_values()

    # --------------------------------------------------
    # WINDOW
    # --------------------------------------------------

    def center_window(self):

        self.update_idletasks()

        width = 620
        height = 620

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int(
            (screen_width - width) / 2
        )

        y = int(
            (screen_height - height) / 2
        )

        if y < 20:
            y = 20

        if y + height > screen_height - 20:

            y = screen_height - height - 20

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # --------------------------------------------------
    # INTERFACE
    # --------------------------------------------------

    def create_interface(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # HEADER

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        self.icon_label = ctk.CTkLabel(
            header,
            text="📱",
            font=(
                "Arial",
                42
            )
        )

        self.icon_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(0, 15)
        )

        self.title_label = ctk.CTkLabel(
            header,
            text="Редактирование",
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        self.title_label.grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.bundle_label = ctk.CTkLabel(
            header,
            text="",
            text_color="gray",
            font=(
                "Arial",
                12
            )
        )

        self.bundle_label.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(3, 0)
        )

        # CONTENT

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=5
        )

        # FOOTER

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 20)
        )

        self.footer.grid_columnconfigure(
            0,
            weight=1
        )

        self.cancel_button = ctk.CTkButton(
            self.footer,
            text="Отмена",
            width=110,
            height=38,
            fg_color="transparent",
            border_width=1,
            command=self.close_editor
        )

        self.cancel_button.grid(
            row=0,
            column=1,
            padx=5
        )

        self.save_button = ctk.CTkButton(
            self.footer,
            text="Сохранить",
            width=130,
            height=38,
            command=self.save
        )

        self.save_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # FIELDS

        self.name_entry = self.create_entry(
            "Название"
        )

        self.developer_entry = self.create_entry(
            "Разработчик"
        )

        self.subtitle_entry = self.create_entry(
            "Подзаголовок"
        )

        self.category_entry = self.create_entry(
            "Категория"
        )

        # DESCRIPTION

        description_label = ctk.CTkLabel(
            self.content,
            text="Описание",
            font=(
                "Arial",
                13,
                "bold"
            )
        )

        description_label.pack(
            anchor="w",
            pady=(10, 5)
        )

        self.description_text = ctk.CTkTextbox(
            self.content,
            height=110,
            corner_radius=8
        )

        self.description_text.pack(
            fill="x"
        )

        # INFO

        info = ctk.CTkFrame(
            self.content,
            corner_radius=10
        )

        info.pack(
            fill="x",
            pady=(15, 5)
        )

        self.version_label = ctk.CTkLabel(
            info,
            text="Версия: неизвестно",
            text_color="gray"
        )

        self.version_label.pack(
            anchor="w",
            padx=15,
            pady=(10, 3)
        )

        self.size_label = ctk.CTkLabel(
            info,
            text="Размер: неизвестно",
            text_color="gray"
        )

        self.size_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

    # --------------------------------------------------
    # FIELD CREATOR
    # --------------------------------------------------

    def create_entry(
        self,
        label_text
    ):

        label = ctk.CTkLabel(
            self.content,
            text=label_text,
            font=(
                "Arial",
                13,
                "bold"
            )
        )

        label.pack(
            anchor="w",
            pady=(10, 5)
        )

        entry = ctk.CTkEntry(
            self.content,
            height=38,
            corner_radius=8
        )

        entry.pack(
            fill="x"
        )

        return entry

    # --------------------------------------------------
    # LOAD
    # --------------------------------------------------

    def load_values(self):

        self.name_entry.insert(
            0,
            self.app.get(
                "name",
                ""
            )
        )

        self.developer_entry.insert(
            0,
            self.app.get(
                "developerName",
                ""
            )
        )

        self.subtitle_entry.insert(
            0,
            self.app.get(
                "subtitle",
                ""
            )
        )

        self.category_entry.insert(
            0,
            self.app.get(
                "category",
                ""
            )
        )

        description = self.app.get(
            "localizedDescription",
            ""
        )

        self.description_text.insert(
            "1.0",
            description
        )

        bundle = self.app.get(
            "bundleIdentifier",
            ""
        )

        self.bundle_label.configure(
            text=bundle
        )

        versions = self.app.get(
            "versions",
            []
        )

        if versions:

            latest = versions[-1]

            version = latest.get(
                "version",
                "неизвестно"
            )

            size = latest.get(
                "size",
                0
            )

            self.version_label.configure(
                text=f"Версия: {version}"
            )

            self.size_label.configure(
                text=f"Размер: {self.format_size(size)}"
            )

        else:

            self.version_label.configure(
                text="Версия: неизвестно"
            )

            self.size_label.configure(
                text="Размер: неизвестно"
            )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    def save(self):

        name = self.name_entry.get().strip()

        developer = (
            self.developer_entry
            .get()
            .strip()
        )

        subtitle = (
            self.subtitle_entry
            .get()
            .strip()
        )

        category = (
            self.category_entry
            .get()
            .strip()
        )

        description = (
            self.description_text
            .get(
                "1.0",
                "end"
            )
            .strip()
        )


        if not name:

            self.show_error(
                "Название приложения не может быть пустым."
            )

            return


        self.app["name"] = name

        self.app["developerName"] = developer

        self.app["subtitle"] = subtitle

        self.app["category"] = category

        self.app[
            "localizedDescription"
        ] = description


        data = load_apps()

        apps = data.get(
            "apps",
            []
        )


        bundle_id = self.app.get(
            "bundleIdentifier"
        )


        found = False


        for index, existing in enumerate(apps):

            if existing.get(
                "bundleIdentifier"
            ) == bundle_id:

                apps[index] = self.app

                found = True

                break


        if not found:

            apps.append(
                self.app
            )


        data["apps"] = apps


        save_apps(
            data
        )


        # Автоматическое обновление GeraStore

        try:

            sync = GeraStoreSync()

            result = sync.sync(
                commit_message=f"Update {name} from Manager"
            )


        except Exception as e:

            self.show_error(
                "Данные сохранены, но публикация не удалась:\n\n"
                + str(e)
            )

            result = None



        callback = self.on_saved

        self.on_saved = None


        try:

            if self.grab_current() == str(self):

                self.grab_release()


        except Exception:

            pass


        self.destroy()


        if callback:

            try:

                self.parent.after(
                    50,
                    callback
                )

            except Exception:

                pass


    # --------------------------------------------------
    # CLOSE
    # --------------------------------------------------

    def close_editor(self):

        try:

            if self.grab_current() == str(self):

                self.grab_release()

        except Exception:

            pass

        self.destroy()

    # --------------------------------------------------
    # ERROR
    # --------------------------------------------------

    def show_error(
        self,
        message
    ):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Ошибка"
        )

        dialog.geometry(
            "420x180"
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
            wraplength=350
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

    def format_size(
        self,
        size
    ):

        try:

            size = int(
                size
            )

        except Exception:

            return "неизвестно"

        if size <= 0:

            return "неизвестно"

        mb = size / (
            1024 * 1024
        )

        if mb < 1024:

            return f"{mb:.1f} MB"

        gb = mb / 1024

        return f"{gb:.2f} GB"
