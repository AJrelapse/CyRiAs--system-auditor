# Digital Twin-Based Predictive Cyber Risk Assessment System (Frontend)

## Overview

The frontend is a modern **Angular 19** web application that provides an interactive dashboard for monitoring enterprise cybersecurity posture. It visualizes assets, digital twins, knowledge graphs, predictive cyber risks, attack paths, cloud infrastructure, identities, configurations, logs, and risk assessment results through an intuitive user interface.

The application follows a **component-based architecture** with reusable UI components, standalone Angular components, and REST API integration with the FastAPI backend.

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Angular 19 | Frontend Framework |
| TypeScript | Programming Language |
| SCSS | Styling |
| Angular Standalone Components | Modular UI Development |
| Angular Router | Client-side Routing |
| Angular HttpClient | REST API Communication |
| Apache ECharts | Interactive Data Visualization |
| ngx-echarts | Angular Wrapper for ECharts |
| Lucide Angular | SVG Icons |
| RxJS | Reactive Programming |

---

# Frontend Architecture

```
                    +------------------------------+
                    |      Angular Frontend        |
                    +--------------+---------------+
                                   |
                                   |
                           Angular Router
                                   |
            +----------------------+----------------------+
            |                                             |
            ▼                                             ▼
    Dashboard Layout                              Shared Components
            |                                             |
            |                                             |
            ▼                                             ▼
      Feature Pages -----------------------------> REST Services
            |                                             |
            |                                             |
            ▼                                             ▼
      Charts & Tables                          FastAPI Backend APIs
```

---

# Project Structure

```
frontend/
│
├── src/
│
├── app/
│   │
│   ├── layouts/
│   │     └── dashboard-layout/
│   │
│   ├── pages/
│   │     ├── dashboard/
│   │     ├── asset-discovery/
│   │     ├── digital-twin/
│   │     ├── knowledge-graph/
│   │     ├── predictive-risk/
│   │     ├── attack-path/
│   │     ├── risk-assessment/
│   │     ├── cloud/
│   │     ├── identity/
│   │     ├── configuration/
│   │     └── logs/
│   │
│   ├── services/
│   │
│   ├── shared/
│   │     ├── components/
│   │     │      ├── navbar/
│   │     │      ├── sidebar/
│   │     │      └── ui/
│   │     │
│   │     └── models/
│   │
│   ├── app.routes.ts
│   ├── app.config.ts
│   └── app.component.ts
│
├── assets/
│
├── styles.scss
│
├── angular.json
│
├── package.json
│
└── README.md
```

---

# Application Architecture

The frontend follows a **Component-Based Architecture**.

## 1. Layout Layer

Responsible for the overall application structure.

Contains

- Sidebar
- Navbar
- Main Content Area
- Router Outlet

Provides a consistent user experience across all modules.

---

## 2. Routing Layer

Angular Router handles navigation between pages.

Routes include

- Dashboard
- Asset Discovery
- Digital Twin
- Knowledge Graph
- Predictive Risk
- Attack Path
- Risk Assessment
- Cloud
- Identity
- Configuration
- Logs

Each feature is implemented as a standalone Angular component.

---

## 3. Feature Pages

Each page is responsible for a specific cybersecurity module.

### Dashboard

Displays

- Risk Summary
- Asset Statistics
- Security KPIs
- Overall Organizational Risk

---

### Asset Discovery

Displays

- Discovered Assets
- Asset Inventory
- Asset Synchronization Status

---

### Digital Twin

Displays

- Digital Twin Topology
- Infrastructure Relationships
- Asset Summary
- Security Overview

---

### Knowledge Graph

Visualizes

- Assets
- Users
- Cloud Resources
- Vulnerabilities
- Security Controls

using an interactive graph.

---

### Predictive Risk

Displays

- Risk Scores
- Risk Distribution
- Critical Assets
- Risk Progress Indicators

---

### Attack Path

Displays

- Attack Chains
- MITRE ATT&CK Techniques
- Missing Controls
- CVEs
- Risk Scores

---

### Risk Assessment

