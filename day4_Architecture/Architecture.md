%% Kubernetes Architecture - Mermaid Diagram
%% You can render this with Mermaid Live Editor, VS Code Mermaid extension, or Mermaid CLI

flowchart TD
    subgraph ControlPlane["Control Plane / Master Node"]
        APIServer[API Server]
        etcd[etcd]
        ControllerManager[Controller Manager]
        Scheduler[Scheduler]
        APIServer <--> etcd
        ControllerManager --> APIServer
        Scheduler --> APIServer
    end

    subgraph WorkerNode1["Worker Node 1"]
        Kubelet1[kubelet]
        KubeProxy1[kube-proxy]
        CR1[Container Runtime]
        Kubelet1 --> APIServer
        KubeProxy1 --> APIServer
        Kubelet1 --> CR1
        subgraph Pods1["Pods"]
            Pod1[Pod 1]
            Pod2[Pod 2]
            Pod1 --> C1[App Container]
            Pod1 --> C2[Sidecar Container]
            Pod2 --> C3[App Container]
            Pod2 --> C4[Init Container]
        end
        Kubelet1 --> Pod1
        Kubelet1 --> Pod2
    end

    subgraph WorkerNode2["Worker Node 2"]
        Kubelet2[kubelet]
        KubeProxy2[kube-proxy]
        CR2[Container Runtime]
        Kubelet2 --> APIServer
        KubeProxy2 --> APIServer
        Kubelet2 --> CR2
        subgraph Pods2["Pods"]
            Pod3[Pod 3]
            Pod4[Pod 4]
            Pod3 --> C5[App Container]
            Pod3 --> C6[Sidecar Container]
            Pod4 --> C7[App Container]
        end
        Kubelet2 --> Pod3
        Kubelet2 --> Pod4
    end

    subgraph Networking["Networking"]
        LB[Load Balancer]
        Service[Service]
        Endpoint1[Endpoint (Pod IP:Port)]
        Endpoint2[Endpoint (Pod IP:Port)]
        LB --> Service
        Service --> Endpoint1
        Service --> Endpoint2
        Endpoint1 --> Pod1
        Endpoint2 --> Pod3
        APIServer --> Service
        KubeProxy1 -.-> Service
        KubeProxy2 -.-> Service
    end

    subgraph Storage["Storage"]
        PVC[PersistentVolumeClaim]
        PV[PersistentVolume]
        SC[StorageClass]
        PVC <--> PV
        PV <--> SC
        Pod1 --> PVC
        Pod3 --> PVC
        APIServer --> PVC
    end

    %% Communication notes
    classDef cp fill:#e6f3ff,stroke:#0066cc,stroke-width:2px;
    classDef wn fill:#f0fff0,stroke:#009900,stroke-width:2px;
    classDef net fill:#f9f9f9,stroke:#666666;
    classDef st fill:#fff0f0,stroke:#990000,stroke-width:2px;
    class APIServer,etcd,ControllerManager,Scheduler cp;
    class Kubelet1,KubeProxy1,CR1 wn;
    class Kubelet2,KubeProxy2,CR2 st;
    class LB,Service,Endpoint1,Endpoint2 net;
    class PVC,PV,SC st;
