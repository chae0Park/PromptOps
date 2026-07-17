# 05. Database Design

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | Database Design |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the relational database schema, entities, relationships, constraints, and persistence strategy for the AI-powered RFQ Operations Platform. |

---

# 1. Purpose

This document defines the database architecture of the AI-powered RFQ Operations Platform.

The database is responsible for:

- Persisting quotation requests
- Recording workflow execution
- Storing pricing information
- Managing approval history
- Supporting audit logging
- Enabling future reporting and analytics

PostgreSQL serves as the single source of truth for all operational data.

---

# 2. Design Principles

The database follows several core principles.

---

## DP-001 Single Source of Truth

Operational data is stored only once.

All services reference the same persisted records.

---

## DP-002 Normalization

Data is normalized to reduce duplication while maintaining readability and performance.

---

## DP-003 Auditability

No important workflow action is lost.

Critical changes are recorded through audit logs rather than destructive updates.

---

## DP-004 Referential Integrity

Relationships between entities are enforced through foreign keys.

Orphan records are not permitted.

---

## DP-005 Extensibility

The schema is designed to support future features including:

- Multiple quotations
- Product catalog expansion
- User authentication
- Analytics
- Approval workflows
- Version history

---

# 3. Database Overview

The MVP consists of the following primary tables.

| Table | Purpose |
|--------|----------|
| rfqs | Customer quotation requests |
| rfq_items | Individual requested products |
| quotations | Calculated quotation results |
| workflow_history | Workflow state transitions |
| approvals | Human approval records |
| audit_logs | System audit trail |

These tables represent the core operational data required for the MVP.

---

# 4. Entity Relationship Diagram

```text
RFQs
 │
 ├──────────────┐
 │              │
 ▼              ▼
RFQ Items   Quotations
 │              │
 │              ▼
 │        Approvals
 │
 ▼
Workflow History
 │
 ▼
Audit Logs
```

Each quotation originates from a single RFQ, while each RFQ may contain multiple requested items.

---

# 5. Table Definitions

## 5.1 RFQs

The `rfqs` table stores every quotation request received from customers.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_number | VARCHAR | Unique RFQ identifier |
| customer_name | VARCHAR | Customer name |
| company_name | VARCHAR | Company name |
| customer_email | VARCHAR | Customer email |
| email_subject | TEXT | Original email subject |
| email_body | TEXT | Original email content |
| status | VARCHAR | Current workflow state |
| received_at | TIMESTAMP | Email received timestamp |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### Constraints

- Primary Key: `id`
- Unique: `rfq_number`
- `customer_email` must be valid
- `status` must match supported workflow states

---

## 5.2 RFQ Items

Each RFQ may contain one or more requested products.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_id | UUID | Foreign key to RFQs |
| product_name | VARCHAR | Requested product |
| quantity | INTEGER | Requested quantity |
| specification | TEXT | Product specification |
| notes | TEXT | Additional notes |
| created_at | TIMESTAMP | Record creation time |

### Relationship

```text
RFQ
 │
 ├──────── Item
 ├──────── Item
 ├──────── Item
```

One RFQ may contain many RFQ Items.

---

## 5.3 Quotations

The quotations table stores calculated pricing results.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_id | UUID | Related RFQ |
| subtotal | DECIMAL | Price before discounts |
| discount | DECIMAL | Applied discount |
| tax | DECIMAL | Tax amount |
| total | DECIMAL | Final quotation |
| currency | VARCHAR | Currency code |
| generated_at | TIMESTAMP | Pricing completion time |

### Relationship

```text
RFQ
 │
 ▼
Quotation
```

Each RFQ produces one quotation in the MVP.

Future versions may support quotation revisions.

---

## 5.4 Workflow History

Every workflow transition is recorded.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_id | UUID | Related RFQ |
| previous_status | VARCHAR | Previous workflow state |
| new_status | VARCHAR | Current workflow state |
| changed_by | VARCHAR | User or system |
| changed_at | TIMESTAMP | Transition time |

Example:

```text
Received
    │
Extracting
    │
Validating
    │
Pricing
    │
Review Required
    │
Approved
    │
Completed
```

No workflow transition should overwrite previous history.

---

## 5.5 Approvals

The approvals table records all human approval decisions.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_id | UUID | Related RFQ |
| reviewer | VARCHAR | Reviewer name or identifier |
| decision | VARCHAR | Approved or Rejected |
| comments | TEXT | Reviewer comments |
| reviewed_at | TIMESTAMP | Review timestamp |

### Decision Values

Supported values include:

- Approved
- Rejected

Future versions may support additional statuses such as:

- Pending
- Escalated
- Reopened

---

## 5.6 Audit Logs

The audit log records important system events.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary key |
| rfq_id | UUID | Related RFQ |
| event_type | VARCHAR | Event category |
| event_details | JSONB | Additional event information |
| actor | VARCHAR | User or system |
| created_at | TIMESTAMP | Event timestamp |

### Example Events

- RFQ Received
- Extraction Completed
- Validation Passed
- Validation Failed
- Pricing Calculated
- Review Started
- Approved
- Rejected
- Draft Generated
- Workflow Completed

Audit logs should be immutable.

---

# 6. Relationships

The relational structure is illustrated below.

```text
RFQs
 │
 ├─────────────── RFQ Items
 │
 ├─────────────── Quotations
 │
 ├─────────────── Workflow History
 │
 ├─────────────── Approvals
 │
 └─────────────── Audit Logs
```

Relationship summary:

| Parent | Child | Cardinality |
|---------|-------|-------------|
| RFQs | RFQ Items | One-to-Many |
| RFQs | Quotations | One-to-One (MVP) |
| RFQs | Workflow History | One-to-Many |
| RFQs | Approvals | One-to-Many |
| RFQs | Audit Logs | One-to-Many |

