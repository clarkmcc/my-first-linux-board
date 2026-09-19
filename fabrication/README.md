# JLCPCB fabrication package

These files correspond to the final KiCad source in `hardware/`.

| Upload or use | File |
|---|---|
| Bare PCB | `clarks-board-JLCPCB-gerbers.zip` |
| Optional top stencil | `clarks-board-top-stencil.zip` |
| Optional bottom stencil | `clarks-board-bottom-stencil.zip` |
| JLCPCB assembly BOM | `assembly/clarks-board-JLCPCB-BOM.csv` |
| JLCPCB component placement | `assembly/clarks-board-JLCPCB-CPL.csv` |

Order the board as four-layer FR-4, 44 × 44 mm, 1.6 mm nominal thickness, 1 oz outer copper, black solder mask, white silkscreen, and ENIG finish. Use ordinary routed edges; the visible copper border is inset from the rounded outline. Vias are intended to be tented on both sides.

The ZIPs contain the exact exported Gerbers, plated/non-plated drill files, and paste layers from the built revision. Do not mirror them. All exports share the same origin.

USB impedance and the saved dielectric stackup are provisional. Select a JLCPCB controlled-impedance stackup and revalidate the USB pair before treating a changed layout as impedance-controlled.
