# 10. Testing Strategy

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | Testing Strategy |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the testing approach, quality assurance process, validation strategy, and acceptance criteria for the AI-powered RFQ Operations Platform. |

---

# 1. Purpose

This document defines how the AI-powered RFQ Operations Platform is tested before deployment.

The testing strategy aims to ensure:

- Correct business behavior
- Reliable AI-assisted workflows
- Deterministic pricing
- Stable workflow execution
- Production readiness

Testing is applied at multiple layers to detect issues as early as possible.

---

# 2. Testing Principles

The testing strategy follows five core principles.

---

## TS-001 Automate Where Possible

Repeatable tests should be automated.

Examples:

- API testing
- Pricing calculations
- Validation rules
- Database operations

---

## TS-002 Human Verification for AI

AI outputs require human evaluation.

The platform tests:

- Extraction accuracy
- Draft quality
- Hallucination rate
- Missing information

AI quality cannot be validated solely through automated assertions.

---

## TS-003 Deterministic Business Logic

Business calculations must produce identical outputs for identical inputs.

Every pricing rule should be unit tested.

---

## TS-004 Independent Component Testing

Each subsystem should be tested independently before end-to-end integration.

Components include:

- OpenAI integration
- Pricing engine
- API
- Database
- n8n workflow
- Frontend

---

## TS-005 Production-Like Validation

Testing should closely resemble real operational scenarios using synthetic or anonymized RFQ data.

---

# 3. Testing Pyramid

```text
                Manual Review
                     ▲
             End-to-End Tests
                     ▲
          Integration Tests
                     ▲
              Unit Tests
```

The majority of tests should exist at the unit level.

---

# 4. Test Levels

| Level | Purpose |
|--------|---------|
| Unit Tests | Individual functions |
| Integration Tests | Component interaction |
| End-to-End Tests | Complete RFQ workflow |
| Manual Review | Human validation of AI outputs |

Each level addresses a different category of risk.

---

# 5. Unit Testing

Unit tests verify isolated business logic.

Primary targets include:

- Validation functions
- Pricing calculations
- Discount rules
- Tax calculations
- Utility functions
- Data transformations

Unit tests should execute quickly and without external dependencies.
---

# 6. Integration Testing

Integration tests verify communication between system components.

Major integration points include:

- Frontend ↔ FastAPI
- FastAPI ↔ PostgreSQL
- FastAPI ↔ OpenAI API
- n8n ↔ FastAPI
- n8n ↔ Slack

Objectives:

- Verify API contracts
- Validate data flow
- Confirm error handling
- Ensure correct service orchestration

---

# 7. End-to-End Testing

End-to-end tests simulate the complete quotation workflow.

Example scenario:

```text
Customer Email
      │
      ▼
OpenAI Extraction
      │
      ▼
Validation
      │
      ▼
Pricing
      │
      ▼
Human Approval
      │
      ▼
Email Draft
      │
      ▼
Workflow Complete
```

The expected outcome is a successfully completed quotation with all intermediate workflow states correctly recorded.

---

# 8. AI Evaluation

AI behavior should be evaluated separately from deterministic software.

Evaluation criteria include:

| Metric | Description |
|--------|-------------|
| Extraction Accuracy | Correct field extraction |
| JSON Validity | Valid structured output |
| Hallucination Rate | Unsupported information generated |
| Missing Fields | Required information omitted |
| Email Draft Quality | Professional and accurate response |

Human reviewers should periodically evaluate AI outputs using representative RFQ samples.

---

# 9. Pricing Validation

Pricing calculations should be verified against expected outputs.

Example test case:

| Input | Expected Output |
|--------|-----------------|
| Product A × 10 | Correct subtotal |
| Discount 10% | Correct discount amount |
| Tax 10% | Correct tax |
| Final Total | Correct quotation |

Pricing tests should cover:

- Normal cases
- Boundary values
- Zero discounts
- Large quantities
- Invalid inputs

---

# 10. Validation Testing

Validation rules require dedicated test cases.

Examples include:

| Test | Expected Result |
|------|-----------------|
| Missing customer email | Validation failure |
| Quantity = 0 | Validation failure |
| Invalid email format | Validation failure |
| Unknown product | Validation failure |
| Valid RFQ | Validation success |

Each validation rule should have both positive and negative test cases.
---

# 11. API Testing

Every REST endpoint should be verified.

Recommended test coverage:

| Endpoint | Test Cases |
|----------|------------|
| GET /rfqs | Success, empty list, invalid request |
| GET /rfqs/{id} | Existing ID, missing ID |
| POST /rfqs | Valid request, invalid payload |
| PATCH /rfqs/{id} | Valid update, invalid status |
| POST /approvals | Approve, reject, invalid decision |
| POST /quotations/calculate | Valid RFQ, invalid RFQ |

