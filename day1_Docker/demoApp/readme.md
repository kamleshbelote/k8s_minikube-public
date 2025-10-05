# Day 1 - Docker / Demo App

This directory contains materials for Day 1: building and running a small FastAPI demo app and preparing a Docker image for Minikube.

## Demo app location

- `demoApp/` - FastAPI demo application

## Run the demo FastAPI app (local)

From the `demoApp` directory (`day1_Docker/demoApp`) you can create a virtual environment, install dependencies, and start the app with Uvicorn.

1) Create and activate a venv, then install requirements:

```bash
cd day1_Docker/demoApp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

2) Start Uvicorn in the background (logs written to `uvicorn.log`):

```bash
nohup .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
```

3) Verify the server (run these in another terminal):

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/healthz
curl http://127.0.0.1:8000/readiness
curl -I http://127.0.0.1:8000/static/favicon.svg
```

4) View logs:

```bash
tail -f uvicorn.log
```

5) Stop the background server (find PID and kill):

```bash
ps aux | grep uvicorn
kill <PID>
```

## Next steps

- Build a Docker image for the demo app and load it into Minikube.
- Create Kubernetes manifests (Deployment, Service) to run the app inside Minikube.

## Files included

- `requirements.txt` - Python dependencies for the app (FastAPI, Uvicorn)
- `Dockerfile` - Image build instructions (used to build an image for Minikube or Docker Hub)

## Quick Docker build

From the `day1_Docker/demoApp` directory you can build a local Docker image:

```bash
docker build -t yourusername/demoapp:latest .
```

Replace `yourusername` with your Docker Hub username if you plan to push the image to Docker Hub.

---

Notes:
- The demo app serves a few endpoints: `/`, `/healthz`, `/readiness`, and a static `favicon.svg` at `/static/favicon.svg`.
- If you prefer to run Uvicorn in the foreground for debugging, omit `nohup` and the trailing `&`.