Displays

- Organizational Risk Assessment
- Overall Security Posture
- Asset Risk Summary

---

### Cloud

Displays

- Cloud Resources
- Cloud Services
- Resource Inventory

---

### Identity

Displays

- Users
- Groups
- Roles
- Permissions

---

### Configuration

Displays

- System Configurations
- Configuration Inventory

---

### Logs

Displays

- Security Events
- Log Statistics
- Event Summary

---

# Shared Components

Reusable components improve consistency and reduce code duplication.

Examples

- Sidebar
- Navbar
- Glass Cards
- KPI Cards
- Status Badges
- Empty States
- Tables
- Chart Containers

---

# REST API Communication

The frontend communicates with the FastAPI backend using Angular HttpClient.

Each feature has its own service responsible for API communication.

Example

```
Dashboard Component
        │
        ▼
Dashboard Service
        │
        ▼
FastAPI Backend
```

---

# Data Flow

```
Angular Component
        │
        ▼
Angular Service
        │
        ▼
HTTP Request
        │
        ▼
FastAPI Backend
        │
        ▼
JSON Response
        │
        ▼
Angular Component
        │
        ▼
UI Rendering
```

---

# UI Features

The application provides

- Interactive Dashboards
- Liquid Glass UI Design
- Responsive Layout
- Dark Theme
- Interactive Charts
- Dynamic Tables
- Animated KPI Cards
- Force-Directed Knowledge Graph
- Digital Twin Visualization
- Responsive Sidebar
- Floating Navigation Bar

---

# Data Visualization

The frontend uses **Apache ECharts** for visual analytics.

Charts include

- Force Graphs
- Bar Charts
- Pie Charts
- Line Charts
- Progress Bars
- Distribution Charts

---

# Prerequisites

Before running the project, install

- Node.js 18+
- npm
- Angular CLI

Verify installation

```bash
node -v
```

```bash
npm -v
```

```bash
ng version
```

---

# Clone the Repository

```bash
git clone <repository-url>
```

```bash
cd frontend
```

---

# Install Dependencies

```bash
npm install
```

---

# Install Additional Packages

If not already installed

```bash
npm install echarts ngx-echarts
```

```bash
npm install lucide-angular lucide
```

---

# Configure Backend URL

Update the API base URL inside the Angular environment or service files.

Example

```typescript
export const environment = {
    production: false,
    apiUrl: "http://localhost:8000"
};
```

Ensure the backend server is running before starting the frontend.

---

# Run the Frontend

```bash
ng serve
```

or

```bash
npm start
```

---

# Development Server

Angular development server

```
http://localhost:4200
```

---

# Build for Production

```bash
ng build
```

The production build will be generated inside

```
dist/
```

---

# Application Modules

The frontend consists of the following modules.

- Dashboard
- Asset Discovery
- Digital Twin
- Knowledge Graph
- Predictive Risk
- Attack Path
- Risk Assessment
- Cloud
- Identity
- Configuration
- Logs

---

# API Integration

The frontend consumes the following backend APIs.

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

# Frontend Workflow

```
User Opens Application
          │
          ▼
Dashboard Layout
          │
          ▼
Sidebar Navigation
          │
          ▼
Feature Module
          │
          ▼
Angular Service
          │
          ▼
REST API Request
          │
          ▼
Backend Response
          │
          ▼
Charts • Tables • Cards
          │
          ▼
Interactive Dashboard
```

---

# Future Enhancements

- Real-time dashboard using WebSockets
- Live threat notifications
- Advanced filtering and search
- Export reports to PDF
- Multi-language support
- Theme customization
- Command Palette (Ctrl + K)
- AI-powered assistant
- Role-Based Access Control (RBAC)
- Mobile-responsive dashboard improvements

---

# Authors

**Digital Twin-Based Predictive Cyber Risk Assessment System for Continuous Information Systems Auditing**

Developed as a modern Angular-based cybersecurity dashboard for visualizing enterprise infrastructure, digital twins, predictive cyber risks, knowledge graphs, attack paths, and continuous information systems auditing.