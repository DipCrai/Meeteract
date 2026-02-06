import tkinter as tk

def log(ui_text_widget, message: str):
    def _append():
        ui_text_widget.configure(state="normal")
        ui_text_widget.insert(tk.END, message + "\n")
        ui_text_widget.see(tk.END)
        ui_text_widget.configure(state="disabled")

    try:
        ui_text_widget.after(0, _append)
    except Exception:
        pass