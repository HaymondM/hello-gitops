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

Run the application with:
```
python app.py
```

The app will start on `http://localhost:5000`. Visit the root URL (`/`) to see "Hello world".

### Troubleshooting

- If you encounter import errors, ensure Flask is installed.
- The app runs in debug mode by default.
