# PromptOps

Prompt evaluation and operations platform.

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