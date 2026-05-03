# services/security_service.py

from models.event      import Event
from patterns.observer import EventSystem


class SecurityService:
    """
    ✓ GOOD DESIGN: SecurityService handles ONLY security logic.
    Zero notification code inside this class.
    Fires a 'security_alert' event — observers handle delivery.

    Contrast with bad_design where this class had copy-pasted
    Email and SMS blocks identical to OrderService.
    """

    def __init__(self, event_system: EventSystem) -> None:
        self._event_system = event_system

    def detect_suspicious_login(self, user_id: int, recipient: str,
                                 ip_address: str) -> None:
        """Detect suspicious login and fire a security alert event."""
        print(f"\n[SecurityService] Suspicious login from {ip_address} "
              f"for user {user_id}")

        self._event_system.emit(Event(
            event_type = "security_alert",
            recipient  = recipient,
            message    = (
                f"Suspicious login detected from IP {ip_address}. "
                f"Was this you? If not, reset your password immediately."
            ),
        ))

    def trigger_password_reset(self, user_id: int, recipient: str) -> None:
        """Fire a password reset event."""
        print(f"\n[SecurityService] Password reset requested "
              f"for user {user_id}")

        self._event_system.emit(Event(
            event_type = "password_reset",
            recipient  = recipient,
            message    = (
                "Your password reset link is ready. "
                "This link expires in 15 minutes."
            ),
        ))
