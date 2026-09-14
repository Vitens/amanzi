---
title: Backwash water reuse
type: reference
audience: everyone
status: outline
---

# Backwash water reuse

Library name: **Backwash water reuse**. Recycle / split that can close a loop upstream.

## Place it when

You return flush or a side stream to an earlier unit.

## Streams

- Splitter-style: incoming flow split toward product/recycle according to the block.
- Quality is passed through (no treatment).

## Inputs (UI groups)

- Split fractions / recycle design fields as in the form.

## Outputs / design tables

- Flows on each branch.
- Energy if pumping is included.
- Note: recycle mass helper returns empty to help the quantity solver converge (fact for key users filling this page).

## Science

[How Amanzi calculates](../../explanation/how-amanzi-calculates.md) (recycle iteration).
