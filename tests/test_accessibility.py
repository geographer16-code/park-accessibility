from park_access.geo import haversine_m


def test_accessibility_threshold():
    # Same point => 0 meters => accessible
    d0 = haversine_m(52.0, 5.0, 52.0, 5.0)
    assert d0 < 500

    # ~1km north (rough) => not accessible
    d1 = haversine_m(52.0, 5.0, 52.009, 5.0)
    assert d1 > 500
