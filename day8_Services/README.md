# Kubernetes Services

Kubernetes Services are an abstraction layer that provides a stable endpoint for a set of pods. They enable network access to a dynamic set of pods and handle load balancing.

## Types of Services

### 1. ClusterIP
- **Purpose**: Default service type for internal communication within the cluster
- **Use Case**: Backend services, internal APIs, databases
- **Access**: Only accessible within the cluster
- **Configuration**:
  - `targetPort`: Port where the pod is listening
  - `port`: Port exposed by the service internally
- **Example**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: backend
```

### 2. NodePort
- **Purpose**: Exposes the service on each node's IP at a static port
- **Port Range**: 30000-32767
- **Components**:
  - `targetPort`: Port exposed by the Pod (e.g., 80)
  - `port`: Service port exposed to other pods (e.g., 80)
  - `nodePort`: Port exposed to external users (e.g., 30001)
- **Access Methods**:
  1. Through NodePort: `http://<node-ip>:nodePort`
  2. Direct pod access: `kubectl port-forward pod/<pod-name> 8080:80`
- **Example**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30001
  selector:
    app: frontend
```

### 3. LoadBalancer
- **Purpose**: Exposes the service externally using a cloud provider's load balancer
- **Use Case**: Production applications requiring external access
- **Components**:
  - Creates a ClusterIP Service
  - Creates a NodePort Service
  - Creates an external load balancer pointing to NodePort
- **Access**:
  - Cloud: Through Load Balancer IP
  - Minikube: 
    1. Using `minikube tunnel`
    2. Through NodePort: `http://<minikube-ip>:<node-port>`
- **Example**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-lb
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: frontend
```

### 4. ExternalName
- **Purpose**: Maps a service to a DNS name
- **Use Case**: Accessing external services using internal DNS
- **Benefits**:
  - Service abstraction for external dependencies
  - Easy migration between external and internal services
  - Consistent DNS naming within cluster

#### ExternalName Service Demo

1. **Create ExternalName Service**
```yaml
# File: externalname.yaml
apiVersion: v1
kind: Service
metadata:
  name: external-api-service
spec:
  type: ExternalName
  externalName: api.github.com
```

2. **Apply the Configuration**
```bash
kubectl apply -f externalname.yaml
```

3. **Usage Example**:
   - Pods in your cluster can now access `api.github.com` using:
   - `external-api-service.default.svc.cluster.local`
   - Or simply `external-api-service` within the same namespace

4. **Testing the Service**:
```bash
# Create a test pod
kubectl run curl-test --image=curlimages/curl -i --tty -- sh

# Inside the pod, access the external service
curl http://external-api-service

# The above command is equivalent to
curl http://api.github.com
```

5. **Common Use Cases**:
   - Database services hosted outside the cluster
   - Third-party APIs
   - Services in different clusters
   - Cloud provider services

6. **Important Notes**:
   - No proxying - direct DNS resolution
   - HTTPS certificates must match external name
   - No health checking provided
   - Only works with DNS names, not IP addresses

## Common Use Cases

### Three-Tier Application Example
1. **Frontend** (LoadBalancer/NodePort)
   - Exposed to external users
   - `type: LoadBalancer/NodePort`

2. **Backend API** (ClusterIP)
   - Internal access only
   - Communicates with frontend and database
   - `type: ClusterIP`

3. **Database** (ClusterIP)
   - Strictly internal access
   - Only accessible by backend
   - `type: ClusterIP`

## Useful Commands

```bash
# List all services
kubectl get svc

# Get service details
kubectl describe svc <service-name>

# Port forward to a pod
kubectl port-forward pod/<pod-name> <local-port>:<pod-port>

# Access NodePort service
curl http://$(minikube ip):<node-port>

# Start minikube tunnel for LoadBalancer
minikube tunnel
```

## Best Practices
1. Use ClusterIP for internal communication
2. Use NodePort for development/testing
3. Use LoadBalancer for production external access
4. Always set appropriate labels and selectors
5. Use meaningful service names
6. Document port mappings