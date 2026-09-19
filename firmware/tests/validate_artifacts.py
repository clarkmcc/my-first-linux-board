#!/usr/bin/env python3
"""Validate resolved Buildroot firmware artifacts for the Boot Console board."""

from __future__ import annotations

import argparse
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(message: str) -> None:
    raise AssertionError(message)


def one(paths: list[Path], description: str) -> Path:
    paths = [path for path in paths if path.is_file()]
    if len(paths) != 1:
        fail(f"expected one {description}, found {len(paths)}: {paths}")
    return paths[0]


def one_dir(paths: list[Path], description: str) -> Path:
    paths = [path for path in paths if path.is_dir()]
    if len(paths) != 1:
        fail(f"expected one {description}, found {len(paths)}: {paths}")
    return paths[0]


def config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if match := re.fullmatch(r"((?:CONFIG_|BR2_)[A-Za-z0-9_]+)=(.*)", line):
            values[match.group(1)] = match.group(2)
        elif match := re.fullmatch(r"# ((?:CONFIG_|BR2_)[A-Za-z0-9_]+) is not set", line):
            values[match.group(1)] = "n"
    return values


def require(cfg: dict[str, str], path: Path, expected: dict[str, str]) -> None:
    wrong = [f"{key}={cfg.get(key, '<missing>')} (expected {value})" for key, value in expected.items() if cfg.get(key) != value]
    if wrong:
        fail(f"{path}: resolved configuration mismatch:\n  " + "\n  ".join(wrong))


