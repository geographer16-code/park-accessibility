import json
from pathlib import Path
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def download_parks_geojson(
    city_name: str,
    out_path: str = "data/parks.geojson",
    force: bool = False,
    timeout_s: int = 60,
):
    """
    Download all parks (leisure=park) for a city from OpenStreetMap
    and save them as a GeoJSON file.
    """

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # If file already exists and we don't force download, reuse it
    if out_file.exists() and not force:
        return out_file

    query = f"""
    [out:json][timeout:60];
    area["name"="{city_name}"]["boundary"="administrative"]->.searchArea;
    (
      way["leisure"="park"](area.searchArea);
      relation["leisure"="park"](area.searchArea);
    );
    out geom;
    """

    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=timeout_s
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        if out_file.exists():
            return out_file
        raise RuntimeError("Failed to download data from Overpass API") from e

    features = []

    for element in data.get("elements", []):
        geometry = element.get("geometry")
        if not geometry:
            continue

        coordinates = [(p["lon"], p["lat"]) for p in geometry]

        # Close polygon if needed
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        feature = {
            "type": "Feature",
            "properties": {
                "osm_id": element.get("id"),
                "name": element.get("tags", {}).get("name"),
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates],
            },
        }

        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    out_file.write_text(
        json.dumps(geojson, indent=2),
        encoding="utf-8"
    )

    return out_file
