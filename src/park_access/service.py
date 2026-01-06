from functools import lru_cache
from typing import Optional, Tuple, Dict, Any

from fastapi import FastAPI, Query

from park_access.downloader import download_parks_geojson
from park_access.kdtree import build_park_kdtree, nearest_park
from park_access.geo import haversine_m

import json
from pathlib import Path

app = FastAPI(title="Park Accessibility API")


def _load_parks_from_geojson(path: str) -> list[dict]:
    """
    Load parks from a GeoJSON FeatureCollection created by downloader.py.
    Returns a list of dicts with: name, lat, lon.
    """
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    parks = []

    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}
        name = props.get("name") or "Unnamed park"

        geom = feat.get("geometry", {}) or {}
        if geom.get("type") != "Polygon":
            continue

        coords = geom.get("coordinates", [])
        if not coords or not coords[0]:
            continue

        # coords[0] is the outer ring: [(lon, lat), (lon, lat), ...]
        ring = coords[0]
        lons = [pt[0] for pt in ring]
        lats = [pt[1] for pt in ring]
        if not lons or not lats:
            continue

        # simple centroid (average) good enough for assignment
        lon_c = sum(lons) / len(lons)
        lat_c = sum(lats) / len(lats)

        parks.append({"name": name, "lat": lat_c, "lon": lon_c})

    return parks


@lru_cache(maxsize=1)
def _get_index(city: str = "Amsterdam") -> Tuple[Any, list[dict]]:
    """
    Build (and cache) the KD-Tree and metadata once.
    """
    geojson_path = download_parks_geojson(city_name=city)
    parks = _load_parks_from_geojson(str(geojson_path))
    tree, meta = build_park_kdtree(parks)
    return tree, meta


@app.get("/check_accessibility")
def check_accessibility(
    lat: float = Query(..., description="Latitude, e.g. 52.36"),
    lon: float = Query(..., description="Longitude, e.g. 4.88"),
    city: str = Query("Amsterdam", description="City name used to load parks"),
    threshold_m: float = Query(500.0, description="Accessibility threshold in meters"),
) -> Dict[str, Any]:
    tree, meta = _get_index(city)

    park = nearest_park(tree, meta, lat, lon)
    if not park:
        return {"error": "No parks found for this city."}

    dist = haversine_m(lat, lon, park["lat"], park["lon"])
    return {
        "nearest_park": park.get("name"),
        "distance_m": round(dist, 2),
        "accessible": dist < threshold_m,
        "threshold_m": threshold_m,
    }
