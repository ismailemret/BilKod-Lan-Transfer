"""BİLKOD LAN Transfer UI using in-memory device and offer fixtures."""

import argparse
from datetime import datetime
import tkinter as tk
from tkinter import ttk

from contracts.models import DeviceInfo, TransferOffer
from fixtures.fake_devices import get_mock_devices
from ui.offer_dialog import IncomingOfferDialog
from utils.logger import get_logger


logger = get_logger(__name__)


class MainWindow(tk.Tk):
    """Arrange the device, transfer and status panels without performing I/O."""

    def __init__(self) -> None:
        super().__init__()
        self.title("BİLKOD LAN Transfer")
        self.geometry("1000x650")
        self.minsize(800, 500)
        self.resizable(True, True)
        self._devices: dict[str, DeviceInfo] = {}
        self.selected_device: DeviceInfo | None = None

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
        self.device_tree.bind("<<TreeviewSelect>>", self._on_device_selected)

        scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.device_tree.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.device_tree.configure(yscrollcommand=scrollbar.set)

        self.target_label = ttk.Label(panel, text="Hedef: Yok", wraplength=300)
        self.target_label.grid(row=2, column=0, sticky="w", pady=(8, 0))

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

    def _append_log(self, message: str) -> None:
        self.log_area.configure(state="normal")
        try:
            self.log_area.insert("end", f"{datetime.now():%H:%M:%S} | {message}\n")
            self.log_area.see("end")
        finally:
            self.log_area.configure(state="disabled")
        logger.info(message)

    def load_devices(self, devices: list[DeviceInfo]) -> None:
        """Replace the device list with remote peers from the supplied snapshot."""
        self.device_tree.delete(*self.device_tree.get_children())
        self._devices = {device.device_id: device for device in devices if not device.is_self}
        for device in self._devices.values():
            self.device_tree.insert(
                "", "end", iid=device.device_id,
                values=(device.hostname, device.ip_address),
            )
        self._on_device_selected()

    def on_scan_clicked(self) -> None:
        self.load_devices(get_mock_devices())
        self._append_log(f"{len(self._devices)} cihaz bulundu (sahte veri)")

    def _on_device_selected(self, event: tk.Event | None = None) -> None:
        previous_device = self.selected_device
        selection = self.device_tree.selection()
        self.selected_device = self._devices.get(selection[0]) if selection else None
        device = self.selected_device
        target = f"Hedef: {device.hostname} ({device.ip_address})" if device else "Hedef: Yok"
        self.target_label.configure(text=target)
        if self.selected_device != previous_device:
            self._append_log(target)

    def on_incoming_offer(
        self, offer: TransferOffer, sender: DeviceInfo | None = None
    ) -> None:
        """Display an offer and notify the decision stub on the Tk UI thread."""
        dialog = IncomingOfferDialog(self, offer, sender)
        self.wait_window(dialog)
        accepted = dialog.result
        status = "Aktarım Başlatılıyor..." if accepted else "Aktarım Reddedildi"
        self.status_text.set(status)
        self._append_log(status)
        self.on_offer_decision(offer, accepted=accepted)

    def on_offer_decision(self, offer: TransferOffer, accepted: bool) -> None:
        """Log a decision; the network response will be integrated separately."""
        self._append_log(f"Teklif kararı: {offer.transfer_id}, accepted={accepted}")

    def on_select_file_clicked(self) -> None:
        pass

    def on_send_clicked(self) -> None:
        pass

    def on_cancel_clicked(self) -> None:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BİLKOD LAN Transfer")
    parser.add_argument("--demo-offer", action="store_true", help="Sahte gelen teklifi göster")
    args = parser.parse_args()
    window = MainWindow()
    if args.demo_offer:
        from fixtures.fake_transfers import MOCK_OFFER

        sender = next(
            (device for device in get_mock_devices() if device.device_id == MOCK_OFFER.sender_id),
            None,
        )
        window.after(500, lambda: window.on_incoming_offer(MOCK_OFFER, sender))
    window.mainloop()
