# models/notification.py

from __future__ import annotations
from patterns.strategy import NotificationStrategy


class Notification:
    """
    Context class for the Strategy pattern.

    Holds a recipient, a message, and an active NotificationStrategy.
    Delegates actual delivery to whatever strategy is currently set.
    The strategy can be swapped at runtime via set_strategy().

    Usage:
        n = Notification("a@b.com", "Hello!", EmailStrategy())
        n.deliver()                   # delivers via Email

        n.set_strategy(SMSStrategy()) # swap channel at runtime
        n.deliver()                   # now delivers via SMS
    """

    def __init__(self, recipient: str, message: str,
                 strategy: NotificationStrategy):
        self.recipient  = recipient
        self.message    = message
        self._strategy  = strategy

    def set_strategy(self, strategy: NotificationStrategy) -> None:
        """Swap the delivery channel at runtime — impossible in bad design."""
        self._strategy = strategy

    def deliver(self) -> bool:
        """Delegate delivery to the active strategy."""
        return self._strategy.send(self.recipient, self.message)

    def get_channel(self) -> str:
        """Return the name of the currently active channel."""
        return self._strategy.get_channel_name()
