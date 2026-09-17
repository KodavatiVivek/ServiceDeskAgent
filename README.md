# Enterprise Service Desk Agent Platform

A microservices-based AI-assisted IT service desk platform that intelligently routes support requests, retrieves approved knowledge, executes authorized service actions, and maintains auditable records of all decisions.

KJOE
Modifyinh redame fie for testing
## 🎯 Product Vision

Empower IT support teams with an intelligent agent that:
- **Answers** IT service desk questions with approved knowledge and best practices
- **Contextualizes** responses using ServiceNow incident data and historical resolutions
- **Executes** authorized service actions (ticket creation, account unlock, password reset)
- **Governs** access through role-based controls and approval workflows
- **Audits** all decisions for compliance and operational intelligence

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Service Topology](#service-topology)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Request Lifecycle](#request-lifecycle)
- [Knowledge Domains](#knowledge-domains)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Development](#development)
- [Roadmap](#roadmap)
- [Known Limitations](#known-limitations)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Make (for convenience commands)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/KodavatiVivek/ServiceDeskAgent.git
cd ServiceDeskAgent

# Start all services
make up

# Verify services are running
curl http://localhost:8000/health

# View logs
make logs

# Stop all services
make down
```

### First Request

```bash
curl -X POST http://localhost:8000/api/v1/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "How do I troubleshoot CyberArk password checkout failure?",
    "user_id": "user123",
    "user_role": "l1_support",
    "incident_id": "INC0010001"
  }'
```

Expected Response:
```json
{
  "correlation_id": "uuid-here",
  "answer": "This looks like a PAM/CyberArk support issue. Based on the available SOP or KB context, the recommended next steps are: ...",
  "domain": "security",
  "sub_domain": "pam",
  "sources": [
    {"title": "CyberArk Safe Membership Guide", "source": "data/pam/safe_membership.txt", "score": 0.75}
  ],
  "tool_results": []
}
```

---

## 🏗️ Architecture Overview

The platform uses a **service-oriented architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PUBLIC GATEWAY (8000)                      │
│         Single entry point for all external requests              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR SERVICE (8001)                     │
│  Central workflow coordinator: planning, guardrails, sequencing   │
└────────────┬────────────────┬──────────────────┬────────────────┘
             │                │                  │
    ┌────────▼────┐  ┌───────▼───────┐  ┌──────▼────────┐
    │ RAG Service │  │ Tool Service  │  │ Audit Service │
    │    (8002)   │  │    (8003)     │  │    (8005)     │
    └─────────────┘  └───────────────┘  └───────────────┘
             │
    ┌────────▼────────────┐
    │ Ingestion Service   │
    │      (8004)         │
    └─────────────────────┘
```

### Design Principles

✅ **Service Independence** — Each service owns its domain and can scale independently  
✅ **Clear Boundaries** — Well-defined internal APIs for service-to-service communication  
✅ **Graceful Degradation** — Failures in RAG or tools do not block user responses  
✅ **Audit Trail** — Every decision is recorded with correlation IDs  
✅ **Role-Based Access** — RBAC enforced at the tool execution boundary  

---

## 🔧 Service Topology

| Service | Port | Exposure | Responsibility |
|---------|------|----------|-----------------|
| **Gateway** | 8000 | Public | Request validation, correlation ID, response schema |
| **Orchestrator** | 8001 | Internal | Workflow orchestration, planner, guardrails, response assembly |
| **RAG** | 8002 | Internal | Domain-routed keyword retrieval, document ranking |
| **Tool** | 8003 | Internal | RBAC enforcement, tool dispatch, external adapter calls |
| **Ingestion** | 8004 | Internal | Document ingestion, chunking, embedding (placeholder) |
| **Audit** | 8005 | Internal | Event storage, compliance logging, audit trail |

---

## 📡 API Documentation

### Public API: `/api/v1/agent/ask`

**Endpoint:** `POST /api/v1/agent/ask`

**Request Schema:**
```json
{
  "user_query": "string (required)",
  "user_id": "string (optional, defaults to 'anonymous')",
  "user_role": "string (optional, defaults to 'employee')",
  "incident_id": "string (optional, for ServiceNow context)"
}
```

**Response Schema:**
```json
{
  "correlation_id": "uuid string",
  "answer": "natural language response",
  "domain": "security | network | cloud | application | general",
  "sub_domain": "pam | iam | vpn | aws | azure | crm | general",
  "sources": [
    {
      "title": "document title",
      "source": "source path or url",
      "score": 0.0 to 1.0
    }
  ],
  "tool_results": [
    {
      "tool_name": "string",
      "status": "success | failed",
      "data": "tool-specific response"
    }
  ]
}
```

**Example Queries:**

| Query | Domain | Sub-Domain | Tools Called |
|-------|--------|-----------|--------------|
| "How do I troubleshoot CyberArk password checkout?" | security | pam | rag_search |
| "Account locked after failed MFA" | security | iam | rag_search, servicenow_fetch_incident |
| "VPN connection fails" | network | vpn | rag_search |
| "Create an incident for cloud access issue" | cloud | cloud | rag_search, servicenow_create_incident |
| "Unlock my account" | security | iam | servicenow_fetch_incident, avatier_unlock_account (requires approval) |

### Internal APIs

#### RAG Service: `/internal/rag/search`
```json
POST /internal/rag/search
{
  "query": "user query text",
  "domain": "security",
  "sub_domain": "pam",
  "top_k": 5,
  "user_context": {"user_id": "...", "role": "..."},
  "correlation_id": "uuid"
}
```

#### Tool Service: `/internal/tools/execute`
```json
POST /internal/tools/execute
{
  "tool_name": "servicenow_fetch_incident",
  "payload": {"incident_id": "INC0010001", ...},
  "user_context": {"user_id": "...", "role": "..."},
  "correlation_id": "uuid"
}
```

#### Audit Service: `/internal/audit/events`
```json
GET /internal/audit/events
# Returns last 50 audit events

POST /internal/audit/events
{
  "event_type": "agent_request_completed",
  "correlation_id": "uuid",
  "user_id": "user123",
  "planner_decision": {...},
  "metadata": {...}
}
```

---

## 👥 User Roles & Permissions

The platform supports 5 predefined roles with escalating permissions:

```
┌────────────┬──────────────────┬────────────────┬─────────────────────┐
│ Role       │ ServiceNow Read   │ ServiceNow     │ Sensitive Actions   │
│            │                  │ Write          │ (Avatier, CRM)      │
├────────────┼──────────────────┼────────────────┼─────────────────────┤
│ employee   │ ✅               │ ❌             │ ❌                  │
│ l1_support │ ✅               │ ✅             │ ❌                  │
│ l2_support │ ✅               │ ✅             │ ❌                  │
│ manager    │ ✅               │ ✅             │ ✅ (requires appr.) │
│ admin      │ ✅               │ ✅             │ ✅ (requires appr.) │
└────────────┴──────────────────┴────────────────┴─────────────────────┘
```

### Role Descriptions

- **employee**: Read-only access to ServiceNow (view incidents, knowledge base)
- **l1_support**: Can create and update tickets, troubleshoot with KB
- **l2_support**: Same as l1_support, escalation authority for complex issues
- **manager**: Write access + sensitive actions (account unlock, password reset)
- **admin**: Full platform access, all tool permissions

⚠️ **Security Note:** Role is currently accepted from the request body and must be replaced with authenticated claims in production (see [Known Limitations](#known-limitations)).

---

## 🔄 Request Lifecycle

### Step-by-Step Flow

```
1. CLIENT REQUEST
   └─> POST /api/v1/agent/ask with user_query, user_role, incident_id

2. GATEWAY SERVICE
   └─> Generate correlation_id
   └─> Validate request schema
   └─> Forward to orchestrator with 60-second timeout

3. ORCHESTRATOR SERVICE
   └─> Input guardrails check (block prompt injection patterns)
   └─> Run simple_planner to classify intent, domain, and needed tools
   
4. CONDITIONAL: RETRIEVAL
   If retrieval_required:
   └─> Call RAG Service with domain/sub_domain metadata
   └─> Retrieve up to 5 relevant documents
   └─> If RAG fails, include synthetic "service unavailable" document
   
5. CONDITIONAL: INCIDENT CONTEXT
   If incident_id detected:
   └─> Call Tool Service: servicenow_fetch_incident
   └─> Retrieve incident details (state, priority, work notes)
   
6. CONDITIONAL: TOOL EXECUTION
   For each selected_tool (except *_retriever markers):
   └─> Check RBAC via Tool Service
   └─> If allowed, execute tool (ServiceNow, Avatier, CRM)
   └─> If role mismatch, return permission denied
   └─> If tool fails, append error to tool_results and continue
   
7. ANSWER GENERATION
   └─> Template-based response assembly
   └─> Include domain-specific opening
   └─> Append top 3 retrieved documents (truncated to ~240 chars)
   └─> Add ServiceNow status if incident fetched
   └─> Add approval warning if approval_required
   
8. OUTPUT GUARDRAILS
   └─> Current: no-op (placeholder for PII redaction, secret scanning)
   
9. AUDIT
   └─> Emit agent_request_completed event with correlation_id
   └─> Store planner decision and tool results
   
10. RESPONSE
    └─> Return AgentAskResponse to client
    └─> Hide planner_decision from public response
```

### Error Handling

- **Gateway failures**: Return HTTP 502 with exception detail
- **RAG unavailable**: Return synthetic "RAG service unavailable" document
- **Tool failures**: Append to tool_results and continue
- **Audit failures**: Log silently; never fail user response
- **Input guardrail violation**: Return HTTP 400 Bad Request

---

## 📚 Knowledge Domains

The platform currently supports 5 support domains with hard-coded knowledge:

### 1. Security / PAM
**Keywords:** cyberark, pam, password checkout, vault, safe membership

**Documents:**
- CyberArk Safe Membership Guide
- Password Checkout Escalation Matrix
- CPM Troubleshooting Guide

**Example Query:** "How do I resolve CyberArk safe membership issues?"

### 2. Security / IAM
**Keywords:** iam, account locked, mfa, password reset

**Documents:**
- IAM Account Recovery Procedures

**Example Query:** "My account is locked after MFA failure"

### 3. Network
**Keywords:** vpn, dns, firewall, proxy

**Documents:**
- VPN Setup and Troubleshooting Guide

**Example Query:** "VPN connection keeps dropping"

### 4. Cloud
**Keywords:** aws, azure, cloud

**Documents:**
- Cloud Access SOP

**Example Query:** "How do I provision AWS access?"

### 5. Application / CRM
**Keywords:** crm, app, application, offboarding

**Documents:**
- CRM Offboarding Runbook

**Example Query:** "CRM access for new hire"

---

## 🐳 Deployment

### Docker Compose

All services are containerized and orchestrated via `docker-compose.yml`:

```bash
# Build and start all services
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f [service-name]

# Stop all services
docker compose down

# Remove volumes (reset state)
docker compose down -v
```

### Service Dependencies

```
gateway-service
  └─> depends_on: orchestrator-service (via HTTP)

orchestrator-service
  └─> depends_on: rag-service (via HTTP)
  └─> depends_on: tool-service (via HTTP)
  └─> depends_on: audit-service (via HTTP)

ingestion-service
  └─> independent (called ad-hoc)
```

### Network Configuration

- **Exposed to Host:** Gateway on port 8000
- **Internal Only:** All other services communicate via container names
- **Example internal URL:** `http://orchestrator-service:8001/internal/orchestrate`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Service URLs (for local Docker)
ORCHESTRATOR_URL=http://orchestrator-service:8001
RAG_SERVICE_URL=http://rag-service:8002
TOOL_SERVICE_URL=http://tool-service:8003
AUDIT_SERVICE_URL=http://audit-service:8005

# Azure OpenAI (not yet implemented)
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# ServiceNow (mocked currently)
SERVICENOW_BASE_URL=https://your-instance.service-now.com
SERVICENOW_USERNAME=your-username
SERVICENOW_PASSWORD=your-password

# Avatier (mocked currently)
AVATIER_BASE_URL=https://avatier-instance.com
AVATIER_API_KEY=your-api-key

# CRM (mocked currently)
CRM_BASE_URL=https://crm-instance.com
CRM_API_KEY=your-api-key
```

### Service Configuration

Each service has its own `app/config.py`:

- **Gateway**: `ORCHESTRATOR_URL`
- **Orchestrator**: `RAG_SERVICE_URL`, `TOOL_SERVICE_URL`, `AUDIT_SERVICE_URL`
- **RAG**: `vector_backend` (defaults to "keyword"; future: "azure_ai_search")
- **Tool**: RBAC rules defined in middleware
- **Audit**: In-memory storage (future: persistent)

---

## 👨‍💻 Development

### Project Structure

```
ServiceDeskAgent/
├── services/
│   ├── gateway-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── api/
│   │   │   │   ├── routes.py
│   │   │   │   └── health.py
│   │   │   ├── clients/
│   │   │   │   └── orchestrator_client.py
│   │   │   └── schemas/
│   │   │       ├── request.py
│   │   │       └── response.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── orchestrator-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   │   ├── routes.py
│   │   │   │   └── health.py
│   │   │   ├── planner/
│   │   │   │   ├── planner.py
│   │   │   │   └── schemas.py
│   │   │   ├── guardrails/
│   │   │   │   ├── input_guardrails.py
│   │   │   │   └── output_guardrails.py
│   │   │   ├── answer/
│   │   │   │   └── generator.py
│   │   │   ├── clients/
│   │   │   │   ├── rag_client.py
│   │   │   │   ├── tool_client.py
│   │   │   │   └── audit_client.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── rag-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   │   ├── routes.py
│   │   │   │   └── health.py
│   │   │   ├── retrievers/
│   │   │   │   ├── base.py
│   │   │   │   ├── pam_retriever.py
│   │   │   │   ├── iam_retriever.py
│   │   │   │   ├── network_retriever.py
│   │   │   │   ├── cloud_retriever.py
│   │   │   │   └── app_retriever.py
│   │   │   ├── registry/
│   │   │   │   └── domain_registry.py
│   │   │   ├── schemas/
│   │   │   │   ├── search_request.py
│   │   │   │   └── search_response.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── tool-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   │   ├── routes.py
│   │   │   │   └── health.py
│   │   │   ├── middleware/
│   │   │   │   └── rbac_check.py
│   │   │   ├── servicenow/
│   │   │   │   └── tools.py
│   │   │   ├── avatier/
│   │   │   │   └── tools.py
│   │   │   ├── crm/
│   │   │   │   └── tools.py
│   │   │   ├── registry/
│   │   │   │   └── tool_registry.py
│   │   │   ├── schemas/
│   │   │   │   └── tool_request.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── audit-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   │   ├── routes.py
│   │   │   │   └── health.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── ingestion-service/
│       ├── app/
│       │   ├── main.py
│       │   ├── api/
│       │   │   ├── routes.py
│       │   │   └── health.py
│       │   └── config.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── libs/
│   ├── common/
│   │   ├── correlation.py
│   │   └── http_client.py
│   └── schemas/
│       └── README.md
│
├── data/
│   ├── pam/
│   │   ├── cyberark_checkout_sop.txt
│   │   └── (other PAM docs)
│   ├── iam/
│   │   ├── account_unlock.txt
│   │   └── (other IAM docs)
│   ├── network/
│   │   ├── vpn_sop.txt
│   │   └── (other network docs)
│   ├── cloud/
│   │   ├── access_sop.txt
│   │   └── (other cloud docs)
│   └── app/
│       ├── crm_offboarding.txt
│       └── (other app docs)
│
├── tests/
│   ├── README.md
│   └── (test files coming)
│
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_planner.py -v

# Run with coverage
pytest --cov=services tests/
```

⚠️ **Note:** Test suite is currently a placeholder (`tests/README.md` only).

### Development Workflow

1. **Edit code** in any service directory
2. **Restart services** with `make down && make up`
3. **View logs** with `make logs` or `make logs orchestrator-service`
4. **Test endpoints** with curl or Postman

### Common Make Commands

```bash
make up          # docker compose up --build
make down        # docker compose down
make logs        # docker compose logs -f
make test        # python -m pytest tests
```

---

## 🛣️ Roadmap

The platform evolves in 6 phases from scaffold to production-ready:

### Phase 1: Harden Scaffold ✅ (Current)
- ✅ Fix planner phrase/routing mismatches
- ✅ Add comprehensive test suite
- ✅ Implement trusted authentication layer
- ✅ Validate source file consistency
- ✅ Add structured error handling

### Phase 2: Real ServiceNow Read Path
- Fetch incident details before retrieval
- Implement similar-incident search
- Normalize incident fields for RAG
- Incident-aware knowledge retrieval
- Audit read operations

### Phase 3: Production RAG
- Connect ingestion pipeline (PDF, SharePoint)
- Generate embeddings with approved model
- Deploy Azure AI Search or vector backend
- ACL-based filtering per user role
- Citation and source anchoring

### Phase 4: LLM Answer Synthesis
- Azure OpenAI client integration
- Prompt template management
- Groundedness validation
- PII/secret redaction guardrails
- Model telemetry and token metrics

### Phase 5: Controlled Write Actions
- Real ServiceNow write adapters
- Avatier/CRM integration
- Approval workflow state machine
- Idempotency keys and rollback
- Compensation rules

### Phase 6: Operational Readiness
- Persistent audit (SQL/CosmosDB)
- App Insights/Log Analytics integration
- Dashboards and alerting
- SLO targets and monitoring
- Load testing and security testing
- CI/CD automation

---

## ⚠️ Known Limitations

### Critical (Must Fix Before Production)

1. **Client-Controlled Role**
   - **Issue:** `user_role` is accepted from request body and trusted
   - **Risk:** Caller can claim any role (employee → admin bypass)
   - **Fix:** Implement OAuth2/OIDC; derive role from signed JWT claims

2. **No Real Approval Workflow**
   - **Issue:** `approval_required` is planner metadata only; no enforcement
   - **Risk:** Sensitive actions (password reset, disable) execute without approval
   - **Fix:** Implement approval state machine with signed approval tokens

3. **Mock Enterprise Integrations**
   - **Issue:** ServiceNow, Avatier, CRM return synthetic data
   - **Risk:** No real incident fetch, account unlock, or password reset
   - **Fix:** Implement authenticated adapters with retries and timeouts

4. **No Output Guardrails**
   - **Issue:** Output guardrails are a no-op placeholder
   - **Risk:** Responses may contain PII, secrets, or false information
   - **Fix:** Add PII redaction, secret scanning, grounding validation

### High Priority

5. **Volatile Audit Storage**
   - **Issue:** Audit events are in-memory; lost on restart
   - **Risk:** No audit trail for compliance
   - **Fix:** Persist events to SQL/CosmosDB; secure audit APIs

6. **Phrase Matching Failures**
   - **Issue:** "create a ticket" doesn't match "create ticket" phrase
   - **Risk:** Common user phrases fail to trigger correct tools
   - **Fix:** Use intent classification or normalized regex patterns

7. **VPN + MFA Routing**
   - **Issue:** IAM rule (with MFA) evaluates before network rule
   - **Risk:** VPN questions misclassified as IAM
   - **Fix:** Implement weighted scoring or intent classifier

8. **Incident Context Not Used**
   - **Issue:** RAG retrieval runs on original query; incident details ignored
   - **Risk:** KB retrieval misses context from incident description
   - **Fix:** Fetch incident first; enrich query before retrieval

### Medium Priority

9. **Missing Source Files**
   - **Issue:** Four hard-coded document paths do not exist
   - **Risk:** Inconsistent source-of-truth
   - **Fix:** Validate source existence in build; sync actual files

10. **No Similar-Incident Search**
    - **Issue:** Tool is in RBAC matrix but not implemented
    - **Risk:** Missing valuable historical resolution context
    - **Fix:** Implement ServiceNow search adapter

11. **Tool Failures Not Surfaced**
    - **Issue:** Failed tools appended to results; answer ignores them
    - **Risk:** User doesn't know action failed
    - **Fix:** Generate explicit failure response with next steps

12. **No Automated Tests**
    - **Issue:** Test suite contains only README
    - **Risk:** Regressions not caught; integration breaks on changes
    - **Fix:** Add unit, contract, integration, and e2e tests

### Low Priority

13. **Duplicated HTTP Client Code**
    - **Issue:** Services each implement POST helpers; shared lib unused
    - **Fix:** Standardize with tracing and retry logic

14. **Unused Configuration**
    - **Issue:** `vector_backend` and `DOMAIN_INDEXES` unused
    - **Fix:** Either implement or remove until needed

### Not Yet Implemented (Future Phases)

- Azure OpenAI integration (variables exist; not used)
- LangChain or LangGraph orchestration
- Vector embeddings and semantic retrieval
- PDF/SharePoint ingestion pipeline
- Container health checks and restart policies
- Distributed tracing (OpenTelemetry)
- Metrics and observability

---

## 🔐 Security Considerations

### Current State (Scaffold)
- ✅ RBAC enforced at tool boundary
- ✅ Input guardrails block known injection patterns
- ✅ Correlation IDs enable audit trail
- ❌ No authentication
- ❌ No encrypted inter-service communication
- ❌ No audit access control

### Production Recommendations
1. **Authentication**: Implement OAuth2/OIDC with trusted identity provider
2. **Authorization**: Derive roles from JWT claims; validate on every request
3. **Encryption**: TLS/HTTPS for all service-to-service communication
4. **Audit Encryption**: Encrypt audit records at rest
5. **Secret Management**: Use Azure Key Vault for credentials
6. **Rate Limiting**: Implement per-user/per-role rate limits
7. **Secrets Scanning**: Add output guardrail to prevent secret leakage
8. **PII Redaction**: Redact personally identifiable information in responses

---

## 📞 Support & Contributing

### Reporting Issues
Please open GitHub issues with:
- Clear title describing the problem
- Steps to reproduce
- Expected vs. actual behavior
- Relevant logs/stack traces

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make changes and add tests
4. Submit a pull request

---

## 📄 License

[Add your license here, e.g., MIT, Apache 2.0]

---

## 📚 Additional Resources

- [Architecture Deep Dive](docs/architecture.md) — Detailed service design
- [API Reference](docs/api-reference.md) — Complete endpoint documentation
- [Deployment Guide](docs/deployment.md) — Production setup
- [Security Policy](SECURITY.md) — Security practices and vulnerability reporting
- [Planner Rules](docs/planner-rules.md) — Intent classification logic

---

## 🤝 Acknowledgments

Built with FastAPI, Pydantic, Docker, and Python for enterprise IT service delivery.

---

**Last Updated:** September 15, 2026  
**Current Version:** 0.1.0 (Scaffold Phase)  
**Status:** Active Development — Production Roadmap In Progress
