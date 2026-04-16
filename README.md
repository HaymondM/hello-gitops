# hello-gitops
A CI/CD pipeline demo using GitHub Actions, Helm, and ArgoCD to continuously deploy a containerized app to Kubernetes.

## Architecture
git push → GitHub Actions (lint, test, build, push image) → values.yaml updated with SHA tag → ArgoCD detects change → syncs Helm chart → app updated in cluster

## Prerequisites
- Docker
- [kind](https://kind.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/) (optional)

## Running Locally

**Local dev (Windows):**
```powershell
flask --app app run
```

**Local dev (Linux/Mac):**
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

**Docker:**
```bash
docker build -t hello-gitops .
docker run -p 5000:5000 hello-gitops
```

The app will be available at `http://localhost:5000`.

## Local Setup

### 1. Create a kind cluster
```bash
kind create cluster --name hello-gitops --image kindest/node:v1.31.0
```

### 2. Install the nginx ingress controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.0/deploy/static/provider/kind/deploy.yaml
```

Add the required node label:
```bash
kubectl label node hello-gitops-control-plane ingress-ready=true
```

Wait for it to be ready:
```bash
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
```

### 3. Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait for it to be ready:
```bash
kubectl wait --namespace argocd --for=condition=ready pod --selector=app.kubernetes.io/name=argocd-server --timeout=120s
```

Get the admin password:

**Linux/Mac:**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Windows (PowerShell):**
```powershell
$encoded = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($encoded))
```

Access the ArgoCD UI:
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Open `https://localhost:8080` and login with username `admin` and the password from above.

### 4. Deploy the app with ArgoCD
```bash
kubectl apply -f argocd/application.yaml
```

ArgoCD will automatically sync and deploy the app. Verify in the UI or run:
```bash
kubectl get pods
```

### 5. Access the app
```bash
kubectl port-forward service/hello-gitops 9090:80
```
Open `http://localhost:9090` in your browser.

## CI/CD Pipeline

### CI — GitHub Actions
Triggered on every push to `main`:
1. Lint with flake8
2. Run pytest tests
3. Build and push Docker image to ghcr.io with two tags: `latest` and `sha-<commit>`
4. Automatically update `helm/hello-gitops/values.yaml` with the new SHA tag and commit back to the repo

### CD — ArgoCD
ArgoCD watches this repo and automatically syncs when it detects changes to the Helm chart or `values.yaml`. Every deployment is tied to an exact commit SHA for full traceability.

## Multi-Environment Strategy
This demo uses a single environment. In a production setup the recommended approach is:
- Separate `values-staging.yaml` and `values-prod.yaml` per environment
- Separate ArgoCD `Application` manifests per environment
- An App-of-Apps pattern to manage all environments from a single ArgoCD root application
- Separate config repo from app repo to keep automated commits out of application code

## Security Considerations
- Container runs as a non-root user
- Flask debug mode is disabled — Gunicorn is used as the production WSGI server
- Liveness and readiness probes configured in the Helm chart
- Image tagged by git SHA for full audit trail and easy rollback
- In a production environment would add: image scanning (Trivy), RBAC on ArgoCD service accounts, sealed secrets or external secrets operator, network policies, and a private registry with pull secrets

## Repository Structure
```text
hello-gitops/
├── app.py                          # Flask application
├── test.py                         # pytest tests
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container image definition
├── .github/workflows/ci.yml        # GitHub Actions CI pipeline
├── helm/hello-gitops/              # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
├── argocd/
│   └── application.yaml            # ArgoCD Application manifest
└── README.md
```

## Known Limitations & What I'd Improve
- **Local image caching** — kind caches images locally and does not automatically pull updated remote images. This was resolved by having CI automatically update `values.yaml` with the exact SHA tag after each build, forcing ArgoCD to detect a real change and pull the new image. In a real cloud environment (EKS, GKE) this is not an issue as nodes pull directly from the registry.
- **CI pipeline depth** — the current pipeline covers linting, testing, building, and pushing. In a production setup would add: image vulnerability scanning, dependency scanning, container signing, and automated rollback on failed deployments.
- **CI writing back to repo** — having CI commit back to the app repo is a known antipattern. The cleaner approach is a separate GitOps config repo or using ArgoCD Image Updater.
- **Single environment** — multi-environment support would use separate values files and ArgoCD Application manifests per environment.
- **No secret management** — would add sealed secrets or external secrets operator in production.

## Resources Consulted
- [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- [kind Ingress Setup](https://kind.sigs.k8s.io/docs/user/ingress/)
- [GitHub Actions Docker Guide](https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-docker-images)
- [Helm Documentation](https://helm.sh/docs/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/stable/deploying/)