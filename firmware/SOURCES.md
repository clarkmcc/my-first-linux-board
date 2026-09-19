# Pinned sources

The build downloads the official Buildroot 2026.02.2 release archive:

- URL: `https://buildroot.org/downloads/buildroot-2026.02.2.tar.xz`
- SHA-256: `a833429929aefd4175b0651b2b356b761960cd46d36df6a0049d1f117e3ac8a6`

That Buildroot release resolves Linux 6.19.14 and U-Boot 2026.01. The firmware
started from the upstream Lichee Pi Nano boot flow and keeps its compatible
hardware initialization while supplying this board's own device tree and
model name. This external tree intentionally removes networking, SSH, Python,
C++, WireGuard, NFS, and swap features.

The external hash file verifies the Linux archive against kernel.org's signed
checksum manifest:

- Linux 6.19.14 SHA-256: `cde8bf6739be4a0777fedbbba5330b8188c55680c45a922a4dfa289cbec6f185`
- U-Boot 2026.01 SHA-256 (verified by Buildroot's bundled hash): `b60d5865cefdbc75da8da4156c56c458e00de75a49b80c1a2e58a96e30ad0d54`

Primary references:

- Buildroot manual: `https://buildroot.org/downloads/manual/manual.html`
- Buildroot release announcement: `https://lists.buildroot.org/pipermail/buildroot/2026-May/802637.html`
- U-Boot source: `https://source.denx.de/u-boot/u-boot/-/tree/v2026.01`
- Linux stable source: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tag/?h=v6.19.14`
