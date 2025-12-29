from Amsterdam_park_accessibility.data_processing import get_ams_data

def main():
    # Load or download AMS datasets
    ams_boundary, parks_ams, buildings_ams, walking_edges_ams = get_ams_data()

    # -------------------------------
    # Your accessibility analysis here
    # -------------------------------
    print("Running accessibility analysis...")
    # Example:
    # run_accessibility(buildings_ams, parks_ams, walking_edges_ams)

if __name__ == "__main__":
    main()