# Backup Verifier

**Do your backups actually work? Let's find out every night.**

Most of us create backups and then forget about them. Then the day comes when we need one, and it turns out to be corrupted, empty, or three weeks old. A backup that has never been restored is only a hope.

Backup Verifier turns that hope into proof. Every night it takes your latest backup, restores it into a throwaway sandbox, checks that the data is real, and tells you whether it is OK or FAILED. If something breaks, you hear about it on Telegram within minutes.

# Some additional information before proceeding: 
- This whole repo is part of my SAP Mentorship program that will be 3 months long in total so I will be contributing quite often. During those 3 months every week I will have a meet with my mentor where we will be discussing my work, what I have done, any questions that I have and problems that I have stumbled upon between every week. My mentor is I.CH.

## Running in Kubernetes

The verifier is built to run as a nightly Kubernetes CronJob. Here is the short version of the delivery chain:

- You push code, and GitHub Actions lints, tests, scans, and builds the image.
- The new image tag is written to a separate gitops repository, and ArgoCD updates the cluster by itself.

When the temporary PostgreSQL is needed, it runs as a sidecar container in the same pod. This keeps the Docker socket out of the picture, which is a good thing for security.

## Tech stack

Everything here is free and runs on my laptop with 16 GB of RAM.

- **Code:** Python 3.12 with Typer, Pydantic, and pytest
- **Backups and data:** restic and PostgreSQL
- **Packaging:** Docker and Kubernetes, packaged with Helm and deployed by ArgoCD
- **Quality and security:** GitHub Actions, Trivy, Gitleaks, and Syft

## Roadmap

This project grows in layers, and each layer works on its own.

- **Weeks 1 to 3:** the core command line tool, unit tests, a Docker image, CI, and the broken-backup fixtures.
- **Weeks 4 to 7:** PostgreSQL support, then Kubernetes with Helm, Terraform, and GitOps through ArgoCD.
- **Weeks 8 and 9:** Prometheus, Grafana, and Telegram alerts, followed by security hardening.
- **Weeks 10 to 12:** real homelab data, a disaster recovery drill, and the 1.0.0 release.

## A note on security

Never commit passwords, tokens, or restic keys. Secrets belong in Sealed Secrets inside Kubernetes and in GitHub Actions secrets during CI. The verifier only needs read access to your backups, and it runs as a non-root user with CPU and memory limits. Since this repository is public, use example data only. Real client data and real device configs stay out.

## License

MIT. See the `LICENSE` file for details.

## I will constantly be updating and expanding the information here(the README) and add additional stuff.
