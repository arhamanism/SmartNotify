# FastAPI + React Frontend Run Guide

Terminal 1 (backend):

```bash
cd smart_notification_system
pip install fastapi uvicorn
uvicorn api:app --reload --port 8000
```

Terminal 2 (frontend):

```bash
cd smart_notification_system/frontend
npm install
npm run dev
```

Frontend opens at `http://localhost:5173`.

# Smart Notification System
### SE Project — Design Pattern Implementation
**Group Members:** Arham Ali (23K-0637) · Hassan Sheikh (23K-0830) · Usman Khalid (23K-0516)

---

## Project Structure

```
smart_notification_system/
│
├── patterns/                   ← All 4 design patterns
│   ├── strategy.py             # Abstract Strategy interface
│   ├── singleton.py            # NotificationManager (Singleton)
│   ├── factory.py              # NotificationFactory (Factory)
│   └── observer.py             # Observer + EventSystem + NotificationObserver
│
├── channels/                   ← Concrete Strategy implementations
│   ├── email_channel.py        # EmailStrategy
│   ├── sms_channel.py          # SMSStrategy
│   ├── push_channel.py         # PushStrategy
│   └── whatsapp_channel.py     # WhatsAppStrategy
│
├── models/                     ← Data models
│   ├── event.py                # Event dataclass
│   └── notification.py         # Notification (Strategy context)
│
├── services/                   ← Clean business services (no notification code)
│   ├── order_service.py        # OrderService
│   ├── security_service.py     # SecurityService
│   └── promotional_service.py  # PromotionalService
│
├── logger/
│   └── notification_logger.py  # File-based logger
│
├── bad_design/
│   └── bad_implementation.py   # Tightly coupled anti-pattern version
│
├── tests/
│   ├── test_singleton.py       # Singleton unit tests
│   ├── test_factory.py         # Factory unit tests
│   ├── test_strategy.py        # Strategy unit tests
│   ├── test_observer.py        # Observer unit tests
│   └── test_integration.py     # End-to-end integration tests
│
├── main.py                     # Good design demo entry point
├── run_bad_design.py           # Bad design demo entry point
└── run_tests.py                # Run all tests
```

---

## How to Run

### Good Design (all 4 patterns)
```bash
python main.py
```

### Bad Design (anti-pattern comparison)
```bash
python run_bad_design.py
```

### All Tests
```bash
python run_tests.py
```

### Individual test files
```bash
python -m pytest tests/ -v
```

---

## Design Patterns Implemented

| Pattern   | Class                  | File                      | Purpose                                         |
|-----------|------------------------|---------------------------|-------------------------------------------------|
| Strategy  | `NotificationStrategy` | `patterns/strategy.py`    | Interchangeable delivery channels               |
| Singleton | `NotificationManager`  | `patterns/singleton.py`   | One central log, one manager instance           |
| Factory   | `NotificationFactory`  | `patterns/factory.py`     | Centralized Notification object creation        |
| Observer  | `EventSystem`          | `patterns/observer.py`    | Decouple event producers from consumers         |

---

## SOLID Principles

| Principle | How it is satisfied                                                   |
|-----------|-----------------------------------------------------------------------|
| SRP       | Services contain zero notification code — each class has one job     |
| OCP       | New channels and event types added without editing existing classes  |
| LSP       | All Strategy subclasses interchangeable via abstract base class      |
| DIP       | Services depend on EventSystem (abstraction), not concrete channels  |
| DRY       | Each channel defined exactly once in its Strategy class              |

---

## Before vs After Comparison

| Concern              | Bad Design                                      | Good Design (Patterns)                    |
|----------------------|-------------------------------------------------|-------------------------------------------|
| Add WhatsApp channel | Edit 3+ service classes (15+ changes)           | 1 new class + 1 dict entry (2 changes)    |
| Notification logic   | Hardcoded in every service (SRP violated)       | Isolated in Strategy + Observer           |
| Central logging      | 3 separate isolated lists                       | 1 Singleton manager — full system view   |
| Code duplication     | Email/SMS/Push blocks copy-pasted everywhere    | Each channel defined once, reused via DI  |
| Runtime channel swap | Impossible — boolean flags                      | `notification.set_strategy(SMSStrategy())` |
| Unit testing         | Must run full service to test notification code | Each pattern testable in complete isolation |
