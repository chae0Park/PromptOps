# 09. n8n Workflows

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | n8n Workflows |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the workflow automation architecture, node sequence, integrations, error handling, and execution strategy implemented using n8n. |

---

# 1. Purpose

This document defines how workflow automation is implemented using n8n.

The workflow coordinates communication between:

- Email service
- OpenAI API
- FastAPI backend
- PostgreSQL
- Slack
- Human review interface

The workflow engine orchestrates services but does **not** contain business logic.

---

# 2. Workflow Philosophy

The workflow automation follows three principles.

---

## WF-001 Orchestration Only

n8n coordinates services.

Business rules remain inside:

- FastAPI
- Python Pricing Engine

---

## WF-002 Fail Gracefully

Failures should pause or reroute workflows rather than silently failing.

Every failure should be logged.

---

## WF-003 Human-in-the-Loop

Automation stops whenever human review is required.

The workflow resumes only after approval.

---

# 3. High-Level Workflow

```text
Email Received
        │
        ▼
Trigger Workflow
        │
        ▼
OpenAI Extraction
        │
        ▼
Validation
        │
 ┌──────┴────────┐
 │               │
 ▼               ▼
Pass          Review Required
 │               │
 ▼               ▼
Pricing      Human Review
 │               │
 └──────┬────────┘
        ▼
Generate Email Draft
        │
        ▼
Slack Notification
        │
        ▼
Workflow Complete
```

The workflow represents the end-to-end lifecycle of a quotation request.

---

# 4. Primary Workflow

The MVP contains one primary workflow.

Workflow name:

```text
RFQ Processing Workflow
```

Responsibilities include:

- Receive RFQ
- Extract structured information
- Validate extracted data
- Calculate quotation
- Wait for approval
- Generate draft
- Notify operators
- Complete workflow

---

# 5. Trigger Node

Workflow begins when a new RFQ email is received.

Possible trigger nodes include:

- IMAP Email Trigger
- Gmail Trigger
- Webhook Trigger (future)

Output:

- Subject
- Sender
- Timestamp
- Email body
- Attachments (future)

The trigger creates a new workflow execution.
---

# 6. OpenAI Extraction Node

The workflow sends the received RFQ email to the OpenAI API for structured information extraction.

## Inputs

- Email subject
- Email body
- Customer email
- Additional metadata (future)

## Outputs

```json
{
  "customer_name": "",
  "company_name": "",
  "customer_email": "",
  "products": [],
  "delivery_date": "",
  "notes": ""
}
```

The node should return valid JSON only.

---

# 7. Validation Node

The validation node verifies the extracted information before pricing begins.

Validation includes:

- Required fields
- Product existence
- Quantity validation
- Email format
- Date format

Possible outcomes:

```text
Pass
```

or

```text
Fail
```

Failed validation immediately redirects the workflow to manual review.

---

# 8. Pricing Node

The pricing node calls the FastAPI backend.

The backend executes deterministic pricing logic.

n8n does **not** calculate prices.

### Request

```text
POST /quotations/calculate
```

### Response

```json
{
  "quotation_id": "...",
  "total": 1210
}
```

The pricing node simply forwards the response to the next stage.

---

# 9. Human Review Pause

Automation pauses until an operator reviews the quotation.

Workflow state:

```text
Waiting
```

The operator reviews:

- Customer information
- AI extraction
- Pricing
- Generated quotation

Possible outcomes:

```text
Approve
```

or

```text
Reject
```

Only approved quotations continue automatically.

---

# 10. Email Draft Node

After approval, n8n requests an AI-generated customer response.

Input includes:

- Customer information
- Approved quotation
- Product summary
- Pricing summary

Output:

```text
Professional quotation email draft
```

The generated draft remains editable before delivery.

---

# 11. Slack Notification Node

Slack receives notifications throughout the workflow.

Typical events:

- RFQ received
- Validation failed
- Review required
- Workflow completed
- Workflow failed

Example notification:

```text
RFQ-2026-014

Status:
Review Required

Customer:
Example Corp
```

Slack notifications improve operational visibility but do not affect workflow execution.
---

# 12. Database Persistence Node

After successful pricing and approval, the workflow persists the final quotation data.

The workflow stores:

- RFQ
- RFQ Items
- Quotation
- Approval Record
- Workflow History
- Audit Log

The database becomes the single source of truth.

---

# 13. Error Handling

Each workflow node should handle failures independently.

---

