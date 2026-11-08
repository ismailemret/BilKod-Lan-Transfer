"""Issue #12: UI approval tests using only in-memory fixture data."""

import tkinter as tk
import unittest
from unittest.mock import patch

from contracts.models import DeviceInfo
from fixtures.fake_devices import get_mock_devices
from fixtures.fake_transfers import MOCK_OFFER
from ui.main_window import MainWindow
from ui.offer_dialog import IncomingOfferDialog, format_size


class FormatSizeTests(unittest.TestCase):
    def test_binary_unit_boundaries_and_fractional_sizes(self):
        cases = (
            (0, "0 B"),
            (1, "1 B"),
            (1023, "1023 B"),
            (1024, "1.00 KB"),
            (1536, "1.50 KB"),
            (1048576, "1.00 MB"),
            (4194304, "4.00 MB"),
            (1073741824, "1.00 GB"),
            (1099511627776, "1024.00 GB"),
        )
        for size, expected in cases:
            with self.subTest(size=size):
                self.assertEqual(format_size(size_bytes=size), expected)


class TkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            probe = tk.Tk()
        except tk.TclError as error:
            raise unittest.SkipTest(f"Tk ekranı kullanılamıyor: {error}") from error
        probe.withdraw()
        probe.destroy()

    def setUp(self):
        self.window = MainWindow()
        self.window.withdraw()
        self.addCleanup(self.window.destroy)


class MainWindowTests(TkTests):
    def test_load_devices_filters_self_and_replaces_old_rows(self):
        self.window.load_devices(get_mock_devices())
        self.assertEqual(self.window.device_tree.get_children(), ("dev-01", "dev-02"))
        self.assertEqual(
            self.window.device_tree.item("dev-01", "values"),
            ("Laptop-Alpha", "192.168.1.101"),
        )
        replacement = DeviceInfo("new", "New host", "192.168.1.9", 50001)
        self.window.load_devices([replacement])
        self.assertEqual(self.window.device_tree.get_children(), ("new",))
        self.assertEqual(self.window._devices, {"new": replacement})

    def test_selection_event_updates_target_and_log(self):
        devices = get_mock_devices()
        self.window.load_devices(devices)
        self.window.device_tree.selection_set("dev-01")
        self.window.update()
        self.assertEqual(self.window.selected_device, devices[0])
        self.assertEqual(
            self.window.target_label.cget("text"),
            "Hedef: Laptop-Alpha (192.168.1.101)",
        )
        self.assertIn("Hedef: Laptop-Alpha (192.168.1.101)", self.log_text())

    def test_clearing_selection_clears_target(self):
        self.window.load_devices(get_mock_devices())
        self.window.device_tree.selection_set("dev-02")
        self.window.update()
        self.window.device_tree.selection_remove("dev-02")
        self.window.update()
        self.assertIsNone(self.window.selected_device)
        self.assertEqual(self.window.target_label.cget("text"), "Hedef: Yok")
        self.assertIn("Hedef: Yok", self.log_text())

    def test_reload_clears_stale_selection(self):
        self.window.load_devices(get_mock_devices())
        self.window.device_tree.selection_set("dev-01")
        self.window.update()
        self.window.load_devices([])
        self.assertIsNone(self.window.selected_device)
        self.assertEqual(self.window.target_label.cget("text"), "Hedef: Yok")

    def test_scan_logs_number_of_visible_remote_devices(self):
        self.window.on_scan_clicked()
        self.assertEqual(len(self.window.device_tree.get_children()), 2)
        self.assertIn("2 cihaz bulundu (sahte veri)", self.log_text())

    def test_repeated_scans_do_not_repeat_no_target_log(self):
        self.window.on_scan_clicked()
        self.window.on_scan_clicked()
        self.window.update()
        self.assertNotIn("Hedef: Yok", self.log_text())

        self.window.device_tree.selection_set("dev-01")
        self.window.update()
        self.window.on_scan_clicked()
        self.window.update()
        self.window.on_scan_clicked()
        self.window.update()
        self.assertEqual(self.log_text().count("Hedef: Yok"), 1)

    def test_unchanged_selection_does_not_repeat_target_log(self):
        self.window.load_devices(get_mock_devices())
        self.window.device_tree.selection_set("dev-01")
        self.window.update()
        self.window.device_tree.event_generate("<<TreeviewSelect>>")
        self.window.update()
        self.assertEqual(
            self.log_text().count("Hedef: Laptop-Alpha (192.168.1.101)"), 1
        )

    def test_append_log_timestamps_appends_and_disables_widget(self):
        with self.assertLogs("ui.main_window", level="INFO") as logs:
            self.window._append_log("İlk mesaj")
            self.window._append_log("İkinci mesaj")
        self.assertRegex(
            self.log_text(),
            r"^\d{2}:\d{2}:\d{2} \| İlk mesaj\n\d{2}:\d{2}:\d{2} \| İkinci mesaj\n$",
        )
        self.assertEqual(self.window.log_area.cget("state"), "disabled")
        self.assertEqual([record.getMessage() for record in logs.records],
                         ["İlk mesaj", "İkinci mesaj"])

    def test_accept_updates_status_and_notifies_decision(self):
        self.check_offer_decision(True, "Aktarım Başlatılıyor...")

    def test_reject_updates_status_and_notifies_decision(self):
        self.check_offer_decision(False, "Aktarım Reddedildi")

    def check_offer_decision(self, accepted, expected_status):
        sender = get_mock_devices()[0]
        with patch("ui.main_window.IncomingOfferDialog") as dialog_type:
            dialog = dialog_type.return_value
            dialog.result = accepted
            with patch.object(self.window, "wait_window") as wait:
                with patch.object(self.window, "on_offer_decision") as decision:
                    self.window.on_incoming_offer(MOCK_OFFER, sender)
        self.assertEqual(self.window.status_text.get(), expected_status)
        self.assertIn(expected_status, self.log_text())
        dialog_type.assert_called_once_with(self.window, MOCK_OFFER, sender)
        wait.assert_called_once_with(dialog)
        decision.assert_called_once_with(MOCK_OFFER, accepted=accepted)

    def test_decision_stub_only_logs(self):
        for accepted in (True, False):
            with self.subTest(accepted=accepted):
                with self.assertLogs("ui.main_window", level="INFO") as logs:
                    self.window.on_offer_decision(MOCK_OFFER, accepted=accepted)
                self.assertIn("tx-1001", logs.records[0].getMessage())
                self.assertIn(str(accepted), logs.records[0].getMessage())

    def log_text(self):
        return self.window.log_area.get("1.0", "end-1c")


