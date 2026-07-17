# 06. API Specification

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | API Specification |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the REST API endpoints, request/response formats, authentication strategy, and integration patterns for the AI-powered RFQ Operations Platform. |

---

# 1. Purpose

This document defines the backend REST API used by the AI-powered RFQ Operations Platform.

The API enables communication between:

- Next.js frontend
- FastAPI backend
- n8n workflows
- OpenAI integration
- PostgreSQL database

The API is designed around REST principles with JSON as the primary data format.

---

# 2. API Design Principles

The API follows several architectural principles.

---

## AP-001 Resource-Oriented

Endpoints are organized around business resources rather than actions.

Examples:

- RFQs
- Quotations
- Approvals
- Workflow History

---

## AP-002 Stateless

Each request contains all information required for processing.

No server-side session state is maintained.

---

## AP-003 JSON Communication

Requests and responses use JSON.

Example:

```json
{
  "rfq_id": "uuid",
  "status": "Approved"
}
```

---

## AP-004 Predictable Responses

Every endpoint returns a consistent response structure.

```json
{
  "success": true,
  "data": {},
  "message": ""
}
```

Error responses follow the same pattern.

---

## AP-005 Versioning

The API is versioned.

Base URL:

```text
/api/v1
```

Future breaking changes should introduce new versions rather than modifying existing endpoints.

---

# 3. High-Level API Architecture

```text
Next.js
    │
    ▼
FastAPI REST API
    │
 ┌──┴───────────────┐
 ▼                  ▼
PostgreSQL      OpenAI API
        │
        ▼
      n8n
```

The FastAPI service acts as the central backend for all client interactions.

---

# 4. Base URL

Development

```text
http://localhost:8000/api/v1
```

Production

```text
https://your-domain.com/api/v1
```

All examples in this document assume the `/api/v1` prefix.

---

# 5. Authentication

Authentication is outside the MVP scope.

However, the API is designed to support future authentication mechanisms such as:

- JWT
- OAuth 2.0
- API Keys
- Session-based authentication

Protected endpoints should eventually require authenticated access.

---

# 6. Standard Response Format

All API responses follow a common structure.

## Success Response

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

---

