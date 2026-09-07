# Kubernetes Basics

Kubernetes is a container orchestration platform. It helps you deploy, manage, scale, and monitor containerized applications.

## Why Kubernetes

- Automates application deployment
- Scales applications up or down
- Restarts failed containers automatically
- Balances traffic across services
- Makes application updates easier

## Core Components of Kubernetes

### 1. Cluster
A Kubernetes cluster is the full system that runs your applications. It contains a control plane and one or more worker nodes.

### 2. Control Plane
The control plane manages the cluster and makes global decisions.

Main parts of the control plane:

- `kube-apiserver`: The main entry point for all Kubernetes commands and requests.
- `etcd`: Stores cluster data and configuration.
- `kube-scheduler`: Decides which node should run a pod.
- `kube-controller-manager`: Runs controllers that keep the cluster in the desired state.

### 3. Node
A node is a machine, either physical or virtual, that runs application workloads.

Main parts of a node:

- `kubelet`: Makes sure containers in pods are running correctly.
- `kube-proxy`: Handles service networking and traffic routing on the node.
- `Container runtime`: Software such as `containerd` that runs containers.

#### `kube-proxy` clarification

`kube-proxy` does not directly provide normal pod-to-pod communication. Direct pod networking is mainly handled by the CNI plugin.

- Same node pod-to-pod communication: usually handled by the pod network created by the CNI plugin.
- Different node pod-to-pod communication: also handled by the CNI plugin across nodes.
- Service-to-pod communication: handled by `kube-proxy`, which routes traffic from a Service to backend pods that may be on the same node or on different nodes.

So, `kube-proxy` can route service traffic to pods on both the same node and different nodes, but it is not the main component responsible for direct pod-to-pod communication.

### 4. Pod
A pod is the smallest deployable unit in Kubernetes. It usually contains one container, but it can contain multiple closely related containers.

### 5. Deployment
A deployment manages pods and replicas. It helps with updates, rollbacks, and scaling.

### 6. Service
A service gives a stable network identity to a set of pods. It allows communication even if pod IP addresses change.

### 7. Namespace
A namespace is used to organize resources inside a cluster. It is useful when multiple teams or applications share the same cluster.

### 8. ConfigMap and Secret

- `ConfigMap`: Stores non-sensitive configuration data.
- `Secret`: Stores sensitive data such as passwords or tokens.

## Simple Flow

1. You create a deployment.
2. The deployment creates pods.
3. The scheduler places pods on nodes.
4. The kubelet starts containers on the selected node.
5. A service exposes the pods for communication.

## Summary

Kubernetes works by using a control plane to manage worker nodes, and by running applications inside pods. Deployments, services, namespaces, config maps, and secrets make applications easier to manage in a reliable way.

## Diagram

High-level cluster overview: [kubernetes-cluster-overview.excalidraw](kubernetes-cluster-overview.excalidraw)