class OfferDialogTests(TkTests):
    def create_dialog(self, sender=None):
        self.window.deiconify()
        self.window.update()
        self.window.focus_force()
        dialog = IncomingOfferDialog(self.window, MOCK_OFFER, sender)
        self.addCleanup(lambda: dialog.destroy() if dialog.winfo_exists() else None)
        return dialog

    def test_dialog_displays_sender_filename_size_and_modal_settings(self):
        dialog = self.create_dialog(get_mock_devices()[0])
        labels = [child.cget("text") for child in dialog.winfo_children()[0].winfo_children()
                  if child.winfo_class() == "TLabel"]
        self.assertIn("Laptop-Alpha (192.168.1.101)", labels)
        self.assertIn("sample_bilkod.pdf", labels)
        self.assertIn("4.00 MB", labels)
        self.assertEqual(str(dialog.transient()), str(self.window))
        self.assertEqual(dialog.grab_current(), dialog)
        self.assertEqual(dialog.resizable(), (0, 0))

    def test_unknown_sender_uses_sender_id(self):
        dialog = self.create_dialog()
        labels = [child.cget("text") for child in dialog.winfo_children()[0].winfo_children()
                  if child.winfo_class() == "TLabel"]
        self.assertIn("dev-01", labels)

    def test_accept_button_returns_true(self):
        dialog = self.create_dialog()
        self.find_button(dialog, "Kabul Et").invoke()
        self.assertIs(dialog.result, True)
        self.assertFalse(dialog.winfo_exists())

    def test_reject_button_returns_false(self):
        dialog = self.create_dialog()
        self.find_button(dialog, "Reddet").invoke()
        self.assertIs(dialog.result, False)
        self.assertFalse(dialog.winfo_exists())

    def test_window_close_is_rejection(self):
        dialog = self.create_dialog()
        dialog.tk.call(dialog.protocol("WM_DELETE_WINDOW"))
        self.assertIs(dialog.result, False)
        self.assertFalse(dialog.winfo_exists())

    def test_initial_focus_is_reject_button(self):
        dialog = self.create_dialog()
        dialog.update()
        self.assertEqual(dialog.focus_get(), self.find_button(dialog, "Reddet"))

    def test_enter_accepts_and_escape_rejects(self):
        cases = (
            ("Kabul Et", "<Return>", True),
            ("Reddet", "<Return>", False),
            ("Kabul Et", "<Escape>", False),
        )
        for button_text, key, expected in cases:
            with self.subTest(button=button_text, key=key):
                dialog = self.create_dialog()
                dialog.update()
                button = self.find_button(dialog, button_text)
                button.focus_force()
                dialog.update()
                button.event_generate(key)
                self.assertIs(dialog.result, expected)
                self.assertFalse(dialog.winfo_exists())

    @staticmethod
    def find_button(widget, text):
        for child in widget.winfo_children():
            if child.winfo_class() == "TButton" and child.cget("text") == text:
                return child
            button = OfferDialogTests.find_button(child, text)
            if button is not None:
                return button
        return None


if __name__ == "__main__":
    unittest.main(verbosity=2)
