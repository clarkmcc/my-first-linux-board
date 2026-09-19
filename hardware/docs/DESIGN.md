# Final hardware design

The board is a minimal F1C200S Linux computer intended to boot from microSD and expose a console through UART or USB. It uses a four-layer 44 × 44 mm PCB with rounded corners, four M2.5 mounting holes, and an inset exposed-copper border finished with ENIG.

## Power tree

USB-C VBUS enters through a TPS2553 current-limited switch. Three TPS62160 converters generate the processor core, DDR, and I/O rails; a TLV75528 generates the analog rail. A TPS386000 holds the processor in reset until all four rails are valid. The voltage-class net names remain `+1V1`, `+2V5`, and `+3V3`; their precise nominal targets are 1.131707 V, 2.556098 V, and 3.404878 V.

## Boot and interfaces

The 24 MHz crystal provides the processor reference clock. The boot ROM reads SPL from microSD, SPL initializes the integrated DDR, U-Boot loads the kernel and device tree, and Linux mounts the second microSD partition as its root filesystem.

The UART header is ordered GND, TX, RX and uses 3.3 V logic. USB-C carries both 5 V input and the native USB peripheral data pair. The status LED is connected from 3.3 V through R31 and D3 to PC0, so software turns it on by driving PC0 low.

## Assembly

All SMD parts except the microSD socket are on the top side to support hot-plate assembly. The UART header is through-hole. The top side should be reflowed first; solder the bottom microSD socket and UART header afterward. USB-C retention stakes may also benefit from hand soldering.

The component choices and their first-principles purposes are listed in [COMPONENT-PURPOSE.md](COMPONENT-PURPOSE.md).
