# Why each component exists

Every physical reference in the final board is listed below. Each explanation starts from the electrical or mechanical job the part performs; repeated bypass capacitors remain separate because their physical location serves a different current loop.

The board has 89 fitted electronic components and four M2.5 mounting holes. C32-C35 are intentionally absent.

| Reference | Value | Decision basis | Why it exists, from first principles | Evidence |
| --- | --- | --- | --- | --- |
| C1 | 30p / C0G / 1% | Functional | This capacitor supplies the oscillator input side of the crystal load network. Together with C2 and stray capacitance, it sets the load that determines crystal frequency. | XTAL |
| C2 | 30p / C0G / 1% | Functional | This capacitor supplies the oscillator output side of the crystal load network. Its initial 30 pF value needs confirmation with the assembled board, as does C1. | XTAL |
| C3 | 100n / 100V | Reliability | Fast interference can move the DDR comparison voltage and cause bit errors. C3 stores charge at that reference, reducing rapid voltage changes relative to ground. | REF |
| C4 | 100n / 100V | Reliability | The DDR reference must track half the memory supply, including fast supply changes. C4 and C3 form a capacitive divider that preserves this relationship. | REF |
| C5 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C5 provides local charge for U1 pin 22, serving its processor core domain. | AW, REF |
| C6 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C6 provides local charge for U1 pin 35, serving its processor core domain. | AW, REF |
| C7 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C7 provides local charge for U1 pin 71, serving its processor core domain. | AW, REF |
| C8 | 4.7u / 10V | Reliability | The core supply can briefly demand more current than its regulator delivers through the connecting traces. This local 4.7 µF reservoir reduces voltage droop during those changes. | REF |
| C9 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C9 provides local charge for U1 pin 30, serving its DDR memory domain. | AW, REF |
| C10 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C10 provides local charge for U1 pin 31, serving its DDR memory domain. | AW, REF |
| C11 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C11 provides local charge for U1 pin 32, serving its DDR memory domain. | AW, REF |
| C12 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C12 provides local charge for U1 pin 34, serving its DDR memory domain. | AW, REF |
| C13 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C13 provides local charge for U1 pin 36, serving its DDR memory domain. | AW, REF |
| C14 | 4.7u / 10V | Reliability | The DDR supply can briefly demand more current than its regulator delivers through the connecting traces. This local 4.7 µF reservoir reduces voltage droop during those changes. | REF |
| C15 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C15 provides local charge for U1 pin 5, serving its I/O domain. | AW, REF |
| C16 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C16 provides local charge for U1 pin 20, serving its I/O domain. | AW, REF |
| C17 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C17 provides local charge for U1 pin 50, serving its I/O domain. | AW, REF |
| C18 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C18 provides local charge for U1 pin 67, serving its USB domain. | AW, REF |
| C19 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C19 provides local charge for U1 pin 4, serving its headphone supply domain. | AW, REF |
| C20 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C20 provides local charge for U1 pin 73, serving its TV supply domain. | AW, REF |
| C21 | 4.7u / 10V | Reliability | The I/O supply can briefly demand more current than its regulator delivers through the connecting traces. This local 4.7 µF reservoir reduces voltage droop during those changes. | REF |
| C22 | 100n / 100V | Reliability | Trace inductance prevents distant capacitors from supplying very fast current changes. C22 provides local charge for U1 pin 80, serving its analog supply domain. | AW, REF |
| C23 | 4.7u / 10V | Reliability | The analog supply can briefly demand more current than its regulator delivers through the connecting traces. This local 4.7 µF reservoir reduces voltage droop during those changes. | REF |
| C24 | 1u / 25V | Reference precaution | This capacitor stores charge on the VRA1 analog reference, reducing rapid voltage changes. It preserves reference-board support for powered silicon, although its necessity with audio disabled is not documented. | REF |
| C25 | 1u / 25V | Reference precaution | This capacitor stores charge on the VRA2 analog reference, reducing rapid voltage changes. It preserves reference-board support for powered silicon, although its necessity with audio disabled is not documented. | REF |
| C26 | 10u / 10V | Reference precaution | This capacitor reduces rapid voltage changes on TV_VRN, an internal video reference brought outside U1. It preserves reference-board support, although its necessity with video disabled is not documented. | REF |
| C27 | 10u / 10V | Reference precaution | This capacitor reduces rapid voltage changes on TV_VRP, an internal video reference brought outside U1. It preserves reference-board support, although its necessity with video disabled is not documented. | REF |
| C28 | 1u / 25V | Reference precaution | This capacitor resists rapid changes in the voltage difference between the two video reference pins. It reproduces the reference circuit, but its necessity with video disabled is not documented. | REF |
| C29 | 1u / 25V | Reliability | Cable inductance resists sudden input-current changes, which can disturb the 5 V input. This capacitor supplies local charge at the power switch input without directly exposing the larger downstream capacitors. | SWITCH |
| C30 | 100n / 100V | Reliability | The microSD card draws fast current pulses that remote capacitors cannot supply through trace inductance. This 100 nF capacitor supplies those pulses beside the socket power pin. | SD, REF |
| C31 | 10u / 10V | Reliability | A microSD card also changes its current demand over longer intervals during internal operations. This 10 µF reservoir reduces local supply droop while the regulator responds. | SD, REF |
| C36 | 100n / 100V | Reliability | The reset supervisor also needs a steady supply to make dependable voltage decisions. This nearby capacitor supplies its fast current changes without relying on distant capacitors. | SUP |
| C37 | 10u / 10V | Architecture | The switching regulator draws input current in pulses. This nearby capacitor supplies those pulses, reducing input-voltage disturbance and the area of the high-current switching loop. | BUCK |
| C38 | 22u / 16V | Architecture | The inductor current does not exactly match the changing 1.1 V core load current. This output capacitor absorbs the difference and participates in the regulator control response. | BUCK |
| C39 | 10u / 10V | Architecture | The switching regulator draws input current in pulses. This nearby capacitor supplies those pulses, reducing input-voltage disturbance and the area of the high-current switching loop. | BUCK |
| C40 | 22u / 16V | Architecture | The inductor current does not exactly match the changing 2.5 V DDR load current. This output capacitor absorbs the difference and participates in the regulator control response. | BUCK |
| C41 | 10u / 10V | Architecture | The switching regulator draws input current in pulses. This nearby capacitor supplies those pulses, reducing input-voltage disturbance and the area of the high-current switching loop. | BUCK |
| C42 | 22u / 16V | Architecture | The inductor current does not exactly match the changing 3.3 V I/O load current. This output capacitor absorbs the difference and participates in the regulator control response. | BUCK |
| C43 | 1u / 25V | Architecture | Input wiring cannot supply every rapid current change at the analog regulator. This local input capacitor reduces those voltage changes and meets the regulator input-capacitance requirement. | LDO |
| C44 | 1u / 25V | Architecture | The analog regulator needs local output capacitance for a stable control response. C44 supplies that capacitance at the regulator, while the processor capacitors serve the distant load. | LDO |
| D1 | USBLC6-2SC6 | Protection | A charged person or cable can inject a short, high-voltage pulse into USB signals. D1 diverts that pulse toward the supply clamp and ground, reducing stress on U1. | ESD |
| D2 | Green LED / low current | Requested | An LED converts electrical current into visible light. D2 lights from the 3.3 V rail so you can see that this supply is present without relying on software. | LED, USER |
| D3 | Green LED / low current | Requested | An LED can turn a processor output into a visible status signal. D3 lights when PC0 sinks current, allowing Linux to display activity or a state you choose. | LED, AW, USER |
| H1 | M2.5 / 2.7mm | Requested | The board needs a mechanical attachment that does not depend on its connectors. This upper-left 2.7 mm clearance hole provides one of the four requested M2.5 screw locations. | USER |
| H2 | M2.5 / 2.7mm | Requested | The board needs a mechanical attachment that does not depend on its connectors. This upper-right 2.7 mm clearance hole provides one of the four requested M2.5 screw locations. | USER |
| H3 | M2.5 / 2.7mm | Requested | The board needs a mechanical attachment that does not depend on its connectors. This lower-left 2.7 mm clearance hole provides one of the four requested M2.5 screw locations. | USER |
| H4 | M2.5 / 2.7mm | Requested | The board needs a mechanical attachment that does not depend on its connectors. This lower-right 2.7 mm clearance hole provides one of the four requested M2.5 screw locations. | USER |
| J1 | USB-C / USB4105-GF-A | Requested | The board needs an external source of energy and a physical USB connection. This USB-C receptacle supplies 5 V and connects the native USB data pair. | USB |
| J2 | microSD / 104031-0811 | Functional | U1 loses program memory without power, so Linux needs nonvolatile boot storage. This socket connects a removable microSD card that holds the bootloader, kernel, and filesystem. | AW, SD |
| J3 | GND / TX / RX | Functional | The processor sends boot messages as timed voltage pulses before Linux can offer USB services. This header exposes transmit, receive, and their common ground for a 3.3 V UART adapter. | AW, REF |
| L1 | 2.2uH / XFL4020 | Architecture | An inductor stores energy in a magnetic field and resists sudden current changes. It turns the regulator switching pulses into smoother current for the 1.1 V core supply. | BUCK, IND |
| L2 | 2.2uH / XFL4020 | Architecture | An inductor stores energy in a magnetic field and resists sudden current changes. It turns the regulator switching pulses into smoother current for the 2.5 V DDR supply. | BUCK, IND |
| L3 | 2.2uH / XFL4020 | Architecture | An inductor stores energy in a magnetic field and resists sudden current changes. It turns the regulator switching pulses into smoother current for the 3.3 V I/O supply. | BUCK, IND |
| R1 | 2k / 0.1% | Functional | DDR receivers need a comparison voltage halfway between their supply and ground. R1 and equal-valued R2 divide the DDR supply in half, giving a nominal 1.278049 V reference at the revised target. | AW, REF |
| R2 | 2k / 0.1% | Functional | This resistor provides the lower half of the DDR reference divider. Its match to R1 keeps the reference near half the memory supply. | AW, REF |
| R3 | 200k / 1% | Reference precaution | This resistor gives VRA1 a weak path to ground, allowing stored charge to dissipate. The reference boards include it, but the public documentation does not establish its necessity with audio disabled. | REF |
| R4 | 200k / 1% | Reference precaution | This resistor gives VRA2 a weak path to ground, allowing stored charge to dissipate. The reference boards include it, but the public documentation does not establish its necessity with audio disabled. | REF |
| R5 | 5.1k / 1% | Functional | A USB-C source detects a power-consuming device through a resistance to ground on the active configuration pin. R5 supplies that identification on CC1. | USB |
| R6 | 5.1k / 1% | Functional | Reversing the USB-C plug selects the other configuration pin. R6 supplies the same power-consumer identification on CC2, so either plug orientation can receive power. | USB |
| R7 | 47k / 1% | Functional | The SD command wire can be temporarily undriven during startup or bus handover. This weak pullup gives it a defined high level while allowing either device to pull it low. | SD, REF |
| R8 | 47k / 1% | Functional | The SD data 0 wire can be temporarily undriven during startup or bus handover. This weak pullup gives it a defined high level while allowing either device to pull it low. | SD, REF |
| R9 | 47k / 1% | Functional | The SD data 1 wire can be temporarily undriven during startup or bus handover. This weak pullup gives it a defined high level while allowing either device to pull it low. | SD, REF |
| R10 | 47k / 1% | Functional | The SD data 2 wire can be temporarily undriven during startup or bus handover. This weak pullup gives it a defined high level while allowing either device to pull it low. | SD, REF |
| R11 | 47k / 1% | Functional | The SD data 3 wire can be temporarily undriven during startup or bus handover. This weak pullup gives it a defined high level while allowing either device to pull it low. | SD, REF |
| R12 | 22R | Reliability | Fast clock edges reflect from trace discontinuities and can cross an input threshold more than once. This source-series resistor damps those reflections, with 22 Ω as the initial value. | REF |
| R13 | 67.3k / 0.1% | Architecture | The processor needs to remain in reset when its IO supply is too low. This upper divider resistor sets the nominal IO reset threshold to 3.092 V with R14. | SUP |
| R14 | 10k / 0.1% | Architecture | This resistor provides the ground side of the 3.3 V I/O monitoring divider. Its ratio to R13 sets the voltage at which U7 stops the processor. | SUP |
| R15 | 55.6k / 0.1% | Architecture | The supervisor compares its input against 0.4 V rather than the full 2.8 V analog supply. R15 and R16 scale that supply to give a nominal 2.624 V reset threshold. | SUP |
| R16 | 10k / 0.1% | Architecture | This resistor provides the ground side of the 2.8 V analog monitoring divider. Its ratio to R15 sets the voltage at which U7 stops the processor. | SUP |
| R17 | 48.7k / 0.1% | Architecture | The supervisor must distinguish a valid DDR supply from a brownout. This upper divider resistor scales DDR voltage to the sense input; its 10 ppm/C maximum temperature coefficient limits drift of the reset threshold. | SUP |
| R18 | 10k / 0.1% | Architecture | The supervisor senses a fraction of the DDR supply relative to ground. This lower divider resistor completes that ratio, with a 10 ppm/C maximum temperature coefficient to preserve reset-release margin over temperature. | SUP |
| R19 | 15.8k / 0.1% | Architecture | The supervisor compares its input against 0.4 V rather than the full 1.1 V core supply. R19 and R20 scale that supply to give a nominal 1.032 V reset threshold. | SUP |
| R20 | 10k / 0.1% | Architecture | This resistor provides the ground side of the 1.1 V core monitoring divider. Its ratio to R19 sets the voltage at which U7 stops the processor. | SUP |
| R21 | 100k / 1% | Architecture | U7 has no internal pullup on its manual-reset input, so an open button would leave that voltage undefined. This resistor pulls the input high until SW1 connects it to ground. | SUP |
| R22 | 47k / 1% | Architecture | U7 can pull RESET_N low but cannot actively drive it high. R22 supplies the high level after every supervisor channel releases its output. | SUP |
| R23 | 340R / 0.1% | Architecture | The regulator compares a fraction of the core supply against its internal reference to control the output voltage. This low-resistance feedback divider sets the revised target and reduces the voltage error caused by input leakage. | BUCK |
| R24 | 820R / 0.05% | Architecture | The regulator compares a fraction of the supply with its internal reference to control its output voltage. This lower divider resistor uses 0.05% tolerance and 10 ppm/C maximum drift to limit output uncertainty while its low resistance reduces feedback-pin leakage error. | BUCK |
| R25 | 1.8k / 0.1% | Architecture | The regulator compares a fraction of the DDR supply against its internal reference to control the output voltage. This low-resistance feedback divider sets the revised target and reduces the voltage error caused by input leakage. | BUCK |
| R26 | 820R / 0.05% | Architecture | The regulator compares a fraction of the supply with its internal reference to control its output voltage. This lower divider resistor uses 0.05% tolerance and 10 ppm/C maximum drift to limit output uncertainty while its low resistance reduces feedback-pin leakage error. | BUCK |
| R27 | 2.67k / 0.1% | Architecture | The regulator compares a fraction of the IO supply against its internal reference to control the output voltage. This low-resistance feedback divider sets the revised target and reduces the voltage error caused by input leakage. | BUCK |
| R28 | 820R / 0.05% | Architecture | The regulator compares a fraction of the supply with its internal reference to control its output voltage. This lower divider resistor uses 0.05% tolerance and 10 ppm/C maximum drift to limit output uncertainty while its low resistance reduces feedback-pin leakage error. | BUCK |
| R29 | 49.9k / 1% | Architecture | U5 needs a resistance to select its current limit. This 49.9 kΩ resistor sets approximately 520 mA typical, with the documented 475–565 mA range. | SWITCH |
| R30 | 1k / 1% | Functional | An LED does not limit its own current once forward biased. This 1 kOhm resistor drops the remaining rail voltage and limits power-indicator current to a small continuous load. | LED |
| R31 | 1k / 1% | Functional | The status LED and GPIO both need a limit on current. This 1 kOhm resistor sets a low indicator current so PC0 can control D3 directly without another switching component. | LED, AW |
| SW1 | RESET | Bring-up | A stalled processor may be unable to restart itself through software. This button requests a hardware reset without unplugging power or relying on a working console. | SUP |
| U1 | F1C200s | Functional | Linux needs a processor to execute instructions and RAM to hold running programs. U1 supplies both, including 64 MiB of memory inside its package. | AW |
| U2 | TPS62160DGKR | Functional | The 1.1 V core domain cannot run directly from USB 5 V. This switching regulator reduces the voltage while dissipating less heat than a linear regulator at comparable current. | BUCK, AW |
| U3 | TPS62160DGKR | Functional | The 2.5 V DDR domain cannot run directly from USB 5 V. This switching regulator reduces the voltage while dissipating less heat than a linear regulator at comparable current. | BUCK, AW |
| U4 | TPS62160DGKR | Functional | The 3.3 V I/O domain cannot run directly from USB 5 V. This switching regulator reduces the voltage while dissipating less heat than a linear regulator at comparable current. | BUCK, AW |
| U5 | TPS2553DBVT | Protection | Charging the board capacitors or a downstream short can demand excessive current from USB. U5 controls turn-on and limits current, although the board must still obey the source power allowance. | SWITCH |
| U6 | TLV75528PDBVR | Functional | The analog supply needs a lower voltage than the 3.3 V digital rail. This linear regulator produces 2.8 V from protected 5 V with few external parts. | LDO, AW |
| U7 | TPS386000RGPT | Reliability | Logic and memory can behave unpredictably while their supplies are too low. U7 holds the processor in reset until all four monitored rails pass their thresholds and release delays. | SUP |
| Y1 | 24 MHz / CL 18 pF | Functional | Digital operations need a regular timing reference. This quartz crystal resonates at 24 MHz, giving U1 a reference for its internal clock generators. | AW, XTAL |

