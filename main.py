# main.py
"""
╔══════════════════════════════════════════════════════════════════════╗
║         Smart Notification System — Main Entry Point                ║
║                                                                      ║
║  Demonstrates all four design patterns working together:            ║
║    1. Singleton  — NotificationManager (one instance, one log)      ║
║    2. Factory    — NotificationFactory (centralized creation)       ║
║    3. Observer   — EventSystem + NotificationObserver               ║
║    4. Strategy   — Email / SMS / Push / WhatsApp strategies         ║
╚══════════════════════════════════════════════════════════════════════╝

Run:  python main.py
"""

from patterns.singleton  import NotificationManager
from patterns.factory    import NotificationFactory
from patterns.observer   import EventSystem, NotificationObserver
from patterns.strategy   import NotificationStrategy
from channels.sms_channel      import SMSStrategy
from channels.push_channel     import PushStrategy
from channels.whatsapp_channel import WhatsAppStrategy
from channels.email_channel    import EmailStrategy
from services.order_service       import OrderService
from services.security_service    import SecurityService
from services.promotional_service import PromotionalService
from models.event import Event


def print_section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


def main():

    print("=" * 70)
    print("  SMART NOTIFICATION SYSTEM — Design Pattern Demonstration")
    print("=" * 70)

    # ══════════════════════════════════════════════════════════════════
    # STEP 1 — SINGLETON PATTERN
    # Create the one shared NotificationManager.
    # Every service and observer will use this same instance.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 1 — Singleton Pattern: NotificationManager")

    manager  = NotificationManager()
    manager2 = NotificationManager()   # same object — Singleton

    print(f"\n  manager  is manager2    →  {manager is manager2}")
    print(f"  id(manager) == id(manager2) →  {id(manager) == id(manager2)}")
    print("  ✓ Singleton confirmed — one instance, one central log.")

    # ══════════════════════════════════════════════════════════════════
    # STEP 2 — OBSERVER PATTERN SETUP
    # Create EventSystem and register observers (channel × event mappings).
    # Business services fire events; observers handle delivery.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 2 — Observer Pattern: EventSystem subscriptions")

    event_system = EventSystem()

    # order_placed → Email + SMS
    event_system.subscribe("order_placed",
                           NotificationObserver("email", manager))
    event_system.subscribe("order_placed",
                           NotificationObserver("sms",   manager))

    # security_alert → Email + Push
    event_system.subscribe("security_alert",
                           NotificationObserver("email", manager))
    event_system.subscribe("security_alert",
                           NotificationObserver("push",  manager))

    # promotional → Push + WhatsApp
    event_system.subscribe("promotional",
                           NotificationObserver("push",     manager))
    event_system.subscribe("promotional",
                           NotificationObserver("whatsapp", manager))

    # password_reset → SMS only
    event_system.subscribe("password_reset",
                           NotificationObserver("sms", manager))

    # refund_processed → Email + SMS
    event_system.subscribe("refund_processed",
                           NotificationObserver("email", manager))
    event_system.subscribe("refund_processed",
                           NotificationObserver("sms",   manager))

    print("\n  Current subscriptions:")
    for evt, obs_list in event_system.get_subscriptions().items():
        print(f"    {evt:20} →  {', '.join(obs_list)}")

    # ══════════════════════════════════════════════════════════════════
    # STEP 3 — CLEAN BUSINESS SERVICES
    # Each service receives an EventSystem — zero notification code inside.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 3 — Clean Business Services (zero notification code)")

    order_svc    = OrderService(event_system)
    security_svc = SecurityService(event_system)
    promo_svc    = PromotionalService(event_system)

    print("  ✓ OrderService, SecurityService, PromotionalService ready.")
    print("  ✓ None of these classes contain Email/SMS/Push logic.")

    # ══════════════════════════════════════════════════════════════════
    # STEP 4 — FIRE REAL EVENTS
    # ══════════════════════════════════════════════════════════════════

    # ── Scenario 1: Order placed ─────────────────────────────────────
    print_section("SCENARIO 1 — Customer places an order")
    order_svc.place_order(
        user_id   = 101,
        recipient = "hassan@example.com",
        order_id  = "ORD-5001",
    )

    # ── Scenario 2: Security alert ───────────────────────────────────
    print_section("SCENARIO 2 — Suspicious login detected")
    security_svc.detect_suspicious_login(
        user_id    = 101,
        recipient  = "hassan@example.com",
        ip_address = "192.168.99.1",
    )

    # ── Scenario 3: Password reset ───────────────────────────────────
    print_section("SCENARIO 3 — Password reset requested")
    security_svc.trigger_password_reset(
        user_id   = 102,
        recipient = "arham@example.com",
    )

    # ── Scenario 4: Promotional blast ────────────────────────────────
    print_section("SCENARIO 4 — Promotional blast to multiple users")
    promo_svc.send_promotion(
        recipients    = [
            "arham@example.com",
            "usman@example.com",
            "hassan@example.com",
        ],
        promo_message = "Flash Sale! 50% off — Today Only!",
    )

    # ── Scenario 5: Refund processed ────────────────────────────────
    print_section("SCENARIO 5 — Refund notification")
    promo_svc.send_refund_notification(
        recipient = "usman@example.com",
        amount    = 1200,
    )

    # ══════════════════════════════════════════════════════════════════
    # STEP 5 — STRATEGY RUNTIME SWAP
    # Demonstrates that a Notification object can switch channels
    # at runtime — impossible in the bad design.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 5 — Strategy Pattern: Runtime channel swap")

    print("\n  Creating Notification via Factory (Email)...")
    n = NotificationFactory.create_notification(
        "email", "demo@example.com", "Demo message")
    print(f"  Channel before swap : {n.get_channel()}")

    n.set_strategy(SMSStrategy())
    print(f"  Channel after swap  : {n.get_channel()}")

    n.set_strategy(WhatsAppStrategy())
    print(f"  Channel after swap  : {n.get_channel()}")

    n.set_strategy(PushStrategy())
    print(f"  Channel after swap  : {n.get_channel()}")

    print("\n  ✓ Same Notification object — three different channels.")
    print("  ✓ This is the Strategy pattern's runtime flexibility.")

    # ══════════════════════════════════════════════════════════════════
    # STEP 6 — FACTORY EXTENSIBILITY
    # Add a brand new channel (Slack) with 2 changes:
    # 1. Write the class  2. Call register_channel()
    # Zero existing files modified.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 6 — Factory Pattern: Adding a new channel (Slack)")

    class SlackStrategy(NotificationStrategy):
        """New channel — added with zero changes to existing code."""
        def send(self, recipient: str, message: str) -> bool:
            print(f"    [SLACK] Posting to workspace: {recipient}")
            print(f"    [SLACK] Message : {message}")
            print(f"    [SLACK] ✓ Posted successfully")
            return True
        def get_channel_name(self) -> str:
            return "Slack"

    NotificationFactory.register_channel("slack", SlackStrategy)
    print(f"\n  Available channels: "
          f"{NotificationFactory.get_available_channels()}")

    slack_n = NotificationFactory.create_notification(
        "slack", "#dev-alerts", "Build deployed to production.")
    slack_n.deliver()
    print("  ✓ Slack added with 0 changes to existing code (OCP).")

    # ══════════════════════════════════════════════════════════════════
    # STEP 7 — OBSERVER EXTENSIBILITY
    # Add a completely new event type with one line.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 7 — Observer Pattern: Adding a new event type")

    # One subscribe() call — no existing class edited
    event_system.subscribe("delivery_update",
                           NotificationObserver("sms",   manager))
    event_system.subscribe("delivery_update",
                           NotificationObserver("push",  manager))
    event_system.subscribe("delivery_update",
                           NotificationObserver("slack", manager))

    event_system.emit(Event(
        event_type = "delivery_update",
        recipient  = "hassan@example.com",
        message    = "Your package is out for delivery. ETA: 2 hours.",
    ))
    print("  ✓ New event type added with 3 subscribe() calls (OCP).")
    print("  ✓ Zero changes to OrderService, SecurityService, or any pattern.")

    # ══════════════════════════════════════════════════════════════════
    # STEP 8 — SINGLETON LOG + STATS
    # All notifications from all services logged to the same instance.
    # ══════════════════════════════════════════════════════════════════
    print_section("STEP 8 — Singleton Pattern: Centralized log & stats")
    manager.display_all_logs()

    # ══════════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ══════════════════════════════════════════════════════════════════
    print_section("SOLID PRINCIPLES VERIFIED")
    print("""
  ✓ SRP — Services contain zero notification code. Each class has one job.
  ✓ OCP — Added Slack channel + delivery_update event with zero class edits.
  ✓ LSP — All Strategy subclasses interchangeable via NotificationStrategy.
  ✓ DIP — Services depend on EventSystem (abstraction), not concrete channels.
  ✓ DRY — Each channel defined exactly once in its Strategy class.
    """)


if __name__ == "__main__":
    main()
