---
lang: en
title: Limitations
type: reference
audience: everyone
status: draft
---

# Limitations

**Ion exchange** is not in the library. Its block is hidden, and the calculation package does not export the model.

**Activated carbon** and **micropollutant** entry are not part of the public app. The source tree contains both. This reference does not list them as blocks you can place on the hosted demo.

**Spray aeration** is not implemented as a seperate block, but as a switch on sand filtration and marble filtration.

The running spray calculation uses a polynomial in fall height. It does not read a Sauter diameter.

There is no account. **Save** keeps the project in this browser. **Download** writes a JSON file. **Open** replaces what is on screen. There is no Excel, CSV, or map import of a water analysis. Composition is typed on **Abstraction**.

The models are steady. One scenario is one operating point. The canvas is not a map, and the tool does not operate a plant.

A unit with a required anchor left open is reported as not fully connected. A quality loop that does not settle stops after 100 passes.

This documentation is English, Dutch, and German. The architecture documentation stays English.
