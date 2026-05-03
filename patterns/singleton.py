# patterns/singleton.py

import threading
import datetime


class NotificationManager:
    """
    ═══════════════════════════════════════════════════════════════
    SINGLETON PATTERN — Centralized Notification Manager
    ═══════════════════════════════════════════════════════════════
    Guarantees exactly ONE instance across the entire application.
    Every service — OrderService, SecurityService, PromotionalService
    — calls NotificationManager() and gets the SAME object.

    This gives us:
      • One central log   — system-wide stats from a single call
      • Thread safety     — __new__ protected by threading.Lock()
      • No duplication    — no per-service log lists

    PROOF:
        m1 = NotificationManager()
        m2 = NotificationManager()
        assert m1 is m2           # True — same object
        assert id(m1) == id(m2)   # True — same memory address
    ═══════════════════════════════════════════════════════════════
    """

    _instance = None
    _lock     = threading.Lock()   # ensures thread-safe first creation

    # ── Singleton enforcement ────────────────────────────────────────

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance        # always the same object

    def __init__(self):
        if self._initialized:
            return                  # guard: never re-run __init__
        self._initialized  = True
        self._logs         = []
        self._total_sent   = 0
        self._total_failed = 0
        print("[NotificationManager] Singleton instance created.")

    # ── Public API ───────────────────────────────────────────────────

    def log(self, event, notification, success: bool) -> None:
        """
        Record a notification attempt to the central log.
        Called by NotificationObserver after every delivery attempt.
        """
        status = "SUCCESS" if success else "FAILED"
        entry  = {
            "timestamp":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event.event_type,
            "recipient":  event.recipient,
            "channel":    notification.get_channel(),
            "message":    notification.message,
            "status":     status,
        }
        self._logs.append(entry)
        if success:
            self._total_sent   += 1
        else:
            self._total_failed += 1

    def get_stats(self) -> dict:
        """Return system-wide delivery statistics."""
        total = len(self._logs)
        return {
            "total_notifications": total,
            "successful":          self._total_sent,
            "failed":              self._total_failed,
            "success_rate": (
                f"{self._total_sent / total * 100:.1f}%"
                if total else "N/A"
            ),
        }

    def get_logs(self) -> list:
        """Return a copy of the complete notification log."""
        return self._logs.copy()

    def display_all_logs(self) -> None:
        """Pretty-print the full log to stdout."""
        print("\n" + "=" * 70)
        print("  CENTRALIZED NOTIFICATION LOG  (Singleton NotificationManager)")
        print("=" * 70)
        if not self._logs:
            print("  No notifications logged yet.")
        for e in self._logs:
            print(
                f"  [{e['timestamp']}]  {e['status']:8}  |  "
                f"{e['channel']:10}  →  {e['recipient']:30}  |  "
                f"{e['event_type']}"
            )
        print("=" * 70)
        s = self.get_stats()
        print(
            f"  Total: {s['total_notifications']}  |  "
            f"OK: {s['successful']}  |  "
            f"Failed: {s['failed']}  |  "
            f"Success rate: {s['success_rate']}"
        )
        print("=" * 70 + "\n")
