# MSc Turtle Thesis

## 1. Repository Overview

This GitHub repository contains the analytical scripts, supporting data documentation, methodological details and reproducibility resources associated with an MSc Marine Biology thesis investigating sea turtle hatchling and adult orientation along the Sunshine Coast, Queensland, Australia, with particular emphasis on the potential influence of artificial light at night (ALAN).

The research examines spatial and temporal variation in hatchling orientation, relationships between satellite-derived nighttime-light radiance and orientation behaviour, the potential consequences of orientation deviation for hatchling crawling distances and shoreline access, and the association between temporary light barriers and hatchling orientation. The study also investigates adult nesting-track orientation and uses simulation-based power analyses to evaluate sampling requirements for future monitoring.

The repository is intended to complement the thesis Methods chapter by providing more detailed documentation of the analytical workflows, calculations, assumptions and methodological decisions underlying the research. Where available, the original R and Python scripts are provided to support transparency, reproducibility and potential adaptation of the methods for future studies.

The repository is organised around the main analytical components of the thesis, including:

1. **Orientation measurements and circular statistics:** Calculation and interpretation of ocean-relative orientation offset, directional spread and other derived orientation measurements.
2. **VIIRS nighttime-light extraction:** Processing of NASA Black Marble satellite data, extraction of radiance values surrounding emergence locations, and calculation of distances and bearings to neighbouring VIIRS pixels.
3. **Spatial modelling:** Generation and assessment of hypothetical hatchling crawling trajectories to investigate how orientation deviation may influence crawling distances and direct shoreline access.
4. **Simulation-based power analyses:** Evaluation of the sampling effort required to detect hypothetical artificial-light relationships and light-barrier-associated differences in hatchling orientation.

Not all analytical components are currently represented by complete archived scripts. Additional scripts and documentation may be incorporated as the repository is developed.

### Reproducibility and methodological limitations

The repository distinguishes between original analytical scripts and reconstructed workflows. Some analyses, particularly the QGIS spatial modelling, involved interactive processing, manual digitisation and quality-control decisions that cannot be reproduced solely by executing a script. Where applicable, these steps and their associated assumptions are documented to clarify how the final analytical datasets were produced.

The repository also distinguishes between observed biological measurements, satellite-derived environmental variables and hypothetical modelling outputs. Simulated hatchling trajectories represent geometric scenarios rather than observed crawling behaviour, and satellite-derived nighttime-light radiance should not be interpreted as a direct measurement of light exposure experienced by individual hatchlings.

Together, the archived materials are intended to provide a transparent record of the research methods and support the interpretation, evaluation and future replication of the analyses presented in the thesis.
### 2. Repository Structure and File Guide

The repository is organised by research component, with separate directories for orientation calculations, VIIRS nighttime-light extraction, spatial modelling and simulation-based power analyses.

The directory structure is outlined below.

```text
Msc_Turtle_Thesis/
│
├── README.md
│
├── Circular Statistics/
│   └── Orientation_Calculations.md
│
├── VIIRS Extraction/
│   ├── Extraction Scripts/
│   │   ├── 2018/
│   │   ├── 2019/
│   │   ├── 2020/
│   │   ├── 2021/
│   │   ├── 2022/
│   │   ├── 2023/
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   │
│   └── Raw Data Files/
│
├── Spatial Analysis/
│   └── 250m Spatial Scenario
│
└── Power Analysis/
    ├── Between_Beaches
    ├── Within_Beach
    └── Light Barrier
```

### Directory Descriptions

| Directory | Contents |
|---|---|
| Circular Statistics | Mathematical formulas, variable definitions and worked examples for calculating hatchling and adult orientation measurements. |
| VIIRS Extraction | Scripts and supporting data for extracting daily VIIRS nighttime-light radiance surrounding hatchling emergence locations. |
| VIIRS Extraction/Extraction Scripts | Year-specific extraction workflows covering emergence observations from 2018 to 2026. |
| VIIRS Extraction/Raw Data Files | Supporting data files associated with the nighttime-light extraction workflow. |
| Spatial Analysis | Reconstructed PyQGIS workflow for generating hypothetical hatchling crawling trajectories and evaluating shoreline intersections. |
| Power Analysis | Simulation-based analyses evaluating sampling requirements for between-beach ALAN relationships, within-beach ALAN relationships and temporary light-barrier effects. |

### File Guide

**Orientation_Calculations.md**

Documents the mathematical calculations used to derive circular orientation measurements, including orientation-fan spread, circular midpoint, direct ocean bearing, corrected orientation offset, sea-finding classification and adult nesting-track angular differences.

**Between_Beaches**

Contains the simulation analysis examining statistical power to detect hypothetical associations between beach-level mean artificial nighttime radiance and hatchling orientation offset.

**Within_Beach**

Contains the simulation analysis examining statistical power to detect hypothetical associations between within-beach variation in artificial nighttime radiance and hatchling orientation offset.

**Light Barrier**

Contains the simulation-based sample-size analysis for detecting hypothetical reductions in corrected hatchling orientation offset associated with temporary light-barrier deployment.

**250m Spatial Scenario**

Contains the reconstructed and annotated PyQGIS workflow used to model systematic starting locations, hypothetical orientation deviations, shoreline intersections and geometric route classifications.

**VIIRS Yearly Extraction Scripts (2018–2026)**

Contain the year-specific workflows used to extract VIIRS nighttime-light radiance from the nest-containing pixel and its eight surrounding pixels, together with associated distance and bearing calculations.

### Data Availability and Reproducibility

The repository provides supporting methodological documentation and computational workflows for the analyses described in the MSc thesis.

Some original source materials, including NASA VIIRS HDF5 raster files and QGIS project inputs, are not included because of file size, data availability or project-specific dependencies.

The `Circular Statistics` documentation provides mathematical reconstructions of the orientation calculations rather than the original R implementation.

The `Spatial Analysis` workflow is a reconstructed PyQGIS script and does not reproduce every original manual digitisation or quality-control decision.

