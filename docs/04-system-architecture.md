# 04. System Architecture

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | System Architecture |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the overall system architecture, component responsibilities, data flow, and communication between services. |

---

# 1. Purpose

This document defines the technical architecture of the AI-powered RFQ Operations Platform.

The architecture is designed around the following principles:

- Separation of concerns
- Modular components
- Deterministic business logic
- Human-in-the-loop decision making
- AI-assisted automation
- Production-oriented scalability

This document serves as the foundation for backend implementation, infrastructure, deployment, and future system expansion.

---

# 2. Architectural Principles

The platform follows several architectural principles.

---

## AP-001 Modular Design

Each subsystem performs a single responsibility.

Major components include:

- Email ingestion
- Workflow orchestration
- AI extraction
- Validation
- Pricing engine
- Human review interface
- Notification service
- Database

Each module should be independently replaceable.

---

## AP-002 Human-Centered Automation

AI automates repetitive language tasks.

Business decisions remain under human control.

Every quotation requires operator approval before customer delivery.

---

## AP-003 Deterministic Business Logic

Business calculations must never depend on probabilistic AI output.

Examples include:

- Pricing
- Margin
- Discount
- Taxes
- Validation rules

These operations are implemented in Python.

---

## AP-004 Observable System

Every important action generates logs.

The platform should support:

- Workflow tracing
- Debugging
- Audit history
- Error diagnosis

---

## AP-005 Stateless Services

Backend services should remain stateless whenever possible.

Persistent information belongs in PostgreSQL rather than application memory.

---

# 3. High-Level Architecture

```text
                     Customer
                         │
                         ▼
                  RFQ Email Inbox
                         │
                         ▼
                     n8n Workflow
                         │
         ┌───────────────┴────────────────┐
         ▼                                ▼
 OpenAI Information Extraction      Validation Engine
         │                                │
         └───────────────┬────────────────┘
                         ▼
                Python Pricing Engine
                         │
                         ▼
                  PostgreSQL Database
                         │
          ┌──────────────┴───────────────┐
          ▼                              ▼
   Next.js Review UI             Slack Notification
          │
          ▼
    Human Approval
          │
          ▼
 AI Email Draft Generation
          │
          ▼
     Customer Response
```

The architecture separates AI responsibilities from deterministic software components.

---

# 4. Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | Next.js + TypeScript |
| Backend API | FastAPI |
| Workflow Automation | n8n |
| Database | PostgreSQL (Supabase) |
| AI Provider | OpenAI API |
| Business Logic | Python |
| Notifications | Slack |
| Hosting | Vercel |
| Backend Hosting | Render |
| Workflow Hosting | Docker |

Each technology is selected for simplicity, maintainability, and compatibility with modern cloud deployment.

---

# 5. System Components

## 5.1 Email Ingestion

Responsibilities:

- Receive RFQ emails
- Extract metadata
- Trigger workflow
- Store raw email

Inputs:

- Email
- Attachments

Outputs:

- Workflow trigger

---

## 5.2 Workflow Engine (n8n)

Responsibilities:

- Coordinate workflow execution
- Route data between services
- Handle retries
- Trigger notifications
- Record workflow status

The workflow engine contains no business logic.

---

## 5.3 AI Information Extraction Service

The AI service is responsible for converting unstructured customer communication into structured quotation data.

### Responsibilities

- Read customer email
- Understand natural language
- Extract structured RFQ information
- Normalize extracted values
- Produce structured JSON

### Input

- Email body
- Email subject
- Attachments (future support)

### Output

```json
{
  "customer_name": "",
  "company": "",
  "email": "",
  "products": [],
  "delivery_date": "",
  "notes": ""
}
```

### Notes

The AI service is **not** responsible for:

- Pricing
- Validation
- Business rules
- Approval decisions

---

## 5.4 Validation Engine

The validation engine verifies that extracted data satisfies predefined business rules before pricing begins.

### Responsibilities

- Required field validation
- Product validation
- Quantity validation
- Date validation
- Email validation

### Possible Results

- Passed
- Warning
- Failed

