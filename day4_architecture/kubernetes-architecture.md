# Kubernetes Architecture Diagram

## High-Level Kubernetes Architecture

```mermaid
graph TD
    subgraph "Control Plane Components"
        A[API Server] --> B[etcd]
        A --> C[Controller Manager]
        A --> D[Scheduler]
        A --> E[Cloud Controller Manager]
    end
    
    subgraph "Worker Node 1"
        F[kubelet] --> A
        G[kube-proxy] --> A
        H[Container Runtime] --> F
        F --> I[Pods]
        I --> I1[Pod 1]
        I --> I2[Pod 2]
        I1 --> C1[Container 1]
        I1 --> C2[Container 2]
        I2 --> C3[Container 3]
    end
    
    subgraph "Worker Node 2"
        J[kubelet] --> A
        K[kube-proxy] --> A
        L[Container Runtime] --> J
        J --> M[Pods]
        M --> M1[Pod 3]
        M --> M2[Pod 4]
        M1 --> C4[Container 4]
        M2 --> C5[Container 5]
        M2 --> C6[Container 6]
    end
    
    N[External Load Balancer] --> A
    O[Users/Clients] --> N
    
    subgraph "Add-ons"
        P[DNS]
        Q[Dashboard]
        R[Metrics Server]
        S[CNI Plugin]
    end
    
    S -.-> F
    S -.-> J
    P -.-> A
    Q -.-> A
    R -.-> A
```

## Detailed Component Relationships

```mermaid
flowchart TD
    subgraph "Control Plane"
        api[API Server] <--> etcd[(etcd)]
        api <--> sched[Scheduler]
        api <--> cm[Controller Manager]
        api <--> ccm[Cloud Controller Manager]
        
        sched -- "1. Watch for new pods" --> api
        sched -- "2. Assign node to pod" --> api
        cm -- "Watch resources" --> api
        cm -- "Maintain desired state" --> api
        ccm -- "Cloud provider integration" --> api
    end
    
    subgraph "Worker Node"
        kubelet -- "Register node" --> api
        kubelet -- "Watch for assigned pods" --> api
        kubelet -- "Report status" --> api
        
        kubelet --> runtime[Container Runtime]
        kubelet -- "Create/manage" --> pods((Pods))
        
        kproxy[kube-proxy] -- "Watch for Services & Endpoints" --> api
        kproxy -- "Configure iptables/ipvs" --> network((Network Rules))
        
        pods -- "Run on" --> runtime
        
        kubelet -- "Create/configure" --> volumes[(Volumes)]
        volumes -- "Mounted to" --> pods
    end
    
    subgraph "Networking Components"
        cni[CNI Plugin] -- "Configure" --> pod_network((Pod Network))
        cni -- "Allocate IPs" --> pods
        kproxy -- "Route service traffic" --> pod_network
    end
    
    client[Client/kubectl] -- "Request" --> api
    api -- "Authenticate & Authorize" --> client
    api -- "Validate" --> client
```

## Service Architecture

```mermaid
flowchart LR
    subgraph "User Access"
        client[Client]
    end
    
    subgraph "Service Layer"
        svc[Service]
        ep[Endpoints]
        kp[kube-proxy]
    end
    
    subgraph "Pod Layer"
        pod1[Pod 1]
        pod2[Pod 2]
        pod3[Pod 3]
    end
    
    client -- "1. Request to Service IP/DNS" --> svc
    svc -- "2. Tracked by" --> ep
    ep -- "3. Lists pod IPs" --> kp
    kp -- "4. Programs iptables rules" --> network((Network))
    network -- "5. Routes traffic to" --> pod1
    network -- "5. Routes traffic to" --> pod2
    network -- "5. Routes traffic to" --> pod3
    
    pod1 -- "Register with" --> ep
    pod2 -- "Register with" --> ep
    pod3 -- "Register with" --> ep
```

## Deployment Process

```mermaid
sequenceDiagram
    participant Client as Client/kubectl
    participant API as API Server
    participant Etcd as etcd
    participant CM as Controller Manager
    participant Sched as Scheduler
    participant Kubelet as Kubelet
    participant CR as Container Runtime
    
    Client->>API: Create Deployment
    API->>Etcd: Store Deployment
    API->>CM: Notify new Deployment
    CM->>API: Create ReplicaSet
    API->>Etcd: Store ReplicaSet
    CM->>API: Create Pods
    API->>Etcd: Store Pods
    API->>Sched: Notify unscheduled Pods
    Sched->>API: Assign Nodes to Pods
    API->>Etcd: Update Pod with Node assignment
    API->>Kubelet: Notify of assigned Pods
    Kubelet->>CR: Create Containers
    CR->>Kubelet: Container Status
    Kubelet->>API: Update Pod Status
    API->>Etcd: Store Pod Status
```

## Minikube Architecture

```mermaid
graph TD
    subgraph "Host Machine"
        A[Minikube Command] --> B[Docker/VM Driver]
        B --> C[Minikube VM/Container]
        
        subgraph "Minikube VM/Container"
            D[Control Plane Components]
            E[Worker Node Components]
            F[Add-ons]
            
            D --> G[API Server]
            D --> H[etcd]
            D --> I[Controller Manager]
            D --> J[Scheduler]
            
            E --> K[kubelet]
            E --> L[kube-proxy]
            E --> M[Container Runtime]
            
            F --> N[Dashboard]
            F --> O[metrics-server]
            F --> P[storage-provisioner]
        end
    end
    
    Q[kubectl] --> G
```

## Key Components Explained

### Control Plane
- **API Server**: The central management point that receives all REST requests for modifications to the cluster state
- **etcd**: Consistent and highly-available key-value store used as Kubernetes' backing store for all cluster data
- **Controller Manager**: Runs controller processes that regulate the state of the cluster
- **Scheduler**: Watches for newly created pods that have no node assigned and selects a node for them to run on

### Worker Nodes
- **kubelet**: An agent that runs on each node and ensures that containers are running in a pod
- **kube-proxy**: Maintains network rules on nodes that allow network communication to your pods
- **Container Runtime**: Software responsible for running containers (e.g., Docker, containerd, CRI-O)

### Add-ons
- **DNS**: Cluster DNS for service discovery
- **Dashboard**: Web-based UI for cluster management
- **Metrics Server**: Collects resource usage data from kubelets
- **CNI Plugin**: Configures pod networking and implements the Kubernetes networking model