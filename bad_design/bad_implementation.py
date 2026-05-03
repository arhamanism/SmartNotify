# bad_design/bad_implementation.py
"""
╔══════════════════════════════════════════════════════════════════════╗
║         BAD IMPLEMENTATION — NO DESIGN PATTERNS                     ║
║         Smart Notification System (Poorly Designed)                 ║
║                                                                      ║
║  Violations:                                                         ║
║    ❌ DRY  — channel logic copy-pasted in every service             ║
║    ❌ SRP  — business logic + notification logic mixed               ║
║    ❌ OCP  — adding WhatsApp requires editing 3+ classes             ║
║    ❌ DIP  — services depend on concrete channel steps directly      ║
║    ❌ No central log — system-wide stats impossible                  ║
║    ❌ No runtime channel switching                                   ║
║    ❌ Untestable notification logic                                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import datetime


# ─────────────────────────────────────────────────────────────────────
# SERVICE 1: OrderService
# ❌ Handles orders AND sends notifications in the same class
# ─────────────────────────────────────────────────────────────────────

class OrderService:
    """
    ❌ BAD: This class violates Single Responsibility Principle.
    It manages order business logic AND contains hardcoded notification
    delivery code for every channel.

    Adding any new channel means opening this file and editing it —
    violating the Open/Closed Principle.
    """

    def __init__(self):
        # ❌ Each service has its own isolated log — no system-wide view
        self.notification_log = []

    def place_order(self, user_id, user_email, user_phone, order_id,
                    notify_email=True, notify_sms=False, notify_push=False):

        print(f"\n[OrderService] Processing order #{order_id} "
              f"for user {user_id}")

        message = f"Your order #{order_id} has been confirmed!"

        # ❌ Email logic hardcoded directly inside business method
        if notify_email:
            print(f"  [EMAIL] Connecting to SMTP server...")
            print(f"  [EMAIL] To      : {user_email}")
            print(f"  [EMAIL] Subject : Order Confirmation")
            print(f"  [EMAIL] Body    : {message}")
            print(f"  [EMAIL] Sent successfully!")
            self.notification_log.append({
                "type": "email", "to": user_email,
                "message": message, "status": "SENT",
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            })

        # ❌ SMS logic copy-pasted — identical structure to email block
        if notify_sms:
            print(f"  [SMS]   Connecting to Twilio API...")
            print(f"  [SMS]   To      : {user_phone}")
            print(f"  [SMS]   Message : {message}")
            print(f"  [SMS]   Sent successfully!")
            self.notification_log.append({
                "type": "sms", "to": user_phone,
                "message": message, "status": "SENT",
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            })

        # ❌ Push logic also duplicated inline
        if notify_push:
            print(f"  [PUSH]  Connecting to Firebase...")
            print(f"  [PUSH]  Device  : user_{user_id}_token")
            print(f"  [PUSH]  Payload : {message}")
            print(f"  [PUSH]  Sent successfully!")
            self.notification_log.append({
                "type": "push", "to": f"user_{user_id}_token",
                "message": message, "status": "SENT",
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            })

        return {"order_id": order_id, "status": "confirmed"}


# ─────────────────────────────────────────────────────────────────────
# SERVICE 2: SecurityService
# ❌ Complete copy of all notification channel logic from OrderService
# ─────────────────────────────────────────────────────────────────────

class SecurityService:
    """
    ❌ BAD: Has its own full copy of Email, SMS, and Push logic.
    If the SMTP provider changes, you must edit BOTH OrderService
    AND SecurityService AND every other service that exists.
    That is O(n services) changes for a single channel update.
    """

    def __init__(self):
        # ❌ Another completely separate log — disconnected from OrderService
        self.alert_log = []

    def detect_suspicious_login(self, user_id, user_email, user_phone,
                                 ip_address,
                                 notify_email=True,
                                 notify_sms=True,
                                 notify_push=False):

        print(f"\n[SecurityService] Suspicious login detected from "
              f"{ip_address} for user {user_id}")

        message = (f"Alert: Suspicious login from IP {ip_address}. "
                   f"Was this you?")

        # ❌ EXACT SAME EMAIL CODE as OrderService — copy-pasted verbatim
        if notify_email:
            print(f"  [EMAIL] Connecting to SMTP server...")
            print(f"  [EMAIL] To      : {user_email}")
            print(f"  [EMAIL] Subject : Security Alert")
            print(f"  [EMAIL] Body    : {message}")
            print(f"  [EMAIL] Sent successfully!")
            self.alert_log.append({
                "type": "email", "to": user_email,
                "message": message, "status": "SENT",
            })

        # ❌ EXACT SAME SMS CODE as OrderService — copy-pasted verbatim
        if notify_sms:
            print(f"  [SMS]   Connecting to Twilio API...")
            print(f"  [SMS]   To      : {user_phone}")
            print(f"  [SMS]   Message : {message}")
            print(f"  [SMS]   Sent successfully!")
            self.alert_log.append({
                "type": "sms", "to": user_phone,
                "message": message, "status": "SENT",
            })

        # ❌ EXACT SAME PUSH CODE as OrderService — copy-pasted verbatim
        if notify_push:
            print(f"  [PUSH]  Connecting to Firebase...")
            print(f"  [PUSH]  Device  : user_{user_id}_token")
            print(f"  [PUSH]  Payload : {message}")
            print(f"  [PUSH]  Sent successfully!")
            self.alert_log.append({
                "type": "push", "to": f"user_{user_id}_token",
                "message": message, "status": "SENT",
            })

    def trigger_password_reset(self, user_id, user_email, user_phone,
                                notify_email=True, notify_sms=True):

        print(f"\n[SecurityService] Password reset for user {user_id}")
        message = ("Your password reset link is ready. "
                   "This link expires in 15 minutes.")

        # ❌ Yet again — same Email code for the third time in this class
        if notify_email:
            print(f"  [EMAIL] Connecting to SMTP server...")
            print(f"  [EMAIL] To      : {user_email}")
            print(f"  [EMAIL] Subject : Password Reset")
            print(f"  [EMAIL] Body    : {message}")
            print(f"  [EMAIL] Sent successfully!")

        # ❌ Yet again — same SMS code for the third time in this class
        if notify_sms:
            print(f"  [SMS]   Connecting to Twilio API...")
            print(f"  [SMS]   To      : {user_phone}")
            print(f"  [SMS]   Message : {message}")
            print(f"  [SMS]   Sent successfully!")


# ─────────────────────────────────────────────────────────────────────
# SERVICE 3: PromotionalService
# ❌ Third service, third complete copy of all channel logic
# ─────────────────────────────────────────────────────────────────────

class PromotionalService:
    """
    ❌ BAD: Third service, third full copy of notification code.

    ❌ To add WhatsApp right now, you must:
        1. Edit OrderService       → add notify_whatsapp param + block
        2. Edit SecurityService    → add notify_whatsapp param + block
        3. Edit THIS class         → add notify_whatsapp param + block
        4. Update every single caller of these three classes
    That is 15+ code changes for ONE new channel.

    With the good design: create 1 class + add 1 dict entry. Done.
    """

    def __init__(self):
        self.promo_log = []

    def send_promotion(self, users: list, promo_message: str,
                       notify_email=False,
                       notify_sms=False,
                       notify_push=True):

        print(f"\n[PromotionalService] Blasting to {len(users)} users...")

        for user in users:
            # ❌ All three channel blocks duplicated inside this loop
            if notify_email:
                print(f"  [EMAIL] Connecting to SMTP server...")
                print(f"  [EMAIL] To      : {user['email']}")
                print(f"  [EMAIL] Subject : Special Offer!")
                print(f"  [EMAIL] Body    : {promo_message}")
                print(f"  [EMAIL] Sent successfully!")
                self.promo_log.append({
                    "type": "email", "to": user["email"],
                    "message": promo_message, "status": "SENT",
                })

            if notify_sms:
                print(f"  [SMS]   Connecting to Twilio API...")
                print(f"  [SMS]   To      : {user['phone']}")
                print(f"  [SMS]   Message : {promo_message}")
                print(f"  [SMS]   Sent successfully!")
                self.promo_log.append({
                    "type": "sms", "to": user["phone"],
                    "message": promo_message, "status": "SENT",
                })

            if notify_push:
                print(f"  [PUSH]  Connecting to Firebase...")
                print(f"  [PUSH]  Device  : {user['device_token']}")
                print(f"  [PUSH]  Payload : {promo_message}")
                print(f"  [PUSH]  Sent successfully!")
                self.promo_log.append({
                    "type": "push", "to": user["device_token"],
                    "message": promo_message, "status": "SENT",
                })

    def send_refund_notification(self, user_email, user_phone,
                                  amount, currency="Rs",
                                  notify_email=True, notify_sms=True):

        print(f"\n[PromotionalService] Refund notification for {user_email}")
        message = (f"Your refund of {currency}.{amount:.0f} has been "
                   f"processed and will reflect in 2-3 business days.")

        # ❌ Same email block — copy number 6 across the codebase
        if notify_email:
            print(f"  [EMAIL] Connecting to SMTP server...")
            print(f"  [EMAIL] To      : {user_email}")
            print(f"  [EMAIL] Subject : Refund Processed")
            print(f"  [EMAIL] Body    : {message}")
            print(f"  [EMAIL] Sent successfully!")

        # ❌ Same SMS block — copy number 6 across the codebase
        if notify_sms:
            print(f"  [SMS]   Connecting to Twilio API...")
            print(f"  [SMS]   To      : {user_phone}")
            print(f"  [SMS]   Message : {message}")
            print(f"  [SMS]   Sent successfully!")


# ─────────────────────────────────────────────────────────────────────
# DEMO RUNNER
# ─────────────────────────────────────────────────────────────────────

def run_bad_demo():
    print("=" * 70)
    print("  BAD DESIGN — TIGHTLY COUPLED NOTIFICATION SYSTEM")
    print("=" * 70)

    # Three completely independent service objects — no shared infrastructure
    order_svc    = OrderService()
    security_svc = SecurityService()
    promo_svc    = PromotionalService()

    # Scenario 1 — Order placed: Email + SMS
    order_svc.place_order(
        user_id      = 101,
        user_email   = "hassan@example.com",
        user_phone   = "+92-300-1234567",
        order_id     = "ORD-5001",
        notify_email = True,
        notify_sms   = True,
    )

    # Scenario 2 — Security alert: Email + SMS
    security_svc.detect_suspicious_login(
        user_id    = 101,
        user_email = "hassan@example.com",
        user_phone = "+92-300-1234567",
        ip_address = "192.168.99.1",
    )

    # Scenario 3 — Password reset: Email + SMS
    security_svc.trigger_password_reset(
        user_id    = 101,
        user_email = "hassan@example.com",
        user_phone = "+92-300-1234567",
    )

    # Scenario 4 — Promotional blast: Push only
    users = [
        {"email": "arham@example.com",
         "phone": "+92-300-0000001",
         "device_token": "tok_A"},
        {"email": "usman@example.com",
         "phone": "+92-300-0000002",
         "device_token": "tok_B"},
    ]
    promo_svc.send_promotion(
        users         = users,
        promo_message = "Flash Sale! 50% off — Today Only!",
        notify_push   = True,
    )

    # Scenario 5 — Refund notification
    promo_svc.send_refund_notification(
        user_email = "arham@example.com",
        user_phone = "+92-300-0000001",
        amount     = 1200,
    )

    # Show the broken logging situation
    print("\n" + "=" * 70)
    print("  BROKEN LOGGING — Three completely disconnected logs:")
    print("=" * 70)
    print(f"  order_svc.notification_log    : "
          f"{len(order_svc.notification_log)} entries")
    print(f"  security_svc.alert_log        : "
          f"{len(security_svc.alert_log)} entries")
    print(f"  promo_svc.promo_log           : "
          f"{len(promo_svc.promo_log)} entries")
    total = (len(order_svc.notification_log) +
             len(security_svc.alert_log) +
             len(promo_svc.promo_log))
    print(f"\n  Total across system           : {total} entries")
    print(f"  BUT there is no single place to query them all!")
    print(f"  Adding a 4th service = a 4th orphaned log list.")

    print("\n" + "=" * 70)
    print("  COST OF ADDING WHATSAPP TO THIS SYSTEM:")
    print("=" * 70)
    changes = [
        ("OrderService.place_order()",
         "add notify_whatsapp param + full WhatsApp block"),
        ("SecurityService.detect_suspicious_login()",
         "add notify_whatsapp param + full WhatsApp block"),
        ("SecurityService.trigger_password_reset()",
         "add notify_whatsapp param + full WhatsApp block"),
        ("PromotionalService.send_promotion()",
         "add notify_whatsapp param + full WhatsApp block"),
        ("PromotionalService.send_refund_notification()",
         "add notify_whatsapp param + full WhatsApp block"),
        ("Every caller of these methods",
         "update every function call to pass notify_whatsapp"),
    ]
    for i, (location, change) in enumerate(changes, 1):
        print(f"  {i}. {location}")
        print(f"     → {change}")

    print(f"\n  Total changes: {len(changes)}+ edits for 1 new channel.")
    print(f"  With good design (patterns): 2 changes total.")
    print("=" * 70)


if __name__ == "__main__":
    run_bad_demo()
