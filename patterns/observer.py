# patterns/observer.py

from __future__ import annotations
from abc import ABC, abstractmethod
from models.event        import Event
from patterns.factory    import NotificationFactory
from patterns.singleton  import NotificationManager


# ── Abstract Observer ────────────────────────────────────────────────

class Observer(ABC):
    """
    ═══════════════════════════════════════════════════════════════
    OBSERVER PATTERN — Abstract Observer
    ═══════════════════════════════════════════════════════════════
    Any class that wants to react to system events must implement
    this interface. The EventSystem calls update() automatically
    when a subscribed event is emitted.
    ═══════════════════════════════════════════════════════════════
    """

    @abstractmethod
    def update(self, event: Event) -> None:
        """Called automatically by EventSystem when an event fires."""
        pass


# ── Subject / Publisher ──────────────────────────────────────────────

class EventSystem:
    """
    ═══════════════════════════════════════════════════════════════
    OBSERVER PATTERN — Subject (Publisher)
    ═══════════════════════════════════════════════════════════════
    Maintains a registry of event_type → [Observer] mappings.
    When emit() is called, all registered observers are notified
    automatically — the emitting service knows nothing about channels.

    ✓ Adding a new event type: just call subscribe() once.
    ✓ Adding a new channel to an existing event: call subscribe() once.
    ✓ No if/else chains. No service class edits.
    ═══════════════════════════════════════════════════════════════
    """

    def __init__(self) -> None:
        # { "order_placed": [Observer, Observer], "security_alert": [...] }
        self._observers: dict[str, list[Observer]] = {}

    def subscribe(self, event_type: str, observer: Observer) -> None:
        """Register an observer for a specific event type."""
        self._observers.setdefault(event_type, []).append(observer)
        print(f"  [EventSystem] Subscribed  '{event_type}'"
              f"  →  {type(observer).__name__}"
              f"({observer.channel if hasattr(observer, 'channel') else ''})")

    def unsubscribe(self, event_type: str, observer: Observer) -> None:
        """Remove a specific observer from an event type."""
        if event_type in self._observers:
            try:
                self._observers[event_type].remove(observer)
            except ValueError:
                pass  # observer was not registered — ignore silently

    def emit(self, event: Event) -> None:
        """
        Fire an event. Every subscribed observer is notified.
        The caller (business service) has zero knowledge of channels.
        """
        observers = self._observers.get(event.event_type, [])
        if not observers:
            print(f"  [EventSystem] No observers registered "
                  f"for '{event.event_type}'")
            return
        print(f"\n  [EventSystem] '{event.event_type}' fired "
              f"→ dispatching to {len(observers)} observer(s)...")
        for obs in observers:
            obs.update(event)

    def get_subscriptions(self) -> dict[str, list[str]]:
        """Return a readable summary of all subscriptions."""
        return {
            evt: [
                f"{type(o).__name__}"
                f"({o.channel if hasattr(o, 'channel') else ''})"
                for o in obs_list
            ]
            for evt, obs_list in self._observers.items()
        }


# ── Concrete Observer ────────────────────────────────────────────────

class NotificationObserver(Observer):
    """
    ═══════════════════════════════════════════════════════════════
    OBSERVER PATTERN — Concrete Observer
    ═══════════════════════════════════════════════════════════════
    Bridges the four patterns together:
        Observer  →  Factory  →  Strategy  →  Singleton Manager

    Each instance handles ONE channel for ONE event type.
    Business services never reference this class directly —
    they only call event_system.emit(event).

    ✓ To add WhatsApp to "order_placed" events:
        event_system.subscribe(
            "order_placed",
            NotificationObserver("whatsapp", manager)
        )
    That one line is the ONLY change needed. No class edits.
    ═══════════════════════════════════════════════════════════════
    """

    def __init__(self, channel: str, manager: NotificationManager) -> None:
        self.channel = channel
        self.manager = manager   # Singleton — same instance everywhere

    def update(self, event: Event) -> None:
        """
        Triggered automatically by EventSystem.emit().

        Flow:
          1. Factory creates the correct Notification + Strategy
          2. Notification.deliver() calls Strategy.send()
          3. Singleton manager logs the result centrally
        """
        print(f"    [{self.channel.upper()} Observer] Handling "
              f"'{event.event_type}' for {event.recipient}...")
        try:
            # Factory Pattern: create correct Notification object
            notification = NotificationFactory.create_notification(
                channel   = self.channel,
                recipient = event.recipient,
                message   = event.message,
            )
            # Strategy Pattern: deliver via the injected strategy
            success = notification.deliver()

        except ValueError as exc:
            print(f"    [ERROR] Factory error: {exc}")
            success      = False
            notification = NotificationFactory.create_notification(
                "email", event.recipient, event.message
            )

        # Singleton Pattern: log centrally via the one shared manager
        self.manager.log(event, notification, success)
