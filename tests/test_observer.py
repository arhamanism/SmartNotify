# tests/test_observer.py

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.singleton  import NotificationManager
from patterns.observer   import Observer, EventSystem, NotificationObserver
from models.event        import Event


class TestObserverPattern(unittest.TestCase):
    """
    Verify Observer subscription, automatic dispatch on emit(),
    unsubscription, and integration with the Singleton manager.
    """

    def setUp(self):
        NotificationManager._instance = None
        self.manager      = NotificationManager()
        self.event_system = EventSystem()

    # ── Basic subscribe + emit ───────────────────────────────────────

    def test_subscribed_observer_receives_event(self):
        """An observer subscribed to an event must receive it on emit()."""
        received = []

        class CapturingObserver(Observer):
            def update(self, event):
                received.append(event)

        self.event_system.subscribe("test_event", CapturingObserver())
        self.event_system.emit(
            Event("test_event", "a@b.com", "msg"))
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].event_type, "test_event")

    def test_multiple_observers_all_notified(self):
        """Every observer subscribed to an event must be called."""
        call_log = []

        for i in range(3):
            class Obs(Observer):
                def __init__(self, idx): self.idx = idx
                def update(self, event): call_log.append(self.idx)
            self.event_system.subscribe("multi_event", Obs(i))

        self.event_system.emit(
            Event("multi_event", "x@y.com", "hi"))
        self.assertEqual(len(call_log), 3,
                         "Not all 3 observers were called")

    def test_observer_not_called_for_different_event(self):
        """An observer subscribed to event A must NOT be called for event B."""
        received = []

        class CapturingObserver(Observer):
            def update(self, event): received.append(event)

        self.event_system.subscribe("event_A", CapturingObserver())
        self.event_system.emit(
            Event("event_B", "a@b.com", "msg"))
        self.assertEqual(len(received), 0)

    # ── Emit with no subscribers ─────────────────────────────────────

    def test_emit_unknown_event_does_not_raise(self):
        """Emitting an event with no subscribers must not raise an exception."""
        try:
            self.event_system.emit(
                Event("no_such_event", "a@b.com", "msg"))
        except Exception as e:
            self.fail(f"emit() raised: {e}")

    # ── Unsubscribe ──────────────────────────────────────────────────

    def test_unsubscribed_observer_not_called(self):
        """Observer must not receive events after unsubscribing."""
        received = []

        class CapturingObserver(Observer):
            def update(self, event): received.append(event)

        obs = CapturingObserver()
        self.event_system.subscribe("sub_event", obs)
        self.event_system.emit(Event("sub_event", "a@b.com", "first"))
        self.assertEqual(len(received), 1)

        self.event_system.unsubscribe("sub_event", obs)
        self.event_system.emit(Event("sub_event", "a@b.com", "second"))
        self.assertEqual(len(received), 1,  # still 1 — second not received
                         "Observer received event after unsubscribing")

    def test_unsubscribe_non_registered_observer_does_not_raise(self):
        """Unsubscribing an observer that was never registered must not crash."""
        class Obs(Observer):
            def update(self, event): pass
        try:
            self.event_system.unsubscribe("any_event", Obs())
        except Exception as e:
            self.fail(f"unsubscribe() raised: {e}")

    # ── NotificationObserver integration ────────────────────────────

    def test_notification_observer_logs_to_manager(self):
        """NotificationObserver.update() must log to the Singleton manager."""
        obs = NotificationObserver("email", self.manager)
        self.event_system.subscribe("order_placed", obs)

        logs_before = len(self.manager.get_logs())
        self.event_system.emit(
            Event("order_placed", "a@b.com", "Order confirmed!"))
        logs_after = len(self.manager.get_logs())

        self.assertEqual(logs_after, logs_before + 1,
                         "NotificationObserver did not log to manager")

    def test_two_channel_observers_produce_two_log_entries(self):
        """Two channel observers on the same event → 2 log entries."""
        self.event_system.subscribe(
            "order_placed", NotificationObserver("email", self.manager))
        self.event_system.subscribe(
            "order_placed", NotificationObserver("sms",   self.manager))

        logs_before = len(self.manager.get_logs())
        self.event_system.emit(
            Event("order_placed", "a@b.com", "Confirmed!"))
        logs_after = len(self.manager.get_logs())

        self.assertEqual(logs_after, logs_before + 2)

    def test_notification_observer_log_contains_correct_channel(self):
        """Log entry channel name must match the observer's channel."""
        self.event_system.subscribe(
            "security_alert", NotificationObserver("push", self.manager))
        self.event_system.emit(
            Event("security_alert", "a@b.com", "Suspicious login!"))

        last_log = self.manager.get_logs()[-1]
        self.assertEqual(last_log["channel"], "Push")

    # ── get_subscriptions ────────────────────────────────────────────

    def test_get_subscriptions_returns_dict(self):
        obs = NotificationObserver("email", self.manager)
        self.event_system.subscribe("order_placed", obs)

        subs = self.event_system.get_subscriptions()
        self.assertIn("order_placed", subs)
        self.assertIsInstance(subs["order_placed"], list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
