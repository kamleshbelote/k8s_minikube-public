# Kubernetes Architecture Diagrams

This directory contains diagrams illustrating the architecture of Kubernetes components and their interactions.

## Contents

1. [Kubernetes Architecture in Markdown](kubernetes-architecture.md) - Mermaid diagrams in Markdown format
2. [ASCII Kubernetes Architecture](Architecture.txt) - Text-based diagram viewable in any editor
3. [HTML Renderer](k8s-architecture-renderer.html) - HTML page to render and save diagrams as PNG
4. [Generate PNG Scripts](#generating-png-images) - Scripts to convert diagrams to PNG images

## Diagram Types

The following diagrams are included:

1. **High-Level Kubernetes Architecture** - Overview of control plane, nodes, and add-ons
2. **Component Relationships** - Detailed interactions between Kubernetes components
3. **Service Architecture** - How Kubernetes services route traffic to pods
4. **Deployment Process** - Sequence diagram of the deployment workflow
5. **Minikube Architecture** - Structure of a Minikube cluster
6. **ASCII Kubernetes Architecture** - Text-based diagram showing cluster components

## Generating PNG Images

### Option 1: Using the HTML Renderer

1. Open `k8s-architecture-renderer.html` in a web browser
2. Wait for all diagrams to render
3. Use the "Download" buttons to save each diagram as a PNG
4. Alternatively, take screenshots of each diagram

### Option 2: Using the Online API Script (Recommended)

This option uses the Mermaid.js online API to generate PNGs without additional dependencies:

```bash
./generate-diagrams-online.sh
```

This will create PNG files in an `images` subdirectory.

### Option 3: Using Local Mermaid CLI

This option requires Node.js and npm to be installed:

```bash
./generate-diagram-pngs.sh
```

This will install the required dependencies and generate PNG files in an `images` subdirectory.

## Diagram Descriptions

### 1. High-Level Kubernetes Architecture
Shows the main components of a Kubernetes cluster including the control plane (API server, etcd, scheduler, controller manager) and worker nodes (kubelet, kube-proxy, container runtime).

### 2. Component Relationships
Details the specific interactions between different Kubernetes components, showing how they communicate to maintain the desired state of the cluster.

### 3. Service Architecture
Illustrates how Kubernetes Services work to route traffic from external clients to pods through endpoints and kube-proxy.

### 4. Deployment Process
A sequence diagram showing the workflow when creating a deployment, from the initial command to running containers.

### 5. Minikube Architecture
Shows how Minikube sets up a single-node Kubernetes cluster for development and testing.

### 6. ASCII Kubernetes Architecture
A comprehensive text-based diagram showing the Kubernetes architecture, including control plane components, worker nodes, networking, and storage. This diagram can be viewed in any text editor without requiring special rendering tools.