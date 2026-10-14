# MSc Turtle Thesis

This repository contains the code and supporting information for an MSc thesis investigating the relationship between artificial night-time light and sea turtle hatchling emergence and orientation.

## Project overview

The analysis uses NASA Black Marble VIIRS nighttime-light data to examine artificial light conditions around sea turtle nest emergence locations.

VIIRS data were extracted for emergence observations from 2018 to 2026. For each emergence observation, a 3 × 3 grid of VIIRS pixels was examined, consisting of the pixel containing the nest location and the eight surrounding pixels.

The analysis calculates the distance and bearing from the actual nest location to the centre of each VIIRS pixel.

## VIIRS data

The analysis uses the NASA Black Marble VNP46A2 daily nighttime-light product.

- Product: VNP46A2
- Product type: Daily nighttime lights
- Spatial resolution: 15 arc-seconds
- Format: HDF5
- Data source: NASA LAADS DAAC
- Collection: 002
- DOI: https://doi.org/10.5067/VIIRS/VNP46A2.002

The original VIIRS HDF5 raster files are not stored in this repository because of their size. A data manifest is provided in `data/VIIRS_data_manifest.csv` to document the VIIRS acquisitions used in the analysis.

## 3 × 3 pixel extraction

For each sea turtle emergence observation:

1. The emergence date is matched to the corresponding daily VNP46A2 VIIRS raster.
2. The VIIRS pixel containing the nest location is identified.
3. The centre coordinates of that pixel are determined.
4. The eight surrounding pixels are identified.
5. VIIRS values are extracted for all nine pixels.
6. Distance from the actual nest location to each pixel centre is calculated.
7. Bearing from the actual nest location to each pixel centre is calculated clockwise from north.
8. The brightest surrounding pixel is identified.

The nest-containing pixel is retained in the detailed 3 × 3 dataset but is excluded when identifying the brightest surrounding pixel.

## NoData handling

VIIRS NoData values are retained as missing values rather than being treated as zero.

If individual pixels within a 3 × 3 grid contain NoData, those pixels remain in the detailed dataset with missing VIIRS values.

If all nine pixels are NoData, the emergence observation remains in the detailed 3 × 3 dataset but is excluded from the brightest-pixel analysis because a brightest surrounding pixel cannot be identified.

SUNSHINE COAST LOGGERHEAD HATCHLING: 250 m SPATIAL SCENARIO ANALYSIS
===================================================================
Reconstructed, annotated PyQGIS workflow for a thesis methods repository.

IMPORTANT PROVENANCE
--------------------
This script consolidates the documented workflow and final manual QC decisions.
It is a RECONSTRUCTION, not a verbatim archive of every interactive QGIS script
used during the original analysis. Run only on a COPY of the project and inspect
outputs before replacing any archived thesis results.

Research units:
  * 22 named beaches, 24 physical coastal sections (Noosa and Bribie split).
  * Dune edge and shoreline proxy digitised manually for each section.
  * CRS EPSG:7856 (GDA2020 / MGA zone 56), distances in metres.
  * 250 m refers to along-dune systematic sampling spacing.
  * 500 m refers separately to the maximum direct-route search distance.
  * 5 m is a provisional habitat-boundary digitising tolerance, NOT a
    biological threshold or a measured mapping-error estimate.

Original run, AFTER documented manual QC:
  281 starting points x 15 orientations = 4,215 modelled trajectories.
  3,197 valid direct routes; 160 habitat crossing / reorientation required;
  858 without shoreline intersection within 500 m.
  330 beach x orientation summary rows (22 x 15).

Manual interpretation remains necessary. In particular, a line being within a
buffered sandy-beach polygon does not prove it is traversable by a hatchling.
This is a geometric scenario model, not observed hatchling movement.

REQUIREMENTS
------------
Run in QGIS Python Editor (not standalone Python). QGIS 3.x, PyQGIS available.
The open project must contain all 24 pairs of layers named:
    <Section>_Dune_Edge
    <Section>_Shoreline
Each layer must have one polyline feature. Polygons may instead be supplied
using the existing All_Beach_Polygons_REVIEW layer, but by default this script
rebuilds them from the line layers as documented.


## Repository structure

```text
Msc_Turtle_Thesis/
│
├── README.md
│
├── Power Analysis
│
├── data/
│   └── VIIRS_data_manifest.csv
│
└── scripts/
    ├── 2018/
    ├── 2019/
    ├── 2020/
    ├── 2021/
    ├── 2022/
    ├── 2023/
    ├── 2024/
    ├── 2025/
    └── 2026/
