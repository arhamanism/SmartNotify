# services/promotional_service.py

from models.event      import Event
from patterns.observer import EventSystem


class PromotionalService:
    """
    ✓ GOOD DESIGN: PromotionalService handles ONLY promotion logic.
    Zero notification code inside this class.
    Fires a 'promotional' event per recipient — observers handle delivery.

    Contrast with bad_design where this class had three copy-pasted
    channel blocks looped per user — a maintenance nightmare.
    """

    def __init__(self, event_system: EventSystem) -> None:
        self._event_system = event_system

    def send_promotion(self, recipients: list[str],
                       promo_message: str) -> None:
        """Send a promotional notification to a list of recipients."""
        print(f"\n[PromotionalService] Blasting to "
              f"{len(recipients)} recipients...")

        for recipient in recipients:
            self._event_system.emit(Event(
                event_type = "promotional",
                recipient  = recipient,
                message    = promo_message,
            ))

    def send_refund_notification(self, recipient: str,
                                  amount: float, currency: str = "Rs") -> None:
        """Fire a refund processed event."""
        print(f"\n[PromotionalService] Refund processed "
              f"for {recipient}")

        self._event_system.emit(Event(
            event_type = "refund_processed",
            recipient  = recipient,
            message    = (
                f"Your refund of {currency}.{amount:.0f} "
                f"has been processed and will reflect in 2-3 business days."
            ),
        ))
