# Digital Twin-Based Predictive Cyber Risk Assessment System (Backend)

## Overview

The backend is a **FastAPI-based REST API** that powers the Digital Twin-Based Predictive Cyber Risk Assessment System for Continuous Information Systems Auditing.

It continuously collects data from multiple enterprise sources, constructs a digital twin of the organization's IT infrastructure, generates a cybersecurity knowledge graph, predicts cyber risks, identifies attack paths, and performs automated risk assessment.

The backend follows a **layered architecture** to ensure modularity, scalability, and maintainability.

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| Python 3.11+ | Backend Language |
| SQLAlchemy | ORM |
| PostgreSQL | Relational Database |
| Pydantic | Request & Response Validation |
| Uvicorn | ASGI Server |
| NetworkX | Knowledge Graph Generation |
| Scikit-learn | Predictive Risk Model |
| Pandas | Data Processing |
| NumPy | Numerical Computation |

---

# System Architecture

```
                +----------------------+
                |   Angular Frontend   |
                +----------+-----------+
                           |
                           |
                     REST API Calls
                           |
                           ▼
+-----------------------------------------------------------+
|                     FastAPI Backend                        |
|-----------------------------------------------------------|
| Routes (Controllers)                                      |
|-----------------------------------------------------------|
| Business Logic (Services)                                 |
|-----------------------------------------------------------|
| Digital Twin Engine                                       |
| Knowledge Graph Engine                                    |
| Predictive Risk Engine                                    |
| Attack Path Generator                                     |
| Risk Assessment Engine                                    |
|-----------------------------------------------------------|
| SQLAlchemy ORM                                            |
|-----------------------------------------------------------|
| PostgreSQL Database                                       |
+-----------------------------------------------------------+
```

---

# Project Structure

```
backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │     ├── asset_routes.py
│   │     ├── cloud_routes.py
│   │     ├── configuration_routes.py
│   │     ├── identity_routes.py
│   │     ├── log_routes.py
│   │     ├── digital_twin_routes.py
│   │     ├── knowledge_graph_routes.py
│   │     ├── predictive_risk_routes.py
│   │     ├── attack_path_routes.py
│   │     └── risk_assessment_routes.py
│   │
│   ├── services/
│   │     ├── asset_service.py
│   │     ├── cloud_service.py
│   │     ├── configuration_service.py
│   │     ├── identity_service.py
│   │     ├── log_collection_service.py
│   │     ├── digital_twin_service.py
│   │     ├── knowledge_graph_service.py
│   │     ├── predictive_risk_service.py
│   │     ├── attack_path_service.py
│   │     └── risk_assessment_service.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── database/
│   │
│   ├── utils/
│   │
│   └── config/
│
├── requirements.txt
│
└── README.md
```

---

# Architecture

The backend follows a **Layered Architecture**.

## 1. Routes Layer

Responsible for exposing REST endpoints.

Responsibilities:

- Receive HTTP requests
- Validate request parameters
- Call business services
- Return API responses

Example

```
GET /assets/discover

POST /digital-twin/build

POST /predictive-risk/predict
```

---

## 2. Service Layer

Contains the complete business logic.

Responsibilities

- Asset discovery
- Configuration collection
- Log aggregation
- Cloud synchronization
- Identity synchronization
- Digital Twin generation
- Knowledge Graph construction
- Risk prediction
- Attack path generation
- Risk assessment

This layer is completely independent of the API layer.

---

## 3. Database Layer

Implemented using SQLAlchemy ORM.

Responsibilities

- CRUD Operations
- Transactions
- Database Mapping
- Query Optimization

Database used:

```
PostgreSQL
```

---

## 4. Digital Twin Engine

Constructs a virtual representation of the enterprise infrastructure.

The digital twin contains:

- Assets
- Users
- Identities
- Cloud Resources
- Vulnerabilities
- Security Controls
- Network Relationships

---

## 5. Knowledge Graph Engine

Transforms the digital twin into a graph structure.

Nodes include:

- Assets
- Vulnerabilities
- Users
- Security Controls
- Cloud Resources
- Attack Techniques

Relationships include:

- CONNECTS_TO
- HAS_ACCESS
- MEMBER_OF
- EXPLOITABLE_BY
- MITIGATES
- ADMIN_ACCESS

