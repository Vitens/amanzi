---
title: Streams
type: reference
audience: everyone
status: outline
---

# Streams

Connections between process units. Three types; each unit exposes anchors that must be wired if they are not optional.

## Content to write

- **Product** (blue): treated or forwarded water along the main train.
- **Waste** (red): concentrate, brine, or discarded flow to a waste sink.
- **Flush** (dotted blue): backwash / filter-wash water, often toward recycle or waste.
- Required vs optional anchors; the “not fully connected” message.
- Recycle loops: a recycle/splitter can send water back upstream; the quality solver iterates until mass balance converges (fact only; why is in [How Amanzi calculates](../explanation/how-amanzi-calculates.md)).
- A scenario without a source or without an output cannot be solved.

## Diagrams

- Mermaid: source → unit (product) → output, with waste and flush side edges.
