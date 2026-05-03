# services/order_service.py

from models.event       import Event
from patterns.observer  import EventSystem


class OrderService:
    """
    ✓ GOOD DESIGN: OrderService handles ONLY order logic.
    Zero notification code inside this class.
    It fires an Event — the Observer system handles the rest.

    Contrast with bad_design/bad_implementation.py where this class
    contained hardcoded Email, SMS, and Push blocks.
    """

    def __init__(self, event_system: EventSystem) -> None:
        self._event_system = event_system

    def place_order(self, user_id: int, recipient: str,
                    order_id: str) -> dict:
        """Process an order and fire an event — no notification logic here."""
        print(f"\n[OrderService] Processing order #{order_id} "
              f"for user {user_id}")

        # Business logic only
        order = {
            "order_id": order_id,
            "user_id":  user_id,
            "status":   "confirmed",
        }

        # Fire event — observers decide which channels to use
        self._event_system.emit(Event(
            event_type = "order_placed",
            recipient  = recipient,
            message    = f"Your order #{order_id} has been confirmed!",
        ))

        return order
