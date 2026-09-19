# Boot Console board support

This directory contains the Linux board description, kernel fragment, and
read-only-root-compatible userspace overlay for the F1C200s Boot Console.
`/run`, `/tmp`, `/var`, and `/dev/shm` are RAM-backed; login accounting files
are created under volatile `/var` before either getty starts.

## Hardware contract

- 64 MiB SDRAM starts at `0x80000000`.
- microSD uses SDC0 with PF0 clock, PF1 command, and PF2 data in one-bit mode.
  Card detect is not connected, so `broken-cd` is required. The final image
  limits the bus to the hardware-proven 12.5 MHz.
- UART0 is PE0 RX and PE1 TX at 115200 8N1. It is the bootloader and Linux
  console.
- Native USB D+/D- operates only as a peripheral. There is no ID-detect GPIO or
  software-controlled VBUS source on this board.
- The green status LED is wired from +3V3 through the LED to PC0, so it is
  active low. Linux starts it with the CPU activity trigger.
- The +3V3 voltage-class rail is a fixed, hardware-managed supply with the
  revised nominal target of 3.404878 V. Linux does not sequence a PMIC.

All other exposed SoC peripherals remain disabled by the SoC `.dtsi`. SPI0 is
also unavailable because PC0 is reserved for the status LED.

## USB console and Ethernet

The UART login is always present on `/dev/ttyS0`. A configfs composite gadget
adds CDC ACM serial as `/dev/ttyGS0` and CDC ECM Ethernet as `usb0`; the getty
wrapper waits for a late gadget TTY. Gadget setup also waits asynchronously for
the UDC and network interface, so it never blocks the UART login or startup.

The board uses `192.168.7.2/24`. BusyBox `udhcpd` leases
`192.168.7.10`–`192.168.7.20` to the attached host and deliberately sends no
router or DNS option. Dropbear SSH and a BusyBox HTTP Prometheus endpoint listen
on the link. `/cgi-bin/metrics` is the only HTTP resource; `/` and every other
path intentionally return 404. The endpoint emits Prometheus 0.0.4 text for
board identity, time, CPU, load, memory, VM, pressure, filesystems, microSD,
networking, sockets, entropy, LED state, services, USB gadget state, and any
available thermal, CPU-frequency, and watchdog data:

```sh
curl http://192.168.7.2/cgi-bin/metrics
```

macOS may enumerate ECM before Network Settings creates a service. Find the
interface whose `ether` address is `02:00:00:00:07:01`, assign the host side
`192.168.7.1` for immediate access, and ask macOS to detect the new hardware:

```sh
iface=$(for interface in $(ifconfig -l); do
  ifconfig "$interface" | grep -q 'ether 02:00:00:00:07:01' && echo "$interface"
done)
sudo ifconfig "$iface" inet 192.168.7.1 netmask 255.255.255.0 up
sudo networksetup -detectnewhardware
```

The direct address lasts until the interface is removed or reconfigured. After
`networksetup -detectnewhardware` creates the service, give it the persistent
static address used by this direct link. The service on the tested Mac is named
`Clark's Board Console + Ethernet`:

```sh
sudo networksetup -setmanual "Clark's Board Console + Ethernet" \
  192.168.7.1 255.255.255.0 0.0.0.0
```

If macOS uses a different service name, find it with
`networksetup -listallnetworkservices` and substitute that name. DHCP did not
activate this ECM link reliably, so keep the host address static.

The Buildroot configuration enables root login with an empty password. Pinned
Buildroot 2026.02.2 intentionally has no `/etc/securetty`, so BusyBox does not
restrict root login to a hard-coded terminal list; `ttyS0`, `ttyGS0`, and
Dropbear reach the same passwordless root login. This is for a direct development
cable only. The first boot generates an Ed25519 host key on the FAT boot
partition at `/boot/dropbear`, preserving the SSH identity without writing the
read-only ext4 root. If `/boot` cannot mount, the startup script falls back to an
ephemeral key under `/run` and reports that condition on the console.

The configfs gadget uses Linux Foundation development identity `1d6b:0104`.
This does not allocate a production USB identity to Clark's Board. Its configfs
configuration explicitly reports bus power and 500 mA maximum configured load;
this declaration neither enforces nor measures current. R29 sets the separate
TPS2553 limit to about 520 mA typical with a documented 475–565 mA range.

## Status LED control

The LED class device is normally
`/sys/class/leds/boot-console:green:status`. Disable CPU activity and set the
LED manually with:

```sh
echo none > /sys/class/leds/boot-console:green:status/trigger
echo 1 > /sys/class/leds/boot-console:green:status/brightness
echo 0 > /sys/class/leds/boot-console:green:status/brightness
```

The LED driver accounts for its active-low wiring, so brightness `1` means lit.

## Bootloader requirement

Upstream U-Boot's sunxi SPL code configures PE0 and PE1 as UART0 when
`CONFIG_MACH_SUNIV=y` and `CONFIG_CONS_INDEX=1`. Keep those settings in the
board configuration. Selecting another console index loses the required UART
output before the device tree is available.

## Limits of validation

The board data comes from `hardware/docs/PINOUT.md`. A successful build
can validate preprocessing, device-tree syntax, and resolved kernel options.
UART signaling, SDRAM stability, SD timing, USB enumeration, and LED polarity
still require tests on assembled hardware.
