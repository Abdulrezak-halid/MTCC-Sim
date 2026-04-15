<img width="1536" height="1024" alt="Multi-tier call center simulation overview" src="https://github.com/user-attachments/assets/ae268d7c-18d9-425e-81f3-9fe6da3711ca" />

# Multi-Tier Call Center Simulation Diagram

A simulation of how customer requests flow through a multi-level support system, including classification, routing, escalation, and resolution.

---

## Entry Point

- **Customer Call (Inbound)**
  - Phone / Chat

- **IVR & Auto-Router**
  - Classifies requests by issue type
  - Routes calls to appropriate queue

---

## Tier 1 — Front-Line Agents

Handles basic and common issues.

- **Agent A**
  - General inquiries
  - Password resets

- **Agent B**
  - Order tracking
  - Basic troubleshooting

- **Agent C**
  - Billing questions
  - Account updates

✅ Possible Outcomes:
- Issue resolved
- Escalation to Tier 2

---

## Tier 2 — Specialists

Handles more complex and technical issues.

- **Tech Specialist**
  - Complex issues
  - Deep diagnostics

- **Billing Specialist**
  - Disputes & refunds
  - Fraud review

- **Product Expert**
  - Configuration & setup
  - Compatibility issues

✅ Possible Outcomes:
- Issue resolved
- Escalation to Tier 3 (critical cases)

---

## Tier 3 — Expert Engineers / Management

Handles critical, system-level, or policy-related issues.

- **Engineering Team**
  - Bug fixes
  - System outages

- **Management**
  - Policy decisions
  - Escalation handling

- **Vendor / Third-Party Support**
  - External system issues

✅ Possible Outcomes:
- Issue resolved
- Critical resolution

---

## Flow Summary

1. Customer initiates request
2. IVR classifies and routes
3. Tier 1 handles basic issues
4. Tier 2 handles complex issues
5. Tier 3 handles critical/system-level issues

---

## Resolution States

- ✅ Resolved at Tier
- 🔼 Escalated to next Tier
- 🚨 Critical escalation

<p align="center" width="1536" height="1024">
  <img src="https://github.com/user-attachments/assets/dd09e3e4-26ce-4040-8581-73a38be1e06e" width="600"/>
</p>
