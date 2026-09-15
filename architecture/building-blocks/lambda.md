---
id: bb-lambda
title: Lambda
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0002
  - bb-amanzi-api
  - arc42-07
---

# Lambda

AWS Lambda adapter around the same `AmanziAPI`.

## Content to write

- **Paths:** `lambda/lambda_function.py`, `lambda/Dockerfile`.
- **In:** API Gateway events mapped to API methods.
- **Out:** same payloads as Flask.
- Build/deploy notes remain in `lambda/README.md` (ops, not this site’s tutorials).
- **Owner:** TBD.
