# tests/test_factory.py

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.factory    import NotificationFactory
from patterns.strategy   import NotificationStrategy
from models.notification import Notification


class TestFactoryPattern(unittest.TestCase):
    """
    Verify that NotificationFactory correctly creates Notification
    objects for every channel and validates unknown channels.
    """

    # ── Channel creation ─────────────────────────────────────────────

    def test_creates_email_notification(self):
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "hello")
        self.assertEqual(n.get_channel(), "Email")

    def test_creates_sms_notification(self):
        n = NotificationFactory.create_notification(
            "sms", "+92300", "hello")
        self.assertEqual(n.get_channel(), "SMS")

    def test_creates_push_notification(self):
        n = NotificationFactory.create_notification(
            "push", "device_token_X", "hello")
        self.assertEqual(n.get_channel(), "Push")

    def test_creates_whatsapp_notification(self):
        n = NotificationFactory.create_notification(
            "whatsapp", "+92300", "hello")
        self.assertEqual(n.get_channel(), "WhatsApp")

    # ── Case insensitivity ───────────────────────────────────────────

    def test_case_insensitive_email(self):
        n1 = NotificationFactory.create_notification(
            "EMAIL", "a@b.com", "x")
        n2 = NotificationFactory.create_notification(
            "Email", "a@b.com", "x")
        n3 = NotificationFactory.create_notification(
            "email", "a@b.com", "x")
        self.assertEqual(n1.get_channel(), n2.get_channel())
        self.assertEqual(n2.get_channel(), n3.get_channel())

    def test_strips_whitespace_in_channel(self):
        n = NotificationFactory.create_notification(
            "  sms  ", "+92300", "hi")
        self.assertEqual(n.get_channel(), "SMS")

    # ── Error handling ───────────────────────────────────────────────

    def test_invalid_channel_raises_value_error(self):
        with self.assertRaises(ValueError):
            NotificationFactory.create_notification("fax", "x", "y")

    def test_invalid_channel_error_mentions_channel_name(self):
        with self.assertRaises(ValueError) as ctx:
            NotificationFactory.create_notification("pigeon_post", "x", "y")
        self.assertIn("pigeon_post", str(ctx.exception))

    def test_invalid_channel_error_mentions_available(self):
        with self.assertRaises(ValueError) as ctx:
            NotificationFactory.create_notification("telegram", "x", "y")
        # error message should list available channels
        error_text = str(ctx.exception).lower()
        self.assertIn("email", error_text)

    # ── Return type ──────────────────────────────────────────────────

    def test_returns_notification_instance(self):
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "test")
        self.assertIsInstance(n, Notification)

    # ── Available channels ───────────────────────────────────────────

    def test_get_available_channels_contains_all_four(self):
        channels = NotificationFactory.get_available_channels()
        for ch in ["email", "sms", "push", "whatsapp"]:
            self.assertIn(ch, channels,
                          f"'{ch}' missing from available channels")

    # ── Dynamic registration ─────────────────────────────────────────

    def test_register_channel_makes_it_usable(self):
        """register_channel() must make the new channel immediately available."""
        class TelegramStrategy(NotificationStrategy):
            def send(self, r, m): return True
            def get_channel_name(self): return "Telegram"

        NotificationFactory.register_channel("telegram", TelegramStrategy)
        n = NotificationFactory.create_notification(
            "telegram", "user_id_123", "hi")
        self.assertEqual(n.get_channel(), "Telegram")

    def test_register_channel_appears_in_available(self):
        class SignalStrategy(NotificationStrategy):
            def send(self, r, m): return True
            def get_channel_name(self): return "Signal"

        NotificationFactory.register_channel("signal", SignalStrategy)
        self.assertIn("signal", NotificationFactory.get_available_channels())


if __name__ == "__main__":
    unittest.main(verbosity=2)
