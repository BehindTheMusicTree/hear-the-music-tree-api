---
paths:
  - "hear/**/*.py"
---

# Private resource filtering

Queries and mutations for private user-owned resources must be scoped to the authenticated owner before data is returned or changed. Reuse the repository and api-kit authorization/queryset helpers; do not trust a client-provided user identifier. Confirm indexes and query plans from the actual schema rather than assuming filter keyword order controls index use. Public reference resources may use their documented access policy.
