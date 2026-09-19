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
  active low. Linux starts it with the heartbeat trigger.
- The +3V3 voltage-class rail is a fixed, hardware-managed supply with the
  revised nominal target of 3.404878 V. Linux does not sequence a PMIC.

All other exposed SoC peripherals remain disabled by the SoC `.dtsi`. SPI0 is
also unavailable because PC0 is reserved for the status LED.

## Consoles

The UART login is always present on `/dev/ttyS0`. The built-in `g_serial`
driver defaults to CDC ACM and creates `/dev/ttyGS0`; the wrapper waits for that
node before starting its getty, including when the UDC probes late. Disconnecting
the USB cable does not terminate the device-side TTY.

The Buildroot configuration enables root login with an empty password. Pinned
Buildroot 2026.02.2 intentionally has no `/etc/securetty`, so BusyBox does not
restrict root login to a hard-coded terminal list; both `ttyS0` and `ttyGS0`
reach the same passwordless root login. This image is for direct bring-up only.

For this bring-up image, `g_serial` uses the upstream development identity
`0525:a4a7` donated for the Linux-USB CDC ACM gadget. This does not allocate a
USB product identity to Boot Console and must not be treated as a production
VID/PID.

The board-specific Linux patch corrects legacy `g_serial`'s generic
self-powered descriptor: Boot Console reports itself as VBUS-powered with a
500 mA configured-load budget. `CONFIG_USB_GADGET_VBUS_DRAW=500` supplies the
same fallback for composite configurations. This declaration neither enforces
nor measures current. R29 sets the separate TPS2553 limit to about 520 mA
typical with a documented 475-565 mA range, and assembled-hardware startup
current remains unmeasured.

## Status LED control

The LED class device is normally
`/sys/class/leds/boot-console:green:status`. Disable the heartbeat and set the
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
