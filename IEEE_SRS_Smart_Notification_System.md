# Software Requirements Specification (SRS)
## Smart Notification System Using Software Design Patterns

**Document Version:** 1.0  
**Prepared For:** SE Project Evaluation  
**Prepared By:** Arham Ali (23K-0637), Hassan Sheikh (23K-0830), Usman Khalid (23K-0516)  
**Date:** May 2026

---

## Revision History

| Version | Date | Description | Author(s) |
|---|---|---|---|
| 1.0 | May 2026 | Initial IEEE-format SRS | Project Group |

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the **Smart Notification System**. The system demonstrates how software design patterns improve maintainability, extensibility, and modularity in an event-driven notification architecture.

### 1.2 Scope
The Smart Notification System is an educational and functional prototype that:
- Triggers notifications based on events (order placement, security alert, promotional campaign, etc.).
- Delivers notifications using multiple channels (Email, SMS, Push, WhatsApp, and dynamically added channels).
- Demonstrates four core design patterns: **Strategy**, **Factory**, **Observer**, and **Singleton**.
- Provides a backend API and a frontend dashboard for real-time demonstration and evaluation.
- Maintains centralized notification logs and system statistics.

The system is intended for academic demonstration and architectural validation rather than production-scale deployment.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification  
- **API**: Application Programming Interface  
- **UI**: User Interface  
- **OCP**: Open/Closed Principle  
- **SRP**: Single Responsibility Principle  
- **DIP**: Dependency Inversion Principle  
- **Event**: A business action that may trigger notifications  
- **Channel**: Delivery medium for notifications (email, SMS, etc.)

### 1.4 References
- IEEE style SRS conventions (ISO/IEC/IEEE 29148 inspired structure)
- Project Proposal: *Smart Notification System Using Software Design Patterns*
- Project source code and test suite

### 1.5 Overview
This document describes:
- Overall product perspective and constraints
- Functional requirements and use cases
- External interfaces
- Non-functional requirements
- Verification criteria and acceptance conditions

---

## 2. Overall Description

### 2.1 Product Perspective
The product is a standalone educational software system with:
- **Backend**: Python FastAPI service implementing business logic and pattern-based notification flow.
- **Frontend**: React dashboard for interacting with APIs, firing events, and visualizing logs/stats.
- **In-memory runtime state**: Subscriptions, logs, and counters managed during process lifetime.

### 2.2 Product Functions
At a high level, the system shall:
1. Receive or generate business events.
2. Resolve interested observers for each event.
3. Create notification objects via factory logic.
4. Deliver messages using selected channel strategies.
5. Record each dispatch in centralized singleton logs.
6. Expose status through API and interactive UI.

### 2.3 User Classes and Characteristics
- **Project Evaluator/Teacher**
  - Needs clear demonstration of architecture and outcomes.
  - Uses frontend dashboard and/or API docs.
- **Student Developer**
  - Extends channels/events and validates design pattern behavior.
  - Uses codebase, tests, and demo UI.

### 2.4 Operating Environment
- OS: Windows 10/11 (project tested in Windows environment)
- Runtime: Python 3.x, Node.js + npm
- Backend Framework: FastAPI + Uvicorn
- Frontend Framework: React + Vite
- Browser: Modern Chromium/Firefox/Edge

### 2.5 Design and Implementation Constraints
- Educational prototype with emphasis on readability and pattern clarity.
- In-memory state (no persistent database requirement).
- Localhost API integration (`http://localhost:8000/api`) for demo environment.
- Modular architecture must preserve pattern boundaries.

### 2.6 Assumptions and Dependencies
- Python and npm are installed and accessible via terminal.
- Required Python/JS packages are installed before execution.
- Backend runs before frontend for complete functionality.
- Network access is available to `localhost` ports used by app.

---

## 3. External Interface Requirements

### 3.1 User Interfaces
The frontend dashboard provides:
- Sidebar navigation for key sections (Overview, Fire Events, Live Logs, pattern pages, comparison, tests).
- Header with guided demo trigger and progress indicator.
- Form-driven event firing and channel selection.
- Real-time log table with filtering and clear/reset controls.
- Pattern-specific pages explaining and validating architecture behavior.

### 3.2 Hardware Interfaces
No special hardware interfaces required.

### 3.3 Software Interfaces
- **Backend API (FastAPI)** provides JSON endpoints for:
  - Statistics retrieval
  - Logs retrieval and clearing
  - Event firing (generic and specific scenarios)
  - Subscription add/remove
  - Channel registration
  - Singleton verification proof