Failed validation immediately pauses workflow execution.

---

## 5.5 Pricing Engine

The pricing engine contains deterministic business logic implemented in Python.

### Responsibilities

- Product pricing
- Quantity calculation
- Discount calculation
- Margin calculation
- Final quotation generation

### Inputs

- Product list
- Quantities
- Pricing rules

### Outputs

- Unit prices
- Discounts
- Total quotation
- Margin

### Design Principle

Identical inputs must always produce identical outputs.

---

## 5.6 Database

PostgreSQL serves as the single source of truth for operational data.

### Responsibilities

- Store RFQs
- Store workflow history
- Store approvals
- Store pricing
- Store audit logs

The application should never rely on in-memory workflow state.

---

## 5.7 Frontend Application

The Next.js application provides the human review interface.

### Responsibilities

- Display quotations
- Display workflow status
- Edit extracted values
- Review pricing
- Approve or reject quotations
- View workflow history

The frontend performs presentation only.

Business logic remains in backend services.

---

## 5.8 Notification Service

Slack provides operational visibility.

### Responsibilities

- Notify workflow events
- Notify failures
- Notify review requests

Notifications do not affect quotation processing.

Workflow execution must continue even if Slack is unavailable.

---

# 6. Component Communication

The platform follows a request-response architecture between independent services.

```text
Email
   │
   ▼
n8n
   │
   ▼
OpenAI
   │
   ▼
Validation
   │
   ▼
Pricing Engine
   │
   ▼
Database
   │
   ▼
Frontend
```

Every service communicates through clearly defined interfaces.

No component accesses another component's internal implementation directly.

---

# 7. Data Flow

The quotation data flows through the system in a predictable sequence.

```text
Customer Email
      │
      ▼
Raw Email
      │
      ▼
Structured Extraction
      │
      ▼
Validated Data
      │
      ▼
Calculated Pricing
      │
      ▼
Human Approval
      │
      ▼
Final Quotation
      │
      ▼
Persistent Storage
```

Each transformation stage produces a new representation of the quotation rather than modifying previous records.

---

# 8. Service Responsibilities

To ensure maintainability, each service owns a clearly defined responsibility.

| Component | Primary Responsibility | Owns Business Logic |
|------------|------------------------|---------------------|
| Email Service | Receive RFQ emails | No |
| n8n | Workflow orchestration | No |
| OpenAI | Language understanding | No |
| Validation Engine | Data validation | Yes |
| Pricing Engine | Pricing calculations | Yes |
| PostgreSQL | Data persistence | No |
| Next.js | User interface | No |
| Slack | Notifications | No |

Only the Validation Engine and Pricing Engine contain business rules.

---

# 9. Sequence Diagram

The following sequence illustrates the complete interaction between services.

```text
Customer
    │
    ▼
Email Service
    │
    ▼
n8n Workflow
    │
    ├──────────────► OpenAI
    │                    │
    │◄───────────────────┘
    │
    ├──────────────► Validation
    │                    │
    │◄───────────────────┘
    │
    ├──────────────► Pricing Engine
    │                    │
    │◄───────────────────┘
    │
    ├──────────────► PostgreSQL
    │
    ▼
Next.js Review
    │
Human Approval
    │
    ▼
OpenAI Email Draft
    │
    ▼
Slack Notification
    │
    ▼
Workflow Complete
```

Each interaction is logged and associated with a unique workflow identifier.

---

# 10. Error Handling Architecture

The platform is designed to isolate failures whenever possible.

## AI Failure

If AI extraction fails:

- Log the error.
- Retry according to workflow policy.
- If retries fail, send the quotation for manual review.

---

## Validation Failure

If validation fails:

- Stop pricing execution.
- Notify reviewers.
- Await manual correction.

---

## Pricing Failure

If pricing fails:

- Stop workflow.
- Preserve extracted data.
- Notify operators.

---

## Database Failure

If persistence fails:

- Retry database operation.
- Log failure.
- Prevent workflow completion until persistence succeeds.

---

## Notification Failure

Slack notification failures do not block workflow completion.

