import geopandas as gpd
from shapely import geometry

# Read the shapefile
gdf = gpd.read_file("abbottstown_pa_union.shp")

# Reproject to projected coordinate system
gdf = gdf.to_crs("EPSG:3857")

# Get the extent of the shapefile
total_bounds = gdf.total_bounds

# Get minX, minY, maxX, maxY
minX, minY, maxX, maxY = total_bounds

# Create a fishnet
x, y = (minX, minY)
geom_array = []

# Polygon Size
square_size = 1000
while y <= maxY:
    while x <= maxX:
        geom = geometry.Polygon(
            [
                (x, y),
                (x, y + square_size),
                (x + square_size, y + square_size),
                (x + square_size, y),
                (x, y)
            ]
        )
        geom_array.append(geom)
        x += square_size
    x = minX
    y += square_size

fishnet = gpd.GeoDataFrame(geom_array, columns=["geometry"]).set_crs("EPSG:3857")
fishnet.to_file("fishnet_grid.shp")