- **Frontend (React)** consumes backend endpoints through Axios client.

### 3.4 Communications Interfaces
- HTTP/1.1 over localhost:
  - Backend default: `localhost:8000`
  - Frontend default: `localhost:5173`

---

## 4. System Features and Functional Requirements

### 4.1 Feature: Event-Based Notification Triggering
**Description:** The system triggers notifications when business events are emitted.

**Functional Requirements:**
- **FR-1:** The system shall support predefined event types including `order_placed`, `security_alert`, `promotional`, `password_reset`, and `refund_processed`.
- **FR-2:** The system shall allow custom event firing with user-provided event type, recipient, message, and optional channels.
- **FR-3:** The system shall return number of notifications sent per event dispatch.

### 4.2 Feature: Multi-Channel Delivery (Strategy Pattern)
**Description:** Delivery behavior is abstracted by strategy interfaces and concrete channel implementations.

**Functional Requirements:**
- **FR-4:** The system shall provide built-in delivery strategies for Email, SMS, Push, and WhatsApp.
- **FR-5:** The system shall allow selecting one or more channels at runtime for a fired event.
- **FR-6:** The system shall support interchangeable channel behavior without changing service-layer code.

### 4.3 Feature: Notification Object Creation (Factory Pattern)
**Description:** Notification creation is centralized in a factory.

**Functional Requirements:**
- **FR-7:** The system shall create notification instances through a factory component.
- **FR-8:** The system shall support dynamic registration of new channels at runtime.
- **FR-9:** Newly registered channels shall become available for future event dispatch without modifying existing services.

### 4.4 Feature: Event Subscription and Dispatch (Observer Pattern)
**Description:** Observers subscribe to event types and are notified on event emission.

**Functional Requirements:**
- **FR-10:** The system shall maintain mappings of event types to subscribed channels/observers.
- **FR-11:** The system shall allow adding and removing subscriptions at runtime.
- **FR-12:** Emitting an event shall notify all currently subscribed observers for that event.

### 4.5 Feature: Centralized Manager and Logging (Singleton Pattern)
**Description:** A singleton manager maintains shared logs and counters.

**Functional Requirements:**
- **FR-13:** The system shall ensure a single shared notification manager instance is used application-wide.
- **FR-14:** The manager shall log each notification attempt with timestamp, event type, channel, recipient, message, and status.
- **FR-15:** The system shall expose aggregate counters (total, successful, failed notifications).
- **FR-16:** The system shall provide an endpoint that verifies singleton identity at runtime.

### 4.6 Feature: Demonstration Dashboard
**Description:** UI enables interactive understanding and evaluation.

**Functional Requirements:**
- **FR-17:** The dashboard shall display live statistics and recent activity.
- **FR-18:** The dashboard shall provide a guided demo workflow that triggers multiple sample scenarios.
- **FR-19:** The dashboard shall provide a searchable live logs view.
- **FR-20:** The dashboard shall include pages that explain pattern roles and system behavior.

### 4.7 Feature: Testing and Validation
**Description:** Unit and integration tests verify architecture and behavior.

**Functional Requirements:**
- **FR-21:** The system shall include unit tests for Strategy, Factory, Observer, and Singleton components.
- **FR-22:** The system shall include integration tests for end-to-end event-to-notification flow.
- **FR-23:** The test suite shall be executable through a single script command.

---

## 5. Non-Functional Requirements

### 5.1 Maintainability
- **NFR-1:** Code shall remain modular with clear separation between services, patterns, channels, and API/UI layers.
- **NFR-2:** Adding a new channel should not require modifications across multiple service classes.

### 5.2 Usability
- **NFR-3:** UI labels, controls, and pages shall be self-explanatory for academic demonstration.
- **NFR-4:** System should support demonstration flow without requiring code edits.

### 5.3 Reliability
- **NFR-5:** For valid inputs, API endpoints shall return deterministic JSON responses.
- **NFR-6:** Input validation errors shall be handled with explicit HTTP error messages.

### 5.4 Performance
- **NFR-7:** Typical API operations should complete within acceptable interactive latency in local demo conditions.
- **NFR-8:** UI polling intervals should keep logs/stats reasonably up to date without overloading local runtime.

### 5.5 Portability
- **NFR-9:** The system shall run in a standard Python + Node environment on common desktop OSs.