## Email Trigger Failure

Recovery:

- Log failure
- Retry according to configured policy
- Notify administrator if retries fail

---

## OpenAI Failure

Recovery:

- Retry request
- Log error
- If retries fail, move quotation to manual review

---

## Validation Failure

Recovery:

- Stop workflow
- Notify reviewer
- Await manual correction

---

## Pricing Failure

Recovery:

- Log pricing error
- Notify operator
- Pause workflow until pricing issue is resolved

---

## Database Failure

Recovery:

- Retry persistence
- Prevent workflow completion
- Log database error

---

## Slack Failure

Recovery:

- Log notification failure
- Continue workflow execution

Slack is treated as a non-critical integration.

---

# 14. Retry Strategy

Some nodes support automatic retries.

| Node | Retry |
|------|-------|
| Email Trigger | Yes |
| OpenAI | Yes |
| FastAPI | Yes |
| PostgreSQL | Yes |
| Slack | Yes (limited) |

Retries should use exponential backoff where practical.

Repeated failures should escalate to manual investigation.

---

# 15. Workflow Variables

Recommended workflow variables:

| Variable | Description |
|-----------|-------------|
| rfq_id | RFQ identifier |
| workflow_id | Workflow execution ID |
| quotation_id | Generated quotation |
| customer_email | Customer email |
| current_status | Workflow status |
| retry_count | Retry attempts |
| execution_time | Workflow duration |

These variables simplify debugging and workflow tracking.

---

# 16. Logging Strategy

Every node should generate structured logs.

Recommended log fields:

- Workflow ID
- Node Name
- Execution Time
- Status
- Error Message (if applicable)
- Timestamp

Example:

```text
Workflow: RFQ-2026-014

Node:
Pricing Engine

Status:
Success

Duration:
420 ms
```

Consistent logging improves troubleshooting and operational monitoring.
---

# 17. Workflow Execution States

Each workflow execution progresses through a predefined sequence of states.

```text
Started
    │
    ▼
Running
    │
 ┌──┴───────────────┐
 │                  │
 ▼                  ▼
Waiting        Failed
 │                  │
 ▼                  ▼
Completed     Retried
```

## State Definitions

| State | Description |
|--------|-------------|
| Started | Workflow execution created |
| Running | Active processing |
| Waiting | Human review required |
| Completed | Successfully finished |
| Failed | Error encountered |
| Retried | Restarted after failure |

Each state transition should be timestamped and recorded in the workflow history table.

---

# 18. Workflow Design Decisions

## WD-001 Visual Workflow

**Decision**

Use n8n's visual workflow editor.

**Reason**

- Easier maintenance
- Faster onboarding
- Clear execution flow
- Simplified debugging

---

## WD-002 Backend Owns Business Logic

**Decision**

Keep pricing and validation outside n8n.

**Reason**

Business rules require:

- Unit testing
- Version control
- Deterministic execution

These are better implemented in Python than visual workflow nodes.

---

## WD-003 Stateless Workflow

**Decision**

Do not store business state inside n8n.

**Reason**

Workflow state should always be recoverable from PostgreSQL.

This allows workflow retries without losing operational history.

---

## WD-004 Human Approval Pause

**Decision**

Pause workflow until explicit operator approval.

**Reason**

Critical business decisions require human verification.

Automation resumes only after approval is recorded.

---

## WD-005 Independent Integrations

**Decision**

Each external service communicates through isolated workflow nodes.

**Reason**

This simplifies:

- Testing
- Monitoring
- Error recovery
- Future replacement of individual services

---

# 19. Future Workflow Enhancements

Potential future workflows include:

- Automatic customer acknowledgment emails
- Vendor quotation requests
- Multi-stage approval workflows
- Escalation workflows for overdue reviews
- Scheduled reminder notifications
- Attachment processing (PDF, Excel)
- OCR integration for scanned RFQs
- Multi-language RFQ processing
- Analytics and reporting pipelines

These workflows can be added without modifying the primary RFQ Processing Workflow.

---

# 20. Conclusion

The n8n workflow architecture provides a reliable orchestration layer that coordinates the AI-powered RFQ Operations Platform.

By delegating language understanding to OpenAI, business logic to FastAPI and the Python Pricing Engine, persistence to PostgreSQL, and notifications to Slack, the workflow remains modular, maintainable, and easy to extend.

This separation of concerns enables rapid development while preserving deterministic business behavior and human oversight throughout the quotation process.

---

