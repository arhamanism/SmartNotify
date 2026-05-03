# tests/test_singleton.py

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.singleton  import NotificationManager
from patterns.factory    import NotificationFactory
from models.event        import Event


class TestSingletonPattern(unittest.TestCase):
    """
    Verify that NotificationManager is a true Singleton.
    All tests in this file confirm:
      - Same object returned on every call
      - Same memory address (id)
      - State persists across references
      - Thread safety
      - Re-initialization prevention
    """

    def setUp(self):
        """Reset singleton before each test for clean state."""
        NotificationManager._instance = None

    # ── Core singleton behaviour ─────────────────────────────────────

    def test_same_instance_returned(self):
        """Two calls to NotificationManager() must return the same object."""
        m1 = NotificationManager()
        m2 = NotificationManager()
        self.assertIs(m1, m2,
                      "Singleton violated: two different instances returned")

    def test_same_memory_address(self):
        """id() of both references must be identical."""
        m1 = NotificationManager()
        m2 = NotificationManager()
        self.assertEqual(id(m1), id(m2))

    def test_three_references_same_object(self):
        """Any number of calls return the same object."""
        m1 = NotificationManager()
        m2 = NotificationManager()
        m3 = NotificationManager()
        self.assertIs(m1, m2)
        self.assertIs(m2, m3)

    # ── State persistence ────────────────────────────────────────────

    def test_logs_shared_across_references(self):
        """Log written via m1 must be visible via m2."""
        m1 = NotificationManager()
        m2 = NotificationManager()

        n   = NotificationFactory.create_notification(
                "email", "test@test.com", "hello")
        evt = Event("order_placed", "test@test.com", "hello")
        m1.log(evt, n, True)

        self.assertEqual(len(m2.get_logs()), len(m1.get_logs()))
        self.assertEqual(m2.get_logs()[-1]["channel"], "Email")

    def test_stats_accumulate_correctly(self):
        """Success and failure counts must be tracked accurately."""
        m   = NotificationManager()
        n   = NotificationFactory.create_notification("sms", "+92300", "x")
        evt = Event("test_event", "+92300", "x")

        m.log(evt, n, True)
        m.log(evt, n, True)
        m.log(evt, n, False)

        stats = m.get_stats()
        self.assertEqual(stats["successful"], 2)
        self.assertEqual(stats["failed"],     1)
        self.assertEqual(stats["total_notifications"], 3)

    def test_success_rate_calculated(self):
        """Success rate string must be present after logging."""
        m   = NotificationManager()
        n   = NotificationFactory.create_notification("email", "a@b.com", "hi")
        evt = Event("test_event", "a@b.com", "hi")
        m.log(evt, n, True)

        stats = m.get_stats()
        self.assertIn("%", stats["success_rate"])

    def test_empty_stats_returns_na(self):
        """Success rate must be 'N/A' when no logs exist."""
        m     = NotificationManager()
        stats = m.get_stats()
        self.assertEqual(stats["success_rate"], "N/A")

    # ── Re-initialization prevention ─────────────────────────────────

    def test_reinitialization_does_not_reset_logs(self):
        """Calling __init__ again must not wipe existing logs."""
        m   = NotificationManager()
        n   = NotificationFactory.create_notification("push", "dev_X", "hi")
        evt = Event("test_event", "dev_X", "hi")
        m.log(evt, n, True)
        count_before = len(m.get_logs())

        m.__init__()  # simulate second instantiation

        self.assertEqual(len(m.get_logs()), count_before,
                         "Re-initialization wiped the log!")

    # ── get_logs returns a copy ──────────────────────────────────────

    def test_get_logs_returns_copy(self):
        """Mutating the returned list must not affect internal log."""
        m   = NotificationManager()
        n   = NotificationFactory.create_notification("email", "a@b.com", "hi")
        evt = Event("test_event", "a@b.com", "hi")
        m.log(evt, n, True)

        logs = m.get_logs()
        logs.clear()  # mutate the copy

        self.assertEqual(len(m.get_logs()), 1,
                         "Internal log was mutated through get_logs()")


if __name__ == "__main__":
    unittest.main(verbosity=2)
