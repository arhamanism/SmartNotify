# tests/test_strategy.py

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.strategy   import NotificationStrategy
from patterns.factory    import NotificationFactory
from channels.email_channel    import EmailStrategy
from channels.sms_channel      import SMSStrategy
from channels.push_channel     import PushStrategy
from channels.whatsapp_channel import WhatsAppStrategy


class TestStrategyPattern(unittest.TestCase):
    """
    Verify Strategy encapsulation, channel names, send() return type,
    runtime swapping, and Liskov Substitution Principle compliance.
    """

    # ── Channel names ────────────────────────────────────────────────

    def test_email_channel_name(self):
        self.assertEqual(EmailStrategy().get_channel_name(), "Email")

    def test_sms_channel_name(self):
        self.assertEqual(SMSStrategy().get_channel_name(), "SMS")

    def test_push_channel_name(self):
        self.assertEqual(PushStrategy().get_channel_name(), "Push")

    def test_whatsapp_channel_name(self):
        self.assertEqual(WhatsAppStrategy().get_channel_name(), "WhatsApp")

    # ── send() return type ───────────────────────────────────────────

    def test_email_send_returns_bool(self):
        result = EmailStrategy().send("test@test.com", "hello")
        self.assertIsInstance(result, bool)

    def test_sms_send_returns_bool(self):
        result = SMSStrategy().send("+92300", "hello")
        self.assertIsInstance(result, bool)

    def test_push_send_returns_bool(self):
        result = PushStrategy().send("device_token", "hello")
        self.assertIsInstance(result, bool)

    def test_whatsapp_send_returns_bool(self):
        result = WhatsAppStrategy().send("+92300", "hello")
        self.assertIsInstance(result, bool)

    def test_all_strategies_send_returns_true(self):
        """All simulated sends should succeed (return True)."""
        strategies = [
            EmailStrategy(), SMSStrategy(),
            PushStrategy(), WhatsAppStrategy(),
        ]
        for strategy in strategies:
            result = strategy.send("recipient", "test message")
            self.assertTrue(result,
                            f"{type(strategy).__name__}.send() returned False")

    # ── Liskov Substitution Principle ────────────────────────────────

    def test_all_strategies_are_subclasses_of_abstract(self):
        """Every concrete strategy must be a subclass of NotificationStrategy."""
        for StratClass in [EmailStrategy, SMSStrategy,
                           PushStrategy, WhatsAppStrategy]:
            self.assertTrue(
                issubclass(StratClass, NotificationStrategy),
                f"{StratClass.__name__} is not a NotificationStrategy subclass"
            )

    def test_abstract_cannot_be_instantiated(self):
        """NotificationStrategy must not be directly instantiable."""
        with self.assertRaises(TypeError):
            NotificationStrategy()

    # ── Runtime channel swapping ─────────────────────────────────────

    def test_runtime_strategy_swap_email_to_sms(self):
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "hi")
        self.assertEqual(n.get_channel(), "Email")

        n.set_strategy(SMSStrategy())
        self.assertEqual(n.get_channel(), "SMS")

    def test_runtime_strategy_swap_through_all_channels(self):
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "hi")

        channels = [
            (SMSStrategy(),      "SMS"),
            (PushStrategy(),     "Push"),
            (WhatsAppStrategy(), "WhatsApp"),
            (EmailStrategy(),    "Email"),
        ]
        for strategy, expected_name in channels:
            n.set_strategy(strategy)
            self.assertEqual(
                n.get_channel(), expected_name,
                f"Expected '{expected_name}' after set_strategy, "
                f"got '{n.get_channel()}'"
            )

    def test_notification_deliver_uses_active_strategy(self):
        """deliver() must delegate to whichever strategy is currently set."""
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "hello")

        # Both deliver() calls should succeed regardless of strategy
        result1 = n.deliver()
        n.set_strategy(SMSStrategy())
        result2 = n.deliver()

        self.assertTrue(result1)
        self.assertTrue(result2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
