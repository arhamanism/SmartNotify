# channels/whatsapp_channel.py

from patterns.strategy import NotificationStrategy


class WhatsAppStrategy(NotificationStrategy):
    """
    Concrete Strategy — WhatsApp Business API.

    ✓ OCP DEMONSTRATION:
    This entire new channel was added by:
      1. Creating THIS file  (new class — open for extension)
      2. Adding one entry to NotificationFactory._channel_map
    Zero changes to any existing service, observer, or pattern class.
    This is the Open/Closed Principle in action.

    In a real system, replace the print statements with the
    WhatsApp Business API (Meta Graph API) HTTP calls.
    """

    def send(self, recipient: str, message: str) -> bool:
        print(f"    [WA]    Connecting to WhatsApp Business API...")
        print(f"    [WA]    To      : {recipient}")
        print(f"    [WA]    Message : {message}")
        print(f"    [WA]    ✓ Delivered successfully")
        return True

    def get_channel_name(self) -> str:
        return "WhatsApp"