The power-analysis scripts document simulation procedures, but reproducing the numerical results may require the original prepared input datasets.

The repository should therefore be used alongside the thesis Methods section, which provides the scientific context, sampling design, statistical analyses and interpretation of results.

### Repository Citation

The repository is available at:

https://github.com/Lauren-Millie/Msc_Turtle_Thesis

The repository should be cited alongside the MSc thesis when referring to its supplementary methodological documentation, computational workflows or archived analysis scripts.

### 3. Orientation Measurements and Circular Statistics

**Corresponding thesis section:** 2.2 Data preparation and derived orientation metrics

Hatchling and adult orientation variables were derived from recorded compass bearings using circular angular calculations. These included the corrected orientation-fan spread, circular fan midpoint, direct ocean bearing, corrected orientation offset, geometric sea-finding classification and adult nesting-track angular differences.

The mathematical equations, variable definitions and worked examples are provided in the Circular Statistics folder. These calculations document the methods used to derive the orientation measurements and provide a reference for independent verification. The original R implementation is not currently archived in the repository.

## 4. VIIRS Nighttime-Light Data and Extraction

**Corresponding thesis section:** 2.3 Artificial-Light and Environmental Data

### 4.1 Project Overview

Artificial light at night (ALAN) was investigated using NASA Black Marble nighttime-light data derived from the Visible Infrared Imaging Radiometer Suite (VIIRS).

The analysis used satellite-derived nighttime radiance to characterise artificial-light conditions surrounding sea turtle hatchling emergence locations along the Sunshine Coast, Queensland, Australia.

Daily VIIRS data were extracted for emergence observations from 2018 to 2026. For each emergence observation, a 3 × 3 grid of VIIRS pixels was examined, consisting of the pixel containing the recorded nest location and its eight immediately surrounding pixels.

The extraction workflow calculated the radiance, geographic coordinates, distance and compass bearing associated with each pixel. These measurements were used to investigate the spatial distribution of satellite-detected nighttime radiance relative to hatchling emergence locations and orientation directions.

### 4.2 VIIRS Data Source

The daily nighttime-light data were obtained from NASA's Black Marble VNP46A2 product.

**Dataset information:**

- **Product:** VNP46A2
- **Product name:** VIIRS/NPP Daily Gridded Day Night Band 500 m Linear Lat Lon Grid
- **Collection:** 002
- **Data source:** NASA Level-1 and Atmosphere Archive and Distribution System Distributed Active Archive Center (LAADS DAAC)
- **Satellite:** Suomi National Polar-orbiting Partnership (Suomi-NPP)
- **Sensor:** Visible Infrared Imaging Radiometer Suite (VIIRS)
- **Spatial resolution:** 15 arc-seconds (approximately 500 m nominal resolution)
- **Temporal resolution:** Daily
- **Original file format:** HDF5 (HDF-EOS5)
- **Data layer:** DNB BRDF-Corrected Nighttime Lights
- **DOI:** https://doi.org/10.5067/VIIRS/VNP46A2.002

The VNP46A2 product provides atmospherically and moonlight-corrected nighttime radiance estimates, allowing artificial-light conditions to be investigated using satellite-derived measurements.

The original HDF5 raster files are not included in this repository because of their size. The extraction scripts and supporting data files are organised within the `VIIRS Extraction` directory.

### 4.3 Repository Organisation

The VIIRS materials are organised into two main components: the extraction scripts and the associated data files.

```text
VIIRS Extraction/
├── Extraction Scripts/
│   ├── 2018/
│   ├── 2019/
│   ├── 2020/
│   ├── 2021/
│   ├── 2022/
│   ├── 2023/
│   ├── 2024/
│   ├── 2025/
│   └── 2026/
└── Raw Data Files/
```

**Extraction Scripts**

The 'Extraction Scripts' directory contains the year-specific Python extraction workflows used to process daily VIIRS nighttime-light data for the corresponding hatchling emergence observations.

Scripts are separated by year to reflect the organisation of the source emergence records and daily satellite rasters.

**Raw Data Files**

The 'Raw Data Files directory contains supporting data files associated with the VIIRS extraction workflow.

The original NASA HDF5 raster files are not archived in the repository and must be obtained separately from NASA LAADS DAAC if the extraction is to be reproduced.

### 4.4 Three-by-Three Pixel Extraction

For each hatchling emergence observation, the extraction workflow examined a 3 × 3 neighbourhood of VIIRS pixels centred on the pixel containing the recorded nest location.

This neighbourhood consisted of nine pixels:

- One central pixel containing the recorded emergence location.
- Eight immediately adjacent surrounding pixels.

The extraction was conducted using the following procedure:

1. **Match the emergence date to the daily VIIRS raster.** The recorded emergence date was used to identify the corresponding VNP46A2 nighttime-light raster.

2. **Identify the nest-containing pixel.** The geographic coordinates of the emergence location were used to identify the raster pixel containing the nest.

3. **Calculate the central pixel coordinates.** The geographic coordinates of the centre of the nest-containing pixel were determined.

4. **Identify the eight surrounding pixels.** The immediately adjacent pixels were extracted to produce the complete 3 × 3 neighbourhood.

5. **Extract nighttime radiance.** The VIIRS radiance value associated with each of the nine pixels was extracted.

6. **Calculate distance to each pixel centre.** The distance between the recorded nest coordinates and the geographic centre of each pixel was calculated.

7. **Calculate bearing to each pixel centre.** The compass bearing from the nest location to the centre of each pixel was calculated in degrees clockwise from north.

8. **Identify the brightest surrounding pixel.** The pixel with the highest valid radiance value among the eight surrounding pixels was identified.

The central nest-containing pixel was retained in the detailed extraction dataset but excluded from the selection of the brightest surrounding pixel.

This distinction allowed the analysis to identify the direction of the brightest satellite-detected radiance in the surrounding neighbourhood rather than selecting the pixel containing the nest itself.

### 4.5 Distance and Bearing Calculations

For each of the nine pixels, the extraction workflow calculated the distance and bearing from the actual emergence location to the centre of the VIIRS pixel.

