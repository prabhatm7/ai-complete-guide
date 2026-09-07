# Kubernetes Practise

This folder contains two local Kubernetes learning setups:

- `kind/` for a cluster created from YAML
- `minikube/` for a cluster created with CLI commands

## Folder Layout

- `kind/config.yaml`: cluster definition for `kind`
- `kind/README.md`: how to start and use the `kind` cluster
- `minikube/README.md`: how to start and use the `minikube` cluster

## Which One Should You Use?

Use `kind` when you want:

- a cluster defined in YAML
- a reproducible multi-node local cluster
- to practice how Kubernetes nodes are arranged

Use `minikube` when you want:

- a simple local learning cluster started from commands
- a beginner-friendly workflow
- built-in addons and helper commands

## Important Difference

`kind/config.yaml` works only with `kind`.

It does not work with `minikube start`.

## Quick Start

For the `kind` workflow, read [kind/README.md](kind/README.md).

For the `minikube` workflow, read [minikube/README.md](minikube/README.md).

## Common kubectl Context Commands

Check the current context:

```bash
kubectl config current-context
```

List all contexts:

```bash
kubectl config get-contexts
```

If both `kind` and `minikube` clusters are running at the same time, switch between them with:

```bash
kubectl config use-context kind-practise
kubectl config use-context minikube
```

The context you select with `kubectl config use-context ...` becomes the default cluster context for `kubectl` until you change it again.

Switch to the `kind` cluster:

```bash
kubectl config use-context kind-practise
```

Switch to the default `minikube` cluster:

```bash
kubectl config use-context minikube
```

You can verify the default context any time with:

```bash
kubectl config current-context
```