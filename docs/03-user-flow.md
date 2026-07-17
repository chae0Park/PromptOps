# 03. User Flow

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | User Flow |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the end-to-end user journey, workflow states, decision points, and user interactions throughout the quotation process. |

---

# 1. Purpose

This document describes how users interact with the AI-powered RFQ Operations Platform from the moment an RFQ email is received until the quotation process is completed.

The objective is to provide a clear operational workflow that connects business processes with the technical implementation described in the architecture and API specifications.

---

# 2. Primary Workflow

The MVP supports one primary operational workflow.

```text
Customer
    │
    ▼
Send RFQ Email
    │
    ▼
Email Received
    │
    ▼
LLM Information Extraction
    │
    ▼
Validation
    │
    ▼
Pricing Engine
    │
    ▼
Human Review
    │
 ┌──┴─────────────┐
 │                │
 ▼                ▼
Reject         Approve
 │                │
 ▼                ▼
Correction   Email Draft
 │                │
 └──────┬─────────┘
        ▼
 Store Results
        │
        ▼
Workflow Complete
```

---

# 3. User Roles

## Customer

Responsibilities:

- Send quotation request
- Receive quotation response

Customers never access the platform directly.

---

## Operations Specialist

Responsibilities:

- Review extracted information
- Verify pricing
- Edit quotation details
- Approve quotations
- Reject quotations when necessary

---

## Administrator

Responsibilities:

- Maintain workflow configuration
- Manage pricing rules
- Review logs
- Monitor workflow execution

---

# 4. Workflow States

Each quotation progresses through predefined workflow states.

| State | Description |
|--------|-------------|
| Received | RFQ email received |
| Extracting | AI extraction in progress |
| Validating | Business validation executing |
| Pricing | Pricing calculation executing |
| Review Required | Waiting for operator approval |
| Approved | Quotation approved |
| Rejected | Quotation rejected |
| Completed | Workflow finished |
| Failed | Workflow terminated due to error |

Workflow states are persisted in PostgreSQL to allow full traceability.

---

# 5. User Journey

## Step 1 — Customer Sends RFQ

The workflow begins when a customer sends an email requesting a quotation.

Typical information includes:

- Requested products
- Quantities
- Delivery requirements
- Due dates
- Additional notes

The customer performs no additional actions within the platform.

---

## Step 2 — Email Reception

The email service receives the RFQ and automatically triggers the n8n workflow.

The system records:

- Sender
- Subject
- Timestamp
- Attachments
- Email body

The workflow status becomes:

> Received

---

## Step 3 — AI Information Extraction

The email content is submitted to the OpenAI API for structured extraction.

Expected output includes:

- Customer information
- Product list
- Quantities
- Specifications
- Delivery requirements
- Due dates
- Notes

The extracted information is stored before further processing.

---

## Step 4 — Validation

After extraction, the platform validates the structured data before any pricing logic is executed.

Validation includes:

- Required fields are present.
- Product names are recognized.
- Quantities are valid.
- Email address format is valid.
- Due date format is valid.

### Validation Success

If validation succeeds:

```text
Validation
     │
     ▼
Pricing Engine
```

Workflow status:

> Validating → Pricing

---

### Validation Failure

If validation fails:

```text
Validation
     │
     ▼
Review Required
```

The operator is notified through Slack and the quotation waits for manual correction.

Workflow status:

> Review Required

---

## Step 5 — Pricing Calculation

Once validation succeeds, the pricing engine performs deterministic quotation calculations.

Inputs include:

- Product
- Quantity
- Unit price
- Discount rules
- Margin rules

Outputs include:

- Unit price
- Discount
- Total price
- Margin
- Final quotation

No AI model participates in this step.

Workflow status:

> Pricing

---

## Step 6 — Human Review

The quotation is presented to the Operations Specialist.

The review page displays:

- Original customer email
- Extracted information
- Validation results
- Pricing summary
- Workflow history

The operator may:

- Edit extracted values
- Correct customer information
- Modify quantities
- Recalculate pricing
- Approve
- Reject

Workflow status:

> Review Required

---

# 6. Approval Flow

## Approval

If the quotation is approved:

```text
Review
   │
Approve
   │
   ▼
Generate Draft
```

The approval record includes:

- Reviewer
- Timestamp
- Final quotation values
- Approval status

---

## Rejection

If the quotation is rejected:

```text
Review
   │
Reject
   │
   ▼
Correction
```

The quotation remains in the system until corrected and resubmitted for review.

Rejected quotations are never deleted.

---

# 7. Email Draft Generation

After approval, the system requests an LLM to generate a quotation response draft.

The generated draft includes:

- Customer greeting
- Quotation summary
- Product list
- Pricing summary
- Closing message

The generated content is editable.

Operators remain responsible for the final message.

Workflow status:

> Approved

---

# 8. Slack Notifications

Slack notifications improve operational visibility.

Notifications are sent when:

- RFQ received
- Validation failed
- Human review required
- Workflow completed
- Workflow failed

Each notification contains:

- Quotation ID
- Customer
- Current status
- Assigned reviewer (if applicable)
- Timestamp

Slack notifications do not replace workflow logs.

---

# 9. Workflow Completion

The workflow completes after:

- Human approval
- Email draft generation
- Database persistence
- Notification delivery

Final workflow status:

> Completed

At this stage, all workflow information has been stored and is available for future review.

---

# 10. Alternative Flows

Not every quotation follows the primary success path. The following scenarios describe how the system responds to exceptions.

---

## AF-001 Missing Required Information

### Scenario

The LLM cannot extract one or more mandatory fields.

Examples:

