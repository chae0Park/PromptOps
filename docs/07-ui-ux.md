# 07. UI / UX Design

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | UI / UX Design |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the user interface, interaction patterns, design principles, and screen layouts for the AI-powered RFQ Operations Platform. |

---

# 1. Purpose

This document defines the user experience and interface design for the AI-powered RFQ Operations Platform.

The UI is designed primarily for Operations Specialists who review AI-generated quotation information before approving customer quotations.

The design emphasizes:

- Simplicity
- Speed
- Readability
- Transparency
- Minimal cognitive load
- Human-centered decision making

---

# 2. Design Principles

---

## UX-001 Clarity First

The interface should prioritize understanding over visual complexity.

Users should immediately identify:

- Current workflow status
- Customer information
- Pricing summary
- Required actions

---

## UX-002 Minimize Clicks

Frequently used operations should require as few interactions as possible.

Examples:

- Approve quotation
- Reject quotation
- Edit extracted values
- View workflow history

---

## UX-003 Human-in-the-Loop

The interface should support review rather than replace decision-making.

AI suggestions must always remain editable.

---

## UX-004 Visual Hierarchy

Information should be organized by operational importance.

Priority order:

1. Workflow status
2. Customer information
3. Requested products
4. Pricing summary
5. AI extraction details
6. Audit history

---

## UX-005 Consistency

Layouts, buttons, colors, spacing, and terminology should remain consistent across all screens.

---

# 3. Primary Users

## Operations Specialist

Primary responsibilities:

- Review quotations
- Verify AI extraction
- Edit quotation information
- Approve pricing
- Reject incorrect quotations

This is the primary user for the MVP.

---

## Administrator

Responsibilities:

- Monitor workflow execution
- Review logs
- Troubleshoot failures
- Configure pricing rules (future)

Administrative functions are intentionally limited in the MVP.

---

# 4. Screen Overview

The MVP consists of the following screens.

| Screen | Purpose |
|----------|----------|
| Dashboard | Workflow overview |
| RFQ Detail | Review quotation |
| Pricing View | Pricing summary |
| Workflow History | View state transitions |
| Error View | Failed workflow review |
| Settings (Future) | Configuration |

The MVP intentionally limits the number of screens to reduce complexity.

---

# 5. Navigation Structure

```text
Dashboard
     │
     ├──────── RFQ Detail
     │              │
     │              ├──────── Pricing
     │              │
     │              └──────── Workflow History
     │
     └──────── Failed Workflows
```

Navigation should remain shallow.

Users should never be more than two clicks away from the Dashboard.
---

# 6. Dashboard

The Dashboard is the landing page for Operations Specialists.

## Objectives

- Display current workload
- Highlight quotations requiring attention
- Surface workflow failures
- Provide quick navigation

---

## Dashboard Layout

```text
--------------------------------------------------------
 AI-powered RFQ Operations Platform
--------------------------------------------------------

Pending Reviews          12

Completed Today          18

Failed Workflows          2

----------------------------------------

Recent RFQs

----------------------------------------

RFQ-1001    Review Required

RFQ-1002    Pricing

RFQ-1003    Completed

RFQ-1004    Failed

----------------------------------------
```

---

## Dashboard Widgets

Recommended widgets include:

- Pending Reviews
- Completed Today
- Failed Workflows
- Recent RFQs
- Recent Activity

Widgets should prioritize operational awareness rather than analytics.

---

# 7. RFQ Detail Screen

This screen is the primary workspace for reviewing quotation requests.

---

## Layout

```text
---------------------------------------------------

Workflow Status

Customer Information

------------------------------------------

Original Email

------------------------------------------

Extracted Information

------------------------------------------

Requested Products

------------------------------------------

Pricing Summary

------------------------------------------

Comments

------------------------------------------

Approve      Reject

---------------------------------------------------
```

---

## Editable Fields

Operators may edit:

- Customer name
- Company
- Email
- Product name
- Quantity
- Specifications
- Notes

All modifications should be recorded in the audit trail.

---

## Read-Only Fields

The following fields should not be edited:

- RFQ Number
- Workflow ID
- Creation Timestamp
- Original Email
- Workflow History

---

# 8. Pricing View

The Pricing View presents deterministic calculation results.

---

## Layout

```text
Product

Quantity

Unit Price

Discount

Tax

---------------------------------

Total

---------------------------------

Margin

---------------------------------
```

---

## Goals

Allow operators to quickly verify:

- Unit pricing
- Discount calculations
- Tax
- Final quotation

The layout should emphasize readability over data density.

---

# 9. Workflow History Screen

This screen displays every workflow transition.

```text
Received

↓

Extracting

↓

Validation

↓

Pricing

↓

Review Required

↓

Approved

↓

Completed
```

Each event includes:

- Timestamp
- Previous state
- New state
- User/System
- Notes (if available)

Workflow history is read-only.

---

# 10. Failed Workflow Screen

Failed workflows require operator attention.

Information displayed:

- RFQ Number
- Failure reason
- Failed component
- Error message
- Retry option

