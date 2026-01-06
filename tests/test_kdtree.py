from park_access.kdtree import build_park_kdtree, nearest_park


def test_kdtree_nearest():
    parks = [
        {"name": "A", "lat": 0.0, "lon": 0.0},
        {"name": "B", "lat": 0.0, "lon": 10.0},
        {"name": "C", "lat": 10.0, "lon": 0.0},
    ]
    tree, meta = build_park_kdtree(parks)
    p = nearest_park(tree, meta, 0.2, 0.1)
    assert p["name"] == "A"
