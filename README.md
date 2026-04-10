# hello-gitops
A CI/CD pipeline demo using GitHub Actions, Helm, and ArgoCD to continuously deploy a containerized app to Kubernetes.

## Flask Web App

This repository includes a simple Flask web application that responds with "Hello world" to HTTP GET requests.

### Setup

1. Ensure you have Python installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the App

**Windows:**
```powershell
flask --app app run
```

**Linux/Mac:**
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

The app will start on `http://localhost:5000`. Visit the root URL (`/`) to see "Hello world".

### Docker

Build and run the containerized app:
```
docker build -t hello-world-app .
docker run -p 5000:5000 hello-world-app
```

### Troubleshooting

- If you encounter import errors, ensure Flask and gunicorn are installed via `pip install -r requirements.txt`.
- Debug mode is only enabled when `FLASK_ENV=development` is set (development only).
- The Docker image runs with a non-root user for security and includes health checks.
