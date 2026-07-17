# 01. Project Overview

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | Project Overview |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Define the overall vision, business objective, product scope, and high-level architecture of the platform. |

---

# 1. Executive Summary

The AI-powered RFQ Operations Platform is an internal operational system designed to automate repetitive quotation processing workflows while maintaining human oversight over business-critical decisions.

The platform receives quotation requests (RFQs) through email, extracts structured information using Large Language Models (LLMs), validates the extracted data, calculates pricing through deterministic business logic, and prepares quotation drafts for human review before customer delivery.

Rather than replacing operational staff, the system functions as an AI-assisted operations platform that reduces manual work, minimizes processing time, and improves quotation consistency.

The project demonstrates how modern AI capabilities can be integrated into existing business workflows without sacrificing reliability, traceability, or operational control.

---

# 2. Problem Statement

Many organizations still process quotation requests manually.

A typical quotation workflow includes:

- Reading customer emails
- Identifying requested products
- Extracting quantities and specifications
- Looking up pricing tables
- Applying pricing rules
- Preparing quotation documents
- Sending confirmation emails
- Recording the transaction internally

Although each individual task is simple, the entire workflow requires significant manual effort and introduces opportunities for human error.

Common operational issues include:

- Manual transcription mistakes
- Missing quotation information
- Inconsistent pricing calculations
- Slow response times
- Limited process visibility
- Repetitive administrative work

As quotation volume increases, these inefficiencies become increasingly expensive.

---

# 3. Product Vision

Create an AI-assisted quotation operations platform that combines:

- Intelligent document understanding
- Deterministic pricing logic
- Human approval workflows
- Business process automation

The platform should enable operations teams to spend less time on repetitive administrative work while maintaining complete control over pricing decisions.

---

# 4. Product Goal

The primary goal of this project is **not** to fully automate quotation generation.

Instead, the goal is to build a production-oriented operational workflow where AI accelerates repetitive tasks while humans remain responsible for final business decisions.

Success is achieved when AI becomes an operational assistant rather than an autonomous decision maker.

---

# 5. Target Users

## Primary User

Operations Specialist

Responsibilities include:

- Reviewing incoming RFQs
- Validating extracted information
- Confirming quotation accuracy
- Approving quotation drafts
- Sending finalized quotations

---

## Secondary User

Sales Representative

Responsibilities include:

- Reviewing quotation history
- Monitoring quotation status
- Following up with customers
- Accessing approved quotations

---

## Administrator

Responsibilities include:

- Managing pricing rules
- Monitoring workflow execution
- Reviewing system logs
- Managing user permissions
- Maintaining reference data

---

# 6. Product Scope

The MVP focuses on a single quotation workflow from email intake to quotation approval.

Included features:

- RFQ email ingestion
- AI-based information extraction
- Structured data validation
- Deterministic pricing calculation
- Human approval interface
- Draft email generation
- Slack notification
- Database persistence

The following capabilities are intentionally excluded from the MVP:

- ERP integration
- Inventory synchronization
- Automatic quotation approval
- Customer portal
- Vendor portal
- Multi-language quotation generation
- Analytics dashboards
- Golden Set evaluation framework

These features may be considered in future iterations but are outside the scope of this version.

---

# 7. Design Principles

The platform follows several core engineering principles.

## AI assists humans

AI generates recommendations.

Humans make business decisions.

---

## Deterministic business logic

Business rules such as pricing calculations must remain deterministic and fully explainable.

LLMs are never responsible for calculating quotation prices.

---

## Human-in-the-loop

Every quotation must receive human approval before customer communication.

No quotation is sent automatically.

---

## Traceability

Every workflow step should be observable.

System actions must be logged for debugging, auditing, and operational review.

---

## Modularity

Each component should operate independently.

Examples include:

- Email ingestion
- Information extraction
- Pricing engine
- Human review
- Notification service

This architecture allows future replacement or expansion without affecting the entire platform.

---

# 8. High-Level Workflow

The quotation workflow consists of the following stages:

