# tests/test_integration.py

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.singleton  import NotificationManager
from patterns.factory    import NotificationFactory
from patterns.observer   import EventSystem, NotificationObserver
from channels.sms_channel      import SMSStrategy
from channels.push_channel     import PushStrategy
from channels.whatsapp_channel import WhatsAppStrategy
from channels.email_channel    import EmailStrategy
from services.order_service       import OrderService
from services.security_service    import SecurityService
from services.promotional_service import PromotionalService
from models.event import Event


class TestIntegration(unittest.TestCase):
    """
    End-to-end tests: all four patterns working together through
    the full service → event → observer → factory → strategy → log pipeline.
    """

    def setUp(self):
        NotificationManager._instance = None
        self.manager      = NotificationManager()
        self.event_system = EventSystem()

        # Wire up observers — same as main.py setup
        self.event_system.subscribe(
            "order_placed",     NotificationObserver("email",    self.manager))
        self.event_system.subscribe(
            "order_placed",     NotificationObserver("sms",      self.manager))
        self.event_system.subscribe(
            "security_alert",   NotificationObserver("email",    self.manager))
        self.event_system.subscribe(
            "security_alert",   NotificationObserver("push",     self.manager))
        self.event_system.subscribe(
            "promotional",      NotificationObserver("push",     self.manager))
        self.event_system.subscribe(
            "promotional",      NotificationObserver("whatsapp", self.manager))
        self.event_system.subscribe(
            "password_reset",   NotificationObserver("sms",      self.manager))
        self.event_system.subscribe(
            "refund_processed", NotificationObserver("email",    self.manager))
        self.event_system.subscribe(
            "refund_processed", NotificationObserver("sms",      self.manager))

        self.order_svc    = OrderService(self.event_system)
        self.security_svc = SecurityService(self.event_system)
        self.promo_svc    = PromotionalService(self.event_system)

    # ── OrderService integration ─────────────────────────────────────

    def test_order_placement_fires_two_notifications(self):
        """order_placed has 2 observers → must produce 2 log entries."""
        before = len(self.manager.get_logs())
        self.order_svc.place_order(101, "hassan@example.com", "ORD-001")
        self.assertEqual(len(self.manager.get_logs()), before + 2)

    def test_order_placement_channels_are_email_and_sms(self):
        self.order_svc.place_order(101, "hassan@example.com", "ORD-002")
        logs     = self.manager.get_logs()
        channels = {e["channel"] for e in logs}
        self.assertIn("Email", channels)
        self.assertIn("SMS",   channels)

    def test_order_event_type_logged_correctly(self):
        self.order_svc.place_order(101, "hassan@example.com", "ORD-003")
        last_logs = self.manager.get_logs()[-2:]
        for entry in last_logs:
            self.assertEqual(entry["event_type"], "order_placed")

    # ── SecurityService integration ──────────────────────────────────

    def test_security_alert_fires_two_notifications(self):
        """security_alert has 2 observers → must produce 2 log entries."""
        before = len(self.manager.get_logs())
        self.security_svc.detect_suspicious_login(
            101, "hassan@example.com", "192.168.1.1")
        self.assertEqual(len(self.manager.get_logs()), before + 2)

    def test_security_alert_channels_are_email_and_push(self):
        self.security_svc.detect_suspicious_login(
            101, "hassan@example.com", "10.0.0.1")
        logs     = self.manager.get_logs()
        channels = {e["channel"] for e in logs}
        self.assertIn("Email", channels)
        self.assertIn("Push",  channels)

    def test_password_reset_fires_one_sms(self):
        before = len(self.manager.get_logs())
        self.security_svc.trigger_password_reset(
            101, "hassan@example.com")
        after = len(self.manager.get_logs())
        self.assertEqual(after, before + 1)
        self.assertEqual(self.manager.get_logs()[-1]["channel"], "SMS")

    # ── PromotionalService integration ──────────────────────────────

    def test_promotional_blast_two_recipients_four_logs(self):
        """2 recipients × 2 observers (push+whatsapp) = 4 log entries."""
        before = len(self.manager.get_logs())
        self.promo_svc.send_promotion(
            ["arham@example.com", "usman@example.com"],
            "Flash Sale! 50% off"
        )
        self.assertEqual(len(self.manager.get_logs()), before + 4)

    def test_refund_fires_email_and_sms(self):
        before = len(self.manager.get_logs())
        self.promo_svc.send_refund_notification(
            "arham@example.com", 1200)
        after = len(self.manager.get_logs())
        self.assertEqual(after, before + 2)
        channels = {e["channel"]
                    for e in self.manager.get_logs()[before:]}
        self.assertIn("Email", channels)
        self.assertIn("SMS",   channels)

    # ── Singleton shared across all services ─────────────────────────

    def test_singleton_log_accumulates_across_all_services(self):
        """Singleton log must grow as all three services fire events."""
        before = len(self.manager.get_logs())

        self.order_svc.place_order(101, "a@b.com", "ORD-X")     # +2
        self.security_svc.detect_suspicious_login(
            101, "a@b.com", "1.2.3.4")                           # +2
        self.promo_svc.send_promotion(["a@b.com"], "Sale!")       # +2

        after = len(self.manager.get_logs())
        self.assertEqual(after, before + 6)

    def test_singleton_is_same_object_throughout(self):
        """manager fetched mid-test must be the same singleton."""
        m_direct = NotificationManager()
        self.assertIs(m_direct, self.manager)

    # ── Strategy runtime swap in integration ─────────────────────────

    def test_strategy_swap_after_factory_creation(self):
        """Notification created by Factory can have its strategy swapped."""
        n = NotificationFactory.create_notification(
            "email", "a@b.com", "hello")
        self.assertEqual(n.get_channel(), "Email")

        n.set_strategy(WhatsAppStrategy())
        self.assertEqual(n.get_channel(), "WhatsApp")

        result = n.deliver()
        self.assertTrue(result)

    # ── Dynamic channel registration + observer ──────────────────────

    def test_dynamic_channel_usable_via_observer(self):
        """Dynamically registered channel must work end-to-end via Observer."""
        from patterns.strategy import NotificationStrategy

        class SlackStrategy(NotificationStrategy):
            def send(self, r, m): return True
            def get_channel_name(self): return "Slack"

        NotificationFactory.register_channel("slack", SlackStrategy)
        self.event_system.subscribe(
            "dev_alert", NotificationObserver("slack", self.manager))

        before = len(self.manager.get_logs())
        self.event_system.emit(
            Event("dev_alert", "#dev-channel", "Deploy complete"))
        after = len(self.manager.get_logs())

        self.assertEqual(after, before + 1)
        self.assertEqual(self.manager.get_logs()[-1]["channel"], "Slack")


if __name__ == "__main__":
    unittest.main(verbosity=2)
