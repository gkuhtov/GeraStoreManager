import customtkinter as ctk
from datetime import datetime

from ui.app_list import AppList
from ui.add_app import AddApp
from core.app_database import load_apps


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("GeraKStore Manager")

        # Компактное окно.
        self.geometry("1000x650")
        self.minsize(900, 560)

        self.center_window()

        self.current_page = None
        self.page_header = None

        self.create_interface()

        self.show_dashboard()

    # ==================================================
    # WINDOW
    # ==================================================

    def center_window(self):

        self.update_idletasks()

        width = 1000
        height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int(
            (screen_width - width) / 2
        )

        y = int(
            (screen_height - height) / 2
        )

        # Защита от выхода за нижнюю границу экрана.

        if y < 20:
            y = 20

        if y + height > screen_height - 20:

            y = screen_height - height - 20

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ==================================================
    # INTERFACE
    # ==================================================

    def create_interface(self):

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_sidebar()

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

    # ==================================================
    # SIDEBAR
    # ==================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=190,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(
            False
        )

        # LOGO

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="GeraKStore",
            font=(
                "Arial",
                25,
                "bold"
            )
        )

        self.logo.pack(
            pady=(25, 5)
        )

        self.version = ctk.CTkLabel(
            self.sidebar,
            text="Manager",
            font=(
                "Arial",
                13
            ),
            text_color="gray"
        )

        self.version.pack(
            pady=(0, 20)
        )

        # NAVIGATION

        self.dashboard_button = self.create_nav_button(
            "⌂  Главная",
            self.show_dashboard
        )

        self.apps_button = self.create_nav_button(
            "▣  Приложения",
            self.show_apps
        )

        self.add_button = self.create_nav_button(
            "＋  Добавить IPA",
            self.show_add
        )

        self.publish_button = self.create_nav_button(
            "↑  Публикация",
            self.show_publish
        )

        self.export_button = self.create_nav_button(
            "▤  Репозиторий",
            self.show_repository
        )

        # BOTTOM

        self.sidebar_bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        self.sidebar_bottom.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=12
        )

        self.settings_button = ctk.CTkButton(
            self.sidebar_bottom,
            text="⚙  Настройки",
            height=38,
            fg_color="transparent",
            hover_color=(
                "gray75",
                "gray25"
            ),
            anchor="w",
            command=self.show_settings
        )

        self.settings_button.pack(
            fill="x"
        )

    def create_nav_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color=(
                "gray75",
                "gray25"
            ),
            anchor="w",
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

        return button

    # ==================================================
    # PAGE MANAGEMENT
    # ==================================================

    def clear_content(self):

        if self.current_page:

            self.current_page.destroy()

            self.current_page = None

        if self.page_header:

            self.page_header.destroy()

            self.page_header = None

    def create_page_title(
        self,
        title,
        subtitle=""
    ):

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(20, 8)
        )

        self.page_header = header

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=(
                "Arial",
                26,
                "bold"
            )
        )

        title_label.pack(
            anchor="w"
        )

        if subtitle:

            subtitle_label = ctk.CTkLabel(
                header,
                text=subtitle,
                font=(
                    "Arial",
                    13
                ),
                text_color="gray"
            )

            subtitle_label.pack(
                anchor="w",
                pady=(3, 0)
            )

    # ==================================================
    # DASHBOARD DATA
    # ==================================================

    def get_dashboard_stats(self):
        """Читает data/apps.json и считает статистику."""

        try:
            data = load_apps()
            apps = data.get("apps") or []
        except Exception:
            apps = []

        app_count = len(apps)
        version_count = 0
        last_update = None

        for app in apps:
            versions = app.get("versions") or []
            version_count += max(len(versions), 1)

            for key in ("appUpdateTime", "addedDate"):
                raw = app.get(key)
                if not raw:
                    continue
                try:
                    value = str(raw).replace("Z", "+00:00")
                    dt = datetime.fromisoformat(value)
                    if last_update is None or dt > last_update:
                        last_update = dt
                except Exception:
                    pass

        if last_update is None:
            status = "Пусто"
        else:
            status = last_update.strftime("%d.%m.%Y")

        # Сортируем приложения по дате обновления (новые сверху)
        def sort_key(app):
            raw = app.get("appUpdateTime") or app.get("addedDate") or ""
            try:
                return datetime.fromisoformat(
                    str(raw).replace("Z", "+00:00")
                )
            except Exception:
                return datetime.min

        recent = sorted(apps, key=sort_key, reverse=True)[:6]

        return {
            "app_count": app_count,
            "version_count": version_count,
            "status": status,
            "recent": recent,
        }

    def format_size(self, size):
        try:
            size = int(size)
        except Exception:
            return "—"

        if size <= 0:
            return "—"

        mb = size / (1024 * 1024)
        if mb >= 100:
            return f"{mb:.0f} MB"
        return f"{mb:.1f} MB"

    def get_app_version(self, app):
        versions = app.get("versions") or []
        if versions:
            return versions[-1].get("version") or app.get("version") or "—"
        return app.get("version") or "—"

    def get_app_size(self, app):
        versions = app.get("versions") or []
        if versions:
            return versions[-1].get("size") or app.get("size") or 0
        return app.get("size") or 0

    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        self.clear_content()

        self.create_page_title(
            "Главная",
            "Управление приложениями GeraKStore"
        )

        self.current_page = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=8
        )

        stats = self.get_dashboard_stats()

        self.create_stat_cards(stats)
        self.create_quick_actions()
        self.create_recent_section(stats)

    def create_stat_cards(self, stats):

        cards = ctk.CTkFrame(
            self.current_page,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=8
        )

        for column in range(3):
            cards.grid_columnconfigure(column, weight=1)

        self.create_stat_card(
            cards,
            0,
            "📦",
            "Приложения",
            str(stats["app_count"])
        )

        self.create_stat_card(
            cards,
            1,
            "🚀",
            "Версии",
            str(stats["version_count"])
        )

        self.create_stat_card(
            cards,
            2,
            "🕒",
            "Обновлено",
            stats["status"]
        )

    def create_stat_card(
        self,
        parent,
        column,
        icon,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 23)
        )

        icon_label.pack(
            anchor="w",
            padx=16,
            pady=(12, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 22, "bold")
        )

        value_label.pack(
            anchor="w",
            padx=16
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color="gray"
        )

        title_label.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    def create_quick_actions(self):

        section = ctk.CTkFrame(
            self.current_page,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            pady=12
        )

        title = ctk.CTkLabel(
            section,
            text="Быстрые действия",
            font=("Arial", 18, "bold")
        )

        title.pack(
            anchor="w",
            pady=(0, 8)
        )

        buttons = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )

        buttons.pack(fill="x")

        add_button = ctk.CTkButton(
            buttons,
            text="＋  Добавить IPA",
            height=42,
            command=self.show_add
        )

        add_button.pack(
            side="left",
            padx=(0, 10)
        )

        apps_button = ctk.CTkButton(
            buttons,
            text="▣  Открыть приложения",
            height=42,
            command=self.show_apps
        )

        apps_button.pack(side="left")

    # ==================================================
    # RECENT
    # ==================================================

    def create_recent_section(self, stats):

        section = ctk.CTkFrame(
            self.current_page,
            corner_radius=12
        )

        section.pack(
            fill="both",
            expand=True,
            pady=8
        )

        title = ctk.CTkLabel(
            section,
            text="Последние приложения",
            font=("Arial", 18, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        recent = stats.get("recent") or []

        if not recent:
            info = ctk.CTkLabel(
                section,
                text="Пока приложений нет",
                text_color="gray"
            )
            info.pack(pady=25)
            return

        list_frame = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )
        list_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        for app in recent:
            self.create_recent_row(list_frame, app)

    def create_recent_row(self, parent, app):

        row = ctk.CTkFrame(
            parent,
            corner_radius=10,
            fg_color=("gray90", "gray17")
        )
        row.pack(
            fill="x",
            pady=4,
            padx=4
        )

        name = app.get("name") or "Без названия"
        version = self.get_app_version(app)
        category = app.get("category") or "—"
        size_text = self.format_size(self.get_app_size(app))

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(
            side="left",
            fill="x",
            expand=True,
            padx=14,
            pady=10
        )

        name_label = ctk.CTkLabel(
            left,
            text=name,
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        name_label.pack(anchor="w")

        meta_label = ctk.CTkLabel(
            left,
            text=f"v{version}  ·  {category}  ·  {size_text}",
            font=("Arial", 12),
            text_color="gray",
            anchor="w"
        )
        meta_label.pack(anchor="w", pady=(2, 0))

        open_btn = ctk.CTkButton(
            row,
            text="Открыть",
            width=90,
            height=32,
            command=self.show_apps
        )
        open_btn.pack(
            side="right",
            padx=12,
            pady=10
        )

    # ==================================================
    # APPLICATIONS
    # ==================================================

    def show_apps(self):

        self.clear_content()

        self.create_page_title(
            "Приложения",
            "Все приложения в GeraKStore Manager"
        )

        self.current_page = AppList(
            self.content
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

    # ==================================================
    # ADD IPA
    # ==================================================

    def show_add(self):

        self.clear_content()

        self.create_page_title(
            "Добавить IPA",
            "Добавление нового приложения в GeraKStore"
        )

        self.current_page = AddApp(
            self.content
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 10)
        )

    # ==================================================
    # PUBLISH
    # ==================================================

    def show_publish(self):

        self.clear_content()

        self.create_page_title(
            "Публикация",
            "Подготовка изменений к публикации"
        )

        self.current_page = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30
        )

        label = ctk.CTkLabel(
            self.current_page,
            text="Публикация будет подключена следующим этапом.",
            text_color="gray"
        )

        label.pack(
            pady=50
        )

    # ==================================================
    # REPOSITORY
    # ==================================================

    def show_repository(self):

        self.clear_content()

        self.create_page_title(
            "Репозиторий",
            "Состояние локального GeraKStore"
        )

        self.current_page = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30
        )

        label = ctk.CTkLabel(
            self.current_page,
            text="Подключение репозитория будет добавлено следующим этапом.",
            text_color="gray"
        )

        label.pack(
            pady=50
        )

    # ==================================================
    # SETTINGS
    # ==================================================

    def show_settings(self):

        self.clear_content()

        self.create_page_title(
            "Настройки",
            "Настройки GeraKStore Manager"
        )

        self.current_page = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.current_page.pack(
            fill="both",
            expand=True,
            padx=30
        )

        label = ctk.CTkLabel(
            self.current_page,
            text="Настройки будут добавлены следующим этапом.",
            text_color="gray"
        )

        label.pack(
            pady=50
        )