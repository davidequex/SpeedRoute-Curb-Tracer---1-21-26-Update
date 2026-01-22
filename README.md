[README.md](https://github.com/user-attachments/files/24785602/README.md)
# SpeedRoute  
### Deterministic Curb & Road Geometry Extraction for Traffic Control Plans

> **Status:** Early-stage prototype · Active development  
> **Focus:** Geometry-first inference · CAD-ready output  
> **Domain:** Traffic control plans / civil drafting acceleration

---

## Overview

**SpeedRoute** is an experimental system for converting satellite imagery into **clean, CAD-usable curb polylines**, designed specifically for **traffic control base plan workflows**.

Instead of relying on heavy machine learning or noisy edge detection, SpeedRoute explores a **deterministic, geometry-driven approach**:

- Infer curb geometry from road structure  
- Enforce global street alignment  
- Output simplified, human-editable DXF geometry  

This repository represents an **early but functional prototype**, focused on validating whether classical geometry + domain constraints can meaningfully reduce manual basing time.

---

## The Problem

Traffic control plans require base geometry that is:

- Straight, aligned, and readable  
- CAD-compatible (DXF)  
- Easy to adjust manually  
- Free from pixel noise and visual clutter  

However:

- Raw satellite imagery is too detailed  
- Edge detection produces unusable noise  
- ML segmentation is costly, opaque, and brittle for small firms  

**SpeedRoute reframes the problem**:  
> _Curbs don’t need to be detected perfectly — they need to be inferred plausibly._

---

## Visual Results (Current Prototype)

### Input: Satellite Imagery
<img width="1145" height="798" alt="Screenshot 2026-01-21 at 8 32 30 PM" src="https://github.com/user-attachments/assets/9110cf44-5503-4c6e-a212-1b83f60be2f4" />


---

### Intermediate: Road Mask Extraction
<img width="2867" height="2011" alt="road_mask" src="https://github.com/user-attachments/assets/8c65ade7-6357-47ae-ac63-6633c8f74686" />

---

### Output: Inferred Curb Polylines (DXF)
<img width="811" height="562" alt="Screenshot 2026-01-21 at 8 06 19 PM" src="https://github.com/user-attachments/assets/6b5fc9e3-b159-4fbe-9437-45c70130c207" />


---

## How It Works (High-Level)

```
Satellite Image
      ↓
Road Mask (CV)
      ↓
Global Orientation Lock
      ↓
Tile-Based Geometry Inference
      ↓
DXF Polyline Export
```

---

## Key Engineering Ideas

### Geometry Over Pixels
Rather than tracing edges, the system:
- Estimates dominant street orientation (PCA)
- Locks geometry to an orthogonal grid
- Infers curbs as parallel offsets from road bands

---

### Global Grid Locking
A single dominant orientation is estimated across the entire image, preventing angle drift between tiles and enforcing realistic street alignment.

---

### Tile-Based Processing
Large images are processed tile-by-tile, allowing scalability and local reasoning while inheriting global constraints.

---

### CAD-First Output
All results are exported as DXF polylines designed to be edited downstream.

---

## Code Structure (Current)

```
src/
├── build_road_mask.py
├── simplify.py
├── run_plan_d.py
├── export_dxf.py
├── load_dxf.py
├── metrics.py
```

---

## Known Limitations

- No curve handling  
- No intersection modeling  
- No topology merging  
- Road mask quality sensitive  

---

## Status Disclaimer

This repository represents **ongoing research**, not a finished product.

---

## Author

Built as part of the **SpeedRoute Traffic Control Design** tooling initiative.
