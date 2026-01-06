import folium
from pathlib import Path


def make_accessibility_map(
    parks: list[dict],
    inaccessible_points: list[tuple[float, float]],
    out_path: str = "outputs/accessibility_map.html",
):
    # Center map on first park
    center_lat = parks[0]["lat"]
    center_lon = parks[0]["lon"]

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Parks → green
    for p in parks:
        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=4,
            color="green",
            fill=True,
            fill_opacity=0.7,
            popup=p.get("name") or "Park",
        ).add_to(m)

    # Inaccessible points → red
    for lat, lon in inaccessible_points:
        folium.CircleMarker(
            location=[lat, lon],
            radius=2,
            color="red",
            fill=True,
            fill_opacity=0.4,
        ).add_to(m)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    m.save(out_path)
    print(f"Saved interactive map to {out_path}")
