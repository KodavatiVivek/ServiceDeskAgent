# Enterprise Service Desk Agent Platform

This scaffold implements the agreed architecture:

- One public endpoint exposed through `gateway-service`
- Internal services behind the gateway
- `orchestrator-service` owns the agent workflow
- `rag-service` owns domain retrieval
- `tool-service` owns ServiceNow, Avatier, and CRM tool execution
- `ingestion-service` owns document ingestion
- `audit-service` owns audit events and observability hooks

## Public endpoint

```http
POST /api/v1/agent/ask
```

Only `gateway-service` exposes a public port.

## First local run

From the project root:

```bash
docker compose up --build
```

Then test:

```bash
curl -X POST http://localhost:8000/api/v1/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "How do I troubleshoot CyberArk password checkout failure?",
    "user_id": "u123",
    "user_role": "l1_support"
  }'
```

ServiceNow context test:

```bash
curl -X POST http://localhost:8000/api/v1/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "Analyze INC123456 and suggest next steps",
    "user_id": "u123",
    "user_role": "l1_support",
    "incident_id": "INC123456"
  }'
```

Ticket creation test:

```bash
curl -X POST http://localhost:8000/api/v1/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "My CyberArk password checkout failed. Create a ticket.",
    "user_id": "u123",
    "user_role": "l1_support"
  }'
```

## Architecture

```text
Existing Application
        |
        v
Gateway Service
        |
        v
Orchestrator Service
        |
        +---------------------+
        |                     |
        v                     v
RAG Service             Tool Service
        |                     |
        v                     v
Vector/Search           ServiceNow / Avatier / CRM

Ingestion Service -> Vector/Search
Audit Service <- All services
```

## Build order

1. Gateway service
2. Orchestrator service
3. RAG service with PAM retrieval
4. Tool service with ServiceNow read tools
5. Tool service with ServiceNow write tools
6. Avatier tools
7. Approval and RBAC
8. Ingestion service
9. Audit and observability
10. Azure VM deployment with Docker Compose
