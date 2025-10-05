## 3. Update Kubernetes Deployment Manifest

Edit `k8s-deployment.yaml` to use your Docker Hub image instead of the local image. Replace `kamleshbelote` with your Docker Hub username or the image path you pushed to.

## 3. Update Kubernetes Deployment Manifest

Edit `k8s-deployment.yaml` to use your Docker Hub image instead of the local image:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demoapp-deployment
  labels:
    app: demoapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demoapp
  template:
    metadata:
      labels:
        app: demoapp
    spec:
      containers:
      - name: demoapp
        # Replace "kamleshbelote" with your actual Docker Hub username
        image: kamleshbelote/demoapp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /readiness
            port: 8000
          initialDelaySeconds: 2
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

## 4. Deploy to Minikube

Apply the updated deployment and service manifests:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

## 5. Verify Deployment

Check if the pod is running:

```bash
kubectl get pods -l app=demoapp
```

Access the service:

```bash
minikube service demoapp-service --url
```

Test the endpoints:

```bash
# Get service URL
SERVICE_URL=$(minikube service demoapp-service --url)

# Test the endpoints
curl $SERVICE_URL/
curl $SERVICE_URL/healthz
curl $SERVICE_URL/readiness
```

## 6. Troubleshooting

### Image Pull Errors

If you encounter image pull errors, check:

1. Docker Hub credentials:
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=https://index.docker.io/v1/ \
     --docker-username=yourusername \
     --docker-password=yourpassword \
     --docker-email=your.email@example.com
   ```

2. Update deployment to use the secret:
   ```yaml
   spec:
     containers:
     # ... container spec ...
    imagePullSecrets:
     - name: regcred
   ```

### Pod Status Check

To debug pod issues:

```bash
kubectl describe pod -l app=demoapp
kubectl logs -l app=demoapp
```

## 7. Cleaning Up

To remove the deployment and service:

```bash
kubectl delete -f k8s-service.yaml
kubectl delete -f k8s-deployment.yaml
```