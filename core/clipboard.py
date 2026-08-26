import tkinter as tk


def _get_widget(event):
    w = event.widget
    # CTkEntry / CTkTextbox — обёртки, настоящее поле внутри
    if hasattr(w, "_entry"):
        return w._entry
    if hasattr(w, "_textbox"):
        return w._textbox
    return w


def copy_text(event=None):
    try:
        w = _get_widget(event)
        try:
            text = w.selection_get()
        except tk.TclError:
            return "break"
        w.clipboard_clear()
        w.clipboard_append(text)
    except Exception:
        pass
    return "break"


def cut_text(event=None):
    try:
        w = _get_widget(event)
        try:
            text = w.selection_get()
        except tk.TclError:
            return "break"
        w.clipboard_clear()
        w.clipboard_append(text)
        try:
            w.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
    except Exception:
        pass
    return "break"


def paste_text(event=None):
    try:
        w = _get_widget(event)
        try:
            text = w.clipboard_get()
        except tk.TclError:
            return "break"

        # заменить выделение, если есть
        try:
            w.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

        try:
            w.insert("insert", text)
        except tk.TclError:
            try:
                w.insert(tk.INSERT, text)
            except Exception:
                pass
    except Exception:
        pass
    return "break"


def select_all(event=None):
    try:
        w = _get_widget(event)
        # Text / Textbox
        try:
            w.tag_add("sel", "1.0", "end")
            w.mark_set("insert", "1.0")
            return "break"
        except tk.TclError:
            pass
        # Entry
        try:
            w.select_range(0, "end")
            w.icursor("end")
        except Exception:
            pass
    except Exception:
        pass
    return "break"


def _on_control_key(event):
    """
    Работает и на EN, и на RU раскладке.
    Смотрим physical keycode (Windows):
      C=67, V=86, X=88, A=65
    """
    code = getattr(event, "keycode", None)
    if code == 67:      # C
        return copy_text(event)
    if code == 86:      # V
        return paste_text(event)
    if code == 88:      # X
        return cut_text(event)
    if code == 65:      # A
        return select_all(event)
    return None


def enable_clipboard(root):
    """Включить Ctrl+C/X/V/A для всего приложения."""

    # Обычные латинские бинды
    root.bind_all("<Control-c>", copy_text)
    root.bind_all("<Control-C>", copy_text)
    root.bind_all("<Control-x>", cut_text)
    root.bind_all("<Control-X>", cut_text)
    root.bind_all("<Control-v>", paste_text)
    root.bind_all("<Control-V>", paste_text)
    root.bind_all("<Control-a>", select_all)
    root.bind_all("<Control-A>", select_all)

    # Для русской (и любой другой) раскладки — по keycode
    root.bind_all("<Control-KeyPress>", _on_control_key)