Distances were calculated using the geographic coordinates of the nest and pixel centre.

Bearings were expressed as compass directions measured clockwise from north:

- 0° = North
- 90° = East
- 180° = South
- 270° = West

These calculations provided a geographic representation of the position of each VIIRS pixel relative to the nest.

The resulting bearings could subsequently be compared with hatchling orientation bearings and the direct ocean bearing to examine whether hatchling orientation was more closely aligned with the ocean or with the direction of the brightest surrounding VIIRS pixel.

The pixel-centre bearing represents the direction towards the centre of a satellite raster cell. It does not necessarily identify the precise location or direction of an individual artificial-light source.

### 4.6 Identifying the Brightest Surrounding Pixel

The brightest surrounding VIIRS pixel was defined as the pixel with the highest valid nighttime radiance value among the eight pixels immediately adjacent to the nest-containing pixel.

The nest-containing pixel was excluded from this selection.

For each emergence observation, the extraction therefore retained the relevant information needed to identify:

- The location of the brightest surrounding pixel.
- Its nighttime radiance value.
- The distance between the nest and the pixel centre.
- The compass bearing from the nest to the pixel centre.

These measurements provided the basis for subsequent directional comparisons between hatchling orientation, the direct ocean bearing and the brightest surrounding satellite-detected radiance.

The brightest surrounding pixel was treated as an indicator of the spatial distribution of nighttime radiance, rather than as a direct measurement of the artificial-light exposure experienced by individual hatchlings.

### 4.7 NoData Handling

Missing VIIRS radiance measurements were handled separately from valid zero-radiance observations.

Pixels containing NoData values were retained as missing values rather than being assigned a radiance of zero.

The following rules were applied:

1. Pixels with valid radiance values were retained for extraction and comparison.
2. Pixels containing NoData values were recorded as missing.
3. Missing pixel values did not prevent other valid pixels within the same 3 × 3 neighbourhood from being retained.
4. Emergence observations for which all nine pixels contained NoData were retained in the detailed extraction dataset but excluded from analyses requiring identification of the brightest surrounding pixel.

This approach prevented missing satellite observations from being incorrectly interpreted as locations with no artificial nighttime radiance.

### 4.8 Extraction Coverage and Missing Rasters

The VIIRS extraction workflows were organised by emergence year, covering observations from 2018 through 2026.

Not all emergence dates necessarily had an available or usable daily raster. Where the corresponding satellite data were unavailable, the missing extraction could not be treated as a valid zero-radiance observation.

The annual folders document the extraction workflows associated with each year, including the processing of emergence locations and their corresponding daily nighttime-light rasters.

The years represented in the extraction directory describe the scope of the data-processing workflow and do not imply that every emergence observation from those years was included in every subsequent statistical analysis.

### 4.9 Reproducibility and Data Availability

The year-specific extraction scripts are provided in the VIIRS Extraction/Extraction Scripts directory.

The supporting data files are organised under VIIRS Extraction/Raw Data Files.

To reproduce the extraction, the corresponding daily NASA Black Marble VNP46A2 Collection 002 raster files must be obtained from NASA LAADS DAAC and matched to the emergence dates and geographic coordinates used in the analysis.

The original HDF5 raster files are excluded from the repository because of their storage requirements.

Reproduction also requires access to the appropriate input emergence records, including their dates and geographic coordinates, and the software environment required to execute the year-specific extraction scripts.

### 4.10 Interpretation of Satellite-Derived Radiance

VIIRS nighttime-light radiance was used as a spatial indicator of artificial-light conditions surrounding hatchling emergence locations.

However, satellite-derived radiance should not be interpreted as a direct measurement of light visible to hatchlings at beach level.

Local environmental conditions, including coastal vegetation, dune morphology, artificial structures and the position of individual light sources, can influence the visibility of artificial light from the nest location.

Additionally, the brightest surrounding pixel represents the highest measured radiance among neighbouring satellite cells, not necessarily the brightest individual light source or the direction of greatest perceived illumination.

These limitations were considered when interpreting relationships between VIIRS nighttime radiance and hatchling orientation.

### 4.11 Data Citation

NASA Black Marble VNP46A2, Collection 002.

NASA Level-1 and Atmosphere Archive and Distribution System Distributed Active Archive Center (LAADS DAAC).

https://doi.org/10.5067/VIIRS/VNP46A2.002

## 5. Spatial Modelling of Hypothetical Hatchling Crawling Trajectories

**Corresponding thesis section:** 2.5 Spatial Modelling of Hypothetical Crawling Distance

### 5.1 Project Overview

Spatial modelling was conducted to investigate how deviations from the direct oceanward direction could influence hypothetical sea turtle hatchling crawling distances and the likelihood of a straight-line route intersecting the shoreline.

The analysis used Geographic Information Systems (GIS) to generate hypothetical hatchling crawling trajectories across Sunshine Coast beaches in Queensland, Australia.

Rather than reproducing observed hatchling crawling paths, the model evaluated a standardised set of orientation scenarios from systematically distributed starting locations. This allowed the influence of angular deviation and local beach geometry to be examined independently of the spatial distribution of observed nests.

The spatial modelling workflow consisted of:

1. Digitising coastal reference boundaries and sandy-beach habitat.
2. Generating systematic starting locations along the dune edge.
3. Establishing a direct oceanward reference bearing for each location.
4. Generating alternative hypothetical trajectories at predetermined angular deviations.
5. Calculating shoreline intersection distances.
6. Classifying trajectories according to shoreline access and habitat constraints.
7. Calculating additional hypothetical crawling distances.
8. Statistically evaluating changes in crawling distance and accepted-route probability.

### 5.2 Spatial Data Sources and Software

The spatial analysis was conducted using QGIS and Python scripts executed within the QGIS Python environment (PyQGIS).

**Software and spatial reference information:**

- **GIS software:** QGIS
- **Version:** 3.44.14-Solothurn
- **Scripting environment:** Python within QGIS (PyQGIS)
- **Coordinate reference system:** GDA2020 / MGA zone 56
- **EPSG code:** EPSG:7856
- **Distance units:** Metres

