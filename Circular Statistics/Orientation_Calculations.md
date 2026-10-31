# Circular Statistics: Orientation Calculations

**Thesis correspondence:** Section 2.2, Data Preparation and Derived Orientation Measurements.

This document gives the mathematical equations and worked examples for the derived hatchling and adult orientation measures described in the thesis. **The original R script used by Ebony is not available.** These equations implement the documented mathematical definitions; they have **not** been verified line-by-line against Ebony's original implementation or all field records.

## 1. Compass-bearing conventions and circular angular difference

All bearings are measured in degrees clockwise from north and normalised to the interval 0°–360° (with 360° equivalent to 0°). Define the shortest *absolute* angular difference between two bearings, $a$ and $b$, as:

$$
d(a,b)=180^\circ-\left|180^\circ-\left|a-b\right|\right|
$$

Here, $d(a,b)$ is in the interval 0°–180°. For example, for $a=350^\circ$ and $b=10^\circ$:

$$
d(350^\circ,10^\circ)=180^\circ-\left|180^\circ-340^\circ\right|=20^\circ
$$

For calculating a midpoint, the *signed* shortest difference is also needed:

$$
\Delta(a,b)=\big((a-b+180^\circ)\bmod 360^\circ\big)-180^\circ
$$

The modulo operation wraps the result around a complete circle. At an exact 180° separation, the signed direction is ambiguous.

## 2. Corrected hatchling track spread

Let $A$ and $B$ denote the two peripheral bearings of the principal hatchling orientation fan. The corrected fan spread, $S$, is:

$$
\boxed{S=d(A,B)=180^\circ-\left|180^\circ-\left|A-B\right|\right|}
$$

**Example:** If $A=350^\circ$ and $B=10^\circ$:

$$
S=180^\circ-\left|180^\circ-\left|350^\circ-10^\circ\right|\right|=20^\circ
$$

The calculated spread is 0°–180°. A smaller value describes a narrower principal fan.

## 3. Circular midpoint of the hatchling orientation fan

Let $M$ denote the midpoint of the shorter circular arc connecting $A$ and $B$. First calculate:

$$
\Delta(A,B)=\big((A-B+180^\circ)\bmod 360^\circ\big)-180^\circ
$$

Then:

$$
\boxed{M=\left(B+\frac{\Delta(A,B)}{2}\right)\bmod 360^\circ}
$$

**Example:** For $A=350^\circ$ and $B=10^\circ$:

$$
\Delta(350^\circ,10^\circ)=\big((350^\circ-10^\circ+180^\circ)\bmod 360^\circ\big)-180^\circ=-20^\circ
$$

$$
M=\left(10^\circ+\frac{-20^\circ}{2}\right)\bmod 360^\circ=0^\circ
$$

This avoids the incorrect arithmetic midpoint of 180°. For bearings exactly 180° apart, the circular midpoint is not uniquely defined; the original data-handling rule needs confirmation.

## 4. Direct ocean bearing

Let $H$ denote the recorded high-tide-line bearing and $O$ the direct ocean bearing. The oceanward perpendicular is:

$$
\boxed{O=(H+s\times90^\circ)\bmod360^\circ},\qquad s\in\{-1,+1\}
$$

Here $s$ selects the perpendicular direction pointing **towards the ocean**. It cannot be inferred from $H$ alone without the shoreline and field-recording convention.

**Example:** If $H=20^\circ$ and the clockwise perpendicular points oceanward, then $s=+1$ and:

$$
O=(20^\circ+90^\circ)\bmod360^\circ=110^\circ
$$

**Verification needed:** Confirm how the oceanward sign was selected in the original dataset.

## 5. Corrected hatchling orientation offset

Let $M$ denote the fan midpoint and $O$ the direct ocean bearing. The corrected ocean-relative offset, $\theta$, is:

$$
\boxed{\theta=d(M,O)=180^\circ-\left|180^\circ-\left|M-O\right|\right|}
$$

**Example:** If $M=350^\circ$ and $O=10^\circ$:

$$
\theta=180^\circ-\left|180^\circ-\left|350^\circ-10^\circ\right|\right|=20^\circ
$$

The absolute offset is 0°–180°. A value above 180° is not possible under this shortest-angle definition and should be checked against the source data or reporting.

## 6. Geometric sea-finding classification

Using the corrected orientation offset $\theta$ and fan spread $S$, the oceanward reference direction is considered inside the principal orientation fan when:

