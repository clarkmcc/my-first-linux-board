# Boot Console firmware

This Buildroot external tree creates a minimal microSD image for the F1C200s
Boot Console. The first milestone boots U-Boot SPL, U-Boot, Linux, and BusyBox
with a login on UART0 PE0/PE1 at 115200 8N1. UART is the primary bring-up and
recovery console because it is available before Linux. Linux additionally
offers a CDC ACM login and CDC ECM Ethernet on the native USB peripheral port.
The board runs a live status page and Dropbear SSH at `192.168.7.2`.

The network stack is limited to the directly attached USB link. A tiny DHCP
server gives the host a `192.168.7.x` address without a gateway or DNS option,
so the link does not replace the host's normal Internet route. The image has no
package manager, Python, or C++ runtime. The fixed hardware rails need no PMIC
driver. The root ext4 filesystem
mounts read-only; `/run`, `/tmp`, and `/var` are tmpfs. Development images permit local
passwordless root login on the physical UART, USB gadget console, and SSH.
Treat this as a physically attached development image, not a production security
configuration. A generated Dropbear host key persists under `/boot/dropbear` on
the FAT partition; other runtime state remains in RAM.
The broad upstream `multi_v5_defconfig` retains I2C core and some unrelated
modules; no I2C controller is enabled in this board's device tree. Wi-Fi, SPI,
and sound support resolve disabled.

For a ground-up explanation of how the hardware, boot stages, kernel, device
tree, and root filesystem fit together, see
[Embedded Linux from first principles](docs/EMBEDDED-LINUX-FROM-FIRST-PRINCIPLES.md).

## Build

On Linux with the Buildroot host prerequisites installed:

```sh
make
```

On macOS or another Docker host:

```sh
./build-container.sh
```

The container wrapper keeps sources and intermediate output in the named Linux
volume `boot-console-buildroot-2026-02-2`. This is required on case-insensitive
macOS filesystems because the Linux source contains case-distinct names. It
copies the final images and resolved configurations into `output/`.

Both commands run from this directory. The pinned configuration uses eight
jobs within each package while Buildroot keeps package orchestration serial.
`make configure` only resolves the Buildroot configuration. Downloads, unpacked
source, and generated output stay in ignored `dl/`, `build/`, and `output/`
directories. See [SOURCES.md](SOURCES.md) for pins and source provenance.

After changing the DTS, kernel or U-Boot fragments, Linux patches, or boot
script, run `make rebuild-board`; the Docker equivalent is
`./build-container.sh rebuild-board`. This rebuilds board outputs while keeping
the expensive cross toolchain. After changing `configs/boot_console_defconfig`,
run `make clean` and then `make` so every resolved setting is rebuilt.

The useful generated files are:

- `output/.config`: resolved Buildroot configuration
- `output/build.log`: console log from the latest container build
- `output/build/linux-6.19.14/.config`: resolved Linux configuration
- `output/build/uboot-2026.01/.config`: resolved U-Boot configuration
- `output/images/linux.dtb`: board device tree
- `output/images/u-boot-sunxi-with-spl.bin`: SPL plus U-Boot
- `output/images/rootfs.ext4`: read-only-at-runtime BusyBox root filesystem
- `output/images/sdcard.img`: complete microSD image

## Image and boot flow

The Allwinner ROM finds SPL at byte 8 KiB. The raw SPL/U-Boot area ends at
1 MiB, followed by a 16 MiB FAT boot partition and then the ext4 root
partition. U-Boot loads `zImage` at `0x80008000` and `linux.dtb` at
`0x82000000`. Kernel arguments select `/dev/mmcblk0p2`, ext4, `rootwait`, and
read-only mounting. SDC0 uses the proven one-bit, 12.5 MHz configuration and
does not require a card-detect switch. Both U-Boot and Linux identify the
hardware as `Clark's Board`.

Do not write `sdcard.img` to removable media until its target device has been
checked separately. The build does not flash hardware.

## Hardware validation boundary

Configuration and compilation can prove that the selected upstream software
builds, but they cannot prove SDRAM timing, UART levels, SD signal integrity,
USB enumeration, or LED polarity. Those checks require an assembled board.
