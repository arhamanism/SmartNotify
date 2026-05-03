# channels/sms_channel.py

from patterns.strategy import NotificationStrategy


class SMSStrategy(NotificationStrategy):
    """
    Concrete Strategy — SMS delivery via Twilio.
    In a real system, replace the print statements with
    the twilio-python SDK: client.messages.create(...)
    """

    def send(self, recipient: str, message: str) -> bool:
        print(f"    [SMS]   Connecting to Twilio API...")
        print(f"    [SMS]   To      : {recipient}")
        print(f"    [SMS]   Message : {message}")
        print(f"    [SMS]   ✓ Delivered successfully")
        return True

    def get_channel_name(self) -> str:
        return "SMS"