$$
\boxed{\theta\leq\frac{S}{2}}
$$

The binary classification can be written as:

$$
\mathrm{SeaFinding}=\begin{cases}
1, & \theta\leq S/2,\\
0, & \theta>S/2.
\end{cases}
$$

**Example:** For $\theta=12^\circ$ and $S=30^\circ$, $12^\circ\leq15^\circ$, so the event is classified as geometrically sea-finding. This does **not** establish that hatchlings physically reached the water. The thesis reports 268 events with sufficient information for this classification.

## 7. Adult UP-track ocean-relative offset

Let $U$ be the recorded adult UP-track bearing and $O$ the direct ocean bearing. The shortest angular separation is:

$$
\boxed{\theta_{\mathrm{UP}}=d(U,O)=180^\circ-\left|180^\circ-\left|U-O\right|\right|}
$$

**Example:** If $U=345^\circ$ and $O=5^\circ$:

$$
\theta_{\mathrm{UP}}=180^\circ-\left|180^\circ-\left|345^\circ-5^\circ\right|\right|=20^\circ
$$

This follows the thesis definition of comparison between *recorded bearings*. Whether any field-direction transformation was made before calculation should be confirmed against the original dataset.

## 8. Adult DOWN-track ocean-relative offset

Let $D$ be the recorded adult DOWN-track bearing. Then:

$$
\boxed{\theta_{\mathrm{DOWN}}=d(D,O)=180^\circ-\left|180^\circ-\left|D-O\right|\right|}
$$

**Example:** If $D=15^\circ$ and $O=5^\circ$:

$$
\theta_{\mathrm{DOWN}}=180^\circ-\left|180^\circ-\left|15^\circ-5^\circ\right|\right|=10^\circ
$$

## 9. Adult UP–DOWN angular difference

If the comparison uses the two **recorded** bearings without reversing either direction, the shortest separation is:

$$
\boxed{\theta_{\mathrm{UP-DOWN}}=d(U,D)=180^\circ-\left|180^\circ-\left|U-D\right|\right|}
$$

**Example:** If $U=350^\circ$ and $D=10^\circ$:

$$
\theta_{\mathrm{UP-DOWN}}=20^\circ
$$

**Verification needed:** This expression measures separation of recorded bearings. If the original analysis reversed the UP track by 180° to compare actual opposing movement directions, that would be a different metric. Do not label this a verified original calculation until the convention is checked.

## 10. Mean and standard deviation of corrected orientation offset

For $n$ emergence events with corrected absolute offsets $\theta_1,\theta_2,\ldots,\theta_n$, the arithmetic mean is:

$$
\boxed{\bar\theta=\frac{1}{n}\sum_{i=1}^{n}\theta_i}
$$

The sample standard deviation is:

$$
\boxed{SD=\sqrt{\frac{\sum_{i=1}^{n}(\theta_i-\bar\theta)^2}{n-1}}}
$$

The thesis reports $n=269$, mean offset $\bar\theta\approx21.86^\circ$, and standard deviation $SD\approx25.58^\circ$. These are arithmetic summaries of **absolute angular offsets**, not circular means of the original compass bearings.

## 11. Data-derived orientation-deviation thresholds

The first threshold is the mean plus one sample standard deviation:

$$
\boxed{T_1=\bar\theta+SD}
$$

Using the rounded reported values:

$$
T_1=21.86^\circ+25.58^\circ=47.44^\circ\approx47.4^\circ
$$

The second threshold is the mean plus two sample standard deviations:

$$
\boxed{T_2=\bar\theta+2SD}
$$

$$
T_2=21.86^\circ+2(25.58^\circ)=73.02^\circ\approx73.0^\circ
$$

| Exploratory category | Corrected absolute orientation offset |
| --- | --- |
| Low deviation | $\theta\leq T_1$ |
| Moderate deviation | $T_1<\theta\leq T_2$ |
| High deviation | $\theta>T_2$ |

These thresholds are dataset-specific descriptive categories, not independently validated biological thresholds. Calculations from unrounded source values may differ slightly in the final decimal places.

## Reproducibility and provenance

The original R code used for these calculations was not available when this document was prepared. The equations are a **mathematical specification consistent with the documented thesis Methods**, rather than a verified reproduction of the original code. For exact reproduction, the original field data, directional conventions, handling of missing or ambiguous bearings, and any manual quality-control decisions must also be documented.