## Schematic annotations

These five symbols are not purchased or placed on the board.

| Reference | Why it exists |
| --- | --- |
| #FLG01 | KiCad needs to know that ground has a power source despite the passive connection in its netlist. This annotation supplies that information and creates no physical component. |
| #FLG02 | KiCad needs to know that USB VBUS has a power source despite the passive connection in its netlist. This annotation supplies that information and creates no physical component. |
| #FLG03 | KiCad needs to know that the core rail has a power source despite the passive connection in its netlist. This annotation supplies that information and creates no physical component. |
| #FLG04 | KiCad needs to know that the DDR rail has a power source despite the passive connection in its netlist. This annotation supplies that information and creates no physical component. |
| #FLG05 | KiCad needs to know that the I/O rail has a power source despite the passive connection in its netlist. This annotation supplies that information and creates no physical component. |

## Intentionally unpopulated references

| Reference | Omitted value | Why it is not fitted |
| --- | --- | --- |
| C32 | 1 nF | This capacitor would filter fast disturbances at a supervisor sense input. It is optional with U7, so the final board uses short sense traces and built-in transient rejection. |
| C33 | 1 nF | This capacitor would filter fast disturbances at a supervisor sense input. It is optional with U7, so the final board uses short sense traces and built-in transient rejection. |
| C34 | 1 nF | This capacitor would filter fast disturbances at a supervisor sense input. It is optional with U7, so the final board uses short sense traces and built-in transient rejection. |
| C35 | 1 nF | This capacitor would filter fast disturbances at a supervisor sense input. It is optional with U7, so the final board uses short sense traces and built-in transient rejection. |


