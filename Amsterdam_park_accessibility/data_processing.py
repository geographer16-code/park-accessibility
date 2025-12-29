import requests
import geopandas as gpd
from shapely.geometry import shape

class AmsterdamBoundary:
    """
    A class to download and process Amsterdam Municipality Boundary from WFS data.
    """

    def __init__(self):
        self.url = 'https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0?'
        self.params = {
            'request': 'GetFeature',
            'service': 'WFS',
            'version': '2.0.0',
            'typeNames': 'bg:Gemeentegebied',
            'outputFormat': 'application/json'
        }
        self.gemeente_gdf = None
        self.ams_boundary = None

    def download_data(self):
        """Download WFS data and return as JSON."""
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            print("Data download successful")
            return response.json()
        else:
            raise Exception(f"Failed to download data. Status code: {response.status_code}")

    def to_geodataframe(self, data_json):
        """Convert GeoJSON to GeoDataFrame."""
        features = data_json['features']
        geoms = [shape(f['geometry']) for f in features]
        properties = [f['properties'] for f in features]

        self.gemeente_gdf = gpd.GeoDataFrame(properties, geometry=geoms, crs="EPSG:28992")
        self.gemeente_gdf = self.gemeente_gdf.to_crs(epsg=4326)
        return self.gemeente_gdf

    def filter_amsterdam(self):
        """Filter GeoDataFrame for Amsterdam boundary."""
        if self.gemeente_gdf is None:
            raise Exception("GeoDataFrame is empty. Run to_geodataframe() first.")
        self.ams_boundary = self.gemeente_gdf[self.gemeente_gdf['naam'] == 'Amsterdam']
        return self.ams_boundary
