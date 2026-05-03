# models/event.py

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """
    Immutable data object passed through the Observer system.
    Produced by business services, consumed by NotificationObserver.
    """
    event_type: str      # e.g. "order_placed", "security_alert"
    recipient:  str      # email / phone / device token
    message:    str      # notification body
    timestamp:  datetime = field(default_factory=datetime.now)
