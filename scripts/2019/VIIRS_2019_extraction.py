exec("""
from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsField,
    QgsVectorLayer,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea
)
from PyQt5.QtCore import QVariant
from datetime import datetime
import math


# ============================================================
# SETTINGS
# ============================================================

NEST_LAYER_NAME = "VIIRS 2019 data"

# TEST ONLY: these are the first three nests
TEST_NESTS = ["69N", "72N", "74N"]


# ============================================================
# FIND THE NEST CSV LAYER
# ============================================================

project = QgsProject.instance()

nest_layer = project.mapLayersByName(NEST_LAYER_NAME)

if not nest_layer:
    raise Exception(
        "Could not find the layer named: " + NEST_LAYER_NAME
    )

nest_layer = nest_layer[0]

print("")
print("Found nest layer:", nest_layer.name())


# ============================================================
# FIND ALL LOADED VIIRS RASTERS
# ============================================================

raster_layers = []

for layer in project.mapLayers().values():

    if layer.type() == 1:  # Raster layer

        name = layer.name()

        if "VNP46A2.A2019" in name:
            raster_layers.append(layer)


print("Found", len(raster_layers), "2019 VIIRS raster layers.")

for layer in raster_layers:
    print("  ", layer.name())


if len(raster_layers) == 0:
    raise Exception(
        "No 2019 VIIRS raster layers were found."
    )


# ============================================================
# MATCH A DATE TO THE CORRECT VIIRS RASTER
# ============================================================

def find_viirs_raster(date_string):

    # Try DD/MM/YYYY first
    try:
        date = datetime.strptime(
            str(date_string),
            "%d/%m/%Y"
        )
    except:

        # Try YYYY-MM-DD if necessary
        try:
            date = datetime.strptime(
                str(date_string),
                "%Y-%m-%d"
            )
        except:

            # Try QGIS date objects
            try:
                date = date_string.toPyDateTime()
            except:
                raise Exception(
                    "Could not understand date: " +
                    str(date_string)
                )

    day_of_year = date.timetuple().tm_yday

    viirs_code = (
        "A" +
        str(date.year) +
        str(day_of_year).zfill(3)
    )

    print(
        "Date",
        date.strftime("%d/%m/%Y"),
        "->",
        viirs_code
    )

    for raster in raster_layers:

        if viirs_code in raster.name():
            return raster

    return None


# ============================================================
# CREATE OUTPUT LAYER: 9 PIXELS PER NEST
# ============================================================

detail = QgsVectorLayer(
    "Point?crs=EPSG:4326",
    "VIIRS_3x3_TEST",
    "memory"
)

detail_fields = [

    QgsField("Nest_ID", QVariant.String),
    QgsField("Emergence_Date", QVariant.String),
    QgsField("Pixel", QVariant.String),

    QgsField(
        "VIIRS_Value",
        QVariant.Double
    ),

    QgsField(
        "Pixel_Longitude",
        QVariant.Double
    ),

    QgsField(
        "Pixel_Latitude",
        QVariant.Double
    ),

    QgsField(
        "Distance_m",
        QVariant.Double
    ),

    QgsField(
        "Bearing_deg",
        QVariant.Double
    )
]

detail.dataProvider().addAttributes(detail_fields)
detail.updateFields()


# ============================================================
# CREATE OUTPUT LAYER: BRIGHTEST SURROUNDING PIXEL
# ============================================================

summary = QgsVectorLayer(
    "None",
    "VIIRS_Brightest_TEST",
    "memory"
)

summary_fields = [

    QgsField("Nest_ID", QVariant.String),
    QgsField("Emergence_Date", QVariant.String),

    QgsField(
        "Brightest_Pixel",
        QVariant.String
    ),

    QgsField(
        "Brightest_VIIRS",
        QVariant.Double
    ),

    QgsField(
        "Brightest_Longitude",
        QVariant.Double
    ),

    QgsField(
        "Brightest_Latitude",
        QVariant.Double
    ),

    QgsField(
        "Brightest_Distance_m",
        QVariant.Double
    ),

    QgsField(
        "Brightest_Bearing_deg",
        QVariant.Double
    )
]

summary.dataProvider().addAttributes(summary_fields)
summary.updateFields()


# ============================================================
# DISTANCE CALCULATOR
# ============================================================

distance_calc = QgsDistanceArea()

distance_calc.setSourceCrs(
    QgsCoordinateReferenceSystem("EPSG:4326"),
    project.transformContext()
)

distance_calc.setEllipsoid("WGS84")


# ============================================================
# PROCESS EACH TEST NEST
# ============================================================

nest_count = 0

for nest in nest_layer.getFeatures():

    nest_id = str(
        nest["Nest_ID"]
    )

    if nest_id not in TEST_NESTS:
        continue

    nest_count += 1

    emergence_date = nest["Emergence_Date"]

    nest_lat = float(
        nest["Latitude"]
    )

    nest_lon = float(
        nest["Longitude"]
    )

    print("")
    print("====================================")
    print("Processing:", nest_id)
    print("Date:", emergence_date)
    print("Nest:", nest_lat, nest_lon)
    print("====================================")


    # --------------------------------------------------------
    # FIND CORRECT VIIRS RASTER
    # --------------------------------------------------------

    raster = find_viirs_raster(
        emergence_date
    )

    if raster is None:

        print(
            "WARNING: No VIIRS raster found for",
            nest_id,
            emergence_date
        )

        continue

    print(
        "Using raster:",
        raster.name()
    )


    # --------------------------------------------------------
    # RASTER INFORMATION
    # --------------------------------------------------------

    provider = raster.dataProvider()

    raster_extent = raster.extent()

    raster_width = raster.width()
    raster_height = raster.height()

    x_min = raster_extent.xMinimum()
    x_max = raster_extent.xMaximum()

    y_min = raster_extent.yMinimum()
    y_max = raster_extent.yMaximum()

    x_resolution = (
        (x_max - x_min) /
        raster_width
    )

    y_resolution = (
        (y_max - y_min) /
        raster_height
    )


    # --------------------------------------------------------
    # FIND THE PIXEL CONTAINING THE NEST
    # --------------------------------------------------------

    nest_x = nest_lon
    nest_y = nest_lat

    nest_column = int(
        math.floor(
            (nest_x - x_min) /
            x_resolution
        )
    )

    nest_row = int(
        math.floor(
            (y_max - nest_y) /
            y_resolution
        )
    )

    print(
        "Nest pixel:",
        "Column =", nest_column,
        "Row =", nest_row
    )


    # --------------------------------------------------------
    # 3 x 3 PIXEL DIRECTIONS
    # --------------------------------------------------------

    directions = [

        (-1, -1, "NW"),
        ( 0, -1, "N"),
        ( 1, -1, "NE"),

        (-1,  0, "W"),
        ( 0,  0, "Nest Pixel"),
        ( 1,  0, "E"),

        (-1,  1, "SW"),
        ( 0,  1, "S"),
        ( 1,  1, "SE")
    ]


    surrounding_values = []


    # --------------------------------------------------------
    # PROCESS THE 9 PIXELS
    # --------------------------------------------------------

    for dc, dr, pixel_name in directions:

        pixel_column = nest_column + dc
        pixel_row = nest_row + dr


        # Pixel centre
        pixel_x = (
            x_min +
            (pixel_column + 0.5) *
            x_resolution
        )

        pixel_y = (
            y_max -
            (pixel_row + 0.5) *
            y_resolution
        )


        pixel_point = QgsPointXY(
            pixel_x,
            pixel_y
        )


        # ----------------------------------------------------
        # SAMPLE VIIRS VALUE
        # ----------------------------------------------------

        value, ok = provider.sample(
            pixel_point,
            1
        )


        viirs_value = None

        if ok:

            try:

                value_float = float(value)

                # VIIRS fill value
                if (
                    math.isnan(value_float)
                    or
                    value_float <= -999
                ):

                    viirs_value = None

                else:

                    viirs_value = value_float

            except:

                viirs_value = None


        # ----------------------------------------------------
        # DISTANCE
        # ----------------------------------------------------

        nest_point = QgsPointXY(
            nest_lon,
            nest_lat
        )

        distance_m = (
            distance_calc.measureLine(
                nest_point,
                pixel_point
            )
        )


        # ----------------------------------------------------
        # BEARING
        # ----------------------------------------------------

        lon1 = math.radians(
            nest_lon
        )

        lon2 = math.radians(
            pixel_x
        )

        lat1 = math.radians(
            nest_lat
        )

        lat2 = math.radians(
            pixel_y
        )

        dlon = lon2 - lon1

        bearing_x = (
            math.sin(dlon) *
            math.cos(lat2)
        )

        bearing_y = (

            math.cos(lat1) *
            math.sin(lat2)

            -

            math.sin(lat1) *
            math.cos(lat2) *
            math.cos(dlon)
        )

        bearing = math.degrees(
            math.atan2(
                bearing_x,
                bearing_y
            )
        )

        if bearing < 0:
            bearing += 360


        # ----------------------------------------------------
        # ADD TO DETAILED TABLE
        # ----------------------------------------------------

        feature = QgsFeature(
            detail.fields()
        )

        feature["Nest_ID"] = nest_id
        feature["Emergence_Date"] = str(
            emergence_date
        )

        feature["Pixel"] = pixel_name

        feature["VIIRS_Value"] = (
            viirs_value
        )

        feature["Pixel_Longitude"] = (
            pixel_x
        )

        feature["Pixel_Latitude"] = (
            pixel_y
        )

        feature["Distance_m"] = (
            distance_m
        )

        feature["Bearing_deg"] = (
            bearing
        )

        feature.setGeometry(
            QgsGeometry.fromPointXY(
                pixel_point
            )
        )

        detail.dataProvider().addFeature(
            feature
        )


        # ----------------------------------------------------
        # STORE SURROUNDING PIXELS FOR BRIGHTEST SEARCH
        # ----------------------------------------------------

        if (
            pixel_name != "Nest Pixel"
            and
            viirs_value is not None
        ):

            surrounding_values.append({

                "pixel": pixel_name,

                "value": viirs_value,

                "longitude": pixel_x,

                "latitude": pixel_y,

                "distance": distance_m,

                "bearing": bearing
            })


    # ========================================================
    # FIND BRIGHTEST SURROUNDING PIXEL
    # ========================================================

    if surrounding_values:

        brightest = max(
            surrounding_values,
            key=lambda x: x["value"]
        )


        # ----------------------------------------------------
        # ADD SUMMARY FEATURE
        # ----------------------------------------------------

        summary_feature = QgsFeature(
            summary.fields()
        )

        summary_feature["Nest_ID"] = (
            nest_id
        )

        summary_feature["Emergence_Date"] = (
            str(emergence_date)
        )

        summary_feature["Brightest_Pixel"] = (
            brightest["pixel"]
        )

        summary_feature["Brightest_VIIRS"] = (
            brightest["value"]
        )

        summary_feature["Brightest_Longitude"] = (
            brightest["longitude"]
        )

        summary_feature["Brightest_Latitude"] = (
            brightest["latitude"]
        )

        summary_feature["Brightest_Distance_m"] = (
            brightest["distance"]
        )

        summary_feature["Brightest_Bearing_deg"] = (
            brightest["bearing"]
        )

        summary.dataProvider().addFeature(
            summary_feature
        )


        print(
            "Brightest surrounding pixel:",
            brightest["pixel"]
        )

        print(
            "VIIRS:",
            brightest["value"]
        )

        print(
            "Distance:",
            brightest["distance"]
        )

        print(
            "Bearing:",
            brightest["bearing"]
        )

    else:

        print(
            "WARNING: No valid surrounding VIIRS pixels."
        )


# ============================================================
# FINISH
# ============================================================

detail.updateExtents()
summary.updateExtents()

project.addMapLayer(detail)
project.addMapLayer(summary)

print("")
print("====================================")
print("TEST COMPLETE")
print("====================================")
print("Nests processed:", nest_count)
print("")
print(
    "Open the attribute table for:"
)
print(
    "VIIRS_3x3_TEST"
)
print("")
print(
    "and:"
)
print(
    "VIIRS_Brightest_TEST"
)
print("")
""")
