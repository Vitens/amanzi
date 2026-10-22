---
lang: en
title: Backwash water reuse
type: reference
audience: everyone
status: draft
---

# Backwash water reuse

Library name: **Backwash water reuse**. Returns part of a waste or flush stream to the product train.

## Streams

In: waste. Out: product. Out: waste.

The product outlet is the recovered water. The waste outlet is what is not recovered.

## Inputs

| Field | Unit | Default | Range |
|---|---|---|---|
| `recycle_efficiency` | fraction | 0.8 | 0.5–0.95 |

The label says %. The stored value is the fraction. 0.8 recovers 80% of the incoming waste flow to the product outlet.

## Energy

The parametric energy total for this block is the constant 0.5 kWh/m³. It is not a pump curve.
