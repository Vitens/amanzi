---
lang: en
title: Process units
type: reference
audience: everyone
status: draft
---

# Process units

One page per block in the public library. Science is in [Explanation](../../explanation/index.md). Stream colours are in [Streams](../streams.md).

Most blocks also accept the shared design fields from `model.yml`:

| Field | Unit | Default | Range |
|---|---|---|---|
| `units` | — | 1 | 1–40 |
| `minimal_capacity` | m³/h | 50 | 1–10000 |
| `nominal_capacity` | m³/h | 100 | from the minimum upward |
| `maximal_capacity` | m³/h | 150 | from the nominal upward |
| `inlet_elevation` | m | 5 | 0–25 |
| `influent_pressure_loss` | mH₂O | 0 | 0–10 |
| `pressurized` | — | false | |

A page below names a field only when that block replaces the shared default or adds its own. Electricity and chemical CO₂ rows are added for every block that reports a consumption. See [Key figures](../key-figures.md).

Where a unit label says `%` and the range is between 0 and 1, the value is a fraction. See [Units of measure](../units.md).

## Sources and storage

- [Abstraction](groundwater.md)
- [Reservoir](reservoir.md)

## Aeration and gas

- [Tower aeration](toweraeration.md)
- [Spray aeration](sprayaerator.md) — hidden as its own block; the fields are on the filters
- [Plate aeration](plate.md)
- [Cascade](cascade.md)
- [Membrane degassing](membranedegassing.md)
- [Vacuum degassing](vacuum.md)

## Filtration

- [Sand filtration](sandfiltration.md)
- [Marble filtration](marblefiltration.md)

## Chemicals and membranes

- [Pellet softening](softening.md)
- [Chemical dosage](dosing.md)
- [Membrane filtration](membrane.md)

## Transport and sinks

- [Sand trap](sandtrap.md)
- [Transport pipeline](pipeline.md)
- [Splitter](splitter.md)
- [Backwash water reuse](recycle.md)
- [Output](output.md)
- [Waste stream](waste.md)

Ion exchange is omitted. Activated carbon is not in the public app. Both are in [Limitations](../limitations.md).