Two principal geographic reference sources were used.

**Queensland Government coastline data**

The Queensland Government's *Coastline - Queensland* dataset, available through the Queensland Spatial Catalogue (QSpatial), provided a common spatial reference for the Sunshine Coast shoreline.

This dataset was used as a geographic reference rather than as a reconstruction of historical shoreline positions corresponding to individual nesting seasons.

**Esri World Imagery**

Esri World Imagery provided the satellite and aerial imagery basemap used for manually identifying and digitising coastal boundaries.

The imagery was used to identify the seaward dune or vegetation edge and the approximate wet–dry sand boundary representing the shoreline.

These manually digitised features were subsequently used to construct the geometric modelling environment.

### 5.3 Study Beaches and Coastal Sections

The analysis included 22 named nesting beaches along the Sunshine Coast.

For spatial processing, these beaches were represented by 24 physically continuous coastal sections.

Noosa and North Bribie were each divided into two sections because waterways interrupted the continuity of the beach environment.

The sections were processed separately when generating spatial features and hypothetical trajectories.

However, their original beach identities were retained for subsequent statistical analyses, resulting in 22 beaches for beach-level comparisons.

### 5.4 Coastal Boundary Digitisation

Two principal coastal boundaries were manually digitised for each continuous beach section.

**Dune-edge boundary**

The seaward dune or vegetation edge was used to define the landward boundary of the sandy-beach environment.

This boundary also provided the reference line for systematically distributing hypothetical hatchling starting locations.

**Shoreline boundary**

The approximate wet–dry sand boundary was digitised as a shoreline or high-tide proxy.

This boundary represented the target line for evaluating whether hypothetical straight-line trajectories intersected the shoreline.

The digitised boundaries were used to construct sandy-beach habitat polygons representing the modelled coastal environment.

Because the boundaries were derived from imagery rather than direct field surveys, they represent approximations of coastal geometry. The shoreline proxy does not represent the exact tidal position during individual hatchling emergence events.

### 5.5 Systematic Starting-Point Generation

Hypothetical starting locations were generated systematically along the digitised dune-edge boundaries.

Each continuous coastal section was divided into approximately equal intervals, with the interval length not exceeding 250 m.

A starting location was placed at the midpoint of each interval.

This approach produced a standardised distribution of starting locations along the study beaches rather than relying on the observed locations of individual hatchling emergence events.

A total of **281 hypothetical starting locations** were generated.

Each starting location was assigned a unique identifier and associated beach identity.

The 250 m distance refers specifically to the spacing used for generating starting locations. It does not represent the maximum permitted crawling distance.

### 5.6 Direct Oceanward Reference Route

For each starting location, a direct route towards the digitised shoreline was established as the 0° reference orientation.

The direct shoreline bearing and corresponding distance provided the baseline against which alternative hypothetical trajectories were evaluated.

This reference route represented the geometrically direct route from the starting location to the shoreline under the modelled beach configuration.

The 0° route was retained as the reference scenario for calculating additional crawling distance associated with angular deviation.

### 5.7 Hypothetical Orientation Scenarios

Alternative trajectories were generated by applying predetermined clockwise and anticlockwise angular deviations to the direct shoreline bearing.

The selected angular deviations were informed by the observed hatchling orientation distribution and were used to represent progressively greater departures from the direct oceanward direction.

Fifteen orientation scenarios were evaluated at each starting location:

| Orientation scenario | Angular deviation |
|---|---|
| Direct reference | 0° |
| Clockwise and anticlockwise | ±15° |
| Clockwise and anticlockwise | ±45° |
| Clockwise and anticlockwise | ±55° |
| Clockwise and anticlockwise | ±65° |
| Clockwise and anticlockwise | ±75° |
| Clockwise and anticlockwise | ±85° |
| Clockwise and anticlockwise | ±105° |

Each of the 281 starting locations was assigned the same 15 scenarios.

This generated:

**281 starting locations × 15 orientation scenarios = 4,215 hypothetical trajectories.**

The resulting trajectories represented straight-line geometric scenarios rather than observed hatchling crawling behaviour.

### 5.8 Trajectory Generation and Shoreline Intersection

Straight-line trajectories were generated from each starting location along the specified orientation bearings.

Each trajectory was assessed to determine whether it intersected the digitised shoreline.

Where an eligible intersection was identified, the distance between the starting location and the shoreline intersection was calculated in metres.

A maximum shoreline-intersection distance of **500 m** was imposed.

Trajectories that did not intersect an eligible shoreline within this distance were classified as having no shoreline intersection.

The 500 m threshold was used to restrict the model to the local beach environment. It was a methodological search limit rather than a biologically established maximum hatchling crawling distance.

### 5.9 Sandy-Beach Habitat Assessment

Hypothetical trajectories were also evaluated against the digitised sandy-beach habitat polygons.

This assessment determined whether a trajectory remained within the modelled beach environment or crossed an area interpreted as unsuitable habitat.

A spatial tolerance of **5 m** was applied to accommodate minor discrepancies associated with imagery alignment and manual digitisation.

This tolerance permitted small boundary deviations where they were attributable to mapping uncertainty and did not represent an identifiable crossing of unsuitable habitat.

The tolerance was not intended to represent a biological movement threshold or a measured estimate of spatial error.

Manual inspection remained necessary because a trajectory falling within a buffered polygon did not automatically demonstrate that the route was physically traversable by hatchlings.

### 5.10 Trajectory Classification

Each hypothetical trajectory was assigned to one of three mutually exclusive categories.

**Accepted direct route**

A trajectory was classified as accepted when it intersected an eligible shoreline within 500 m and satisfied the sandy-beach habitat criteria.

**Habitat crossing**

A trajectory was classified as a habitat crossing when it extended beyond the permitted sandy-beach corridor or intersected identifiable unsuitable habitat.

These trajectories represented scenarios in which continued movement along the modelled straight-line bearing would require crossing unsuitable habitat or changing direction.

