# patterns/factory.py

from channels.email_channel    import EmailStrategy
from channels.sms_channel      import SMSStrategy
from channels.push_channel     import PushStrategy
from channels.whatsapp_channel import WhatsAppStrategy
from models.notification       import Notification
from patterns.strategy         import NotificationStrategy


class NotificationFactory:
    """
    ═══════════════════════════════════════════════════════════════
    FACTORY PATTERN — Centralized Notification Object Creation
    ═══════════════════════════════════════════════════════════════
    Single creation point for all Notification objects.
    Callers pass a string channel name; Factory instantiates
    the correct Strategy and wraps it in a Notification.

    ✓ Adding a new channel (e.g. Slack):
        1. Create SlackStrategy(NotificationStrategy) in channels/
        2. Add  "slack": SlackStrategy  to _channel_map below
        → Zero changes to any service, observer, or other pattern.

    ✓ Without Factory every service would need its own if/else:
        if ch == "email": strategy = EmailStrategy()
        elif ch == "sms": strategy = SMSStrategy()
        ...
        Duplicated in every service — DRY and OCP both violated.
    ═══════════════════════════════════════════════════════════════
    """

    # ── Channel registry ─────────────────────────────────────────────
    # To add a new channel: append ONE entry here. Nothing else changes.
    _channel_map: dict[str, type] = {
        "email":    EmailStrategy,
        "sms":      SMSStrategy,
        "push":     PushStrategy,
        "whatsapp": WhatsAppStrategy,
    }

    # ── Public API ───────────────────────────────────────────────────

    @staticmethod
    def create_notification(channel: str,
                            recipient: str,
                            message: str) -> Notification:
        """
        Create and return a fully configured Notification object.

        Args:
            channel   : one of "email", "sms", "push", "whatsapp"
            recipient : destination address / phone / device token
            message   : notification body text

        Returns:
            Notification instance ready to call .deliver() on

        Raises:
            ValueError: if channel is not in _channel_map
        """
        key = channel.lower().strip()

        if key not in NotificationFactory._channel_map:
            available = list(NotificationFactory._channel_map.keys())
            raise ValueError(
                f"Unsupported channel '{channel}'. "
                f"Available channels: {available}"
            )

        strategy = NotificationFactory._channel_map[key]()
        return Notification(recipient, message, strategy)

    @staticmethod
    def get_available_channels() -> list[str]:
        """Return list of all registered channel names."""
        return list(NotificationFactory._channel_map.keys())

    @staticmethod
    def register_channel(name: str,
                         strategy_class: type[NotificationStrategy]) -> None:
        """
        Dynamically register a new channel at runtime.
        Supports plugin-style extensibility without modifying this file.

        Example:
            class SlackStrategy(NotificationStrategy): ...
            NotificationFactory.register_channel("slack", SlackStrategy)
        """
        NotificationFactory._channel_map[name.lower()] = strategy_class
        print(f"[Factory] Channel '{name}' registered dynamically.")
