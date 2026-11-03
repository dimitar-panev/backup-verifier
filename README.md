# Info before starting
- This whole repo is part of my SAP Mentorship program that will be 3 months long in total so I will be contributing quite often. During those 3 months every week I will have a meet with my mentor where we will be discussing my work, what I have done, any questions that I have and problems that I have stumbled upon between every week. My mentor is I.CH.

# What the Tool Does
- Every night, Backup Verifier automatically executes a 7-step verification pipeline:
- Finds the newest backup (restic snapshot or PostgreSQL database dump).
- Checks backup age (RPO) to ensure it is recent enough.
- Checks file integrity to confirm the backup archive is not damaged.
- Restores into a sandbox (an isolated temporary directory/volume).
- Verifies real data inside the sandbox (e.g., checks that specific files exist or queries a temporary PostgreSQL database to verify tables contain rows).
- Measures restore duration (RTO) from start to finish.
- Reports OK or FAILED, exporting metrics to a dashboard and sending an email notification via Postfix if a check fails.

# I Decided to track the most important stuff by with two important metrics:
RPO (Recovery Point Objective): How much data could be lost (measured by the age of the newest backup).
RTO (Recovery Time Objective): How long it takes to recover (measured by total restore duration).

# The project is bult across three layers
- The Tool: A Python 3.12 CLI application that performs the 7-step verification locally or in a container.
- The Automation: Containerized with Docker, tested and scanned via GitHub Actions CI/CD, and scheduled nightly in Kubernetes via GitOps (ArgoCD).
- The Eyes (Observability): Metrics exported to Prometheus & Grafana, with failure alerts routed through Alertmanager and Postfix (SMTP).

# The full stack that I am planning to use is this:

|        Category       |                       Tools & Technologies                       |
|:---------------------:|:----------------------------------------------------------------:|
| Workspace             | Git, GitHub, VS Code                                             |
| Core Application      | Python 3.12, Typer, Pydantic, PyYAML, psycopg, prometheus-client |
| Backup Targets        | restic, PostgreSQL                                               |
| Testing & Quality     | pytest, ruff, Intentionally Broken Backups                       |
| Containers            | Docker (via OrbStack), Docker Hub                                |
| CI/CD & Security      | GitHub Actions, Gitleaks, Trivy, Syft (SBOM)                     |
| Kubernetes            | Kubernetes (k3d), kubectl, k9s                                   |
| Deployment & GitOps   | Helm, ArgoCD, Sealed Secrets, Terraform (optional)               |
| Monitoring & Alerting | Pushgateway, Prometheus, Grafana, Alertmanager, Postfix (Email)  |
| Documentation         | Markdown, Mermaid, MkDocs (GitHub Pages)                         |