## Evidence

- **AW:** [Allwinner F1C200s datasheet](https://linux-sunxi.org/images/5/5e/Allwinner_F1C200s_Datasheet_V1.1.pdf), pin descriptions and operating supplies.
- **REF:** F1C200S and Lichee Pi Nano reference-circuit connections reviewed during design.
- **BUCK:** [TI TPS62160 datasheet](https://www.ti.com/lit/ds/symlink/tps62160.pdf), operating principle and application component selection.
- **IND:** [Coilcraft XFL4020-222 data](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xfl/xfl4020/xfl4020-222/).
- **LDO:** [TI TLV755P datasheet](https://www.ti.com/lit/ds/symlink/tlv755p.pdf), input and output capacitor requirements.
- **SUP:** [TI TPS386000 datasheet](https://www.ti.com/lit/ds/symlink/tps386000.pdf), sense dividers, reset outputs, manual reset, and supply bypass.
- **SWITCH:** [TI TPS2553 datasheet](https://www.ti.com/lit/ds/symlink/tps2553.pdf), current limit and application capacitors.
- **ESD:** [ST USBLC6-2 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf).
- **XTAL:** [Raltron H130A selected crystal](https://www.raltron.com/webproducts/specs/CRYSTAL/H130A-24.000-18-2030-EXT-TR.pdf), 24 MHz and 18 pF load specification.
- **USB / SD:** USB-C sink identification and microSD interface requirements applied in the final schematic.
- **LED:** [Kingbright APT1608LZGCK](https://www.kingbrightusa.com/images/catalog/spec/apt1608lzgck.pdf), low-current green 0603 LED.
- **USER:** Four corner screws, USB-C, and two indicators were requested in the design brief.
- **CAD:** Power flags are KiCad electrical-rule annotations, not physical circuit elements.
