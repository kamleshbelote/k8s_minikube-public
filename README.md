# Certified Kubernetes Administrator (CKA) Exam Preparation

Welcome to the comprehensive CKA exam preparation repository! This repository contains structured study materials, hands-on practice exercises, and detailed setup guides to help you successfully prepare for the Certified Kubernetes Administrator exam.

## About CKA Exam

The Certified Kubernetes Administrator (CKA) exam is a performance-based test that certifies that candidates can perform the responsibilities of Kubernetes administrators. The exam tests candidates' knowledge, skills, and abilities to perform the tasks of a Kubernetes administrator, including:

- Cluster architecture and setup
- Workloads & Scheduling
- Services & Networking
- Storage management
- Security configurations
- Troubleshooting
- And more...

## Documentation

- [Minikube Installation Guide for Ubuntu](./minikube-ubuntu-installation.md) - Complete step-by-step guide for installing Minikube on Ubuntu systems
- [Kubernetes Official Documentation](https://kubernetes.io/docs/home/) - Reference to the official Kubernetes documentation

## Quickstart

1. Install Minikube (see the documentation link above)
2. Clone this repository: `git clone https://github.com/kamleshbelote/k8s_minikube.git`
3. Start Minikube: `./start_minikube.sh`
4. Follow the Day 1 instructions to run the demo app locally or in Minikube

## Learning Path

This repository follows a structured learning path designed to gradually build your Kubernetes skills from the basics to more advanced topics required for the CKA exam.

### Daily Study Materials

- [Day 1: Docker / Demo App](./day1_Docker/readme.md) - Build and run a FastAPI demo app, create Docker image and deploy to Minikube
- [Day 2: Deployment](./day2_Deployment/readme.md) - Kubernetes deployment examples, manifests, and scaling strategies
- [Day 3: Services](./day3_Service/readme.md) - Understanding and working with Kubernetes Services, networking, and service discovery
- [Day 4: Architecture](./day4_Architecture/README.md) - Kubernetes architecture diagrams, component interactions, and visualizations
  - [ASCII Kubernetes Architecture](./day4_Architecture/Architecture.txt) - Text-based architecture diagram
- [Day 5: Multi-Node Clusters](./day5_SetupMultiNode/README.md) - Setting up and managing multi-node Kubernetes clusters with specialized node types
- [Day 6: Pods](./day6_Pods/README.md) - Detailed guide to Kubernetes Pods, lifecycle management, and configuration options

### Topics Covered

| Day | Topic | Key Concepts |
|-----|-------|-------------|
| 1 | Docker | Containerization, Images, Registries |
| 2 | Deployments | ReplicaSets, Rolling updates, Scaling |
| 3 | Services | ClusterIP, NodePort, LoadBalancer, Networking |
| 4 | Architecture | Control plane, Worker nodes, Components |
| 5 | Multi-Node | Node setup, Labels, Taints, Tolerations |
| 6 | Pods | Pod lifecycle, Multi-container pods, Health checks |

## Repository Structure

- `day1_Docker/` - Day 1 materials: demo app, Dockerfile, and k8s manifests
- `day2_Deployment/` - Day 2 deployment examples and manifests  
- `day3_Service/` - Day 3 materials: Kubernetes Services examples and manifests
- `day4_Architecture/` - Day 4 materials: Kubernetes architecture diagrams and visualizations
- `day5_SetupMultiNode/` - Day 5 materials: Multi-node cluster setup and management
- `day6_Pods/` - Day 6 materials: Pod management, configuration, and best practices
- `start_minikube.sh` - Script to start Minikube cluster
- `minikube-ubuntu-installation.md` - Minikube installation documentation

## CKA Exam Tips

- Time management is crucial - You have 2 hours to complete the exam
- Be proficient with `kubectl` commands and YAML manifest creation
- Practice debugging and troubleshooting Kubernetes clusters
- Use shortcuts and aliases to save time:
  ```bash
  alias k=kubectl
  export do="--dry-run=client -o yaml"
  ```
- Know how to use the Kubernetes documentation (bookmarked during the exam)

## Practice Exercises

Each day's folder contains practical exercises that align with CKA exam objectives:
- Creating and managing various Kubernetes resources
- Troubleshooting common issues
- Configuring cluster networking
- Managing storage and persistent volumes
- Implementing security policies

## Upcoming Topics

- Persistent Storage and Volumes
- ConfigMaps and Secrets
- RBAC and Security
- Networking and Network Policies
- Cluster Maintenance and Upgrades
- Troubleshooting

## Contributing

When adding new day folders, please:
1. Create a folder named `dayN_Topic` (e.g., `day7_ConfigMaps`)
2. Include a `README.md` in the folder describing the day's objectives and exercises
3. Add a link to the new day in the "Daily Study Materials" section above
4. Update the Topics Covered table with the new information

## License

This repository is provided for educational purposes under the MIT License.
```