Operators may:

- Retry workflow
- Edit data
- Continue manual processing

Failed workflows should be visually distinct from normal quotations.
---

# 11. Buttons & User Actions

The interface should prioritize the most common operational actions.

## Primary Actions

- Approve
- Reject
- Save Changes

These actions should use clear visual emphasis.

---

## Secondary Actions

- View Workflow History
- Retry Workflow
- Refresh Data
- Return to Dashboard

Secondary actions should remain accessible without distracting from the primary workflow.

---

## Confirmation Dialogs

Potentially destructive actions should require confirmation.

Examples:

### Reject RFQ

```text
Reject this quotation?

[Cancel]    [Reject]
```

---

### Retry Workflow

```text
Retry failed workflow?

[Cancel]    [Retry]
```

Approvals should not require unnecessary confirmation if accidental approvals can be easily reversed in future versions.

---

# 12. Status Indicators

Workflow status should be immediately recognizable.

| Status | Suggested Meaning |
|--------|-------------------|
| Received | Email successfully received |
| Extracting | AI extraction in progress |
| Validating | Business validation running |
| Pricing | Pricing calculation running |
| Review Required | Waiting for human review |
| Approved | Human approval completed |
| Rejected | Manual rejection |
| Completed | Workflow finished |
| Failed | Workflow error |

Status labels should remain consistent across every screen.

---

# 13. Form Design

Forms should reduce operator effort.

Recommendations:

- Group related fields together.
- Use descriptive labels.
- Display validation messages near the affected field.
- Prevent accidental data loss.
- Support keyboard navigation where appropriate.

Example layout:

```text
Customer Name
[____________________]

Company
[____________________]

Email
[____________________]

Notes
[______________________________]
```

---

# 14. Error Messages

Error messages should explain:

- What happened
- Why it happened (if known)
- How the user can resolve it

Examples:

**Good**

> Product quantity must be greater than zero.

**Poor**

> Validation Error

Clear, actionable messages reduce operational delays.

---

# 15. Empty States

When no data is available, the interface should communicate the situation clearly.

Example:

```text
No RFQs require review.

You're all caught up.
```

Avoid displaying empty tables or unexplained blank screens.

---

# 16. Loading States

Long-running operations should provide visible feedback.

Examples include:

- AI extraction
- Pricing calculation
- Workflow retry

Example:

```text
Extracting quotation information...

Loading...
```

Users should always know that processing is in progress.
---

# 17. Accessibility

The interface should remain usable for a wide range of users.

Recommendations include:

- Sufficient color contrast
- Readable typography
- Consistent spacing
- Keyboard accessibility
- Clear focus indicators
- Screen reader compatibility (future)

Accessibility improvements should not compromise operational efficiency.

---

# 18. Responsive Design

Although operators primarily use desktop environments, the interface should adapt gracefully to different screen sizes.

## Desktop (Primary)

Optimized for:

- Large data tables
- Side-by-side comparison
- Multi-panel layouts

---

## Tablet (Supported)

Layouts should stack vertically where necessary while preserving usability.

---

## Mobile (Limited Support)

The MVP supports viewing workflow information on mobile devices.

Editing and approval actions are optimized for desktop use.

---

# 19. UI Components

The application should be built from reusable UI components.

Recommended component library:

| Component | Purpose |
|-----------|---------|
| Button | Primary and secondary actions |
| Card | Group related information |
| Badge | Workflow status display |
| Table | RFQ and quotation lists |
| Modal | Confirm important actions |
| Form | Editable quotation fields |
| Input | Text entry |
| Textarea | Long-form comments |
| Spinner | Loading indicator |
| Toast | Success and error notifications |

Reusable components improve consistency and maintainability.

---

# 20. Design Decisions

## DD-001 Dashboard First

**Decision**

Operators land on the Dashboard after login.

**Reason**

Provides immediate visibility into workload and workflow status.

---

## DD-002 Single Review Screen

**Decision**

Most quotation review tasks occur on a single page.

**Reason**

- Reduces navigation
- Improves efficiency
- Minimizes context switching

---

## DD-003 Read-Only Original Email

**Decision**

The original customer email cannot be edited.

**Reason**

Maintains an immutable record of the customer's request for auditing and comparison.

---

## DD-004 Editable AI Output

**Decision**

All AI-extracted fields remain editable until approval.

**Reason**

Ensures human oversight and allows correction of extraction inaccuracies.

---

## DD-005 Consistent Status Indicators

**Decision**

Use the same workflow status labels across all screens.

**Reason**

Reduces cognitive load and prevents ambiguity during operations.

---

# 21. Conclusion

The UI/UX design prioritizes operational efficiency, transparency, and human oversight.

Rather than maximizing visual complexity, the interface focuses on enabling Operations Specialists to review, verify, and approve quotations with minimal effort while maintaining complete visibility into AI-generated outputs and workflow progress.

This design provides a practical foundation for implementing the frontend using Next.js and reusable TypeScript components while remaining flexible enough to accommodate future platform growth.

---

