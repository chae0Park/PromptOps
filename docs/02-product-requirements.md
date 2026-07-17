# 02. Product Requirements Document (PRD)

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | Product Requirements Document |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the functional and non-functional requirements for the MVP. |

---

# 1. Purpose

This document defines the functional scope, business requirements, constraints, and acceptance criteria for the AI-powered RFQ Operations Platform.

The objective is to ensure that every feature developed during implementation directly supports the operational workflow while remaining aligned with the project's MVP scope.

This PRD serves as the primary reference for system design, development, testing, and deployment.

---

# 2. Product Objective

Build an AI-assisted quotation operations platform that automates repetitive quotation processing while preserving deterministic business logic and mandatory human approval.

The system should:

- Reduce manual quotation processing time.
- Improve quotation consistency.
- Minimize operational errors.
- Increase process visibility.
- Maintain complete auditability.
- Support future extensibility.

---

# 3. Business Context

Many quotation processes remain heavily dependent on manual operations.

Typical workflows require employees to:

- Read customer emails.
- Extract quotation details.
- Interpret requested products.
- Apply pricing policies.
- Calculate quotations.
- Prepare customer responses.
- Record quotation history.

These repetitive tasks consume valuable operational resources and increase the likelihood of human error.

The proposed platform introduces AI only where language understanding provides measurable value while preserving deterministic software for business-critical calculations.

---

# 4. Product Scope

## Included (MVP)

The MVP includes the following capabilities:

### Email Processing

- Receive RFQ emails.
- Parse email content.
- Extract attachments.
- Trigger workflow automatically.

---

### AI Information Extraction

Extract structured information including:

- Customer name
- Company
- Email
- Product names
- Requested quantity
- Required specifications
- Delivery requirements
- Due date
- Additional notes

The extracted information must be stored in structured form.

---

### Validation

Automatically verify:

- Required fields exist.
- Product quantities are valid.
- Product names are recognized.
- Mandatory business information is present.
- Invalid records are flagged for review.

---

### Pricing

Pricing calculations must be performed using deterministic Python logic.

Supported calculations include:

- Unit price
- Quantity pricing
- Discounts
- Margin calculation
- Final quotation price

No LLM may participate in price calculation.

---

### Human Review

Provide an interface allowing operators to:

- Review extracted information.
- Modify incorrect values.
- Confirm calculated prices.
- Approve quotation.
- Reject quotation.
- Request corrections.

---

### Email Draft Generation

Generate a quotation response draft after approval.

The operator must be able to edit the generated email before sending.

---

### Notifications

Notify internal teams through Slack whenever:

- RFQ received
- Validation failed
- Human review required
- Quotation approved
- Workflow failed

---

### Data Storage

Persist workflow information including:

- RFQ metadata
- Extracted fields
- Validation results
- Pricing results
- Approval status
- Generated emails
- Workflow timestamps

All records must be stored in PostgreSQL.

---

# 5. Out of Scope

The following features are intentionally excluded from the MVP.

## ERP Integration

No ERP synchronization.

---

## CRM Integration

No CRM connectivity.

---

## Inventory Management

Inventory availability is not considered.

---

## Automatic Customer Delivery

Customer emails are never sent automatically.

Human approval is always required.

---

## Customer Portal

Customers cannot log into the platform.

---

## Vendor Portal

Vendor communication is outside MVP scope.

---

## Analytics Dashboard

Operational analytics are postponed.

---

## Golden Set Evaluation

Prompt evaluation infrastructure is intentionally excluded.

---

## Prompt Version Management

Version management for prompts is outside the MVP.

---

## Cost Monitoring

AI token cost tracking will be implemented in future releases.

---

# 6. Functional Requirements

Each functional requirement represents a capability that the MVP must support.

---

## FR-001 Receive RFQ Email

### Description

The system shall automatically receive quotation request emails.

### Priority

Critical

### Input

Customer email

### Output

Workflow execution starts.

### Acceptance Criteria

- Email is successfully received.
- Workflow is triggered automatically.
- Email metadata is stored.

---

## FR-002 Extract RFQ Information

### Description

The system shall use an LLM to extract structured quotation information from the email body.

### Required Fields

- Customer Name
- Company
- Email Address
- Product Name
- Quantity
- Specifications
- Delivery Requirement
- Due Date
- Additional Notes

### Acceptance Criteria

- Structured JSON is generated.
- Missing fields are identified.
- Extraction result is stored.

---

## FR-003 Validate Extracted Information

### Description

The system shall validate extracted data before pricing begins.

### Validation Rules

- Required fields exist.
- Quantity > 0
- Product name exists
- Email format valid
- Due date format valid

### Acceptance Criteria

