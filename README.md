# 🔐 Zero-Trust Kubernetes Security Pipeline

![CI Pipeline](https://github.com/sp3640/zero-trust-app/actions/workflows/ci-security.yaml/badge.svg)

A production-grade **supply chain security pipeline** for Kubernetes that 
implements zero-trust principles across 5 security layers.

## 🎯 Problem Solved

Most companies deploy containers without verification — no CVE scanning,
no image signing, no runtime monitoring. This project implements a 
complete security pipeline that:

- **Blocks** vulnerable images before they reach production
- **Proves** image authenticity via cryptographic signing  
- **Enforces** security policies at Kubernetes admission level
- **Detects** runtime threats in real-time

## 🏗️ Architecture

\`\`\`
Developer Push → GitHub Actions CI → GHCR Registry
                      ↓                    ↓
              Trivy CVE Scan          Cosign Signed
              Syft SBOM               Image
              Cosign Sign                  ↓
                                    ArgoCD GitOps
                                          ↓
                              Kubernetes Cluster
                                          ↓
                              OPA Gatekeeper (4 policies)
                                          ↓
                              Running Workload
                                          ↓
                              Falco Runtime Detection
\`\`\`

## 🛡️ Security Layers

| Layer | Tool | What It Does |
|-------|------|-------------|
| 1 | Trivy | CVE scanning + secret detection |
| 2 | Syft | SBOM generation (SPDX format) |
| 3 | Cosign | Keyless image signing via OIDC |
| 4 | OPA Gatekeeper | Admission control policies |
| 5 | Falco | Runtime threat detection |

## ⚡ Demo

### Gatekeeper blocking unauthorized image:
\`\`\`bash
kubectl run test --image=nginx:latest -n default
# Error: Container uses image from untrusted registry
# Error: Container must not run as root
# Error: CPU limit must be set
\`\`\`

### Falco detecting shell spawn:
\`\`\`bash
kubectl exec -it <pod> -n my-app -- /bin/sh
# Falco Alert: CRITICAL - Shell spawned in container
# MITRE ATT&CK: T1059
\`\`\`

## 🔧 Tech Stack

- **App:** Python FastAPI
- **Container:** Docker (multi-stage, non-root)
- **Registry:** GitHub Container Registry (GHCR)
- **CI/CD:** GitHub Actions
- **Scanning:** Trivy (Aqua Security)
- **SBOM:** Syft (Anchore) — SPDX JSON format
- **Signing:** Cosign (Sigstore) — keyless via OIDC
- **Kubernetes:** kind (local), Helm
- **Policies:** OPA Gatekeeper + Rego
- **GitOps:** ArgoCD (app-of-apps pattern)
- **Runtime:** Falco + Falcosidekick

## 📋 Compliance

- ✅ NIST SP 800-218 (SBOM requirement)
- ✅ US Executive Order 14028
- ✅ SLSA Level 2
- ✅ MITRE ATT&CK coverage: T1059, T1041, T1003

## 🚀 Quick Start

\`\`\`bash
# Clone both repos
git clone https://github.com/sp3640/zero-trust-app
git clone https://github.com/sp3640/zero-trust-infra

# Create cluster
kind create cluster --name zero-trust \
  --config zero-trust-app/kind-config.yaml

# Install security tools
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system --create-namespace

kubectl apply -f zero-trust-infra/policies/

helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=modern_ebpf
\`\`\`

## 📊 Results

| Metric | Result |
|--------|--------|
| CI Pipeline duration | ~1 min 9 sec |
| CVEs blocked | 100% CRITICAL |
| Unauthorized images blocked | 100% |
| Runtime alerts | Real-time (<10 sec) |

## 🔗 Related

- [Infrastructure Repo](https://github.com/sp3640/zero-trust-infra)
- [Threat Model](https://github.com/sp3640/zero-trust-infra/blob/main/docs/threat-model.md)