- Missing quantity
- Missing product name
- Missing customer email

### System Behavior

```text
Extraction
      │
      ▼
Validation Failed
      │
      ▼
Review Required
```

The operator manually supplies the missing information before the workflow continues.

---

## AF-002 Unknown Product

### Scenario

The requested product does not exist in the product catalog.

### System Behavior

- Validation fails.
- Pricing is skipped.
- Slack notification is sent.
- Workflow waits for operator action.

No quotation price is generated.

---

## AF-003 Pricing Rule Error

### Scenario

The pricing engine cannot calculate a quotation because pricing data is incomplete or invalid.

### System Behavior

- Pricing execution stops.
- Error is logged.
- Operator is notified.
- Workflow enters the Failed state.

---

## AF-004 OpenAI Extraction Failure

### Scenario

The OpenAI API returns an error or fails to produce a valid structured response.

### System Behavior

- Failure is logged.
- Retry policy may be applied.
- If retries fail, the quotation moves to manual review.

Workflow status:

> Failed

---

## AF-005 Slack Notification Failure

### Scenario

Slack is temporarily unavailable.

### System Behavior

- Notification failure is logged.
- Workflow continues.
- Core quotation processing is not blocked.

Notifications are considered non-critical.

---

# 11. Error States

The platform distinguishes operational errors from business validation failures.

| Error Type | Example | Recovery |
|------------|----------|----------|
| Validation Error | Missing quantity | Manual correction |
| AI Error | Extraction failure | Retry or manual review |
| Pricing Error | Missing pricing rule | Update pricing data |
| Database Error | Write failure | Retry and logging |
| Workflow Error | n8n execution failure | Manual restart |
| External Service Error | Slack unavailable | Continue without notification |

Each error generates an audit log entry.

---

# 12. User Interaction Summary

## Customer

| Action | System Response |
|---------|-----------------|
| Sends RFQ | Workflow starts |
| Waits | No platform interaction |
| Receives quotation | End of customer journey |

---

## Operations Specialist

| Action | Result |
|---------|--------|
| Reviews extraction | Corrects AI output if necessary |
| Reviews pricing | Confirms business accuracy |
| Approves quotation | Draft generated |
| Rejects quotation | Workflow returns for correction |

---

## Administrator

| Action | Purpose |
|---------|---------|
| Review logs | Troubleshooting |
| Update pricing rules | Maintain business logic |
| Monitor workflows | Operational visibility |
| Manage configuration | System maintenance |

---

# 13. State Transition Diagram

```text
Received
    │
    ▼
Extracting
    │
    ▼
Validating
    │
 ┌──┴──────────────┐
 │                 │
 ▼                 ▼
Pricing      Review Required
 │                 │
 ▼                 ▼
Review       Manual Correction
 │                 │
 ├──────┐          │
 │      │          │
 ▼      ▼          │
Approved Rejected──┘
 │
 ▼
Draft Generation
 │
 ▼
Completed
```

Every transition is timestamped and stored to support auditing and debugging.

---

# 14. UX Principles

The platform is designed for operational efficiency rather than feature richness.

The user interface should emphasize:

- Minimal clicks
- Clear workflow progression
- Immediate visibility of validation issues
- Easy correction of extracted data
- Fast approval process

Operators should always understand:

- Current workflow status
- Pending actions
- Validation results
- Pricing summary
- Approval history

The system should never hide critical business information behind multiple screens.

---

# 15. Workflow Notifications

Notifications improve operational awareness without becoming a dependency for workflow execution.

## Notification Matrix

| Event | Recipient | Channel |
|--------|-----------|---------|
| RFQ Received | Operations Team | Slack |
| Validation Failed | Operations Team | Slack |
| Pricing Failed | Operations Team | Slack |
| Review Required | Assigned Reviewer | Slack |
| Workflow Completed | Operations Team | Slack |
| Workflow Failed | Administrator | Slack |

Notifications should include enough context for users to identify the quotation without opening the application.

Recommended fields:

- RFQ ID
- Customer Name
- Current Status
- Timestamp
- Direct link to the review page

---

# 16. Audit Trail

Every workflow action should create an immutable audit event.

Each event contains:

- Event ID
- Workflow ID
- Quotation ID
- User (if applicable)
- Event Type
- Previous Status
- New Status
- Timestamp

Example audit sequence:

```text
RFQ Received
      │
Extraction Completed
      │
Validation Passed
      │
Pricing Calculated
      │
Review Started
      │
Approved
      │
Draft Generated
      │
Workflow Completed
```

This audit history enables operational transparency, troubleshooting, and future compliance requirements.

---

# 17. Success Scenario

A successful quotation follows the sequence below.

```text
Customer
      │
      ▼
RFQ Email
      │
      ▼
AI Extraction
      │
      ▼
Validation Passed
      │
      ▼
Pricing Calculated
      │
      ▼
Human Review
      │
      ▼
Approved
      │
      ▼
Email Draft Generated
      │
      ▼
Stored in PostgreSQL
      │
      ▼
Slack Notification
      │
      ▼
Completed
```

No manual intervention is required until the review stage.

---

# 18. Conclusion

The user flow described in this document represents the complete operational lifecycle of an RFQ within the AI-powered RFQ Operations Platform.

The workflow is intentionally designed around three core principles:

- AI performs language understanding and drafting tasks.
- Deterministic software performs business calculations and validation.
- Human operators retain final approval authority.

This separation of responsibilities improves operational efficiency while ensuring that business-critical decisions remain reliable, transparent, and auditable.

The workflow defined here provides the foundation for the subsequent architecture, database, API, UI/UX, and workflow automation specifications.

---