**No shoreline intersection**

A trajectory was classified as having no shoreline intersection when it did not intersect an eligible shoreline within the maximum 500 m search distance.

These classifications describe geometric route outcomes rather than observed hatchling survival, successful sea entry or actual behavioural reorientation.

### 5.11 Final Spatial Modelling Results

Following manual quality control, the final spatial modelling dataset contained 4,215 hypothetical trajectories.

| Trajectory classification | Number of trajectories |
|---|---:|
| Accepted direct route | 3,197 |
| Habitat crossing | 160 |
| No shoreline intersection within 500 m | 858 |
| **Total** | **4,215** |

The final dataset represented 281 starting locations, 15 orientation scenarios and 22 named beaches.

The corresponding beach-by-orientation summary contained 330 combinations (22 beaches × 15 orientations).

These counts represent the final quality-controlled thesis dataset and provide reference values against which regenerated spatial outputs can be checked.

### 5.12 Additional Hypothetical Crawling Distance

For accepted trajectories, additional hypothetical crawling distance was calculated by comparing the distance travelled along an offset trajectory with the corresponding direct 0° reference route from the same starting location.

Additional distance was calculated as:

**Additional crawling distance = Offset-route distance − Direct-route distance**

Positive values indicate that the offset trajectory required a longer straight-line distance to reach the shoreline than the direct reference route.

Only accepted trajectories were included in the continuous distance analysis.

Non-accepted trajectories were excluded from the distance calculations rather than being assigned zero or an assumed crawling distance.

The distance dataset included:

- **2,919 accepted nonzero-offset trajectories**, used to evaluate additional crawling distance.
- **278 accepted 0° reference routes**, retained for descriptive comparison.

These values together account for the 3,197 accepted trajectories.

### 5.13 Statistical Analysis of Crawling Distance

Statistical analyses of the modelled crawling-distance outputs were conducted separately in R.

The analysis examined whether additional hypothetical crawling distance increased with progressively greater angular deviation.

Comparisons were conducted between successive absolute orientation offsets:

- 15° to 45°
- 45° to 55°
- 55° to 65°
- 65° to 75°
- 75° to 85°
- 85° to 105°

Trajectories were matched according to their starting location and clockwise or anticlockwise direction.

Only pairs in which both trajectories were classified as accepted were retained for the corresponding distance comparison.

Median paired distance changes were calculated at the beach level and tested against zero using one-sided Wilcoxon signed-rank tests.

P-values were adjusted using the Holm method to account for multiple comparisons.

The final paired comparison included five beaches and was interpreted cautiously because of the limited number of eligible beach-level observations.

This approach was adopted after alternative mixed-effects distance models showed inadequate residual diagnostics.

### 5.14 Statistical Analysis of Accepted-Route Probability

The probability of a hypothetical trajectory being classified as an accepted direct route was analysed separately from crawling distance.

This analysis included all **3,934 nonzero-offset trajectories**, including accepted and non-accepted routes.

A binomial generalised linear mixed-effects model (GLMM) with a logit link was used.

The response variable was binary:

- **1:** Accepted direct route.
- **0:** Non-accepted trajectory.

The model included:

- Absolute orientation offset as a fixed effect.
- Clockwise or anticlockwise deviation direction as a fixed effect.
- Beach as a random intercept.
- Starting location as a random intercept.

An interaction between angular offset and deviation direction was evaluated before retaining the additive model based on model comparison.

Model adequacy was assessed using simulated residual diagnostics implemented through the DHARMa package in R.

This analysis investigated how angular deviation and direction were associated with the probability of a straight-line trajectory reaching an eligible shoreline within the modelled beach environment.

### 5.15 Repository Organisation

The spatial modelling materials are stored in the [`Spatial Analysis`](./Spatial%20Analysis/) directory.

The existing repository includes the reconstructed PyQGIS workflow labelled `250m Spatial Scenario`.

```text
Spatial Analysis/
└── 250m Spatial Scenario
```

**250m Spatial Scenario**

This file contains an annotated PyQGIS reconstruction of the spatial modelling workflow used to generate systematic starting locations, hypothetical orientation scenarios, shoreline intersections and route classifications.

The script consolidates the documented modelling procedures and final manual quality-control decisions.

It is not a verbatim archive of every interactive QGIS command used during the original analysis.

The downstream statistical analyses of additional crawling distance and accepted-route probability were conducted in R and are separate from the PyQGIS workflow.

### 5.16 Reproducing the Spatial Analysis

The reconstructed spatial workflow is intended to be executed within the QGIS Python Editor, rather than as a standalone Python script.

The workflow requires an appropriately configured QGIS project containing the digitised coastal boundaries.

The script expects matching dune-edge and shoreline line layers for the 24 continuous coastal sections, using the naming conventions:

```text
<Section>_Dune_Edge
<Section>_Shoreline
```

Each corresponding line layer must contain the required coastal boundary geometry.

The script can also use an existing `All_Beach_Polygons_REVIEW` layer, depending on its configuration.

The reconstructed workflow does not automatically reproduce the original manual digitisation, imagery interpretation or every subsequent quality-control decision.

For this reason, the script should be run on a copy of the original QGIS project, and regenerated layers should be inspected before being treated as equivalent to the final thesis outputs.

The script is designed to avoid overwriting existing thesis GeoPackages and can generate separate review layers for inspection.

A new output file path should be specified when exporting regenerated results.

The final quality-controlled counts of 281 starting locations, 4,215 trajectories, 3,197 accepted routes, 160 habitat crossings and 858 routes without an eligible shoreline intersection provide reference values for checking the regenerated outputs.

### 5.17 Methodological Limitations

The spatial analysis was designed to evaluate hypothetical geometric consequences of hatchling orientation deviation, rather than to reconstruct actual hatchling movement.

Several limitations should be considered when interpreting the results.

**Straight-line movement assumption**

Each trajectory represented a fixed straight-line heading. Actual hatchlings may change direction, respond to environmental cues or encounter obstacles not represented in the model.

**Digitised coastal boundaries**