## Error Response

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "quantity",
      "reason": "Quantity must be greater than zero."
    }
  ]
}
```

This consistent structure simplifies frontend integration and error handling.

---

# 7. RFQ Endpoints

## GET /rfqs

Returns a list of RFQs.

### Request

```http
GET /api/v1/rfqs
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "rfq_number": "RFQ-2026-001",
      "customer_name": "John Smith",
      "status": "Review Required"
    }
  ]
}
```

---

## GET /rfqs/{id}

Returns a single RFQ.

### Request

```http
GET /api/v1/rfqs/{id}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "customer_name": "John Smith",
    "company_name": "Example Corp",
    "customer_email": "john@example.com",
    "status": "Pricing"
  }
}
```

---

## POST /rfqs

Creates a new RFQ.

This endpoint is primarily intended for internal workflow integration.

### Request

```json
{
  "customer_name": "John Smith",
  "customer_email": "john@example.com",
  "company_name": "Example Corp"
}
```

### Response

```json
{
  "success": true,
  "message": "RFQ created.",
  "data": {
    "id": "uuid"
  }
}
```

---

## PATCH /rfqs/{id}

Updates editable RFQ fields after human review.

### Request

```json
{
  "customer_name": "Jane Smith",
  "status": "Approved"
}
```

### Response

```json
{
  "success": true,
  "message": "RFQ updated."
}
```

---

# 8. Quotation Endpoints

## GET /quotations/{rfq_id}

Returns the quotation associated with an RFQ.

### Response

```json
{
  "success": true,
  "data": {
    "subtotal": 1200,
    "discount": 100,
    "tax": 110,
    "total": 1210,
    "currency": "USD"
  }
}
```

---

## POST /quotations/calculate

Triggers deterministic quotation calculation.

### Request

```json
{
  "rfq_id": "uuid"
}
```

### Response

```json
{
  "success": true,
  "message": "Pricing completed.",
  "data": {
    "quotation_id": "uuid"
  }
}
```

The pricing engine should always produce deterministic results for identical inputs.
---

# 9. Approval Endpoints

## POST /approvals

Creates a human approval record.

### Request

```json
{
  "rfq_id": "uuid",
  "decision": "Approved",
  "comments": "Pricing verified."
}
```

### Response

```json
{
  "success": true,
  "message": "Approval recorded."
}
```

---

## GET /approvals/{rfq_id}

Returns approval history for an RFQ.

### Response

```json
{
  "success": true,
  "data": [
    {
      "reviewer": "Operations User",
      "decision": "Approved",
      "comments": "Pricing confirmed.",
      "reviewed_at": "2026-07-18T09:30:00Z"
    }
  ]
}
```

---

# 10. Workflow Endpoints

## GET /workflow/{rfq_id}

Returns the workflow history for an RFQ.

### Response

```json
{
  "success": true,
  "data": [
    {
      "previous_status": "Received",
      "new_status": "Extracting",
      "changed_at": "2026-07-18T09:00:00Z"
    },
    {
      "previous_status": "Extracting",
      "new_status": "Validating",
      "changed_at": "2026-07-18T09:01:00Z"
    }
  ]
}
```

---

## POST /workflow/retry

Retries a failed workflow.

### Request

```json
{
  "rfq_id": "uuid"
}
```

### Response

```json
{
  "success": true,
  "message": "Workflow restarted."
}
```

Only workflows in the **Failed** state are eligible for retry.

---

# 11. Health Endpoints

## GET /health

Returns the overall application health status.

### Response

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

---

## GET /health/database

Checks database connectivity.

### Response

```json
{
  "success": true,
  "data": {
    "database": "connected"
  }
}
```

---

## GET /health/openai

Checks connectivity to the OpenAI API.

### Response

```json
{
  "success": true,
  "data": {
    "openai": "available"
  }
}
```

---

# 12. Error Codes

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Validation Failed |
| 500 | Internal Server Error |
| 503 | External Service Unavailable |

The API should use standard HTTP status codes whenever possible.

---

# 13. Validation Rules

Input validation should occur before business logic execution.

Examples include:

| Field | Validation |
|--------|------------|
| customer_email | Valid email format |
| quantity | Greater than zero |
| product_name | Required |
| status | Supported workflow state |
| currency | ISO 4217 format |
| rfq_id | Valid UUID |

Invalid requests return **HTTP 422** with descriptive validation messages.
---

# 14. API Security

Although authentication is outside the MVP scope, the API is designed to support secure production deployment.

## Security Principles

- HTTPS-only communication
- Environment-based secret management
- Server-side API key storage
- Input validation
- Output sanitization
- Rate limiting (future)
- Authentication middleware (future)

Sensitive information must never be exposed to frontend clients.

---

## API Keys

The following secrets should be stored securely:

- OpenAI API Key
- PostgreSQL credentials
- Slack Webhook URL
- SMTP credentials (future)

Secrets should be loaded from environment variables.

---

# 15. Idempotency

Some operations may be retried due to network failures or workflow recovery.

Examples:

- Workflow retries
- RFQ creation
- Notification delivery

Endpoints should avoid creating duplicate resources when receiving repeated identical requests.

Where appropriate, unique identifiers such as `rfq_number` should be used to detect duplicate submissions.

---

# 16. API Logging

Every API request should generate structured logs.

Recommended log fields include:

| Field | Description |
|--------|-------------|
| Request ID | Unique request identifier |
| Endpoint | API route |
| HTTP Method | GET, POST, PATCH, etc. |
| Status Code | Response status |
| Execution Time | Request duration |
| Timestamp | Processing time |
| User | Authenticated user (future) |

Sensitive request data should not be written to logs.

---

# 17. API Integration Flow

The backend coordinates interactions between multiple services.

```text
Frontend
     │
     ▼
FastAPI
     │
 ┌───┼───────────────┐
 ▼   ▼               ▼
DB OpenAI         Pricing Engine
 │                  │
 └──────────┬───────┘
            ▼
          Response
```

FastAPI acts as the orchestration layer between external integrations and internal business services.

---

# 18. API Design Decisions

## AD-001 REST Architecture

**Decision**

Use REST rather than GraphQL.

**Reason**

- Simpler implementation
- Easy integration with n8n
- Familiar tooling
- Lower operational complexity

---

## AD-002 JSON Payloads

**Decision**

Use JSON for all request and response bodies.

**Reason**

- Broad compatibility
- Human-readable format
- Native FastAPI support
- Easy frontend integration

---

## AD-003 Versioned Endpoints

**Decision**

Prefix all endpoints with `/api/v1`.

**Reason**

- Supports backward compatibility
- Simplifies future breaking changes
- Enables gradual API evolution

---

## AD-004 Backend-Centric Logic

**Decision**

Keep business logic on the server.

**Reason**

- Prevents client-side manipulation
- Centralizes validation
- Simplifies maintenance
- Improves security

---

# 19. Conclusion

The REST API provides a clean and extensible interface for the AI-powered RFQ Operations Platform.

By centralizing validation, pricing, workflow coordination, and persistence behind a versioned FastAPI service, the platform ensures consistent communication between the frontend, automation workflows, AI services, and the database.

This API specification establishes the contract that guides implementation, testing, and future system evolution.

---

