---
id: arc42-07
title: Deployment view
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0002
  - bb-pyodide-worker
  - bb-flask-server
  - bb-lambda
---

# 7. Deployment view

Where the software runs. Production choice among the three is TBD ([arc42-01](01-introduction-and-goals.md)).

## Content to write

- **Pyodide static zip:** GitHub release; any static file server; wheels in the UI bundle; cite `.github/workflows/deploy-ui.yml`.
- **`amanzi-server`:** Flask on port 7331, serves `ui/dist`, opens browser unless `--no-browser`.
- **AWS Lambda:** Docker image `lambda/Dockerfile`, same `AmanziAPI`.
- CI: user docs and architecture docs zip artifacts; UI deploy workflow.
- TBD: operator of demo host, TLS, RTO/RPO, which backend demo uses.

## Diagrams

```mermaid
flowchart LR
  subgraph pyodideNode [PyodideZip]
    staticFiles[StaticUI]
    worker[PyodideWorker]
  end
  subgraph flaskNode [DevServer]
    flask[AmanziServer]
    vite[ViteDev]
  end
  subgraph lambdaNode [AWS]
    gw[APIGateway]
    fn[LambdaFunction]
  end
  designer[Designer] --> staticFiles
  designer --> vite
  vite --> flask
  designer --> gw
  gw --> fn
```
