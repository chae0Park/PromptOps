# 13. Interview Guide

**Project Name**

AI-powered RFQ Operations Platform

---

## Document Information

| Item | Value |
|------|-------|
| Document | Interview Guide |
| Version | v1.0 |
| Status | Final |
| Author | Chaeyoung Park |
| Purpose | Explain the project's business value, technical decisions, architecture, implementation approach, and interview talking points. |

---

# 1. Purpose

This document serves as an interview reference for discussing the AI-powered RFQ Operations Platform.

Rather than focusing only on implementation details, it explains:

- Why the project was built
- Business problems being solved
- Key architectural decisions
- AI integration strategy
- Technical trade-offs
- Potential interview questions and answers

The goal is to demonstrate practical engineering judgment rather than simply presenting a technical demo.

---

# 2. Business Problem

Many manufacturing and trading companies still process quotation requests manually.

A typical workflow involves:

1. Receiving RFQ emails
2. Reading customer requirements
3. Extracting product specifications
4. Calculating pricing
5. Contacting vendors
6. Preparing customer quotations
7. Tracking progress manually

This process is:

- Time-consuming
- Repetitive
- Error-prone
- Difficult to scale

The project automates these operational steps while keeping humans responsible for final approval.

---

# 3. Project Goal

The objective is to build an AI-assisted quotation operations platform that reduces repetitive manual work while maintaining business reliability.

The platform should:

- Automatically process incoming RFQs
- Extract structured information using AI
- Calculate pricing using deterministic business rules
- Generate communication drafts
- Support human review before customer delivery

The result is improved operational efficiency without sacrificing accuracy.

---

# 4. Why AI?

Artificial Intelligence is used only where it provides clear advantages.

Suitable AI tasks include:

- Reading unstructured emails
- Extracting product information
- Summarizing customer requests
- Drafting emails

These tasks involve natural language understanding.

Business-critical pricing decisions remain deterministic and fully controlled by application logic.

---
---

# 5. Why Not Let AI Calculate Pricing?

This is one of the most important architectural decisions in the project.

The pricing engine is intentionally implemented using deterministic Python logic instead of an LLM.

Reasons include:

- Pricing must be reproducible.
- Business rules require consistency.
- Customers expect predictable quotations.
- Pricing decisions should be auditable.
- AI hallucinations are unacceptable in financial calculations.

AI assists with understanding information, while deterministic code performs business calculations.

This separation improves reliability and aligns with enterprise software engineering best practices.

---

# 6. Why Use n8n?

The project uses n8n as the workflow orchestration platform.

Advantages include:

- Visual workflow management
- Rapid automation development
- Easy API integrations
- Email automation
- Slack integration
- Human approval steps
- Future workflow extensibility

Instead of embedding workflow logic inside application code, orchestration is handled independently through n8n.

This separation keeps the backend focused on business logic.

---

# 7. Why FastAPI?

FastAPI was selected because it provides:

- High performance
- Automatic API documentation
- Strong typing
- Easy integration with Python
- Excellent support for AI-related services

It also simplifies integration between the pricing engine and AI extraction service.

---

# 8. Why Next.js?

Next.js provides several advantages for internal business applications.

These include:

- Modern React architecture
- Fast development experience
- TypeScript support
- Component reusability
- Efficient routing
- Easy deployment through Vercel

The frontend primarily serves internal operations users rather than external customers.

---

# 9. Why PostgreSQL?

PostgreSQL is used because it provides:

- Strong relational consistency
- ACID transactions
- Mature ecosystem
- Excellent indexing
- Reliable production performance

Quotation processing requires structured relationships between customers, RFQs, pricing, and workflow status.

A relational database is therefore the most appropriate choice.
---

# 10. Why Human Review?

Although AI automates much of the workflow, the final quotation is always reviewed by a human operator.

Human approval provides:

- Business accountability
- Error detection
- Customer-specific adjustments
- Compliance with internal policies

This approach follows the principle of **Human-in-the-Loop (HITL)**, which is widely adopted in enterprise AI systems.

---

# 11. Why Separate AI from Business Logic?

The architecture intentionally separates AI capabilities from deterministic business logic.