- Validation status returned.
- Invalid fields identified.
- Workflow pauses if validation fails.

---

## FR-004 Calculate Pricing

### Description

The system shall calculate quotation pricing using deterministic Python business rules.

### Inputs

- Product
- Quantity
- Pricing Rules
- Discount Rules

### Outputs

- Unit Price
- Discount
- Margin
- Total Price

### Acceptance Criteria

- Results are deterministic.
- Same input always returns same output.
- Calculation history stored.

---

## FR-005 Human Approval

### Description

Operators shall review quotation information before customer communication.

### User Actions

- Approve
- Reject
- Edit
- Save
- Continue

### Acceptance Criteria

- Approval recorded.
- Reviewer identified.
- Timestamp stored.

---

## FR-006 Generate Customer Email

### Description

Generate an editable quotation email after approval.

### Acceptance Criteria

- Draft generated.
- Operator can modify.
- Final version stored.

---

## FR-007 Slack Notification

### Description

Send workflow notifications to Slack.

### Notification Events

- RFQ received
- Validation failed
- Waiting for review
- Approved
- Workflow error

### Acceptance Criteria

- Notification delivered.
- Delivery failure logged.

---

## FR-008 Store Workflow Data

### Description

Persist every workflow stage.

### Stored Data

- Email metadata
- Extraction
- Validation
- Pricing
- Approval
- Generated email
- Workflow logs

### Acceptance Criteria

- Records successfully written.
- Historical records searchable.

---

# 7. Non-Functional Requirements

---

## NFR-001 Reliability

The system should recover gracefully from workflow failures.

Requirements:

- Failed workflows logged.
- Retry supported.
- Partial failures isolated.

---

## NFR-002 Maintainability

The architecture should allow independent modification of:

- LLM
- Pricing engine
- Database
- Workflow automation
- Frontend

without affecting unrelated components.

---

## NFR-003 Performance

Target performance for the MVP:

| Operation | Target |
|-----------|---------|
| Email ingestion | <10 sec |
| AI extraction | <20 sec |
| Pricing | <2 sec |
| Human review loading | <3 sec |
| Slack notification | <5 sec |

These targets are operational goals rather than hard guarantees.

---

## NFR-004 Security

The system should:

- Store API keys securely.
- Prevent unauthorized access.
- Log authentication failures.
- Protect quotation records.

Authentication implementation is outside the MVP but should be supported by the architecture.

---

## NFR-005 Auditability

Every important action must produce an audit log.

Examples include:

- Workflow started
- Extraction completed
- Validation failed
- Pricing calculated
- Approval completed
- Email generated
- Slack notification sent

---

# 8. Business Rules

The following business rules define the expected behavior of the system throughout the quotation workflow.

---

## BR-001 Human Approval Required

Every quotation must receive explicit human approval before customer communication.

Automatic quotation delivery is prohibited.

---

## BR-002 Deterministic Pricing

All pricing calculations must be performed exclusively by deterministic Python logic.

Large Language Models must never calculate:

- Unit prices
- Discounts
- Taxes
- Margins
- Final quotation totals

---

## BR-003 AI Usage

AI may only be used for:

- Natural language understanding
- Information extraction
- Summarization
- Email draft generation

AI outputs are considered recommendations and require human verification before use.

---

## BR-004 Validation Before Pricing

Pricing calculations may only begin after all required validation rules have passed.

If validation fails, the workflow must pause until corrected.

---

## BR-005 Workflow Traceability

Every workflow stage must be recorded with:

- Timestamp
- Event type
- Workflow status
- Associated quotation
- Execution result

---

## BR-006 Immutable Workflow History

Historical workflow records must not be overwritten.

Changes should create new records rather than modifying historical events.

---

## BR-007 Error Recovery

Unexpected workflow failures must:

- Record the error
- Preserve existing data
- Notify operators
- Allow manual retry

---

# 9. Assumptions

The MVP assumes the following conditions.

- Incoming RFQ emails are written in English.
- Product pricing data is available before workflow execution.
- Pricing rules are maintained externally.
- Operators understand quotation review procedures.
- Slack is available for internal notifications.
- OpenAI API credentials are configured.
- PostgreSQL is operational.
- Internet connectivity is available during workflow execution.

---

# 10. Constraints

The project intentionally adopts several implementation constraints.

### Scope Constraints

- Single quotation workflow
- Single organization
- Single database
- Single AI provider
- No ERP integration
- No CRM integration

### Technical Constraints

- Next.js frontend
- FastAPI backend
- PostgreSQL database
- n8n workflow orchestration
- OpenAI API
- Deterministic Python pricing engine

Changing these technologies is outside the MVP scope.

---