The dune and shoreline boundaries were interpreted from imagery and were not direct measurements of shoreline conditions during individual emergence events.

**Habitat classification**

The sandy-beach polygons provided a simplified representation of potentially traversable habitat. A route satisfying the polygon criteria was not necessarily free from obstacles or physically traversable in the field.

**Maximum intersection distance**

The 500 m limit was a methodological constraint and did not represent a biological limit on hatchling movement.

**Manual quality control**

Some spatial classifications required visual interpretation and manual correction. Consequently, the complete original analysis cannot be reproduced solely by executing the reconstructed script.

**Interpretation of route outcomes**

Accepted routes represent hypothetical shoreline intersections, not confirmed successful sea entry. Habitat crossings and routes without shoreline intersections represent geometric scenarios, not observations of hatchling mortality, disorientation or behavioural responses.

The spatial modelling results should therefore be interpreted as evidence of how beach geometry and orientation deviation may influence potential crawling distance and direct shoreline access under the specified modelling assumptions.

### 5.18 Data Sources and References

**Esri.** (n.d.). *World Imagery* [Satellite and aerial imagery basemap]. ArcGIS Online. https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9

**QGIS Development Team.** (2026). *QGIS Geographic Information System* (Version 3.44.14-Solothurn) [Computer software]. QGIS Association. https://qgis.org/

**Queensland Government.** (n.d.). *Coastline - Queensland* (Version 1.0) [Geospatial dataset]. Queensland Spatial Catalogue (QSpatial).

## 6. Simulation-Based Power Analyses

**Corresponding thesis section:** 2.8 Simulation-Based Power Analyses

### 6.1 Project Overview

Simulation-based power analyses were conducted to evaluate the sampling effort required to detect hypothetical relationships between artificial light at night (ALAN) and sea turtle hatchling orientation, as well as potential differences in orientation associated with temporary light-barrier deployment.

These analyses were developed to support recommendations for future monitoring and experimental study design along the Sunshine Coast, Queensland, Australia.

Rather than estimating additional effects from the observed dataset, the simulations evaluated how statistical power could change under different assumptions about effect size, sample size and variability.

Three power-analysis components were considered:

1. **Between-beach ALAN power analysis:** Evaluating the ability to detect hypothetical relationships between beach-level mean nighttime radiance and hatchling orientation offset.
2. **Within-beach ALAN power analysis:** Evaluating the ability to detect hypothetical relationships between variation in nighttime radiance within individual beaches and hatchling orientation offset.
3. **Light-barrier power analysis:** Estimating the sampling effort required to detect hypothetical reductions in orientation offset associated with temporary light-barrier deployment.

These analyses were intended to inform future study planning rather than demonstrate causal relationships between artificial lighting, light barriers and hatchling orientation.

### 6.2 Repository Organisation

The power-analysis materials are stored in the [`Power Analysis`](./Power%20Analysis/) directory.

The repository contains three corresponding analysis files:

```text
Power Analysis/
├── Between_Beaches
├── Within_Beach
└── Light Barrier
```

**Between_Beaches**

Contains the simulation workflow associated with detecting hypothetical between-beach relationships between artificial nighttime radiance and hatchling orientation.

**Within_Beach**

Contains the simulation workflow associated with detecting hypothetical within-beach relationships between artificial nighttime radiance and hatchling orientation.

**Light Barrier**

Contains the simulation workflow used to evaluate future sample-size requirements for detecting hypothetical light-barrier-associated reductions in corrected hatchling orientation offset.

The three analyses address different statistical questions and should be interpreted separately.

### 6.3 General Principles of Simulation-Based Power Analysis

Statistical power describes the probability that a statistical test will detect a specified effect when that effect exists under the assumed data-generating model.

Simulation-based power analysis estimates this probability by repeatedly generating hypothetical datasets under predefined conditions and analysing each dataset using a specified statistical procedure.

For each simulation scenario, the general procedure involved:

1. Defining the hypothetical effect to be detected.
2. Specifying the sample size and sampling structure.
3. Generating hypothetical observations under the assumed effect and variability.
4. Fitting the corresponding statistical model.
5. Extracting the statistical significance of the effect of interest.
6. Repeating the procedure across multiple simulated datasets.
7. Calculating the proportion of simulations in which the effect was statistically significant.

Estimated statistical power was calculated as:

**Estimated power = Number of simulations with p < 0.05 ÷ Total number of simulations**

A significance threshold of 0.05 and a target statistical power of 80% were used in the documented light-barrier analysis.

The resulting power estimates are conditional on the assumptions used to generate the hypothetical data, including effect size, variability, sampling allocation and statistical model structure.

### 6.4 Between-Beach Artificial-Light Power Analysis

The between-beach power analysis evaluated the sampling effort required to detect hypothetical associations between beach-level mean artificial nighttime radiance and corrected hatchling orientation offset.

This analysis was motivated by the distinction between differences in artificial-light conditions among beaches and variation in nighttime radiance among emergence events within individual beaches.

The between-beach component considered whether beaches with different average artificial-light conditions could exhibit detectable differences in hatchling orientation offset.

The simulation framework reflected the hierarchical structure of the empirical artificial-light analysis, including observations grouped within beaches.

The model structure accounted for:

- Beach-level mean ALAN radiance.
- Within-beach variation in ALAN radiance.
- Moon illumination.
- Clustering of emergence observations within beaches.

The simulation design isolated the hypothetical between-beach relationship by setting the within-beach ALAN coefficient to zero during data generation.

This allowed the ability to detect a between-beach radiance association to be evaluated without simultaneously imposing a within-beach association.

The resulting power estimates were intended to inform the number of beaches and emergence observations potentially required to detect between-beach artificial-light relationships in future monitoring.

The exact effect-size grid, sampling combinations, simulation repetitions and model-fitting settings should be interpreted using the archived `Between_Beaches` script.

### 6.5 Within-Beach Artificial-Light Power Analysis

The within-beach power analysis evaluated the ability to detect hypothetical associations between variation in artificial nighttime radiance within individual beaches and corrected hatchling orientation offset.

