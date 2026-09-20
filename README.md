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

## Repository structure

```text
Msc_Turtle_Thesis/
│
├── README.md
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
