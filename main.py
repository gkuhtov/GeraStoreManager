from ui.main_window import MainWindow
from core.clipboard import enable_clipboard
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    enable_clipboard(app)
    app.mainloop()