NetworkX is used for graph generation.

---

## 6. Predictive Risk Engine

Calculates the cyber risk score for each asset based on:

- Vulnerability Count
- Open Ports
- Criticality
- Missing Security Controls
- Behavioral State
- Historical Security Events

Outputs

- Low Risk
- Medium Risk
- High Risk
- Critical Risk

---

## 7. Attack Path Generator

Generates possible attack paths through the enterprise network.

Each path includes

- Entry Point
- Intermediate Assets
- Target Asset
- CVEs
- MITRE ATT&CK Techniques
- Missing Controls
- Overall Risk Score

---

## 8. Risk Assessment Engine

Aggregates all information from:

- Digital Twin
- Knowledge Graph
- Predictive Risk
- Attack Paths

Generates the final organizational cyber risk assessment.

---

# Backend Workflow

```
Data Collection
        │
        ▼
Asset Discovery
        │
        ▼
Configuration Collection
        │
        ▼
Cloud Synchronization
        │
        ▼
Identity Synchronization
        │
        ▼
Log Collection
        │
        ▼
Digital Twin Construction
        │
        ▼
Knowledge Graph Generation
        │
        ▼
Predictive Risk Analysis
        │
        ▼
Attack Path Generation
        │
        ▼
Risk Assessment
        │
        ▼
REST API Response
```

---

# API Modules

The backend consists of the following modules.

- Dashboard
- Asset Discovery
- Configuration Management
- Cloud Infrastructure
- Identity Management
- Log Collection
- Digital Twin
- Knowledge Graph
- Predictive Risk
- Attack Path
- Risk Assessment

---

# Prerequisites

Before running the project, install:

- Python 3.11 or later
- PostgreSQL
- pgAdmin (Optional)
- Git

Verify installation

```bash
python --version
```

or

```bash
python3 --version
```

---

# Clone the Repository

```bash
git clone <repository-url>
```

```bash
cd backend
```

---

# Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

# Activate the Virtual Environment

### Windows (Command Prompt)

```bash
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### Git Bash

```bash
source venv/Scripts/activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Once activated, your terminal should display:

```
(venv)
```

---

# Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file in the project root.

Example

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/cyber_risk
```

Update the credentials according to your PostgreSQL installation.

---

# Create PostgreSQL Database

Open PostgreSQL or pgAdmin and create a new database.

Example

```
cyber_risk
```

---

# Run Database Migrations

If using Alembic

```bash
alembic upgrade head
```

If migrations are not used, create the tables using your project's initialization script.

---

# Start the Backend Server

```bash
uvicorn app.main:app --reload
```

If your `main.py` is located elsewhere, update the module path accordingly.

---

# Server Information

Default server

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# Example API Endpoints

## Assets

```
GET /assets/discover
GET /assets/inventory
POST /assets/synchronize
```

## Configurations

```
GET /configurations/collect
GET /configurations/inventory
POST /configurations/synchronize
```

## Cloud

```
GET /cloud/state
GET /cloud/resources
POST /cloud/synchronize
```

## Identity

```
GET /identities/state
GET /identities/inventory
POST /identities/synchronize
```

## Logs

```
GET /logs/collect
GET /logs/events
GET /logs/summary
POST /logs/ingest
```

## Digital Twin

```
POST /digital-twin/build
GET /digital-twin/current
POST /digital-twin/synchronize
GET /digital-twin/snapshots
GET /digital-twin/changes
```

## Knowledge Graph

```
POST /knowledge-graph/build
GET /knowledge-graph/graph
```

## Predictive Risk

```
POST /predictive-risk/predict
```

## Attack Path

```
POST /attack-path/generate
```

## Risk Assessment

```
POST /risk-assessment/assess
```

---

# Stopping the Server

Press

```
CTRL + C
```

Deactivate the virtual environment

```bash
deactivate
```

---

# Future Enhancements

- Real-time streaming using WebSockets
- SIEM integration
- Azure AD integration
- AWS Security Hub integration
- Container security monitoring
- Continuous compliance auditing
- AI-powered threat intelligence
- Multi-tenant architecture
- Role-Based Access Control (RBAC)

---