This component addressed a different question from the between-beach analysis.

Whereas the between-beach analysis considered differences in average artificial-light conditions among beaches, the within-beach analysis focused on variation among emergence observations occurring at the same beach.

The distinction is important because relationships detected among beaches do not necessarily imply that similar relationships occur among emergence locations within individual beaches.

The within-beach simulation was intended to investigate the sampling effort required to identify these finer-scale associations under the assumptions specified in the corresponding script.

The exact simulation model, effect-size assumptions, number of beaches, observations per beach and statistical testing procedure are documented by the `Within_Beach` analysis file and should not be assumed to be identical to those used in the between-beach analysis.

### 6.6 Light-Barrier Power Analysis: Study Context

The light-barrier power analysis was developed using observations from the temporary light-barrier pilot study.

The purpose was to estimate the number of future hatchling emergence events that might be required to detect hypothetical reductions in corrected orientation offset associated with light-barrier deployment.

The simulation focused on two beaches:

- Shelly Beach.
- Yaroomba Beach.

These beaches were selected because the pilot dataset contained observations under both light-barrier and no-barrier conditions.

The simulation used the pilot results to establish baseline orientation-offset characteristics and evaluate hypothetical future sampling designs.

The analysis did not assume that the observed pilot association represented a confirmed causal effect of light barriers.

### 6.7 Light-Barrier Pilot Data Preparation

The light-barrier simulation used the prepared pilot dataset containing the following variables:

| Variable | Description |
|---|---|
| `LOCAL` | Beach identity |
| `LIGHT_BARRIER` | Light-barrier status |
| `UNIQUE.IDENTIFIER` | Unique nest identifier |
| `OFFSET.CORRECTED` | Corrected hatchling orientation offset in degrees |

The dataset was restricted to Shelly Beach and Yaroomba Beach.

Light-barrier status was coded as:

- `N`: No barrier.
- `Y`: Light barrier.

Corrected orientation offset was treated as the continuous response variable.

Descriptive statistics were calculated for each beach and barrier-status combination, including the number of emergence events, number of unique nests, mean offset, standard deviation, median, minimum and maximum.

These summaries provided the baseline information used to parameterise the hypothetical future-study simulations.

### 6.8 Estimating the Pilot Light-Barrier Association

A beach-adjusted linear model was fitted to the pilot observations.

The model was specified in R as:

`OFFSET.CORRECTED ~ Barrier + Beach`

Corrected orientation offset was the response variable, while barrier status and beach identity were included as explanatory variables.

The estimated light-barrier coefficient represented the difference in orientation offset associated with barrier presence after accounting for beach identity.

The observed point estimate was approximately **−12.94°**, indicating a lower corrected orientation offset under light-barrier conditions in the fitted pilot model.

The residual standard deviation from this model was approximately **20.73°**.

These values were used to inform the simulation assumptions.

The observed coefficient was treated as an illustrative effect-size estimate rather than evidence of an established treatment effect.

### 6.9 Hypothetical Light-Barrier Effect Sizes

Five hypothetical barrier-associated reductions in corrected orientation offset were evaluated.

| Scenario | Assumed reduction |
|---|---:|
| No effect | 0° |
| Small reduction | 5° |
| Intermediate reduction | 10° |
| Pilot-estimated reduction | 12.94° |
| Larger reduction | 15° |

The zero-effect scenario was included to evaluate the false-positive behaviour of the statistical procedure.

The 12.94° scenario corresponded to the magnitude of the observed beach-adjusted pilot estimate.

The remaining effect sizes represented alternative hypothetical reductions that could be investigated in future monitoring.

These effect sizes were planning assumptions and were not interpreted as established biologically meaningful thresholds.

### 6.10 Future Sample-Size Scenarios

Eight total sample sizes were evaluated:

| Total emergence events | Events per beach × barrier group |
|---:|---:|
| 40 | 10 |
| 60 | 15 |
| 80 | 20 |
| 100 | 25 |
| 120 | 30 |
| 160 | 40 |
| 200 | 50 |
| 240 | 60 |

Each simulated study was balanced across the four combinations of beach and barrier status:

1. Shelly Beach, no barrier.
2. Shelly Beach, light barrier.
3. Yaroomba Beach, no barrier.
4. Yaroomba Beach, light barrier.

This balanced allocation was used to evaluate sampling requirements under a more consistent future monitoring design than the original observational pilot dataset.

The total sample size represented emergence events rather than necessarily independent nests.

### 6.11 Variability Scenarios

Two assumptions about variability in corrected orientation offset were evaluated.

**Observed variability**

The first scenario used the residual standard deviation estimated from the pilot linear model:

**SD = 20.73°**

**Higher variability**

The second scenario increased the observed residual standard deviation by 25%:

**SD = 20.73° × 1.25 ≈ 25.92°**

The higher-variability scenario was included to investigate how additional between-event variability could influence the sample size required to detect a hypothetical barrier-associated reduction.

Both variability scenarios were treated as modelling assumptions rather than predictions of the exact variability expected in future monitoring.

### 6.12 Generation of Hypothetical Emergence Data

Hypothetical corrected orientation offsets were generated using Gamma distributions.

The Gamma distribution was selected to accommodate non-negative, right-skewed orientation-offset measurements.

For each beach, the mean corrected orientation offset under no-barrier conditions was used as the baseline.

For simulated barrier observations, the specified hypothetical reduction was subtracted from the corresponding beach baseline mean.

The Gamma distribution parameters were calculated from the scenario-specific target mean and standard deviation.

The shape parameter was calculated as:

**Shape = (Target mean ÷ Standard deviation)²**

The scale parameter was calculated as:

**Scale = Standard deviation² ÷ Target mean**

These parameters allowed the simulated observations to reflect the assumed mean orientation offset and variability for each scenario.

The simulation required positive target means. Scenarios producing non-positive target means were not valid under the specified Gamma distribution and required review rather than automatic truncation.

### 6.13 Simulation Procedure and Statistical Testing