```text
Customer Email
      │
      ▼
OpenAI
(Extraction)
      │
      ▼
Structured Data
      │
      ▼
Python Business Rules
(Pricing)
      │
      ▼
Human Review
      │
      ▼
Quotation
```

Benefits include:

- Easier testing
- Predictable system behavior
- Reduced AI risk
- Independent upgrades for AI and business rules
- Better maintainability

This modular design also allows future replacement or comparison of AI models without affecting core business functionality.

---

# 12. Key Technical Decisions

| Decision | Reason |
|----------|--------|
| FastAPI | Python ecosystem and AI integration |
| Next.js | Modern frontend development |
| PostgreSQL | Reliable relational database |
| n8n | Workflow orchestration |
| OpenAI API | Natural language understanding |
| Deterministic Pricing | Business consistency |
| Human Approval | Operational safety |
| Docker | Portable workflow deployment |
| Vercel + Render | Simple cloud deployment |

Each technology was selected based on practical operational requirements rather than novelty.

---

# 13. Scalability Strategy

The MVP is intentionally simple but designed for future growth.

Potential scaling strategies include:

- Horizontal API scaling
- Queue-based workflow processing
- Multiple AI providers
- Distributed workflow workers
- Database read replicas
- Redis caching
- Kubernetes deployment

The modular architecture minimizes changes required as system usage increases.
---

# 14. Potential Interview Questions

The following questions are commonly asked when discussing AI-enabled business applications.

---

## Q1. Why did you build this project?

**Suggested Answer**

I wanted to demonstrate how AI can automate repetitive business operations rather than simply generating text.

Many companies receive RFQs by email and spend significant time extracting requirements, calculating prices, drafting responses, and coordinating with vendors. This project streamlines that workflow while ensuring critical business decisions remain deterministic and reviewable.

---

## Q2. Why didn't you let AI calculate pricing?

**Suggested Answer**

Pricing affects revenue and customer trust, so it must be consistent, explainable, and reproducible.

AI is excellent at interpreting unstructured text, but deterministic business logic is more appropriate for financial calculations.

Separating AI from pricing improves reliability and reduces operational risk.

---

## Q3. Why use n8n instead of implementing everything in Python?

**Suggested Answer**

Workflow orchestration is fundamentally different from business logic.

n8n provides visual automation, simplifies integrations with external services, and allows workflows to evolve without modifying backend code.

This separation improves maintainability and accelerates future workflow changes.

---

## Q4. What was the most challenging part?

**Suggested Answer**

The most important challenge was deciding where AI should—and should not—be used.

Rather than maximizing AI usage, I focused on assigning AI to language understanding tasks while keeping business-critical decisions deterministic.

This architectural boundary significantly improves system reliability.

---

## Q5. How would you improve the system?

**Suggested Answer**

Possible future improvements include:

- Confidence-based routing
- Multi-model AI evaluation
- Vendor recommendation
- Advanced analytics
- Queue-based processing
- Multi-user authentication
- Approval history
- Infrastructure auto-scaling

The current architecture already supports these enhancements without major redesign.

---

# 15. Key Takeaways

This project demonstrates several practical software engineering principles:

- AI should augment—not replace—business logic.
- Deterministic systems remain essential for critical operations.
- Human approval increases trust and accountability.
- Modular architecture improves maintainability.
- Workflow orchestration should remain independent of application logic.
- Cloud-native services simplify deployment and scaling.

These principles are applicable across many enterprise AI applications beyond quotation management.

---

# 16. Final Project Summary

The AI-powered RFQ Operations Platform is an end-to-end business automation solution that combines modern web technologies, workflow orchestration, deterministic business logic, and large language models.

The project showcases the ability to:

- Design production-oriented system architectures
- Integrate AI responsibly into business workflows
- Build scalable APIs
- Develop modern frontend applications
- Automate operational processes
- Balance AI capabilities with deterministic software engineering
- Deliver maintainable, enterprise-ready solutions

Rather than presenting AI as the solution to every problem, the project demonstrates thoughtful engineering decisions about where AI creates value and where traditional software design remains the better choice.

---
