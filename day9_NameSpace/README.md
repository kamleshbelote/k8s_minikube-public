# Kubernetes Namespaces

Namespaces provide a mechanism for isolating groups of resources within a single Kubernetes cluster. They are particularly useful for dividing cluster resources between multiple users, teams, or projects.

## What are Namespaces?

Namespaces in Kubernetes:
- Provide scope for names: Resource names must be unique within a namespace
- Allow resource quotas: Control resource allocation across teams
- Enable access control: Apply permissions at namespace level
- Organize resources: Group related resources together

## Demo Components

Our demo includes:
1. Namespace Creation (`demo-namespace`)
2. Pod Deployment with Resource Limits
3. ClusterIP Service Creation

### 1. Namespace Configuration
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: demo-namespace
  labels:
    name: demo-namespace
    env: dev
    team: demo-team
```

### 2. Pod Configuration
```yaml
kind: Pod
apiVersion: v1
metadata: 
  name: demoapp-pod
  namespace: demo-namespace
  labels:
    app: demoapp-namespace
    env: dev
    type: frontend
spec:
  containers:
  - name: demoapp-container
    image: nginx:latest
    resources:
      limits:
        cpu: "500m"
        memory: "256Mi"
      requests:
        cpu: "250m"
        memory: "128Mi"
```

### 3. Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demoapp-service
  namespace: demo-namespace
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: demoapp-namespace
    env: dev
    type: frontend
```

## Common Commands

1. **Namespace Management**:
```bash
# Create namespace
kubectl create namespace demo-namespace

# List all namespaces
kubectl get namespaces

# Get namespace details
kubectl describe namespace demo-namespace
```

2. **Resource Management**:
```bash
# Get resources in namespace
kubectl get all -n demo-namespace

# Get pods in namespace
kubectl get pods -n demo-namespace

# Get services in namespace
kubectl get services -n demo-namespace
```

3. **Service Access**:
```bash
# Within same namespace
curl http://demoapp-service

# From different namespace
curl http://demoapp-service.demo-namespace.svc.cluster.local

# Port forward to access from outside
kubectl port-forward -n demo-namespace svc/demoapp-service 8080:80
```

## Service Discovery

1. **Same Namespace Access**:
   - Use simple service name: `demoapp-service`
   - Port: 80

2. **Cross-Namespace Access**:
   - Use FQDN: `demoapp-service.demo-namespace.svc.cluster.local`
   - Format: `<service-name>.<namespace>.svc.cluster.local`

## Resource Quotas

Our pod has defined resource limits:
- CPU Limit: 500m (half a CPU core)
- Memory Limit: 256Mi
- CPU Request: 250m
- Memory Request: 128Mi

## Best Practices

1. **Namespace Naming**:
   - Use meaningful, team/project-related names
   - Follow consistent naming conventions
   - Add descriptive labels

2. **Resource Organization**:
   - Group related resources in the same namespace
   - Use labels for further organization
   - Consider environment separation (dev, staging, prod)

3. **Access Control**:
   - Implement RBAC at namespace level
   - Use network policies for namespace isolation
   - Apply resource quotas per namespace

4. **Service Discovery**:
   - Use short names within same namespace
   - Use FQDN for cross-namespace communication
   - Document service endpoints

## Cleanup

To remove all resources:
```bash
kubectl delete namespace demo-namespace
```
This will delete all resources within the namespace.