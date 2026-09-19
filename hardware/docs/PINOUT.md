# Pinout

Final pin and net assignments for the fabricated board. Empty net cells are intentional unused pins. The UART header order is GND, TX, RX and uses 3.3 V logic.

| Refdes | Pin | Name | Net | Notes |
|---|---|---|---|---|
| U2 | 1 | PGND | GND | |
| U2 | 2 | VIN | +5V_SYS | |
| U2 | 3 | EN | +5V_SYS | |
| U2 | 4 | AGND | GND | |
| U2 | 5 | FB | FB_1 | |
| U2 | 6 | VOS | +1V1 | |
| U2 | 7 | SW | SW_1 | |
| U2 | 8 | PG |  | |
| U3 | 1 | PGND | GND | |
| U3 | 2 | VIN | +5V_SYS | |
| U3 | 3 | EN | +5V_SYS | |
| U3 | 4 | AGND | GND | |
| U3 | 5 | FB | FB_2 | |
| U3 | 6 | VOS | +2V5 | |
| U3 | 7 | SW | SW_2 | |
| U3 | 8 | PG |  | |
| U4 | 1 | PGND | GND | |
| U4 | 2 | VIN | +5V_SYS | |
| U4 | 3 | EN | +5V_SYS | |
| U4 | 4 | AGND | GND | |
| U4 | 5 | FB | FB_3 | |
| U4 | 6 | VOS | +3V3 | |
| U4 | 7 | SW | SW_3 | |
| U4 | 8 | PG |  | |
| U5 | 1 | IN | VBUS | |
| U5 | 3 | EN | VBUS | |
| U5 | 6 | OUT | +5V_SYS | |
| U5 | 5 | ILIM | ILIM | |
| U5 | 4 | FAULT_N |  | |
| U5 | 2 | GND | GND | |
| U6 | 1 | IN | +5V_SYS | |
| U6 | 2 | GND | GND | |
| U6 | 3 | EN | +5V_SYS | |
| U6 | 4 | NC |  | |
| U6 | 5 | OUT | +2V8_A | |
| U1 | 22 | VDD_CORE | +1V1 | |
| U1 | 35 | VDD_CORE | +1V1 | |
| U1 | 71 | VDD_CORE | +1V1 | |
| U1 | 30 | VCC_DRAM | +2V5 | |
| U1 | 31 | VCC_DRAM | +2V5 | |
| U1 | 32 | VCC_DRAM | +2V5 | |
| U1 | 34 | VCC_DRAM | +2V5 | |
| U1 | 36 | VCC_DRAM | +2V5 | |
| U1 | 5 | VCC_IO | +3V3 | |
| U1 | 20 | VCC_IO | +3V3 | |
| U1 | 50 | VCC_IO | +3V3 | |
| U1 | 67 | UVCC | +3V3 | |
| U1 | 4 | HPVCC | +3V3 | |
| U1 | 73 | TV_VCC | +3V3 | |
| U1 | 80 | AVCC | +2V8_A | |
| U1 | 33 | SVREF | DDR_VREF | |
| U1 | 2 | HPCOMFB |  | |
| U1 | 3 | HPCOM |  | |
| U1 | 75 | TV_VRN | TV_VRN | |
| U1 | 76 | TV_VRP | TV_VRP | |
| U1 | 81 | VRA1 | VRA1 | |
| U1 | 83 | VRA2 | VRA2 | |
| U1 | 74 | TVGND | GND | |
| U1 | 82 | AGND | GND | |
| U1 | 89 | EPAD | GND | |
| U1 | 51 | HOSCI | XTAL_IN | |
| U1 | 52 | HOSCO | XTAL_OUT | |
| U1 | 70 | RESET_N | RESET_N | |
| U1 | 53 | PF5 / SD_D2 | SD_D2 | |
| U1 | 54 | PF4 / SD_D3 | SD_D3 | |
| U1 | 55 | PF3 / SD_CMD | SD_CMD | |
| U1 | 56 | PF2 / SD_CLK | SD_CLK_SRC | |
| U1 | 57 | PF1 / SD_D0 | SD_D0 | |
| U1 | 58 | PF0 / SD_D1 | SD_D1 | |
| U1 | 48 | PE1 / UART0_TX | UART_TX | |
| U1 | 49 | PE0 / UART0_RX | UART_RX | |
| U1 | 68 | USB_DM | USB_D- | |
| U1 | 69 | USB_DP | USB_D+ | |
| U1 | 1 | HPL |  | |
| U1 | 88 | HPR |  | |
| U1 | 72 | TVOUT |  | |
| U1 | 77 | TVIN1 |  | |
| U1 | 78 | TVIN0 |  | |
| U1 | 79 | LRADC0 |  | |
| U1 | 84 | FMINL |  | |
| U1 | 85 | FMINR |  | |
| U1 | 86 | LINL |  | |
| U1 | 87 | MICIN |  | |
| U1 | 6 | PD0 |  | |
| U1 | 7 | PD1 |  | |
| U1 | 8 | PD2 |  | |
| U1 | 9 | PD3 |  | |
| U1 | 10 | PD4 |  | |
| U1 | 11 | PD5 |  | |
| U1 | 12 | PD6 |  | |
| U1 | 13 | PD7 |  | |
| U1 | 14 | PD8 |  | |
| U1 | 15 | PD9 |  | |
| U1 | 16 | PD10 |  | |
| U1 | 17 | PD11 |  | |
| U1 | 18 | PD12 |  | |
| U1 | 19 | PD13 |  | |
| U1 | 21 | PD14 |  | |
| U1 | 23 | PD15 |  | |
| U1 | 24 | PD16 |  | |
| U1 | 25 | PD17 |  | |
| U1 | 26 | PD18 |  | |
| U1 | 27 | PD19 |  | |
| U1 | 28 | PD20 |  | |
| U1 | 29 | PD21 |  | |
| U1 | 37 | PE12 |  | |
| U1 | 38 | PE11 |  | |
| U1 | 39 | PE10 |  | |
| U1 | 40 | PE9 |  | |
| U1 | 41 | PE8 |  | |
| U1 | 42 | PE7 |  | |
| U1 | 43 | PE6 |  | |
| U1 | 44 | PE5 |  | |
| U1 | 45 | PE4 |  | |
| U1 | 46 | PE3 |  | |
| U1 | 47 | PE2 |  | |
| U1 | 59 | PC0 | STATUS_LED_N | |
| U1 | 60 | PC1 |  | |
| U1 | 61 | PC2 |  | |
| U1 | 62 | PC3 |  | |
| U1 | 63 | PA3 |  | |
| U1 | 64 | PA2 |  | |
| U1 | 65 | PA1 |  | |
| U1 | 66 | PA0 |  | |
| U7 | 14 | VDD | +3V3 | |
| U7 | 10 | SENSE1 | SENSE_3V3 | |
| U7 | 9 | SENSE2 | SENSE_2V8 | |
| U7 | 8 | SENSE3 | SENSE_2V5 | |
| U7 | 7 | SENSE4L | SENSE_1V1 | |
| U7 | 6 | SENSE4H | GND | |
| U7 | 1 | MR_N | RESET_BUTTON | |
| U7 | 12 | GND | GND | |
| U7 | 11 | NC_GND | GND | |
| U7 | 21 | EPAD | GND | |
| U7 | 15 | RESET1_N | RESET_N | |
| U7 | 16 | RESET2_N | RESET_N | |
| U7 | 17 | RESET3_N | RESET_N | |
| U7 | 18 | RESET4_N | RESET_N | |
| U7 | 5 | CT1 |  | |
| U7 | 4 | CT2 |  | |
| U7 | 3 | CT3 |  | |
| U7 | 2 | CT4 |  | |
| U7 | 13 | VREF |  | |
| U7 | 19 | WDO_N |  | |
| U7 | 20 | WDI | GND | |
