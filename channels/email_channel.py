# channels/email_channel.py

from patterns.strategy import NotificationStrategy


class EmailStrategy(NotificationStrategy):
    """
    Concrete Strategy — Email delivery via SMTP.
    In a real system, replace the print statements with
    smtplib or an SDK like SendGrid / Mailgun.
    """

    def send(self, recipient: str, message: str) -> bool:
        print(f"    [EMAIL] Connecting to SMTP server...")
        print(f"    [EMAIL] To      : {recipient}")
        print(f"    [EMAIL] Body    : {message}")
        print(f"    [EMAIL] ✓ Delivered successfully")
        return True

    def get_channel_name(self) -> str:
        return "Email"
