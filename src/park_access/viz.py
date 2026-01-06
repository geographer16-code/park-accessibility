from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt

from src.park_access.kdtree import build_park_kdtree, nearest_park
from src.park_access.geo import haversine_m


def load_parks_features(path: str = "data/parks.geojson"):
    geo = json.loads(Path(path).read_text(encoding="utf-8"))
    return geo["features"]


def centroid_of_polygon(coords) -> Tuple[float, float]:
    """
    coords: list of (lon, lat) tuples for outer ring (closed)
    returns (lat, lon)
    """
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]

    if len(coords) < 3:
        return (sum(ys) / len(ys), sum(xs) / len(xs))

    a = 0.0
    cx = 0.0
    cy = 0.0
    for i in range(len(coords) - 1):
        x0, y0 = coords[i]
        x1, y1 = coords[i + 1]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross

    if abs(a) < 1e-12:
        return (sum(ys) / len(ys), sum(xs) / len(xs))

    a *= 0.5
    cx /= (6.0 * a)
    cy /= (6.0 * a)
    return (cy, cx)  # lat, lon


def extract_park_centroids(parks_geojson_path: str = "data/parks.geojson") -> List[Dict]:
    """
    Returns list of dicts: {"name": str|None, "lat": float, "lon": float}
    """
    feats = load_parks_features(parks_geojson_path)
    parks = []
    for f in feats:
        geom = f.get("geometry", {})
        if geom.get("type") != "Polygon":
            continue
        coords = geom.get("coordinates", [])
        if not coords or not coords[0]:
            continue

        ring = coords[0]  # outer ring
        ring_tuples = [(pt[0], pt[1]) for pt in ring]
        lat, lon = centroid_of_polygon(ring_tuples)

        parks.append(
            {
                "name": (f.get("properties", {}) or {}).get("name") or "Unnamed park",
                "lat": float(lat),
                "lon": float(lon),
            }
        )
    return parks


def make_accessibility_bar_chart(accessible_count: int, inaccessible_count: int, out_path: str):
    total = accessible_count + inaccessible_count
    if total == 0:
        raise ValueError("No points to chart.")

    accessible_pct = 100.0 * accessible_count / total
    inaccessible_pct = 100.0 * inaccessible_count / total

    labels = ["Accessible (<500m)", "Not Accessible (>=500m)"]
    values = [accessible_pct, inaccessible_pct]

    plt.figure()
    plt.bar(labels, values)
    plt.ylabel("Percentage (%)")
    plt.title("Park Accessibility (percentage of sampled points)")
    plt.ylim(0, 100)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def generate_grid_points(min_lat, max_lat, min_lon, max_lon, step_deg=0.005):
    points = []
    lat = min_lat
    while lat <= max_lat:
        lon = min_lon
        while lon <= max_lon:
            points.append((lat, lon))
            lon += step_deg
        lat += step_deg
    return points


def main():
    parks = extract_park_centroids("data/parks.geojson")
    print(f"Loaded {len(parks)} parks (centroids)")

    tree, meta = build_park_kdtree(parks)

    # Simple bbox around Amsterdam-ish (you can improve later)
    min_lat, max_lat = 52.30, 52.42
    min_lon, max_lon = 4.75, 5.05

    points = generate_grid_points(min_lat, max_lat, min_lon, max_lon, step_deg=0.005)

    accessible = 0
    inaccessible = 0

    for lat, lon in points:
        nearest = nearest_park(tree, meta, lat, lon)
        d = haversine_m(lat, lon, nearest["lat"], nearest["lon"])
        if d < 500:
            accessible += 1
        else:
            inaccessible += 1

    print(f"Accessible points: {accessible}")
    print(f"Inaccessible points: {inaccessible}")

    make_accessibility_bar_chart(accessible, inaccessible, "outputs/accessibility_bar.png")
    print("Saved bar chart to outputs/accessibility_bar.png")


if __name__ == "__main__":
    main()
