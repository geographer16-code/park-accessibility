from typing import List, Dict, Tuple
import numpy as np
from scipy.spatial import KDTree


def build_park_kdtree(
    parks: List[Dict[str, float]]
) -> Tuple[KDTree, List[Dict[str, float]]]:
    """
    Build a KD-Tree from park latitude/longitude points.

    parks: list of dicts with keys: name, lat, lon
    returns: (KDTree, metadata list)
    """

    points = []
    metadata = []

    for park in parks:
        lat = park["lat"]
        lon = park["lon"]
        points.append([lat, lon])
        metadata.append(park)

    tree = KDTree(np.array(points))
    return tree, metadata


def nearest_park(
    tree: KDTree,
    metadata: List[Dict[str, float]],
    lat: float,
    lon: float,
) -> Dict[str, float]:
    """
    Find the nearest park to a given lat/lon.
    Returns the park dictionary.
    """

    distance, index = tree.query([lat, lon])
    return metadata[index]
