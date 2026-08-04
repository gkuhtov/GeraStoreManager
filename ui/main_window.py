import customtkinter as ctk

from ui.app_list import AppList
from ui.add_app import AddApp


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("GeraStore Manager")

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
            text="GeraStore",
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
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        self.clear_content()

        self.create_page_title(
            "Главная",
            "Управление приложениями GeraStore"
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

        self.create_stat_cards()

        self.create_quick_actions()

        self.create_recent_section()

    def create_stat_cards(self):

        cards = ctk.CTkFrame(
            self.current_page,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=8
        )

        for column in range(3):

            cards.grid_columnconfigure(
                column,
                weight=1
            )

        self.create_stat_card(
            cards,
            0,
            "📦",
            "Приложения",
            "0"
        )

        self.create_stat_card(
            cards,
            1,
            "🚀",
            "Версии",
            "0"
        )

        self.create_stat_card(
            cards,
            2,
            "☁",
            "Статус",
            "Локальный"
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
            font=(
                "Arial",
                23
            )
        )

        icon_label.pack(
            anchor="w",
            padx=16,
            pady=(12, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=(
                "Arial",
                22,
                "bold"
            )
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
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        title.pack(
            anchor="w",
            pady=(0, 8)
        )

        buttons = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x"
        )

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

        apps_button.pack(
            side="left"
        )

    # ==================================================
    # RECENT
    # ==================================================

    def create_recent_section(self):

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
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 4)
        )

        info = ctk.CTkLabel(
            section,
            text="Пока приложений нет",
            text_color="gray"
        )

        info.pack(
            pady=25
        )

    # ==================================================
    # APPLICATIONS
    # ==================================================

    def show_apps(self):

        self.clear_content()

        self.create_page_title(
            "Приложения",
            "Все приложения в GeraStore Manager"
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
            "Добавление нового приложения в GeraStore"
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
            "Состояние локального GeraStore"
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
            "Настройки GeraStore Manager"
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