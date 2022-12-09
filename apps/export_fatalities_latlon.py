import os

import fiona
import pandas as pd
from io_avstats_db import db_utils  # type: ignore  # pylint: disable=no-name-in-module
from pyproj import Transformer


class io_point:
    """This class is a container for points for io raster.

    Points are defined as x, y and a name
    """

    def __init__(self, x, y, name, crs=4326) -> None:
        """
        inputs:
            x, y - coordinates of the point
            name - str giving the name
            crs (4326), ESPG number of the coordinate system the point belongs to
        """
        self.x = x
        self.y = y
        self.name = name
        self.crs = crs

    def transform_crs(self, new_crs: int):
        """
        inputs:
            new_crs: crs that the point should be transformed to.
        outputs:
            a new io_point at the crs specified (the old point remains the same)
        """
        trans = Transformer.from_crs(self.crs, new_crs, always_xy=True)
        x, y = trans.transform(self.x, self.y)
        return io_point(x, y, self.name + str(new_crs), crs=new_crs)


def createPtShapefile(baseName, shapeDict):
    """create a shapefile of points using a geometrical dictionary (pts, lines,
    and boxes), exclude everything in the shapeDict except pts."""
    schema = {"geometry": "Point", "properties": [("Name", "str")]}
    shapeFile = os.path.join(outFilePath, baseName + ".shp")
    pointShp = fiona.open(
        shapeFile, mode="w", driver="ESRI Shapefile", schema=schema, crs="EPSG:3857"
    )
    pts = shapeDict["Points"]
    for pt in pts:
        ptDict = {
            "geometry": {"type": "Point", "coordinates": (pt.x, pt.y)},
            "properties": {"Name": pt.name},
        }
        print(ptDict)
        pointShp.write(ptDict)
    pointShp.close()


outFilePath = r"C:/1-CodeRepos/0-IO-Tools/Play/VisualizeMaps/maps/vectorMaps/"

with db_utils.get_postgres_connection() as conn_pg:
    data_df = pd.read_sql_query(
        """
    SELECT
       ev_id,
       ev_year,
       inj_tot_f,
       dec_latitude,
       dec_longitude
    FROM
        events
    WHERE
        inj_tot_f > 0 AND
        ev_year >= 2011 AND
        ev_year < 2012 AND
        ev_country = 'USA'
    ORDER BY
        ev_year;
        """,
        conn_pg,
    )
print(data_df["ev_id"][0], data_df["ev_year"][0], data_df["inj_tot_f"][0])
print(f'<{data_df["dec_latitude"][0]}>', data_df["dec_longitude"][0])

ptArray = []
for lat, lon in zip(data_df["dec_latitude"], data_df["dec_longitude"]):
    d_lat = lat
    d_lon = lon
    # print(lat, lon, lat[0:2], lat[2:4])
    # d_lat = float(lat[0:2]) + float(lat[2:4]) / 60.0 + float(lat[4:6]) / 3600.0
    # d_lon = float(lon[0:3]) + float(lon[3:5]) / 60.0 + float(lon[5:7]) / 3600.0
    # if lat[6] == "S":
    #     d_lat *= -1
    # if lon[7] == "W":
    #     d_lon *= -1
    print(f"The latitude <{d_lat}> and the longitude <{d_lon}>")
    pt = io_point(d_lon, d_lat, "test1")
    ptArray.append(pt.transform_crs(new_crs=3857))
shapeDict = {"Points": ptArray}
createPtShapefile("testPts", shapeDict=shapeDict)

# dec_latitude <> 'None' AND
#         dec_longitude <> 'None' AND
#         latitude <> '       ' AND
