# Purchasing files

The canonical purchasing BOM covers 89 fitted electronic components. The four mounting holes are fabricated features and are not purchase lines.

- `bom.csv` is the complete grouped purchasing BOM.
- `component-purpose.csv` explains why each group exists.
- `DigiKey-order.csv` and `LCSC-order.csv` are the final supplier split prepared from the available stock snapshots.

Availability and price evidence was checked on September 7, 2026 and is not a reservation. Confirm stock, packaging, quantities, and current pricing before ordering. Preserve the exact precision and temperature-coefficient grades for the regulator feedback and reset-supervisor resistor networks.

The F1C200S was allocated to LCSC. The TPS62160 buck regulators, TPS2553 input switch, Coilcraft inductors, and several passives were also allocated between LCSC and DigiKey according to the quoted in-stock exact manufacturer parts. The JLCPCB assembly upload files are under `fabrication/assembly/`; supplier inventory does not imply JLCPCB assembly inventory.
