"""Modal approval dialog for an incoming transfer offer."""

import tkinter as tk
from tkinter import ttk

from contracts.models import DeviceInfo, TransferOffer


def format_size(size_bytes: int) -> str:
    """Format a byte count in 1024-based B/KB/MB/GB units."""
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size_bytes} B" if unit == "B" else f"{size:.2f} {unit}"
        size /= 1024


class IncomingOfferDialog(tk.Toplevel):
    """Keep a boolean result; closing the window is a rejection."""

    def __init__(
        self, parent: tk.Misc, offer: TransferOffer, sender: DeviceInfo | None = None
    ) -> None:
        super().__init__(parent)
        self.result: bool = False
        self.title("Gelen Aktarım Teklifi")
        self.transient(parent)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._reject)
        self.bind("<Escape>", self._reject)

        content = ttk.Frame(self, padding=20)
        content.grid(row=0, column=0, sticky="nsew")
        sender_text = f"{sender.hostname} ({sender.ip_address})" if sender else offer.sender_id
        for row, (label, value) in enumerate((
            ("Gönderen:", sender_text),
            ("Dosya adı:", offer.filename),
            ("Boyut:", format_size(offer.file_size_bytes)),
        )):
            ttk.Label(content, text=label).grid(row=row, column=0, sticky="nw", padx=(0, 12), pady=6)
            ttk.Label(content, text=value, wraplength=360).grid(row=row, column=1, sticky="w", pady=6)

        buttons = ttk.Frame(content)
        buttons.grid(row=3, column=0, columnspan=2, sticky="e", pady=(16, 0))
        accept_button = ttk.Button(buttons, text="Kabul Et", command=self._accept)
        accept_button.grid(row=0, column=0, padx=(0, 8))
        accept_button.bind("<Return>", self._accept)
        reject_button = ttk.Button(buttons, text="Reddet", command=self._reject)
        reject_button.grid(row=0, column=1)
        reject_button.bind("<Return>", self._reject)

        parent.update_idletasks()
        self.update_idletasks()
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")
        self.wait_visibility()
        self.grab_set()
        reject_button.focus_set()

    def _accept(self, event: tk.Event | None = None) -> str:
        self.result = True
        self.destroy()
        return "break"

    def _reject(self, event: tk.Event | None = None) -> str:
        self.result = False
        self.destroy()
        return "break"
