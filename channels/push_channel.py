# channels/push_channel.py

from patterns.strategy import NotificationStrategy


class PushStrategy(NotificationStrategy):
    """
    Concrete Strategy — Push notification via Firebase Cloud Messaging.
    In a real system, replace the print statements with
    the firebase-admin SDK: messaging.send(message)
    """

    def send(self, recipient: str, message: str) -> bool:
        print(f"    [PUSH]  Connecting to Firebase Cloud Messaging...")
        print(f"    [PUSH]  Device  : {recipient}")
        print(f"    [PUSH]  Payload : {message}")
        print(f"    [PUSH]  ✓ Delivered successfully")
        return True

    def get_channel_name(self) -> str:
        return "Push"