Each endpoint should verify:

- HTTP status code
- Response schema
- Validation behavior
- Error handling

---

# 12. Workflow Testing

The n8n workflow should be validated independently.

Test scenarios include:

- RFQ successfully received
- OpenAI extraction succeeds
- OpenAI extraction fails
- Validation fails
- Pricing succeeds
- Pricing fails
- Human approval resumes workflow
- Slack notification failure
- Database write failure

Every workflow branch should be exercised at least once.

---

# 13. Performance Testing

Although the MVP targets moderate usage, basic performance testing is recommended.

Suggested metrics:

| Metric | Target |
|--------|--------|
| API Response | < 500 ms (excluding AI calls) |
| Pricing Calculation | < 100 ms |
| Database Query | < 200 ms |
| Workflow Startup | < 2 seconds |
| Dashboard Load | < 2 seconds |

External AI response times should be monitored separately.

---

# 14. Manual Testing Checklist

Before each release, perform the following checks:

- RFQ creation
- AI extraction review
- Validation results
- Pricing accuracy
- Approval workflow
- Email draft generation
- Slack notification
- Database persistence
- Workflow history
- Audit log creation

Manual verification complements automated testing for business-critical workflows.

---

# 15. Regression Testing

Regression testing ensures that new changes do not introduce unintended behavior.

Areas requiring regression coverage include:

- Pricing calculations
- Validation rules
- Workflow execution
- API endpoints
- Database persistence
- Frontend interactions

A regression suite should be executed before every production deployment.

---

# 16. Test Data Strategy

Testing should use synthetic or anonymized RFQ data.

Representative datasets should include:

- Simple RFQs
- Multiple products
- Large quantities
- Missing information
- Invalid email formats
- Unknown products
- Discount scenarios
- International customers

No production customer information should be used during development or testing.
---

# 17. Test Environment

The testing environment should closely resemble the production architecture.

Recommended environment:

| Component | Environment |
|-----------|-------------|
| Frontend | Local / Preview (Vercel) |
| Backend | Local FastAPI or Render Preview |
| Database | PostgreSQL (Development) |
| Workflow | Local Docker n8n |
| AI | OpenAI API (Development Key) |
| Notifications | Test Slack Workspace |

Production data should never be used in development or staging environments.

---

# 18. Acceptance Criteria

The MVP is considered production-ready when the following conditions are met.

## Functional Requirements

- RFQ emails are successfully processed.
- AI extracts structured quotation data.
- Validation detects invalid input.
- Pricing calculations are deterministic.
- Human review workflow functions correctly.
- Email drafts are generated after approval.
- Workflow history is persisted.
- Slack notifications are delivered.

---

## Quality Requirements

- All critical unit tests pass.
- Integration tests pass.
- End-to-end workflow executes successfully.
- No blocking defects remain.
- Manual review confirms acceptable AI output quality.

---

# 19. Quality Metrics

Recommended quality indicators:

| Metric | Target |
|--------|--------|
| Unit Test Pass Rate | 100% |
| Integration Test Pass Rate | 100% |
| Critical Bug Count | 0 |
| API Availability | > 99% |
| Pricing Accuracy | 100% |
| AI JSON Validity | > 99% |
| Workflow Success Rate | > 95% |

These targets provide an initial benchmark for evaluating platform readiness.

---

# 20. Testing Design Decisions

## TD-001 Layered Testing

**Decision**

Adopt a layered testing strategy.

**Reason**

Issues are detected earlier, reducing debugging effort and improving maintainability.

---

## TD-002 Human Evaluation for AI

**Decision**

Require manual evaluation of AI-generated outputs.

**Reason**

Automated tests cannot fully assess language quality, completeness, or hallucinations.

---

## TD-003 Deterministic Pricing Verification

**Decision**

Unit test every pricing rule.

**Reason**

Pricing directly impacts customer quotations and must remain completely reliable.

---

## TD-004 Synthetic Test Data

**Decision**

Use synthetic or anonymized RFQ data for testing.

**Reason**

Protects customer privacy while providing realistic validation scenarios.

---

## TD-005 Continuous Regression Testing

**Decision**

Run regression tests before every production deployment.

**Reason**

Ensures new changes do not unintentionally break existing functionality.

---

# 21. Conclusion

A comprehensive testing strategy is essential for ensuring that the AI-powered RFQ Operations Platform remains reliable, maintainable, and production-ready.

By combining automated testing, deterministic validation, end-to-end workflow verification, and human evaluation of AI outputs, the platform balances software engineering best practices with the unique quality assurance requirements of AI-assisted systems.

This testing framework provides confidence that each release maintains functional correctness while preserving the accuracy and transparency required for quotation operations.

---

