from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsRasterLayer
)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon
from datetime import datetime
import math
import re


# ============================================================
# SETTINGS
# ============================================================

INPUT_LAYER_NAME = "VIIRS 2025 data1"

OUTPUT_3X3_NAME = "VIIRS_3x3_2025"
OUTPUT_BRIGHTEST_NAME = "VIIRS_Brightest_2025"

YEAR = 2025


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def unwrap(value):
    """Convert QVariant/NULL values into normal Python values."""
    if value is None:
        return None

    try:
        if value.isNull():
            return None
    except:
        pass

    try:
        value = value.value()
    except:
        pass

    return value


def clean_string(value):
    """Safely convert a value to string."""
    value = unwrap(value)

    if value is None:
        return ""

    return str(value).strip()


def to_float(value):
    """Safely convert a value to float."""
    value = unwrap(value)

    if value is None:
        return None

    try:
        return float(value)
    except:
        return None


def parse_date(date_value):
    """
    Parse DD/MM/YYYY date.
    Returns a datetime object or None.
    """
    date_string = clean_string(date_value)

    if not date_string:
        return None

    # Expected format
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(date_string, fmt)
        except:
            pass

    # Sometimes QGIS may provide an ISO-style date
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_string, fmt)
        except:
            pass

    return None


def find_viirs_raster(date_obj):
    """
    Find the VIIRS raster whose filename contains
    AYYYYDDD for the requested date.
    """

    if date_obj is None:
        return None

    doy = date_obj.timetuple().tm_yday

    target_code = "A{}{:03d}".format(
        date_obj.year,
        doy
    )

    for layer in QgsProject.instance().mapLayers().values():

        if not isinstance(layer, QgsRasterLayer):
            continue

        name = layer.name()

        if target_code in name:
            return layer

    return None


def circular_bearing(origin_lon, origin_lat, target_lon, target_lat):
    """
    Bearing from origin to target, clockwise from north,
    returned as 0-360 degrees.
    """

    lon1 = math.radians(origin_lon)
    lat1 = math.radians(origin_lat)
    lon2 = math.radians(target_lon)
    lat2 = math.radians(target_lat)

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)

    y = (
        math.cos(lat1) * math.sin(lat2)
        -
        math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    )

    bearing = math.degrees(math.atan2(x, y))

    if bearing < 0:
        bearing += 360

    return bearing


def distance_meters(lon1, lat1, lon2, lat2):
    """
    Calculate distance using EPSG:32756.
    """

    source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
    target_crs = QgsCoordinateReferenceSystem("EPSG:32756")

    transform = QgsCoordinateTransform(
        source_crs,
        target_crs,
        QgsProject.instance()
    )

    p1 = transform.transform(
        QgsPointXY(lon1, lat1)
    )

    p2 = transform.transform(
        QgsPointXY(lon2, lat2)
    )

    dx = p2.x() - p1.x()
    dy = p2.y() - p1.y()

    return math.sqrt(dx * dx + dy * dy)


def pixel_center_from_point(raster, lon, lat):
    """
    Find the raster pixel containing the nest and return
    the centre coordinate of that pixel.
    """

    provider = raster.dataProvider()

    # Transform nest coordinate into raster CRS
    source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
    raster_crs = raster.crs()

    transform = QgsCoordinateTransform(
        source_crs,
        raster_crs,
        QgsProject.instance()
    )

    p = transform.transform(
        QgsPointXY(lon, lat)
    )

    extent = raster.extent()
    xres = raster.rasterUnitsPerPixelX()
    yres = raster.rasterUnitsPerPixelY()

    # Pixel column/row
    col = int(
        math.floor(
            (p.x() - extent.xMinimum()) / xres
        )
    )

    row = int(
        math.floor(
            (extent.yMaximum() - p.y()) / yres
        )
    )

    if col < 0 or col >= raster.width():
        return None

    if row < 0 or row >= raster.height():
        return None

    # Pixel centre in raster CRS
    center_x = (
        extent.xMinimum()
        +
        (col + 0.5) * xres
    )

    center_y = (
        extent.yMaximum()
        -
        (row + 0.5) * yres
    )

    center_raster = QgsPointXY(
        center_x,
        center_y
    )

    # Transform back to WGS84
    reverse_transform = QgsCoordinateTransform(
        raster_crs,
        source_crs,
        QgsProject.instance()
    )

    center_wgs84 = reverse_transform.transform(
        center_raster
    )

    return {
        "row": row,
        "col": col,
        "x": center_wgs84.x(),
        "y": center_wgs84.y()
    }


