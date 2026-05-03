from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator

from models.event import Event
from patterns.factory import NotificationFactory
from patterns.observer import EventSystem, NotificationObserver
from patterns.singleton import NotificationManager
from patterns.strategy import NotificationStrategy
from services.order_service import OrderService
from services.promotional_service import PromotionalService
from services.security_service import SecurityService


CHANNEL_LABELS = {
    "Email": "email",
    "SMS": "sms",
    "Push": "push",
    "WhatsApp": "whatsapp",
}

DEFAULT_SUBSCRIPTIONS = {
    "order_placed": ["email", "sms"],
    "security_alert": ["email", "push"],
    "promotional": ["push", "whatsapp"],
    "password_reset": ["sms"],
    "refund_processed": ["email", "sms"],
}


class FireEventBody(BaseModel):
    event_type: str
    recipient: str
    message: str
    channels: list[str] = Field(default_factory=list)

    @field_validator("event_type", "recipient", "message")
    @classmethod
    def non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()


class OrderBody(BaseModel):
    user_id: int
    recipient: EmailStr
    order_id: str


class SecurityAlertBody(BaseModel):
    user_id: int
    recipient: EmailStr
    ip_address: str


class PasswordResetBody(BaseModel):
    user_id: int
    recipient: EmailStr


class PromotionalBody(BaseModel):
    recipients: list[EmailStr]
    message: str


class RefundBody(BaseModel):
    recipient: EmailStr
    amount: float
    currency: str = "Rs"


class SubscriptionBody(BaseModel):
    event_type: str
    channel: str


class ChannelRegisterBody(BaseModel):
    name: str


class MockDynamicStrategy(NotificationStrategy):
    def __init__(self, name: str) -> None:
        self._name = name

    def send(self, recipient: str, message: str) -> bool:
        print(f"[{self._name.upper()} MOCK] recipient={recipient} message={message}")
        return True

    def get_channel_name(self) -> str:
        return self._name.capitalize()


