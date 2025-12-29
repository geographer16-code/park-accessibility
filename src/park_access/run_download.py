from .downloader import download_parks_geojson

if __name__ == "__main__":
    path = download_parks_geojson(city_name="Amsterdam")
    print(f"Parks saved to: {path}")
