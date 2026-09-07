# Kubernetes Container Runtime History

In early Kubernetes versions, Docker Engine was commonly used as the container runtime. Kubernetes supported Docker through a built-in component called `dockershim`.

Later, Kubernetes standardized runtime integration through the `CRI` (Container Runtime Interface). CRI is a Kubernetes API used by the kubelet to talk to container runtimes.

`CRI` and `OCI` are different things:

- `CRI` defines how Kubernetes communicates with a container runtime.
- `OCI` defines industry standards for container images and runtime behavior.

Because of CRI, Kubernetes could support multiple runtimes such as `containerd` and `CRI-O` without needing runtime-specific code in the kubelet.

Docker Engine itself was not a CRI implementation. Even though Docker uses `containerd` internally, Kubernetes did not talk directly to that internal `containerd` when using Docker Engine. Instead, Kubernetes used `dockershim` as an adapter between the kubelet and Docker.

`dockershim` was deprecated in Kubernetes 1.20 and removed in Kubernetes 1.24. After that removal, Docker Engine did not automatically become CRI-compatible. If someone still wanted to use Docker Engine with Kubernetes, they needed an external adapter such as `cri-dockerd`.

Today, the most common Kubernetes runtimes are `containerd` and `CRI-O`. Docker is still useful for building images, and those images work fine on Kubernetes because container images follow OCI standards.

## CRI, `crictl`, `nerdctl`, and `ctr`

### What is `CRI`?

`CRI` stands for Container Runtime Interface. It is the standard interface that lets the kubelet communicate with a container runtime.

With CRI, Kubernetes can work with different runtimes such as `containerd` and `CRI-O` without changing kubelet logic for each runtime.

### What is `crictl`?

`crictl` is a command-line tool for CRI-compatible runtimes. It is mainly used to inspect and debug containers, pods, images, and runtime issues on a Kubernetes node.

You can think of `crictl` as a low-level troubleshooting tool for the container runtime used by Kubernetes.

Examples:

- `crictl ps` to list containers
- `crictl pods` to list pod sandboxes
- `crictl images` to list images
- `crictl logs <container-id>` to view container logs

### What is `nerdctl`?

`nerdctl` is a Docker-compatible CLI for `containerd`. It gives a user experience similar to Docker, but it works directly with `containerd`.

It is useful when you want Docker-like commands on a system that uses `containerd`.

Examples:

- `nerdctl run`
- `nerdctl build`
- `nerdctl ps`
- `nerdctl images`

### What is `ctr`?

`ctr` is the low-level command-line client that comes with `containerd`. It talks directly to `containerd` and is mainly intended for debugging, development, and advanced runtime operations.

It is more technical and less user-friendly than `nerdctl`.

Examples:

- `ctr containers list`
- `ctr images list`
- `ctr tasks list`

In Kubernetes environments, `ctr` can be useful for inspecting `containerd` itself, but it is not the main day-to-day tool for Kubernetes debugging.

### `crictl` vs `nerdctl` vs `ctr`

- `crictl`: focused on CRI-level debugging for Kubernetes runtimes
- `nerdctl`: focused on container management with a Docker-like experience for `containerd`
- `ctr`: focused on low-level direct interaction with `containerd`
- `crictl` is better for node-level Kubernetes runtime troubleshooting
- `nerdctl` is better when you want to work with `containerd` like you would with Docker
- `ctr` is better when you need direct access to `containerd` internals and advanced debugging