1. Customer sends RFQ email.
2. Email is received by the platform.
3. LLM extracts structured quotation information.
4. Validation rules verify extracted fields.
5. Python pricing engine calculates quotation values.
6. Human reviews quotation.
7. Draft customer email is generated.
8. Slack notification is sent.
9. Approved quotation is stored in PostgreSQL.

---

# 9. High-Level System Architecture

The MVP consists of six major components that work together to automate quotation processing while maintaining human oversight.

```text
                Customer
                    │
                    ▼
          RFQ Email Received
                    │
                    ▼
               n8n Workflow
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 OpenAI Information        Validation Rules
    Extraction                  Engine
        │                       │
        └───────────┬───────────┘
                    ▼
          Python Pricing Engine
                    │
                    ▼
             PostgreSQL Database
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
   Next.js Review UI      Slack Notification
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

Each component has a clearly defined responsibility and communicates through well-defined interfaces.

---

# 10. Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | Next.js + TypeScript |
| Backend API | FastAPI |
| Workflow Automation | n8n |
| Database | PostgreSQL (Supabase) |
| AI Model | OpenAI API |
| Pricing Logic | Python |
| Notifications | Slack |
| Deployment | Vercel + Render + Docker |

The technology stack is intentionally lightweight while remaining representative of a modern production architecture.

---

# 11. AI Responsibilities

Artificial Intelligence is responsible for tasks involving language understanding and content generation.

These include:

- Reading customer emails
- Extracting structured RFQ information
- Summarizing quotation requests
- Generating quotation email drafts
- Assisting human operators during review

The AI model is **not** responsible for making business decisions.

---

# 12. Deterministic Responsibilities

Business-critical logic is implemented using deterministic Python code.

Examples include:

- Pricing calculation
- Discount rules
- Margin calculation
- Validation rules
- Required field verification
- Business rule enforcement

This ensures that quotation results remain reproducible, explainable, and auditable.

---

# 13. Human Responsibilities

Human operators remain responsible for all final business decisions.

Required approval activities include:

- Reviewing extracted RFQ information
- Correcting extraction errors
- Verifying calculated prices
- Approving quotation content
- Sending quotations to customers

The system intentionally prevents fully autonomous quotation delivery.

---

# 14. Expected Benefits

The platform is designed to provide measurable operational improvements.

Expected benefits include:

- Reduced quotation processing time
- Lower manual data entry effort
- More consistent quotation quality
- Improved operational traceability
- Reduced human transcription errors
- Faster customer response times
- Easier onboarding for new operations staff

Although exact performance metrics depend on the business environment, the architecture is intended to scale without significantly increasing operational workload.

---

# 15. Future Expansion Opportunities

The MVP establishes a foundation for future enhancements.

Potential future capabilities include:

- ERP integration
- CRM integration
- Vendor quotation automation
- Inventory synchronization
- Multi-language quotation generation
- Customer self-service portal
- Advanced analytics dashboard
- AI-assisted negotiation support
- Automated quotation comparison
- Golden Set evaluation framework
- Prompt version management
- Cost and latency monitoring
- AI quality evaluation dashboard

These features are intentionally excluded from the MVP to maintain a focused and achievable initial release.

---

# 16. Success Criteria

The MVP will be considered successful if it satisfies the following objectives:

- RFQ emails can be processed end-to-end through the workflow.
- Structured quotation information is successfully extracted using AI.
- Pricing calculations are performed exclusively through deterministic business logic.
- Human approval is required before customer communication.
- All workflow events are stored in PostgreSQL.
- Slack notifications are delivered successfully.
- The platform can be deployed using the selected cloud infrastructure.
- The architecture is modular enough to support future expansion.

---

# 17. Conclusion

The AI-powered RFQ Operations Platform demonstrates how generative AI can be integrated into real business operations without replacing deterministic software engineering principles.

Rather than allowing AI to make business decisions, the platform positions AI as an operational assistant that accelerates repetitive work while preserving human oversight, system transparency, and business reliability.

This document serves as the foundation for all subsequent technical specifications, including system architecture, database design, API definitions, workflow automation, testing strategy, deployment, and future roadmap.

---