app = FastAPI(title="Smart Notification System API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = NotificationManager()
event_system = EventSystem()
order_svc = OrderService(event_system)
security_svc = SecurityService(event_system)
promo_svc = PromotionalService(event_system)
initialized_at = datetime.now().isoformat()
observer_registry: dict[str, dict[str, NotificationObserver]] = {}


def normalize_channel(name: str) -> str:
    return name.strip().lower()


def available_channels() -> list[str]:
    return NotificationFactory.get_available_channels()


def ensure_channel_exists(channel: str) -> str:
    key = normalize_channel(channel)
    if key not in available_channels():
        raise HTTPException(status_code=400, detail=f"Unsupported channel '{channel}'")
    return key


def add_subscription(event_type: str, channel: str) -> None:
    key = ensure_channel_exists(channel)
    event = event_type.strip()
    observer_registry.setdefault(event, {})
    if key in observer_registry[event]:
        return
    obs = NotificationObserver(key, manager)
    observer_registry[event][key] = obs
    event_system.subscribe(event, obs)


def remove_subscription(event_type: str, channel: str) -> None:
    event = event_type.strip()
    key = normalize_channel(channel)
    if event not in observer_registry or key not in observer_registry[event]:
        raise HTTPException(status_code=404, detail="Subscription not found")
    obs = observer_registry[event][key]
    event_system.unsubscribe(event, obs)
    del observer_registry[event][key]
    if not observer_registry[event]:
        del observer_registry[event]


def get_subscriptions_map() -> dict[str, list[str]]:
    return {
        event_type: list(channels.keys())
        for event_type, channels in observer_registry.items()
    }


def fire_raw_event(event_type: str, recipient: str, message: str, channels: list[str] | None = None) -> int:
    before = len(manager.get_logs())
    evt = Event(event_type=event_type, recipient=recipient, message=message)
    channels = channels or []
    if channels:
        temp_observers: list[NotificationObserver] = []
        try:
            for channel in channels:
                key = ensure_channel_exists(channel)
                obs = NotificationObserver(key, manager)
                temp_observers.append(obs)
                event_system.subscribe(event_type, obs)
            event_system.emit(evt)
        finally:
            for obs in temp_observers:
                event_system.unsubscribe(event_type, obs)
    else:
        event_system.emit(evt)
    after = len(manager.get_logs())
    return after - before


@app.on_event("startup")
def bootstrap() -> None:
    for event_type, channels in DEFAULT_SUBSCRIPTIONS.items():
        for channel in channels:
            add_subscription(event_type, channel)


@app.get("/api/stats")
def get_stats() -> dict[str, Any]:
    stats = manager.get_stats()
    return {
        **stats,
        "active_observers": sum(len(v) for v in observer_registry.values()),
        "available_channels": available_channels(),
    }


@app.get("/api/logs")
def get_logs() -> list[dict[str, Any]]:
    return manager.get_logs()


@app.get("/api/subscriptions")
def get_subscriptions() -> dict[str, list[str]]:
    return get_subscriptions_map()


@app.get("/api/channels")
def get_channels() -> list[str]:
    return available_channels()


@app.post("/api/events/fire")
def post_fire_event(body: FireEventBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    count = fire_raw_event(body.event_type, body.recipient, body.message, body.channels)
    logs = manager.get_logs()[before:]
    return {"success": True, "notifications_sent": count, "logs": logs}


@app.post("/api/events/order")
def post_order_event(body: OrderBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    order = order_svc.place_order(body.user_id, str(body.recipient), body.order_id)
    sent = len(manager.get_logs()) - before
    return {"success": True, "order": order, "notifications_sent": sent}


@app.post("/api/events/security-alert")
def post_security_event(body: SecurityAlertBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    security_svc.detect_suspicious_login(body.user_id, str(body.recipient), body.ip_address)
    sent = len(manager.get_logs()) - before
    return {"success": True, "notifications_sent": sent}


@app.post("/api/events/password-reset")
def post_password_reset(body: PasswordResetBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    security_svc.trigger_password_reset(body.user_id, str(body.recipient))
    sent = len(manager.get_logs()) - before
    return {"success": True, "notifications_sent": sent}


@app.post("/api/events/promotional")
def post_promotional(body: PromotionalBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    promo_svc.send_promotion([str(r) for r in body.recipients], body.message)
    sent = len(manager.get_logs()) - before
    return {"success": True, "notifications_sent": sent}


@app.post("/api/events/refund")
def post_refund(body: RefundBody) -> dict[str, Any]:
    before = len(manager.get_logs())
    promo_svc.send_refund_notification(str(body.recipient), body.amount, body.currency)
    sent = len(manager.get_logs()) - before
    return {"success": True, "notifications_sent": sent}


@app.post("/api/subscriptions/add")
def post_add_subscription(body: SubscriptionBody) -> dict[str, Any]:
    add_subscription(body.event_type, body.channel)
    return {"success": True, "subscriptions": get_subscriptions_map()}


@app.delete("/api/subscriptions/remove")
def delete_subscription(body: SubscriptionBody = Body(...)) -> dict[str, Any]:
    remove_subscription(body.event_type, body.channel)
    return {"success": True, "subscriptions": get_subscriptions_map()}


@app.post("/api/channels/register")
def register_channel(body: ChannelRegisterBody) -> dict[str, Any]:
    name = normalize_channel(body.name)
    if not name:
        raise HTTPException(status_code=400, detail="Channel name cannot be empty")

    strategy_name = name

    class DynamicStrategy(MockDynamicStrategy):
        def __init__(self) -> None:
            super().__init__(strategy_name)

    NotificationFactory.register_channel(name, DynamicStrategy)
    return {"success": True, "channels": available_channels()}


@app.get("/api/singleton/proof")
def singleton_proof() -> dict[str, Any]:
    manager1 = NotificationManager()
    manager2 = NotificationManager()
    return {
        "instance_id_1": hex(id(manager1)),
        "instance_id_2": hex(id(manager2)),
        "are_same": manager1 is manager2,
        "total_logs": len(manager.get_logs()),
        "initialized_at": initialized_at,
    }


@app.delete("/api/logs/clear")
def clear_logs() -> dict[str, bool]:
    manager._logs.clear()
    manager._total_sent = 0
    manager._total_failed = 0
    return {"success": True}
