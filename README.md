# pkg-rpm-camx-kodiak

RPM packaging for the Qualcomm® Linux CamX camera framework on the Kodiak
platform.

This repository has RPM packaging rules and scripts for prebuilt CamX camera
framework binaries for the Kodiak platform. The package is maintained on the
CentOS Stream 10 (`c10s`) branch and uses the shared GitHub Actions build and
release workflow.

The prebuilt CamX camera framework binaries are available from
[QArtifactory](https://qartifactory-edge.qualcomm.com/ui/native/qsc_releases/software/chip/component/camx.qclinux.0.0/).


## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) | Pull request | Build the RPM(s) so reviewers confirm the package still builds. Read-only — never publishes. |
| [`pkg-release.yml`](.github/workflows/pkg-release.yml) | Manual (`workflow_dispatch`) | Build **and** publish the RPM(s) to Artifactory, behind an approval gate. |

The GitHub Actions workflows use the shared
[`qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils) build
environment and run `rpmbuild` inside the prebuilt `rpm-builder` container
image for the runner's host architecture.

---

## Repository Layout

The `c10s` branch contains the RPM packaging files:

| File | Purpose |
|---|---|
| `camx-kodiak.spec` | Builds the Kodiak CamX runtime and library subpackages. |
| `sources` | SHA-512 checksum for the prebuilt CamX binary archive. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

The prebuilt binary archive is not committed to this repository. The spec file's
`Source0` points to the QArtifactory release, and the checksum in `sources` is
verified before the RPM is built.

---

## Installation

Install the RPM packages from the configured CentOS Stream 10 repository:

```bash
sudo dnf install camx-kodiak
```

Install the camera-service runtime package together with the core package:

```bash
sudo dnf install camx-kodiak libcamx-kodiak1
```

Package roles:

- `camx-kodiak`: CamX Kodiak user-mode camera libraries, plugins, tuning data,
  and `nativehaltest`.
- `libcamx-kodiak1`: CamX libraries used by the camera service (QMMF).

---

## Updating the package version

This is the everyday workflow — **two edits on `c10s`, no tarball in git**:

1. Bump `Version:` in the spec (and the `Source0:` URL if its path changed).
2. Recompute the checksum for the new tarball:
   ```bash
   sha512sum --tag camx-kodiak-<newversion>_<release>.aarch64.tar.gz > sources
   ```
3. Commit the spec + `sources`, open a PR (build verifies it), merge, then run
   **Release**. The first release fetches the new upstream tarball, verifies it,
   and caches it back to Artifactory automatically.

## License

This project is licensed under the BSD 3-Clause License. See [LICENSE.txt](LICENSE.txt) for the complete license text.
