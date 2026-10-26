"""Standalone visual skeleton for the BİLKOD LAN Transfer interface."""

import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    """Arrange the device, transfer and status panels without performing I/O."""

    def __init__(self) -> None:
        super().__init__()
        self.title("BİLKOD LAN Transfer")
        self.geometry("1000x650")
        self.minsize(800, 500)
        self.resizable(True, True)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)

        self._create_device_panel()
        self._create_transfer_panel()
        self._create_status_panel()

    def _create_device_panel(self) -> None:
        panel = ttk.LabelFrame(self, text="Cihazlar", padding=12)
        panel.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=(12, 6))
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        ttk.Button(panel, text="Ağı Tara", command=self.on_scan_clicked).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        self.device_tree = ttk.Treeview(
            panel, columns=("name", "ip"), show="headings", selectmode="browse"
        )
        self.device_tree.heading("name", text="Cihaz adı")
        self.device_tree.heading("ip", text="IP adresi")
        self.device_tree.column("name", width=160, minwidth=100, stretch=True)
        self.device_tree.column("ip", width=130, minwidth=100, stretch=True)
        self.device_tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.device_tree.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.device_tree.configure(yscrollcommand=scrollbar.set)

    def _create_transfer_panel(self) -> None:
        panel = ttk.LabelFrame(self, text="Dosya Seçimi ve Transfer", padding=12)
        panel.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=(12, 6))
        panel.columnconfigure(0, weight=1)

        ttk.Button(
            panel, text="Dosya Seç", command=self.on_select_file_clicked
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.selected_file_label = ttk.Label(panel, text="Seçili dosya: Yok")
        self.selected_file_label.grid(row=1, column=0, sticky="w", pady=(0, 20))

        actions = ttk.Frame(panel)
        actions.grid(row=2, column=0, sticky="w", pady=(0, 20))
        ttk.Button(actions, text="Gönder", command=self.on_send_clicked).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(actions, text="İptal", command=self.on_cancel_clicked).grid(
            row=0, column=1
        )

        self.progress_bar = ttk.Progressbar(
            panel, orient="horizontal", mode="determinate", maximum=100, value=0
        )
        self.progress_bar.grid(row=3, column=0, sticky="ew")
        self.progress_label = ttk.Label(panel, text="%0")
        self.progress_label.grid(row=4, column=0, sticky="e", pady=(6, 0))

    def _create_status_panel(self) -> None:
        panel = ttk.LabelFrame(self, text="Durum ve Log", padding=12)
        panel.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=(6, 12)
        )
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        self.status_text = tk.StringVar(master=self, value="Bekleniyor")
        status_row = ttk.Frame(panel)
        status_row.grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Label(status_row, text="Durum:").grid(row=0, column=0, padx=(0, 6))
        self.status_label = ttk.Label(status_row, textvariable=self.status_text)
        self.status_label.grid(row=0, column=1, sticky="w")

        self.log_area = tk.Text(panel, height=7, wrap="word", state="disabled")
        self.log_area.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.log_area.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_area.configure(yscrollcommand=scrollbar.set)

    def on_scan_clicked(self) -> None:
        pass

    def on_select_file_clicked(self) -> None:
        pass

    def on_send_clicked(self) -> None:
        pass

    def on_cancel_clicked(self) -> None:
        pass


if __name__ == "__main__":
    MainWindow().mainloop()
