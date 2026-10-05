"""Euro → Albanian lek conversion board. Run with ``python3 app.py``."""

from __future__ import annotations

import tkinter as tk
from decimal import Decimal
from tkinter import messagebox

from conversion import format_amount, load_rate, parse_rate, save_rate

PRESETS = (5, 10, 20, 50, 100, 200)
BG = "#101827"
PANEL = "#1c293b"
CARD = "#233348"
TEXT = "#f3f7fb"
MUTED = "#9fb2c6"
ACCENT = "#50dfbb"
FONT = "DejaVu Sans"




class Board(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.rate = load_rate()
        self.title("Euro → Lek | Conversion Board")
        self.configure(bg=BG)
        self.geometry("900x650")
        self.minsize(600, 530)

        outer = tk.Frame(self, bg=BG, padx=36, pady=30)
        outer.pack(fill="both", expand=True)
        outer.grid_columnconfigure(0, weight=1)

        header = tk.Frame(outer, bg=BG)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="EURO  /  LEK", bg=BG, fg=ACCENT,
                 font=(FONT, 11, "bold")).grid(row=0, column=0, sticky="w")
        cog = tk.Button(header, text="⚙", command=self.open_settings, bg=PANEL, fg=TEXT,
                        activebackground=CARD, activeforeground=ACCENT, bd=0,
                        font=(FONT, 23), cursor="hand2", width=3,
                        highlightthickness=0)
        cog.grid(row=0, column=1, rowspan=2, sticky="e")
        tk.Label(header, text="Conversion board", bg=BG, fg=TEXT,
                 font=(FONT, 27, "bold")).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.rate_label = tk.Label(outer, bg=BG, fg=MUTED, font=(FONT, 12))
        self.rate_label.grid(row=1, column=0, sticky="w", pady=(10, 28))

        board = tk.Frame(outer, bg=BG)
        board.grid(row=2, column=0, sticky="nsew")
        outer.grid_rowconfigure(2, weight=1)
        for col in range(3):
            board.grid_columnconfigure(col, weight=1, uniform="cards")
        for row in range(2):
            board.grid_rowconfigure(row, weight=1, uniform="cards")

        self.amount_labels: list[tuple[int, tk.Label]] = []
        for index, euros in enumerate(PRESETS):
            cell = tk.Frame(board, bg=CARD, padx=24, pady=20)
            cell.grid(row=index // 3, column=index % 3, sticky="nsew", padx=7, pady=7)
            tk.Label(cell, text=f"€ {euros}", bg=CARD, fg=MUTED,
                     font=(FONT, 16, "bold"), anchor="w").pack(fill="x")
            value = tk.Label(cell, bg=CARD, fg=TEXT, font=(FONT, 25, "bold"),
                             anchor="w")
            value.pack(fill="x", pady=(16, 4))
            tk.Label(cell, text="Albanian lek  ·  ALL", bg=CARD, fg=ACCENT,
                     font=(FONT, 10), anchor="w").pack(fill="x")
            self.amount_labels.append((euros, value))

        tk.Label(outer, text="Fixed amounts • Change the exchange rate using the gear above",
                 bg=BG, fg=MUTED, font=(FONT, 10)).grid(row=3, column=0,
                                                         sticky="w", pady=(22, 0))
        self.refresh()

    def refresh(self) -> None:
        self.rate_label.configure(text=f"1 EUR  =  {format_amount(self.rate)} ALL")
        for euros, label in self.amount_labels:
            label.configure(text=f"{format_amount(Decimal(euros) * self.rate)} Lek")

    def open_settings(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Exchange rate settings")
        dialog.configure(bg=PANEL)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.geometry("390x260")
        dialog.columnconfigure(0, weight=1)
        tk.Label(dialog, text="Exchange rate", bg=PANEL, fg=TEXT,
                 font=(FONT, 19, "bold")).grid(row=0, column=0, sticky="w", padx=28, pady=(25, 4))
        tk.Label(dialog, text="How many lek for 1 euro?", bg=PANEL, fg=MUTED,
                 font=(FONT, 11)).grid(row=1, column=0, sticky="w", padx=28)
        entry = tk.Entry(dialog, bg=BG, fg=TEXT, insertbackground=TEXT,
                         font=(FONT, 18), relief="flat", bd=10)
        entry.insert(0, str(self.rate))
        entry.grid(row=2, column=0, sticky="ew", padx=28, pady=(18, 15))
        entry.focus_set()
        entry.select_range(0, "end")

        def apply() -> None:
            try:
                new_rate = parse_rate(entry.get())
                save_rate(new_rate)
            except ValueError as exc:
                messagebox.showerror("Invalid rate", str(exc), parent=dialog)
                entry.focus_set()
                return
            except OSError as exc:
                messagebox.showerror("Could not save rate", str(exc), parent=dialog)
                return
            self.rate = new_rate
            self.refresh()
            dialog.destroy()

        actions = tk.Frame(dialog, bg=PANEL)
        actions.grid(row=3, column=0, sticky="e", padx=28)
        tk.Button(actions, text="Cancel", command=dialog.destroy, bg=CARD, fg=TEXT,
                  activebackground=BG, activeforeground=TEXT, relief="flat",
                  padx=14, pady=8, cursor="hand2").pack(side="left", padx=(0, 8))
        tk.Button(actions, text="Save rate", command=apply, bg=ACCENT, fg=BG,
                  activebackground="#84efd3", activeforeground=BG, relief="flat",
                  padx=14, pady=8, cursor="hand2").pack(side="left")
        dialog.bind("<Return>", lambda _event: apply())
        dialog.bind("<Escape>", lambda _event: dialog.destroy())


if __name__ == "__main__":
    Board().mainloop()
