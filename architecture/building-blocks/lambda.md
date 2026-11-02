---
id: bb-lambda
title: Lambda
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0002
  - bb-amanzi-api
  - arc42-07
---

# Lambda

AWS Lambda adapter around the same `AmanziAPI`. Decision: [adr-0002](../decisions/0002-dual-execution-backends.md). Deployment context: [arc42-07](../07-deployment-view.md).

## Repository

- `lambda/lambda_function.py` — handler
- `lambda/Dockerfile` — image
- `lambda/README.md` — build command for operators. That file is not a user tutorial and is not copied here.

## Interface

`handler(event, context)` splits `event['path']` on `/` and takes segment index 2 as the method name (`lambda/lambda_function.py`). For a path `/api/solve/<scenario>` that segment is `solve`, and the next segment is the scenario index. `design` also reads the model uid from the following segment. The body is `json.loads(event['body'])` for `solve`, `report`, and `design`.

| Method segment | API call |
| --- | --- |
| `parameters` | `api.parameters()` |
| `keyfigures` | `api.keyfigures()` |
| `solve` | `api.solve(body, scenario)` |
| `design` | `api.design(body, scenario, model)` |
| `report` | `api.report(body)` |
| `version` | contents of `VERSION` in the image (not an `AmanziAPI` method) |

Success is HTTP 200 with `Access-Control-Allow-Origin: *`. A Python exception is HTTP 500 and `str(e)` as the body.

Payloads for the five API methods match Flask, because both call `amanzi/server/api.py`. The SPA reaches Lambda only when it is configured as the server backend (`VITE_BACKEND=server` and `VITE_SERVER_URL` pointing at the gateway). Which deployed URL that is, is **TBD**.

## Owner

**TBD.**
