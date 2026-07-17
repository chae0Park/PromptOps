# AI-powered RFQ Operations Platform

> An AI-assisted quotation operations platform that automates RFQ processing using LLM-powered information extraction, deterministic pricing logic, workflow automation, and human-in-the-loop approval.

---

## Overview

This project demonstrates how Large Language Models (LLMs) can be integrated into real-world business operations while maintaining deterministic business logic for critical decision-making.

The platform automates the quotation process from receiving an RFQ email to generating quotation drafts, while ensuring pricing calculations remain reliable, auditable, and fully controlled by business rules.

The project is designed as a production-oriented MVP following modern software engineering practices.

---

## Key Features

- 📧 Automated RFQ email intake
- 🤖 AI-powered information extraction
- ✅ Structured data validation
- 💰 Deterministic Python pricing engine
- 👨‍💼 Human-in-the-loop quotation approval
- 📄 Automatic customer quotation draft generation
- 🏭 Vendor inquiry draft generation
- 🔔 Slack notifications
- 🗄 PostgreSQL data persistence
- 🔄 Workflow automation using n8n

---

## System Architecture

```text
Customer Email
       │
       ▼
     n8n Workflow
       │
       ▼
OpenAI Extraction
       │
       ▼
Structured RFQ Data
       │
       ▼
FastAPI Backend
       │
       ▼
Pricing Engine (Python)
       │
       ▼
Human Review Dashboard
       │
       ▼
Quotation Approval
       │
       ▼
Customer / Vendor Email Drafts
       │
       ▼
Slack Notification
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Next.js + TypeScript |
| Backend | FastAPI |
| Database | PostgreSQL (Supabase) |
| AI | OpenAI API |
| Workflow | n8n |
| Deployment | Vercel + Render + Docker |
| Version Control | GitHub |

---

## Structure

```
PromptOps/
├── app/           # Application core
│   ├── api/       # API endpoints
│   ├── services/  # Business logic
│   ├── database/  # Database layer
│   ├── models/    # Data models
│   └── utils/     # Utilities
├── dashboard/     # Dashboard UI
├── evaluation/    # Evaluation pipelines
├── golden_sets/   # Golden test sets
├── reports/       # Generated reports
├── tests/         # Tests
├── docs/          # Documentation
└── data/          # Data files
```


---

## Documentation

Comprehensive project documentation is available in the `docs/` directory.

| Document |
|----------|
| 01. Overview |
| 02. Product Requirements |
| 03. User Flow |
| 04. System Architecture |
| 05. Database Design |
| 06. API Specification |
| 07. UI / UX Design |
| 08. AI & Pricing Engine |
| 09. n8n Workflows |
| 10. Testing Strategy |
| 11. Deployment |
| 12. Development Roadmap |
| 13. Interview Guide |

---


## Overview

PromptOps is an internal AI Operations Evaluation Platform designed to help product teams evaluate LLM outputs, compare prompt versions, detect regressions, and manage AI quality through human-in-the-loop workflows.

## Features

- Golden Set Manager
- Prompt Playground
- Evaluation Engine
- Prompt Versioning
- Regression Detection
- Human Review
- Evaluation Dashboard
- Automatic Report Generation

## Tech Stack

- Python
- FastAPI
- Streamlit
- OpenAI API
- SQLite
- Plotly

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-rfq-platform.git

cd ai-rfq-platform
```

---

### 2. Install Dependencies

Frontend

```bash
cd frontend

npm install
```

Backend

```bash
cd backend

pip install -r requirements.txt
```

Workflow

```bash
docker compose up -d
```

---

### 3. Configure Environment Variables

Create the required `.env` files.

Example:

```text
DATABASE_URL=

OPENAI_API_KEY=

SLACK_WEBHOOK_URL=

NEXT_PUBLIC_API_URL=
```

---

### 4. Start Development

Frontend

```bash
npm run dev
```

Backend

```bash
uvicorn app.main:app --reload
```

n8n

```bash
docker compose up
```

---

## Development Principles

This project follows several important engineering principles.

### Human-in-the-Loop

AI assists decision making.

Humans approve business-critical outputs.

---

### Deterministic Business Logic

LLMs are used only for language understanding.

Pricing calculations remain deterministic Python code.

---

### Modular Architecture

Each service is independently deployable.

- Frontend
- Backend API
- Workflow Engine
- Database
- AI Service

---

### Production-Oriented Design

The architecture prioritizes:

- Maintainability
- Reliability
- Scalability
- Testability

rather than maximizing AI usage.

---

## Future Improvements

Potential future enhancements include:

- Multi-model AI comparison
- Confidence scoring
- Vendor recommendation engine
- Approval workflow management
- Analytics dashboard
- Multi-user authentication
- Queue-based processing
- Kubernetes deployment
- Infrastructure as Code
- Advanced monitoring

---

## AI Usage Disclosure

This project was designed and implemented with AI assistance.

Large Language Models were used to support:

- Architecture brainstorming
- Documentation drafting
- Code generation
- Refactoring
- Development acceleration

Final architectural decisions, implementation strategy, business logic design, and technical validation were performed by the project author.

---

## License

This repository is intended for educational and portfolio purposes.

Feel free to explore the architecture and implementation ideas.

---

## Author

**Chaeyoung Park**

AI Workflow Automation • Technical Operations • AI-assisted Software Engineering

---

> **"AI should automate repetitive work—not replace deterministic business logic."**

---