def get_pixel_center(raster, center_info, dx, dy):
    """
    Get centre coordinate of a neighbouring pixel.
    dx = -1,0,+1
    dy = -1,0,+1
    """

    extent = raster.extent()

    xres = raster.rasterUnitsPerPixelX()
    yres = raster.rasterUnitsPerPixelY()

    raster_crs = raster.crs()
    wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")

    transform_to_raster = QgsCoordinateTransform(
        wgs84,
        raster_crs,
        QgsProject.instance()
    )

    nest_center_raster = transform_to_raster.transform(
        QgsPointXY(
            center_info["x"],
            center_info["y"]
        )
    )

    x = nest_center_raster.x() + dx * xres
    y = nest_center_raster.y() - dy * yres

    point_raster = QgsPointXY(x, y)

    transform_to_wgs84 = QgsCoordinateTransform(
        raster_crs,
        wgs84,
        QgsProject.instance()
    )

    point_wgs84 = transform_to_wgs84.transform(
        point_raster
    )

    return point_wgs84


def sample_raster(raster, lon, lat):
    """
    Sample raster at a WGS84 coordinate.
    """

    provider = raster.dataProvider()

    source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
    raster_crs = raster.crs()

    transform = QgsCoordinateTransform(
        source_crs,
        raster_crs,
        QgsProject.instance()
    )

    point = transform.transform(
        QgsPointXY(lon, lat)
    )

    result = provider.sample(
        point,
        1
    )

    value = result[0]

    if value is None:
        return None

    try:
        if math.isnan(float(value)):
            return None
    except:
        pass

    # Check raster NoData value
    try:
        nodata = provider.sourceNoDataValue(1)

        if nodata is not None:
            if float(value) == float(nodata):
                return None
    except:
        pass

    try:
        return float(value)
    except:
        return None


# ============================================================
# FIND INPUT LAYER
# ============================================================

input_layers = QgsProject.instance().mapLayersByName(
    INPUT_LAYER_NAME
)

if not input_layers:
    raise Exception(
        "Could not find input layer: {}".format(
            INPUT_LAYER_NAME
        )
    )

input_layer = input_layers[0]

print("")
print("=" * 70)
print("VIIRS 2025 EXTRACTION")
print("=" * 70)
print("Input layer:", INPUT_LAYER_NAME)
print("Input features:", input_layer.featureCount())
print("")


# ============================================================
# REMOVE OLD OUTPUTS
# ============================================================

for layer_name in [
    OUTPUT_3X3_NAME,
    OUTPUT_BRIGHTEST_NAME
]:

    old_layers = QgsProject.instance().mapLayersByName(
        layer_name
    )

    for old_layer in old_layers:
        QgsProject.instance().removeMapLayer(
            old_layer.id()
        )

        print("Removed old layer:", layer_name)


# ============================================================
# CREATE 3x3 OUTPUT LAYER
# ============================================================

output_3x3 = QgsVectorLayer(
    "Point?crs=EPSG:4326",
    OUTPUT_3X3_NAME,
    "memory"
)

provider_3x3 = output_3x3.dataProvider()

provider_3x3.addAttributes([

    QgsField("Nest_ID", QVariant.String),

    QgsField("Emergence_Date", QVariant.String),

    QgsField("Pixel_Pos", QVariant.String),

    QgsField("VIIRS", QVariant.Double),

    QgsField("Pixel_Lon", QVariant.Double),

    QgsField("Pixel_Lat", QVariant.Double),

    QgsField("Distance_m", QVariant.Double),

    QgsField("Bearing_deg", QVariant.Double)

])

output_3x3.updateFields()