def decompile(dtb: Path) -> str:
    output = dtb.parent.parent
    local_candidates = [output / "host/bin/dtc"]
    local_candidates.extend((output / "build").glob("linux-*/scripts/dtc/dtc"))
    dtc = shutil.which("dtc") or next((str(path) for path in local_candidates if path.is_file()), None)
    if not dtc:
        fail("dtc is required in PATH, output/host/bin, or the Linux build tree")
    result = subprocess.run(
        [dtc, "-I", "dtb", "-O", "dts", str(dtb)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"dtc could not decode {dtb}:\n{result.stderr}")
    return result.stdout


def node(dts: str, identifying_property: str) -> str:
    position = dts.find(identifying_property)
    if position < 0:
        fail(f"compiled DTB lacks {identifying_property!r}")
    start = dts.rfind("{", 0, position)
    if start < 0:
        fail(f"cannot locate node containing {identifying_property!r}")
    depth = 0
    for end in range(start, len(dts)):
        if dts[end] == "{":
            depth += 1
        elif dts[end] == "}":
            depth -= 1
            if depth == 0:
                return dts[start : end + 1]
    fail(f"unterminated node containing {identifying_property!r}")
    return ""


def named_node(dts: str, name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\{{", dts)
    if not match:
        fail(f"compiled DTB lacks node {name!r}")
    start = match.end() - 1
    depth = 0
    for end in range(start, len(dts)):
        if dts[end] == "{":
            depth += 1
        elif dts[end] == "}":
            depth -= 1
            if depth == 0:
                return dts[start : end + 1]
    fail(f"unterminated compiled DTB node {name!r}")
    return ""


def phandle(text: str) -> str:
    match = re.search(r"\bphandle = <(0x[0-9a-f]+)>;", text)
    if not match:
        fail("compiled DTB node lacks a phandle")
    return match.group(1)


def check_dtb(dtb: Path) -> None:
    dts = decompile(dtb)
    for required in (
        'model = "Clark\'s Board"',
        'stdout-path = "serial0:115200n8"',
        'device_type = "memory"',
        'reg = <0x80000000 0x4000000>',
    ):
        if required not in dts:
            fail(f"{dtb}: compiled tree lacks {required!r}")

    mmc = node(dts, "broken-cd;")
    for required in ("bus-width = <0x01>", "max-frequency = <0xbebc20>", 'status = "okay"'):
        if required not in mmc:
            fail(f"{dtb}: enabled SDC0 node lacks {required!r}")

    regulator = named_node(dts, "regulator-vcc3v3")
    for required in ("regulator-min-microvolt = <0x33f44e>", "regulator-max-microvolt = <0x33f44e>"):
        if required not in regulator:
            fail(f"{dtb}: fixed I/O rail lacks exact nominal setting {required!r}")

    supply = phandle(regulator)
    pio = named_node(dts, "pinctrl@1c20800")
    for bank in ("c", "e", "f"):
        required = f"vcc-p{bank}-supply = <{supply}>"
        if required not in pio:
            fail(f"{dtb}: pin bank P{bank.upper()} does not reference the fixed I/O rail")

    uart_pin_match = re.search(r'pins = "PE0(?:\\0|", ")PE1"', dts)
    if not uart_pin_match:
        fail(f"{dtb}: compiled tree lacks the PE0/PE1 pin group")
    uart_pins = node(dts, uart_pin_match.group(0))
    if 'function = "uart0"' not in uart_pins:
        fail(f"{dtb}: PE0/PE1 are not resolved to UART0")
    uart = named_node(dts, "serial@1c25000")
    if 'status = "okay"' not in uart or f"pinctrl-0 = <{phandle(uart_pins)}>" not in uart:
        fail(f"{dtb}: enabled UART0 does not select the PE0/PE1 pinmux")

    led = node(dts, 'label = "boot-console:green:status"')
    if not re.search(r"gpios = <0x[0-9a-f]+ 0x02 0x00 0x01>", led):
        fail(f"{dtb}: status LED is not PC0 active-low")
    if 'linux,default-trigger = "activity"' not in led:
        fail(f"{dtb}: status LED does not default to the CPU activity trigger")
    if "pinctrl-0" in led or "status-led-pc0-pins" in dts:
        fail(f"{dtb}: status LED retains redundant PC0 pinctrl ownership")

    usb = node(dts, 'dr_mode = "peripheral"')
    if 'status = "okay"' not in usb:
        fail(f"{dtb}: native USB peripheral node is disabled")

    spi = named_node(dts, "spi@1c05000")
    if 'status = "okay"' in spi:
        fail(f"{dtb}: SPI0 is enabled and conflicts with the PC0 status LED")


def check_board_source(board: Path) -> None:
    boot = (board / "boot.cmd").read_text()
    image = (board / "genimage.cfg").read_text()
    inittab = (board / "rootfs-overlay/etc/inittab").read_text()
    wrapper = (board / "rootfs-overlay/usr/sbin/usb-acm-getty").read_text()
    gadget = (board / "rootfs-overlay/usr/sbin/usb-gadget-setup").read_text()
    gadget_service = (board / "rootfs-overlay/etc/init.d/S40usb-gadget").read_text()
    dhcp = (board / "rootfs-overlay/etc/udhcpd.conf").read_text()
    dropbear = (board / "rootfs-overlay/etc/init.d/S50dropbear").read_text()
    web_service = (board / "rootfs-overlay/etc/init.d/S60webui").read_text()
    web_page = (board / "rootfs-overlay/www/index.html").read_text()
    status_cgi = (board / "rootfs-overlay/www/cgi-bin/status").read_text()
    fstab = (board / "rootfs-overlay/etc/fstab").read_text()
    uboot_patch = (board / "patches/uboot/0001-suniv-licheepi-nano-name-clarks-board.patch").read_text()
    if "root=/dev/mmcblk0p2" not in boot or "rootfstype=ext4 ro" not in boot:
        fail("boot.cmd must select the second, read-only ext4 SD partition")
    if not re.search(r"partition rootfs\s*\{[^}]*partition-type = 0x83[^}]*rootfs\.ext4", image, re.S):
        fail("genimage.cfg root partition does not match bootargs")
    if "ttyS0::respawn:/sbin/getty -L ttyS0 115200" not in inittab:
        fail("UART0 getty is missing or has the wrong baud rate")
    if "ttyGS0::respawn:/usr/sbin/usb-acm-getty" not in inittab:
        fail("USB serial getty wrapper is not supervised by init")
    if "while [ ! -c /dev/ttyGS0 ]" not in wrapper or wrapper.count("sleep 2") < 2:
        fail("USB serial getty wrapper does not rate-limit a late gadget TTY")
    for required in (
        'functions/acm.usb0',
        'functions/ecm.usb0',
        'echo 0x80 > "$config/bmAttributes"',
        'echo 500 > "$config/MaxPower"',
        '192.168.7.2 netmask 255.255.255.0',
    ):
        if required not in gadget:
            fail(f"composite USB gadget setup lacks {required!r}")
    if 'while [ ! -d /sys/class/net/usb0 ]' not in gadget or 'while :' not in gadget:
        fail("USB gadget setup does not tolerate delayed UDC/network creation")
    if 'usb-gadget-setup.pid' not in gadget_service or '>/dev/console 2>&1 &' not in gadget_service:
        fail("USB gadget setup is not started asynchronously with a runtime PID file")
    for required in ("start 192.168.7.10", "end 192.168.7.20", "interface usb0", "option subnet 255.255.255.0"):
        if required not in dhcp:
            fail(f"USB DHCP configuration lacks {required!r}")
    if re.search(r"^\s*option\s+(?:router|dns)\b", dhcp, re.M):
        fail("USB DHCP must not replace the attached host's default route or DNS")
    if 'persistent_dir=/boot/dropbear' not in dropbear or 'dropbear -B ' not in dropbear:
        fail("Dropbear does not persist its host key or allow the documented blank development password")
    if 'httpd -p 80 -h /www' not in web_service:
        fail("BusyBox HTTPD service does not serve /www on port 80")
    if 'my-first-linux-board' not in web_page or '/cgi-bin/status' not in web_page or '/proc/uptime' not in status_cgi or '/proc/meminfo' not in status_cgi:
        fail("status web UI or live JSON endpoint is incomplete")
    if not re.search(r"^/dev/mmcblk0p1\s+/boot\s+vfat\s+[^\n]*\brw\b", fstab, re.M):
        fail("FAT boot partition is not mounted read/write for the persistent SSH host key")
    if '-\tmodel = "Lichee Pi Nano";' not in uboot_patch or '+\tmodel = "Clark\'s Board";' not in uboot_patch:
        fail("U-Boot board-name patch does not set the model to Clark's Board")


def same_region(image: Path, offset: int, payload: Path) -> bool:
    with image.open("rb") as image_file, payload.open("rb") as payload_file:
        image_file.seek(offset)
        while chunk := payload_file.read(1024 * 1024):
            if image_file.read(len(chunk)) != chunk:
                return False
    return True


def check_image(images: Path) -> None:
    disk = images / "sdcard.img"
    with disk.open("rb") as stream:
        mbr = stream.read(512)
    if len(mbr) != 512 or mbr[510:512] != b"\x55\xaa":
        fail(f"{disk}: missing MBR signature")
    partitions: list[tuple[int, int, int]] = []
    for index in range(4):
        entry = mbr[446 + 16 * index : 462 + 16 * index]
        kind = entry[4]
        start, sectors = struct.unpack_from("<II", entry, 8)
        if kind or start or sectors:
            partitions.append((kind, start, sectors))
    if len(partitions) != 2 or [part[0] for part in partitions] != [0x0C, 0x83]:
        fail(f"{disk}: expected FAT32-LBA boot then Linux root partitions, got {partitions}")
    boot_part, root_part = partitions
    if boot_part[2] * 512 != 16 * 1024 * 1024:
        fail(f"{disk}: boot partition is not exactly 16 MiB")
    if root_part[1] != boot_part[1] + boot_part[2]:
        fail(f"{disk}: root partition does not immediately follow boot partition")
    if not same_region(disk, boot_part[1] * 512, images / "boot.vfat"):
        fail(f"{disk}: boot partition bytes differ from boot.vfat")
    if not same_region(disk, root_part[1] * 512, images / "rootfs.ext4"):
        fail(f"{disk}: root partition bytes differ from rootfs.ext4")
    uboot = images / "u-boot-sunxi-with-spl.bin"
    if uboot.stat().st_size > 1016 * 1024:
        fail(f"{uboot}: SPL/U-Boot exceeds its 1016 KiB raw region")
    if not same_region(disk, 8 * 1024, uboot):
        fail(f"{disk}: raw boot area differs from {uboot.name}")
    boot_payload = sum((images / name).stat().st_size for name in ("zImage", "linux.dtb", "boot.scr"))
    if boot_payload > 15 * 1024 * 1024:
        fail("boot files leave less than 1 MiB for FAT metadata and allocation overhead")


def overlaps(first: tuple[int, int], second: tuple[int, int]) -> bool:
    return first[0] < second[1] and second[0] < first[1]


def check_memory_layout(output: Path, board: Path) -> None:
    boot = (board / "boot.cmd").read_text()
    dtb_match = re.search(r"load mmc 0:1 (0x[0-9a-fA-F]+) linux\.dtb", boot)
    kernel_match = re.search(r"load mmc 0:1 (0x[0-9a-fA-F]+) zImage", boot)
    if not dtb_match or not kernel_match:
        fail("boot.cmd does not expose fixed zImage and DTB load addresses")
    dtb_start = int(dtb_match.group(1), 16)
    zimage_start = int(kernel_match.group(1), 16)
    images = output / "images"
    dtb_range = (dtb_start, dtb_start + (images / "linux.dtb").stat().st_size)
    zimage_range = (zimage_start, zimage_start + (images / "zImage").stat().st_size)
    ram = (0x80000000, 0x84000000)
    for name, region in (("zImage", zimage_range), ("DTB", dtb_range)):
        if region[0] < ram[0] or region[1] > ram[1]:
            fail(f"{name} load range {region[0]:#x}-{region[1]:#x} is outside 64 MiB RAM")

    linux_dir = one_dir(
        [path for path in (output / "build").glob("linux-*") if not path.name.startswith("linux-headers-")],
        "Linux build directory",
    )
    nm = one(
        [path for path in (output / "host/bin").glob("*buildroot-linux*-nm") if not path.name.endswith("gcc-nm")],
        "target nm tool",
    )
    result = subprocess.run([nm, "-n", linux_dir / "vmlinux"], capture_output=True, text=True, check=False)
    if result.returncode:
        fail(f"cannot inspect vmlinux symbols: {result.stderr}")
    symbols = {
        match.group(2): int(match.group(1), 16)
        for line in result.stdout.splitlines()
        if (match := re.fullmatch(r"([0-9a-fA-F]+)\s+\w\s+(\S+)", line))
    }
    if "_text" not in symbols or "_end" not in symbols:
        fail("vmlinux lacks _text/_end symbols needed for load-overlap validation")
    decompressed = (0x80008000, 0x80008000 + symbols["_end"] - symbols["_text"])
    if decompressed[1] > ram[1]:
        fail(f"decompressed kernel ends beyond RAM at {decompressed[1]:#x}")
    if overlaps(dtb_range, decompressed):
        fail(
            f"DTB {dtb_range[0]:#x}-{dtb_range[1]:#x} overlaps decompressed kernel "
            f"{decompressed[0]:#x}-{decompressed[1]:#x}"
        )
    if overlaps(dtb_range, zimage_range):
        fail(
            f"DTB {dtb_range[0]:#x}-{dtb_range[1]:#x} overlaps compressed zImage "
            f"{zimage_range[0]:#x}-{zimage_range[1]:#x}"
        )
    relocation_headroom = 1024 * 1024
    relocation_end = decompressed[1] + (images / "zImage").stat().st_size + relocation_headroom
    if dtb_start < relocation_end:
        fail(
            f"DTB at {dtb_start:#x} leaves insufficient decompressor relocation room; "
            f"need at least {relocation_end:#x} for kernel + compressed zImage + 1 MiB workspace"
        )


def check_boot_script(output: Path, board: Path) -> None:
    dumpimage = output / "host/bin/dumpimage"
    with tempfile.TemporaryDirectory() as directory:
        extracted = Path(directory) / "boot.payload"
        result = subprocess.run(
            [dumpimage, "-T", "script", "-p", "0", "-o", extracted, output / "images/boot.scr"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            fail(f"dumpimage could not extract boot.scr: {result.stderr}")
        payload = extracted.read_bytes()
    source = (board / "boot.cmd").read_bytes()
    if len(payload) < 8 or struct.unpack(">I", payload[:4])[0] != len(source) or payload[4:8] != b"\0\0\0\0":
        fail("boot.scr has an invalid legacy script payload table")
    if payload[8:] != source:
        fail("boot.scr payload differs from board/boot-console/boot.cmd")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="Buildroot output directory")
    args = parser.parse_args()
    output = args.output.resolve()

    buildroot_path = output / ".config"
    linux_path = one(list((output / "build").glob("linux-*/.config")), "resolved Linux .config")
    uboot_path = one(list((output / "build").glob("uboot-*/.config")), "resolved U-Boot .config")
    busybox_path = one(list((output / "build").glob("busybox-*/.config")), "resolved BusyBox .config")
    dtb_candidates = list((output / "images").glob("*boot-console*.dtb"))
    if not dtb_candidates and (output / "images/linux.dtb").is_file():
        dtb_candidates = [output / "images/linux.dtb"]
    dtb_path = one(dtb_candidates, "Boot Console DTB")

    require(config(buildroot_path), buildroot_path, {
        "BR2_arm": "y",
        "BR2_arm926t": "y",
        "BR2_LINUX_KERNEL": "y",
        "BR2_TARGET_UBOOT": "y",
        "BR2_TARGET_ROOTFS_EXT2": "y",
        "BR2_TARGET_GENERIC_REMOUNT_ROOTFS_RW": "n",
        "BR2_REPRODUCIBLE": "y",
        "BR2_PACKAGE_DROPBEAR": "y",
    })
    require(config(linux_path), linux_path, {
        "CONFIG_ARCH_SUNXI": "y",
        "CONFIG_DEVTMPFS": "y",
        "CONFIG_DEVTMPFS_MOUNT": "y",
        "CONFIG_MMC_SUNXI": "y",
        "CONFIG_VFAT_FS": "y",
        "CONFIG_SERIAL_8250_CONSOLE": "y",
        "CONFIG_USB_MUSB_SUNXI": "y",
        "CONFIG_USB_MUSB_GADGET": "y",
        "CONFIG_CONFIGFS_FS": "y",
        "CONFIG_USB_CONFIGFS": "y",
        "CONFIG_USB_CONFIGFS_ACM": "y",
        "CONFIG_USB_CONFIGFS_ECM": "y",
        "CONFIG_USB_G_SERIAL": "n",
        "CONFIG_USB_GADGET_VBUS_DRAW": "500",
        "CONFIG_USB": "n",
        "CONFIG_NOP_USB_XCEIV": "y",
        "CONFIG_PHY_SUN4I_USB": "y",
        "CONFIG_LEDS_GPIO": "y",
        "CONFIG_LEDS_TRIGGER_ACTIVITY": "y",
        "CONFIG_NET": "y",
        "CONFIG_INET": "y",
        "CONFIG_EXT4_FS": "y",
        "CONFIG_SPI": "n",
    })
    require(config(uboot_path), uboot_path, {
        "CONFIG_ARCH_SUNXI": "y",
        "CONFIG_MACH_SUNIV": "y",
        "CONFIG_CONS_INDEX": "1",
        "CONFIG_BAUDRATE": "115200",
        "CONFIG_DRAM_CLK": "156",
        "CONFIG_SYS_BOOTM_LEN": "0x1000000",
    })
    require(config(busybox_path), busybox_path, {
        "CONFIG_INIT": "y",
        "CONFIG_GETTY": "y",
        "CONFIG_MOUNT": "y",
        "CONFIG_FEATURE_MOUNT_FSTAB": "y",
        "CONFIG_SH_IS_ASH": "y",
        "CONFIG_HTTPD": "y",
        "CONFIG_FEATURE_HTTPD_CGI": "y",
        "CONFIG_UDHCPD": "y",
        "CONFIG_IFCONFIG": "y",
    })
    board = Path(__file__).resolve().parents[1] / "board/boot-console"
    check_dtb(dtb_path)
    check_board_source(board)
    check_image(output / "images")
    check_memory_layout(output, board)
    check_boot_script(output, board)
    print(f"PASS: resolved configs and compiled {dtb_path.name} match the board contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
