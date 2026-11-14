# Research Analyst Multi-Agent Assistant

A coursework implementation for the even-roll-number Research Analyst Agents problem statement. It uses FastAPI, Agno, Groq, a local sample-document library, a browser interface, Docker, Docker Compose, Kubernetes examples, and GitHub Actions CI.

## Architecture

The Agno Team is configured with exactly three collaborating agents in coordinate mode:

1. **Query Analyzer** – classifies the request and extracts focused research questions.
2. **Research Agent** – searches the local sample-document library using `search_library`.
3. **Answer Reviewer** – reviews evidence and produces a structured answer.

The local library is deliberately small and illustrative. It is not an internet search engine or an authoritative source database. The application displays a disclaimer to make that limitation clear.

## Requirements

- Python 3.10+
- A Groq API key: https://console.groq.com/keys
- Docker Desktop (for container execution)

## Run locally on Windows PowerShell

```powershell
# Open this folder in VS Code / PowerShell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

# Create your local environment file
Copy-Item .env.example .env
# Edit .env and replace the placeholder with your Groq API key

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:
- Web application: http://127.0.0.1:8000/
- Swagger API documentation: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health

## Test

```powershell
pytest -v
```

The tests cover the home page, health endpoint, request validation, and local library search. They do not make paid/live Groq API calls.

## Docker

Create `.env` first and configure `GROQ_API_KEY`, then:

```powershell
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f
```

Open http://localhost:8000/. Stop with:

```powershell
docker compose down
```

The image includes a Docker health check. Compose passes configuration from `.env` into the container. Do not put API keys in the Dockerfile or commit `.env`.

## Kubernetes examples

These manifests are optional deployment examples and require a working Kubernetes cluster and an image available to that cluster.

```powershell
kubectl apply -f k8s/configmap.yaml
# Create a real secret locally; do not apply the placeholder secret to production.
kubectl create secret generic research-analyst-secret --from-literal=GROQ_API_KEY=YOUR_REAL_KEY
docker build -t research-analyst:1.0 .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods,svc
```

For a local cluster, make sure the cluster can access the image or push it to a registry and update the deployment image.

## CI/CD

`.github/workflows/ci.yml` runs pytest and builds the Docker image on pushes and pull requests. It does not push the image to a registry or deploy automatically.

## API

### `GET /health`

Returns application health, model configuration, Groq configuration status, and the three agent names. It never returns the API key.

### `POST /ask`

Request:

```json
{
  "question": "What are good practices for evaluating a machine learning classification model?"
}
```

The response contains status, question, answer, consulted sample source titles, and a disclaimer.

## Important notes

- The first run requires a valid Groq API key and internet access to reach Groq.
- The model identifier is configurable through `GROQ_MODEL`.
- The assignment handout mentions `llama-3.3-70b-versatile`; model availability can change at the provider. If Groq reports that the model is unavailable, use a currently supported model ID from your Groq Console and update `.env`.
- This is an educational research assistant, not professional legal, medical, or financial advice.
