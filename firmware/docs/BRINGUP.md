# Firmware validation and first-board bring-up

This procedure separates checks that can run before hardware exists from checks
that require an assembled board. Passing the build checks means the image is
internally consistent. It does not establish that the board boots.

## Pre-hardware gate

Run these commands from `my-first-linux-board/firmware`:

```sh
./build-container.sh
./build-container.sh validate
shasum -a 256 output/images/sdcard.img
```

The validator reads the resolved Buildroot, Linux, and U-Boot configurations. It
decompiles the generated DTB with `dtc` and checks the 64 MiB memory range,
UART0 PE0/PE1 selection, SDC0 settings, PC0 active-low activity LED, native USB
peripheral mode, and disabled SPI0. It also checks the ACM+ECM configfs gadget,
DHCP policy, SSH host-key storage, web endpoint, boot arguments, partitions, and
getty startup. A source-only review or successful DTS preprocessing is not a
substitute for this command.

Record the source revisions from `SOURCES.md`, build log, validator output, image
size, and SHA-256 digest with the board test record. Keep the generated image as
the exact artifact under test.

Before using an image, also confirm from the build log and generated files that:

- SPL plus U-Boot fits in its 1016 KiB raw region beginning at 8 KiB.
- `zImage`, `linux.dtb`, and `boot.scr` fit in the 16 MiB FAT partition.
- The zImage input, decompressed kernel, DTB, U-Boot runtime, and stack do not
  overlap anywhere in `0x80000000`–`0x83ffffff`.
- `/dev/mmcblk0p2` is the ext4 root partition and the kernel command line mounts
  it read-only.
- `CONFIG_USB_CONFIGFS_ACM=y` and `CONFIG_USB_CONFIGFS_ECM=y` are built in;
  legacy `CONFIG_USB_G_SERIAL` is disabled. Development identity `1d6b:0104`
  is expected until a production VID/PID is assigned.

The first-boot image starts from `multi_v5_defconfig`. Its resolved configuration
contains `CONFIG_I2C=y` and several unused I2C controller drivers even though no
I2C node is enabled for this board and no I2C userspace tooling is included.
This is accepted bring-up-image baggage. Kernel size pruning belongs after a
successful hardware boot. `CONFIG_SPI=n` remains required; the IPv4 network
stack exists only for the USB ECM link.

Do not write the image to an SD card as part of this gate. Selecting and
overwriting a removable device is a separate, destructive operation.

## Equipment and setup

Use a current-limited 5 V bench supply or a USB-C source with a USB power meter,
a 3.3 V USB-to-UART adapter, a known-good microSD card prepared from the validated
image, a multimeter, and an oscilloscope for reset and clock checks. Leave the
UART adapter's power pin disconnected. Connect only GND, adapter RX to board TX
(J3 pin 2), and adapter TX to board RX (J3 pin 3). Open 115200 8N1 with no flow
control before applying board power.

Inspect for shorts, reversed polarized parts, solder bridges around U1 and the
microSD socket, and connector damage. With power disconnected, measure resistance
from each rail to ground and record it. Stop if a reading indicates a hard short
or differs sharply from the same rail on another board.

## Power-only check

Start with a conservative current limit. Raise it only after the input and rails
behave normally; do not repeatedly cycle a board that remains at the limit.
Apply 5 V without an SD card and record input current and these rails:

| Test point or net | Nominal value |
| --- | ---: |
| `+1V1` | 1.132 V |
| `+2V5` | 2.556 V |
| `+3V3` | 3.405 V |
| `+2V8_A` | 2.800 V |
| `DDR_VREF` | 1.278 V |

Verify the 24 MHz oscillator starts and `RESET_N` remains low until all monitored
rails are valid, then releases after the expected 14–24 ms delay. Record scope
captures of power-up and reset. Stop for a missing rail, sustained current-limit
operation, excessive heating, an unstable oscillator, or reset that never
releases.

## First boot over UART

Insert the prepared card while power is off, start the UART capture, then apply
power. Preserve the complete log. Expected milestones, in order, are:

1. U-Boot SPL banner on UART0.
2. U-Boot reports approximately 64 MiB DRAM and finds the SD card.
3. U-Boot loads `zImage` and `linux.dtb` and executes `bootz` without an overlap
   or bad-FDT error.
4. Linux emits early console output on `ttyS0`, mounts `/dev/mmcblk0p2` as ext4
   read-only, starts BusyBox init, and presents a login prompt.
5. The green status LED begins flickering with CPU activity.

At the shell, capture:

```sh
cat /proc/cmdline
cat /proc/meminfo
mount
dmesg
cat /sys/class/leds/boot-console:green:status/trigger
```

Confirm usable memory is consistent with 64 MiB minus kernel reservations,
`/` is mounted `ro`, `/run` and `/tmp` are tmpfs, and there is no repeating getty
or driver error. Power-cycle at least ten times and confirm every capture reaches
the login prompt without manual intervention.

## Peripheral checks

For microSD, copy a test file to `/tmp`, read stable data from the root filesystem,
and inspect `dmesg` for timeouts or CRC errors. The final image uses the
hardware-proven one-bit, 12.5 MHz SDC0 configuration with `broken-cd`; hot
insertion is outside this first-board test.

For the LED, disable the trigger and command both states:

```sh
echo none > /sys/class/leds/boot-console:green:status/trigger
echo 1 > /sys/class/leds/boot-console:green:status/brightness
echo 0 > /sys/class/leds/boot-console:green:status/brightness
```

Brightness `1` must light the active-low PC0 LED. Confirm SPI0 is absent or
disabled in the live device tree.

Connect the native USB-C port to a host only after UART boot is stable. Confirm
the host enumerates composite device `1d6b:0104` with CDC ACM and CDC ECM,
`/dev/ttyGS0` and `usb0` exist on the board, and a terminal reaches a login
prompt. Confirm `usb0` is `192.168.7.2/24` and the host receives an address from
`192.168.7.10`–`192.168.7.20` without a default route or DNS setting from this
link. Then test from the host:

```sh
curl http://192.168.7.2/cgi-bin/status
ssh root@192.168.7.2
```

Open `http://192.168.7.2/` and confirm CPU, memory, uptime, load, kernel, and LED
status update. The SSH password is blank on this directly attached development
image. Reboot once and verify the SSH fingerprint remains stable because its
generated host key is stored on the FAT boot partition. Disconnect and reconnect
the host several times; UART must remain usable and the USB getty must not enter
a rapid restart loop.

## Failure localization

No UART text points first to input power, rails, reset, oscillator, boot ROM SD
access, or the PE0/PE1 connection. An SPL banner followed by failure points to
DRAM initialization. A U-Boot prompt without Linux output points to file loading,
load-address overlap, DTB validity, or boot arguments. Kernel output followed by
a root-mount panic points to SDC0, partition numbering, ext4 support, or
`rootwait`. A working UART login with no USB console isolates the problem to the
USB PHY/controller, configfs gadget setup, cable, or host enumeration. ACM
working while Ethernet fails narrows the problem to the ECM function, host
driver, `usb0` setup, or DHCP. Record the full UART log and measured rails before
changing the image or board.
