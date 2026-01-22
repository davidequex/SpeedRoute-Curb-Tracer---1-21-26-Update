import numpy as np
from typing import Tuple

Point = Tuple[float, float]


def distance(p: Point, q: Point) -> float:
    """Euclidean distance between two points."""
    return float(np.hypot(q[0] - p[0], q[1] - p[1]))


def angle(p_prev: Point, p: Point, p_next: Point) -> float:
    """
    Compute the angle (in degrees) at point p formed by p_prev -> p -> p_next.
    Angle is in range [0, 180].
    """
    v1 = np.array([p_prev[0] - p[0], p_prev[1] - p[1]])
    v2 = np.array([p_next[0] - p[0], p_next[1] - p[1]])

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    cos_theta = np.dot(v1, v2) / (norm1 * norm2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_theta)))

def segment_angle(a, b, c) -> float:
    """
    Angle between segment AB and BC in degrees.
    """
    import numpy as np

    v1 = np.array([b[0] - a[0], b[1] - a[1]])
    v2 = np.array([c[0] - b[0], c[1] - b[1]])

    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)

    if n1 == 0 or n2 == 0:
        return 0.0

    cos_theta = np.dot(v1, v2) / (n1 * n2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_theta)))


if __name__ == "__main__":
    a = (717.0, 141.5)
    b = (717.0, 141.0)
    c = (717.0, 140.5)

    print("Distance a→b:", distance(a, b))
    print("Distance b→c:", distance(b, c))
    print("Angle at b:", angle(a, b, c))
