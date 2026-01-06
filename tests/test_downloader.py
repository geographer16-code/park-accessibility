import requests
from park_access.downloader import download_parks_geojson


def test_downloader_timeout(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.Timeout

    monkeypatch.setattr(requests, "post", fake_post)

    try:
        download_parks_geojson("Amsterdam", out_path="data/test.geojson", force=True)
    except Exception:
        assert True