For each combination of hypothetical effect size, total sample size and variability scenario, **2,000 hypothetical datasets** were generated.

Each simulated dataset was analysed using the same general beach-adjusted linear model structure:

`Offset ~ Barrier + Beach`

The statistical significance of the light-barrier coefficient was evaluated using a two-sided test with a significance threshold of 0.05.

A simulated study was counted as detecting the hypothetical association when the barrier coefficient had a p-value below 0.05.

Statistical power was estimated as the proportion of the 2,000 simulated datasets meeting this criterion.

The main simulation used a fixed random seed of `123` to support reproducibility.

The resulting power estimates described the probability of detecting the specified hypothetical reduction under the assumed sampling design and data-generating model.

### 6.14 Identifying Sample Sizes for 80% Statistical Power

For each hypothetical effect size and variability scenario, the estimated statistical power was examined across the eight tested sample sizes.

The first tested sample size achieving at least 80% power was identified as the estimated sampling requirement within the evaluated range.

Where 80% power was not achieved at any tested sample size, no threshold was assigned.

The power analysis indicated that, under the observed-variability assumptions, approximately:

| Hypothetical reduction | Total emergence events required for at least 80% power |
|---|---:|
| 10° | 160 |
| 12.94° | 100 |
| 15° | 80 |

These estimates apply to the balanced two-beach simulation design and should not be interpreted as universal sample-size requirements.

Greater variability generally increases the sampling effort needed to detect a given effect.

### 6.15 False-Positive Rate Assessment

The zero-effect simulation scenario was used to evaluate the behaviour of the statistical testing procedure when no barrier-associated difference was imposed.

For this scenario, the assumed barrier effect was 0°.

The false-positive rate was calculated as the proportion of simulated datasets in which the fitted model nevertheless produced a barrier-associated p-value below 0.05.

These rates were compared with the nominal 5% significance threshold.

This assessment was included to evaluate whether the statistical procedure produced approximately the expected frequency of significant results under the simulated null hypothesis.

### 6.16 Permutation-Based Validation

A supplementary validation analysis was conducted to compare the linear-model power estimates with estimates obtained using beach-stratified permutation tests.

This approach reflected the permutation-based inference used in the original light-barrier pilot analysis.

Three representative scenarios were selected:

| Hypothetical reduction | Total emergence events |
|---|---:|
| 15° | 80 |
| 12.94° | 100 |
| 10° | 160 |

For each scenario:

1. A total of 500 hypothetical datasets were generated using the observed-variability assumption.
2. The beach-adjusted light-barrier coefficient was calculated for each dataset.
3. Barrier-status labels were randomly permuted within each beach.
4. A total of 999 permutations were performed for each simulated dataset.
5. A two-sided permutation p-value was calculated by comparing the observed coefficient with the distribution of coefficients obtained under permutation.
6. Permutation-based statistical power was calculated as the proportion of simulated datasets producing p-values below 0.05.

The validation analysis used a fixed random seed of `456`.

The permutation results were compared with the corresponding linear-model power estimates to assess the sensitivity of the sample-size conclusions to the statistical testing procedure.

### 6.17 Simulation Outputs

The light-barrier simulation workflow was designed to generate several outputs for evaluating future study requirements.

These included:

- Descriptive summaries of the pilot light-barrier observations.
- Estimates of the observed beach-adjusted barrier association and residual variability.
- Statistical power estimates across the specified effect sizes, sample sizes and variability scenarios.
- Estimated sample-size thresholds for achieving at least 80% power.
- False-positive rate summaries from the zero-effect simulations.
- Comparisons between linear-model and permutation-based power estimates.
- Power curves illustrating the relationship between sample size and estimated statistical power.

These outputs provide a basis for evaluating the practical sampling effort required for future light-barrier monitoring.

### 6.18 Reproducing the Power Analyses

The power-analysis workflows are organised within the [`Power Analysis`](./Power%20Analysis/) directory.

The between-beach and within-beach simulation files should be used with their corresponding input data, model assumptions and parameter settings.

The light-barrier workflow was implemented in R and requires the prepared pilot dataset containing beach identity, light-barrier status, unique nest identifiers and corrected orientation offsets.

Reproducing the numerical results requires the same input data, effect-size assumptions, sampling allocation, variability parameters, simulation repetitions, random seeds and statistical testing procedures.

The original pilot data are necessary to reproduce the baseline beach means and residual standard deviation used to generate the light-barrier scenarios.

The archived scripts provide the computational basis for the simulations, while the thesis Methods section provides the broader scientific context and interpretation.

### 6.19 Assumptions and Methodological Limitations

The power analyses were intended to support future study planning and should be interpreted in relation to their underlying assumptions.

**Hypothetical effects**

The simulations imposed specified artificial-light relationships or light-barrier-associated reductions. These were not necessarily effects established by the observed dataset.

**Model-dependent power**

Estimated power depends on the statistical model used to analyse the simulated observations. Different models or testing procedures may produce different power estimates.

**Sampling structure**

The light-barrier simulations assumed balanced sampling across beaches and barrier conditions. Actual future monitoring may produce unequal sample sizes.

**Independence assumptions**

The light-barrier simulation generated observations independently within each beach-by-barrier group and did not explicitly model nest-level clustering.

**Variability assumptions**

The simulations used variability estimated from the pilot dataset, together with a higher-variability scenario. Future monitoring may exhibit different variability.

**Gamma-distributed observations**

The Gamma simulation represented non-negative, right-skewed orientation offsets. The resulting data were analysed using a linear model, as specified in the simulation workflow.

**Limited sample-size grid**

The evaluated sample sizes were discrete values between 40 and 240 emergence events. The first sample size reaching 80% power was therefore the first qualifying value within this grid, not necessarily the exact minimum sample size.

**Interpretation of power**

Statistical power represents the probability of detecting an assumed effect under specified conditions. It does not indicate the probability that the assumed effect exists or establish a causal relationship.

The power-analysis results should therefore be interpreted as conditional planning estimates intended to inform future monitoring design, sampling effort and methodological development.