### 5.6 Security (Prototype Level)
- **NFR-10:** API input schemas shall validate required fields and types.
- **NFR-11:** CORS settings shall support local frontend-backend communication for demo use.

---

## 6. Logical Data Requirements

The system uses runtime in-memory structures:
- **Event**: `event_type`, `recipient`, `message`
- **Notification Log Entry**: `timestamp`, `event_type`, `channel`, `recipient`, `message`, `status`
- **Subscription Registry**: Mapping of `event_type -> channels/observers`
- **Stats**: Total sent, successful, failed, active observers, available channels

No persistent database schema is required for current scope.

---

## 7. Use Cases

### UC-1: Fire Standard Event
- **Actor:** Evaluator/Student
- **Precondition:** Backend is running
- **Main Flow:**
  1. User selects event data in UI.
  2. UI sends API request.
  3. Backend emits event and notifies subscribed channels.
  4. Logs and counters update.
- **Postcondition:** Notification attempts are recorded and visible in UI.

### UC-2: Register New Channel
- **Actor:** Student Developer
- **Precondition:** Backend running
- **Main Flow:**
  1. User enters channel name in Factory page.
  2. UI calls channel registration endpoint.
  3. Factory registers dynamic strategy.
  4. New channel appears in available channel list.
- **Postcondition:** New channel can be used in future dispatches.

### UC-3: Add/Remove Subscription
- **Actor:** Student Developer / Evaluator
- **Precondition:** Event and channel names available
- **Main Flow:**
  1. User submits event + channel pair.
  2. Backend updates observer registry.
  3. UI refreshes subscription view.
- **Postcondition:** Event routing reflects latest subscription mapping.

### UC-4: Validate Singleton Behavior
- **Actor:** Evaluator
- **Precondition:** Backend running
- **Main Flow:**
  1. User opens Singleton page.
  2. UI requests singleton proof endpoint.
  3. Backend returns instance identities and equality result.
- **Postcondition:** Singleton correctness can be shown as runtime evidence.

---

## 8. System Models (Textual)

### 8.1 Architectural View
- UI layer triggers API calls.
- API layer routes requests to services/pattern modules.
- Services emit business events.
- EventSystem dispatches to NotificationObservers.
- NotificationFactory creates Notification objects with selected strategy.
- NotificationManager (singleton) stores centralized logs and counters.

### 8.2 Pattern Responsibility Summary
- **Strategy:** Defines interchangeable channel delivery algorithms.
- **Factory:** Encapsulates notification object/channel creation.
- **Observer:** Decouples event producers from notification consumers.
- **Singleton:** Maintains a single source of truth for logs/statistics.

---

## 9. Verification and Acceptance Criteria

### 9.1 Functional Acceptance
The system is accepted when:
1. Core event flows execute successfully from UI and API.
2. Multiple channels can be used and logged correctly.
3. Subscriptions affect dispatch behavior as expected.
4. Singleton proof confirms single manager instance.
5. New channel registration works without service code modification.
6. Tests run and pass in local environment.

### 9.2 Non-Functional Acceptance
The system is accepted when:
1. UI is understandable for first-time evaluator usage.
2. Architecture remains modular and pattern-compliant.
3. Demonstration can be completed end-to-end in one session.

---

## 10. Future Enhancements (Out of Current Scope)
- Persistent database-backed logs and subscriptions
- Authentication and role-based access for APIs
- Retry queues and delivery acknowledgment tracking
- Real integrations for email/SMS/push providers
- Deployment-ready monitoring and CI/CD quality gates

---

## Appendix A: Setup and Execution Commands

### Backend
```bash
py -m pip install fastapi uvicorn "pydantic[email]"
py -m uvicorn api:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
python run_tests.py
python -m pytest tests/ -v
```

---

## Appendix B: Traceability Matrix (Proposal to Implementation)

| Proposal Item | Requirement IDs | Implementation Evidence |
|---|---|---|
| Event-based triggering | FR-1, FR-2, FR-3 | Event endpoints + services |
| Multiple channels | FR-4, FR-5 | Strategy channels + UI controls |
| Dynamic channel selection | FR-5, FR-8, FR-9 | Channel selection + registration |
| Notification logging | FR-14, FR-15 | Singleton manager logs/stats |
| Simple demonstration interface | FR-17, FR-18, FR-19, FR-20 | Guided frontend dashboard |
| Design pattern focus | FR-6, FR-7, FR-10, FR-13 | Pattern modules and pattern pages |

