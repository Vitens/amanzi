---
lang: en
title: Splitter
type: reference
audience: everyone
status: draft
---

# Splitter

Library name: **Splitter**. Divides one product stream into two product streams.

## Streams

In: product. Out: product, on the right. Out: product, on the bottom.

## Inputs

| Field | Unit | Default | Range |
|---|---|---|---|
| `split` | fraction | 0.5 | 0.01–0.99 |
| `pressurized` | — | false | |

`split` is the fraction that leaves by one of the two outlets. 0.5 sends half each way. The label on the field says %. The stored value is the fraction.
