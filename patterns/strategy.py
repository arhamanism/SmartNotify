# patterns/strategy.py

from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    """
    ═══════════════════════════════════════════════════════════════
    STRATEGY PATTERN — Abstract Strategy Interface
    ═══════════════════════════════════════════════════════════════
    Defines the contract every delivery channel must fulfill.
    All concrete channels (Email, SMS, Push, WhatsApp) implement
    this interface, making them fully interchangeable.

    Key benefit: Services and observers depend on THIS abstraction,
    never on concrete channel classes (Dependency Inversion Principle).
    ═══════════════════════════════════════════════════════════════
    """

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """
        Send a notification to recipient.
        Returns True on success, False on failure.
        """
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        """Return human-readable channel name e.g. 'Email', 'SMS'."""
        pass