---

# 7. Primary Keys

Every table uses UUIDs as primary keys.

| Table | Primary Key |
|--------|-------------|
| rfqs | id |
| rfq_items | id |
| quotations | id |
| workflow_history | id |
| approvals | id |
| audit_logs | id |

UUIDs reduce predictability and simplify distributed system integration.

---

# 8. Foreign Keys

| Child Table | Foreign Key | Parent Table |
|--------------|-------------|--------------|
| rfq_items | rfq_id | rfqs |
| quotations | rfq_id | rfqs |
| workflow_history | rfq_id | rfqs |
| approvals | rfq_id | rfqs |
| audit_logs | rfq_id | rfqs |

All foreign key relationships should enforce referential integrity.

---

# 9. Constraints

The database enforces constraints to maintain data quality and consistency.

## RFQs

- `rfq_number` must be unique.
- `customer_email` cannot be NULL.
- `status` cannot be NULL.
- `received_at` cannot be NULL.

---

## RFQ Items

- `rfq_id` must reference an existing RFQ.
- `quantity` must be greater than zero.
- `product_name` cannot be empty.

---

## Quotations

- `rfq_id` must reference an existing RFQ.
- `total` cannot be negative.
- `currency` should follow ISO 4217 format (e.g., USD, EUR, KRW).

---

## Workflow History

- `previous_status` may be NULL for the initial workflow state.
- `new_status` cannot be NULL.
- `changed_at` cannot be NULL.

---

## Approvals

- `decision` must be one of:
  - Approved
  - Rejected

- `reviewed_at` cannot be NULL.

---

## Audit Logs

- Events cannot be updated after creation.
- Records should never be deleted under normal operations.

---

# 10. Index Strategy

Indexes improve lookup performance for frequently accessed records.

| Table | Indexed Columns |
|--------|-----------------|
| rfqs | rfq_number |
| rfqs | customer_email |
| rfqs | status |
| rfqs | received_at |
| quotations | rfq_id |
| workflow_history | rfq_id |
| workflow_history | changed_at |
| approvals | rfq_id |
| audit_logs | rfq_id |
| audit_logs | created_at |

Additional indexes may be introduced after analyzing production query patterns.

---

# 11. Data Lifecycle

Each RFQ progresses through a complete lifecycle.

```text
Email Received
      │
      ▼
RFQ Created
      │
      ▼
Items Stored
      │
      ▼
Pricing Generated
      │
      ▼
Review Completed
      │
      ▼
Workflow Finished
      │
      ▼
Archived
```

The database preserves each stage for future auditing and reporting.

---

# 12. Soft Delete Strategy

The MVP does not permanently delete operational records.

Instead:

- RFQs remain stored after completion.
- Workflow history is retained indefinitely.
- Audit logs are immutable.
- Approval history is preserved.

If deletion is required in future versions, a soft delete approach is recommended using fields such as:

| Column | Purpose |
|--------|---------|
| deleted_at | Timestamp of deletion |
| deleted_by | User performing deletion |

This approach preserves historical integrity while allowing records to be excluded from active views.

---

# 13. Data Retention

Recommended retention policy:

| Data Type | Retention |
|-----------|-----------|
| RFQs | Long-term |
| Quotations | Long-term |
| Workflow History | Long-term |
| Approvals | Long-term |
| Audit Logs | Long-term |

Retention periods may later be adjusted to comply with organizational or regulatory requirements.

---

# 14. Future Expansion

The database schema is intentionally designed to support future enhancements without major structural changes.

Potential additions include:

- User authentication
- Role-based access control (RBAC)
- Product catalog
- Customer master data
- Vendor management
- RFQ attachments
- Quote version history
- Approval workflows with multiple reviewers
- Workflow templates
- Reporting and analytics tables

These features can be introduced through additional tables while preserving the existing relationships.

---

# 15. Schema Summary

The MVP database consists of six core tables.

```text
rfqs
 │
 ├──────── rfq_items
 │
 ├──────── quotations
 │
 ├──────── workflow_history
 │
 ├──────── approvals
 │
 └──────── audit_logs
```

Together, these tables provide complete support for:

- RFQ storage
- Product requests
- Pricing results
- Workflow tracking
- Human approval
- Operational auditing

---

# 16. Database Design Decisions

The following decisions influenced the schema design.

## DD-001 UUID Primary Keys

**Decision**

Use UUIDs for all primary keys.

**Reason**

- Globally unique identifiers
- Easier distributed system integration
- Reduced predictability compared to sequential IDs

---

## DD-002 JSONB for Event Details

**Decision**

Store variable audit metadata in `JSONB`.

**Reason**

- Flexible event payloads
- Efficient querying in PostgreSQL
- Extensible without frequent schema changes

---

## DD-003 Separate Workflow History

**Decision**

Store workflow transitions in a dedicated table rather than overwriting status fields.

**Reason**

- Complete audit trail
- Historical reporting
- Easier debugging
- Workflow analytics

---

## DD-004 Immutable Audit Records

**Decision**

Audit log entries are append-only.

**Reason**

- Preserves historical accuracy
- Supports compliance requirements
- Prevents accidental loss of operational history

---

# 17. Conclusion

The database design provides a normalized, extensible, and production-ready foundation for the AI-powered RFQ Operations Platform.

By separating operational entities, workflow history, approval records, and audit events, the schema ensures:

- Reliable data integrity
- Complete traceability
- Efficient workflow management
- Clear separation of concerns
- Scalability for future feature development

This database serves as the persistent backbone of the platform and supports all application layers, including workflow orchestration, pricing, AI-assisted processing, frontend review, and operational reporting.

---