The failure is logged for later investigation.

---

# 11. Security Considerations

Although authentication is outside the MVP scope, the architecture is designed to support secure deployment.

Security considerations include:

- Environment variables for secrets.
- Secure API key storage.
- HTTPS communication.
- Server-side API execution.
- Principle of least privilege for database access.
- Audit logging of operational events.

No sensitive credentials should be stored in source code.

---

# 12. Scalability Considerations

The architecture should support future growth without major redesign.

Potential scaling strategies include:

- Independent API scaling
- Separate workflow workers
- Queue-based processing
- Database indexing
- Read replicas
- Caching for reference data
- Horizontal frontend scaling

The modular architecture enables individual services to scale independently as demand increases.

---

# 13. Deployment Architecture

The MVP is designed for cloud-native deployment using managed services.

```text
                    Internet
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
   Customer Email                  Web Browser
        │                               │
        ▼                               ▼
      n8n                         Next.js (Vercel)
        │                               │
        ├───────────────┬───────────────┤
        ▼               ▼               ▼
   OpenAI API      FastAPI (Render)   PostgreSQL
                        │
                        ▼
                 Pricing Engine
                        │
                        ▼
                     Slack API
```

Each service is independently deployable and communicates over secure HTTP APIs.

---

# 14. Architectural Decisions

The following architectural decisions guide the implementation of the platform.

## AD-001 Workflow Orchestration

**Decision:** Use n8n as the workflow orchestrator.

**Reason:**

- Visual workflow management
- Easy integration with external services
- Low operational overhead
- Rapid iteration during MVP development

---

## AD-002 AI Integration

**Decision:** Use the OpenAI API for natural language processing.

**Reason:**

- High-quality language understanding
- Structured JSON extraction
- Email draft generation
- Minimal custom NLP development

---

## AD-003 Deterministic Pricing

**Decision:** Keep all pricing logic in Python.

**Reason:**

- Reproducible results
- Easier testing
- Transparent business rules
- Regulatory and operational reliability

---

## AD-004 Relational Database

**Decision:** Use PostgreSQL as the primary datastore.

**Reason:**

- Strong transactional guarantees
- Structured relational data
- Mature tooling
- Excellent compatibility with FastAPI and Supabase

---

## AD-005 Frontend Framework

**Decision:** Use Next.js with TypeScript.

**Reason:**

- Strong developer experience
- Component-based architecture
- Server-side rendering support
- Excellent deployment experience with Vercel

---

# 15. Design Trade-offs

Every architecture involves trade-offs.

| Decision | Benefit | Trade-off |
|----------|---------|-----------|
| Human approval required | High reliability | Slower than full automation |
| Deterministic pricing | Explainable calculations | Less flexible than AI-generated pricing |
| n8n orchestration | Rapid development | Additional infrastructure component |
| Modular services | Easier maintenance | Increased integration complexity |
| PostgreSQL | Strong consistency | Requires schema management |

These trade-offs intentionally prioritize correctness and maintainability over maximum automation.

---

# 16. Architecture Summary

The architecture is based on a clear separation of responsibilities:

- **OpenAI** handles language understanding and content generation.
- **FastAPI** exposes application services and coordinates backend logic.
- **Python** implements deterministic pricing and validation rules.
- **n8n** orchestrates workflow execution across services.
- **PostgreSQL** persists operational data and workflow history.
- **Next.js** provides the operator-facing review interface.
- **Slack** delivers operational notifications.

This layered design ensures that AI capabilities enhance operational efficiency without replacing deterministic software engineering or human decision-making.

---

# 17. Conclusion

The AI-powered RFQ Operations Platform adopts a modular, production-oriented architecture that balances automation, transparency, and reliability.

By separating AI-assisted language tasks from deterministic business logic and requiring human approval for all business-critical decisions, the system provides a scalable foundation for quotation operations while remaining extensible for future enhancements.

This architecture forms the technical baseline for the database schema, API design, frontend implementation, workflow automation, testing strategy, and deployment configuration described in the remaining project documentation.

---

