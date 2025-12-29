from Amsterdam_park_accessibility.data_processing import get_ams_data
from Amsterdam_park_accessibility.analysis import ParkAccessibility
import os

def main():
    # -------------------------------
    # Config
    # -------------------------------
    TARGET_CRS = "EPSG:28992"
    MAX_DISTANCE = 1500  # meters

    # -------------------------------
    # Load or download AMS datasets
    # -------------------------------
    ams_boundary, parks_ams, buildings_ams, walking_edges_ams = get_ams_data()

    # -------------------------------
    # Initialize model
    # -------------------------------
    access_model = ParkAccessibility(
        place_name="Amsterdam, Netherlands",
        target_crs=TARGET_CRS
    )

    # -------------------------------
    # Generate centroids and snap to graph
    # -------------------------------
    buildings_pts, park_nodes = access_model.generate_building_centroids_and_snap(
        buildings_ams,
        parks_ams
    )

    # -------------------------------
    # Compute accessibility
    # -------------------------------
    accessibility_gdf = access_model.compute_accessibility(
        building_centroids_gdf=buildings_pts,
        park_nodes=park_nodes,
        max_distance=MAX_DISTANCE
    )

    # -------------------------------
    # Save output
    # -------------------------------
    os.makedirs("outputs", exist_ok=True)
    accessibility_gdf.to_file(
        "outputs/buildings_park_access_1500m.gpkg",
        driver="GPKG"
    )

    print("✅ Accessibility analysis complete")
    print(accessibility_gdf[f"park_access_{MAX_DISTANCE}m"].value_counts())

if __name__ == "__main__":
    main()