# 11. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI extraction error | Medium | Human review before approval |
| Incorrect pricing logic | High | Deterministic Python implementation and testing |
| Workflow interruption | Medium | Retry mechanism and workflow logging |
| API downtime | Medium | Error handling and notification |
| Invalid customer email | Low | Validation rules before processing |
| Database failure | High | Persistent logging and recovery strategy |

---

# 12. Acceptance Criteria

The MVP is considered complete when all of the following conditions are satisfied.

### Workflow

- RFQ email successfully starts the workflow.
- Workflow executes without manual intervention until the review stage.

---

### AI Extraction

- Structured quotation information is produced.
- Missing fields are clearly identified.
- Extraction results are stored.

---

### Validation

- Required validation rules execute automatically.
- Invalid quotations are blocked.
- Validation results are logged.

---

### Pricing

- Pricing is calculated using deterministic logic.
- Calculation results are reproducible.
- Pricing history is stored.

---

### Human Review

- Operators can review extracted information.
- Operators can edit quotation data.
- Approval status is recorded.
- Reviewer information is stored.

---

### Email Draft

- AI generates an editable quotation draft.
- Final draft is stored after approval.

---

### Notifications

- Slack notifications are delivered for supported workflow events.
- Notification failures are logged.

---

### Persistence

- Workflow data is stored in PostgreSQL.
- Historical workflow records remain accessible.
- Workflow status can be reconstructed from stored data.

---

# 13. Success Metrics

The success of the MVP will be evaluated using operational, technical, and usability metrics.

## Operational Metrics

| Metric | Target |
|---------|--------|
| Manual quotation work reduction | Significant reduction compared to the current workflow |
| Quotation workflow completion | End-to-end execution without critical failures |
| Human approval coverage | 100% of quotations reviewed before customer delivery |
| Workflow traceability | 100% of major events logged |

---

## Technical Metrics

| Metric | Target |
|---------|--------|
| Successful AI extraction | Consistent structured output for supported RFQs |
| Pricing consistency | Identical outputs for identical inputs |
| Workflow reliability | Stable execution under expected operational load |
| Database persistence | No loss of workflow records |

---

## User Experience Metrics

The platform should allow operators to:

- Understand the workflow without technical knowledge.
- Quickly identify validation issues.
- Edit extracted information efficiently.
- Review pricing before approval.
- Approve quotations with minimal effort.

---

# 14. Dependencies

The MVP depends on the following external services and internal components.

## External Dependencies

- OpenAI API
- Slack Workspace
- Email Provider
- PostgreSQL (Supabase)
- Vercel
- Render

---

## Internal Dependencies

- Pricing rule definitions
- Product master data
- Validation rule configuration
- Prompt templates
- n8n workflow configuration

---

# 15. Future Enhancements

The following enhancements have been identified but are intentionally excluded from the MVP.

## Business Features

- ERP integration
- CRM integration
- Vendor management
- Customer self-service portal
- Inventory synchronization
- Purchase order generation
- Multi-currency quotations
- Multi-language quotation generation

---

## AI Features

- Prompt version management
- Golden Set evaluation
- Automated prompt regression testing
- AI confidence scoring
- Multi-model comparison
- Cost monitoring
- Latency monitoring
- AI evaluation dashboard

---

## Operational Features

- Workflow analytics
- Performance dashboard
- Role-based permissions
- Approval workflows with multiple reviewers
- Advanced search and filtering
- Audit reporting
- Scheduled workflow execution
- Workflow monitoring dashboard

---

# 16. Document References

This document is supported by the following project documentation.

| Document | Purpose |
|----------|---------|
| 01-overview.md | Product overview and vision |
| 03-user-flow.md | End-to-end workflow definitions |
| 04-system-architecture.md | System architecture |
| 05-database-design.md | Database schema |
| 06-api-specification.md | Backend API definitions |
| 07-ui-ux.md | User interface specification |
| 08-ai-pricing-engine.md | AI and pricing responsibilities |
| 09-n8n-workflows.md | Workflow automation |
| 10-testing-strategy.md | Testing methodology |
| 11-deployment.md | Deployment architecture |
| 12-development-roadmap.md | Development phases |
| 13-interview-guide.md | Project explanation for interviews |

---

# 17. Conclusion

The Product Requirements Document defines the complete functional scope of the AI-powered RFQ Operations Platform MVP.

The platform is designed around a clear separation of responsibilities:

- AI performs language understanding and content generation.
- Deterministic software performs business calculations.
- Human operators retain decision-making authority.

This approach ensures that the platform delivers measurable operational improvements while maintaining reliability, transparency, and auditability.

The requirements defined in this document serve as the baseline for system design, implementation, testing, deployment, and future product evolution.

---

