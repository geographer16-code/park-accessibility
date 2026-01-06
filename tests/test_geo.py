from park_access.geo import haversine_m


def test_haversine_known_distance():
    lat1, lon1 = 52.3791, 4.9003  # Amsterdam Centraal
    lat2, lon2 = 52.3731, 4.8922  # Dam Square

    distance = haversine_m(lat1, lon1, lat2, lon2)

    assert 600 < distance < 900