# ============================================================
# CREATE BRIGHTEST OUTPUT
# ============================================================

output_brightest = QgsVectorLayer(
    "Point?crs=EPSG:4326",
    OUTPUT_BRIGHTEST_NAME,
    "memory"
)

provider_brightest = output_brightest.dataProvider()

provider_brightest.addAttributes([

    QgsField("Nest_ID", QVariant.String),

    QgsField("Emergence_Date", QVariant.String),

    QgsField("Brightest_Pos", QVariant.String),

    QgsField("VIIRS", QVariant.Double),

    QgsField("Pixel_Lon", QVariant.Double),

    QgsField("Pixel_Lat", QVariant.Double),

    QgsField("Distance_m", QVariant.Double),

    QgsField("Bearing_deg", QVariant.Double)

])

output_brightest.updateFields()


# ============================================================
# GRID POSITION LABELS
# ============================================================

positions = [

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


# ============================================================
# PROCESS EACH NEST
# ============================================================

total_records = input_layer.featureCount()

processed = 0
skipped_coordinates = 0
missing_rasters = 0
all_nodata = 0
errors = 0

error_list = []

for feature_number, feat in enumerate(
    input_layer.getFeatures(),
    start=1
):

    nest_id = clean_string(
        feat["Nest_ID"]
    )

    emergence_date_string = clean_string(
        feat["Emergence_Date"]
    )

    lat = to_float(
        feat["Latitude"]
    )

    lon = to_float(
        feat["Longitude"]
    )

    print(
        "[{}/{}] Processing {} - {}".format(
            feature_number,
            total_records,
            nest_id,
            emergence_date_string
        )
    )

    # --------------------------------------------------------
    # CHECK COORDINATES
    # --------------------------------------------------------

    if lat is None or lon is None:

        print(
            "   SKIPPED: missing coordinates"
        )

        skipped_coordinates += 1
        continue

    # --------------------------------------------------------
    # PARSE DATE
    # --------------------------------------------------------

    date_obj = parse_date(
        emergence_date_string
    )

    if date_obj is None:

        print(
            "   ERROR: could not parse date"
        )

        errors += 1

        error_list.append(
            (
                nest_id,
                emergence_date_string,
                "Could not parse date"
            )
        )

        continue

    # --------------------------------------------------------
    # FIND VIIRS RASTER
    # --------------------------------------------------------

    raster = find_viirs_raster(
        date_obj
    )

    if raster is None:

        print(
            "   SKIPPED: no VIIRS raster found"
        )

        missing_rasters += 1

        continue

    print(
        "   Raster:",
        raster.name()
    )

    # --------------------------------------------------------
    # FIND NEST PIXEL
    # --------------------------------------------------------

    center_info = pixel_center_from_point(
        raster,
        lon,
        lat
    )

    if center_info is None:

        print(
            "   ERROR: nest outside raster"
        )

        errors += 1

        error_list.append(
            (
                nest_id,
                emergence_date_string,
                "Nest outside raster"
            )
        )

        continue

    # --------------------------------------------------------
    # EXTRACT 3x3
    # --------------------------------------------------------

    pixel_results = []

    for dx, dy, position in positions:

        try:

            pixel_point = get_pixel_center(
                raster,
                center_info,
                dx,
                dy
            )

            pixel_lon = pixel_point.x()
            pixel_lat = pixel_point.y()

            viirs_value = sample_raster(
                raster,
                pixel_lon,
                pixel_lat
            )

            distance = distance_meters(
                lon,
                lat,
                pixel_lon,
                pixel_lat
            )

            bearing = circular_bearing(
                lon,
                lat,
                pixel_lon,
                pixel_lat
            )

            pixel_results.append({

                "position": position,

                "value": viirs_value,

                "lon": pixel_lon,

                "lat": pixel_lat,

                "distance": distance,

                "bearing": bearing

            })

            # ------------------------------------------------
            # ADD TO DETAILED OUTPUT
            # ------------------------------------------------

            new_feature = QgsFeature(
                output_3x3.fields()
            )

            new_feature.setGeometry(
                QgsGeometry.fromPointXY(
                    QgsPointXY(
                        pixel_lon,
                        pixel_lat
                    )
                )
            )

            new_feature["Nest_ID"] = nest_id

            new_feature["Emergence_Date"] = (
                emergence_date_string
            )

            new_feature["Pixel_Pos"] = position

            if viirs_value is not None:
                new_feature["VIIRS"] = viirs_value
            else:
                new_feature["VIIRS"] = None

            new_feature["Pixel_Lon"] = pixel_lon
            new_feature["Pixel_Lat"] = pixel_lat

            new_feature["Distance_m"] = distance
            new_feature["Bearing_deg"] = bearing

            provider_3x3.addFeature(
                new_feature
            )

        except Exception as e:

            print(
                "   ERROR processing pixel:",
                position,
                str(e)
            )

            errors += 1

            error_list.append(
                (
                    nest_id,
                    emergence_date_string,
                    "{}: {}".format(
                        position,
                        str(e)
                    )
                )
            )

    # --------------------------------------------------------
    # FIND BRIGHTEST SURROUNDING PIXEL
    # --------------------------------------------------------

    surrounding_pixels = [

        p for p in pixel_results

        if p["position"] != "Nest Pixel"

        and p["value"] is not None

    ]

    # Count usable pixels
    usable_pixels = [

        p for p in pixel_results

        if p["value"] is not None

    ]

    if len(usable_pixels) == 0:

        print(
            "   All 9 pixels are NoData"
        )

        all_nodata += 1

        processed += 1

        continue

    if len(surrounding_pixels) == 0:

        print(
            "   No usable surrounding pixels"
        )

        processed += 1

        continue

    brightest = max(
        surrounding_pixels,
        key=lambda p: p["value"]
    )

    print(
        "   Brightest:",
        brightest["position"],
        "=",
        brightest["value"]
    )

    # --------------------------------------------------------
    # ADD BRIGHTEST FEATURE
    # --------------------------------------------------------

    bright_feature = QgsFeature(
        output_brightest.fields()
    )

    bright_feature.setGeometry(
        QgsGeometry.fromPointXY(
            QgsPointXY(
                brightest["lon"],
                brightest["lat"]
            )
        )
    )

    bright_feature["Nest_ID"] = nest_id

    bright_feature["Emergence_Date"] = (
        emergence_date_string
    )

    bright_feature["Brightest_Pos"] = (
        brightest["position"]
    )

    bright_feature["VIIRS"] = (
        brightest["value"]
    )

    bright_feature["Pixel_Lon"] = (
        brightest["lon"]
    )

    bright_feature["Pixel_Lat"] = (
        brightest["lat"]
    )

    bright_feature["Distance_m"] = (
        brightest["distance"]
    )

    bright_feature["Bearing_deg"] = (
        brightest["bearing"]
    )

    provider_brightest.addFeature(
        bright_feature
    )

    processed += 1


# ============================================================
# FINALISE OUTPUTS
# ============================================================

output_3x3.updateExtents()
output_brightest.updateExtents()

QgsProject.instance().addMapLayer(
    output_3x3
)

QgsProject.instance().addMapLayer(
    output_brightest
)


# ============================================================
# SUMMARY
# ============================================================

print("")
print("=" * 70)
print("2025 VIIRS EXTRACTION COMPLETE")
print("=" * 70)

print(
    "Input records:",
    total_records
)

print(
    "Successfully processed:",
    processed
)

print(
    "Skipped - missing coordinates:",
    skipped_coordinates
)

print(
    "Missing VIIRS rasters:",
    missing_rasters
)

print(
    "All 9 pixels NoData:",
    all_nodata
)

print(
    "Errors:",
    errors
)

print(
    "3x3 output features:",
    output_3x3.featureCount()
)

print(
    "Brightest output features:",
    output_brightest.featureCount()
)

print("")
print("Expected 3x3 features if all 40 records process:")
print("40 × 9 = 360")
print("")

if error_list:

    print("ERROR DETAILS:")

    for item in error_list:

        print(
            " - {} | {} | {}".format(
                item[0],
                item[1],
                item[2]
            )
        )

print("=" * 70)
