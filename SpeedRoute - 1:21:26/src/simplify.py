import numpy as np
from typing import List, Tuple

Point = Tuple[float, float]
Line = Tuple[Point, Point]


# -------------------------------------------------
# Geometry helpers
# -------------------------------------------------

def snap_angle(angle_rad: float, allowed_rad: List[float]) -> float:
    """
    Snap angle to nearest allowed angle (radians).
    Uses sine distance to handle wraparound.
    """
    best = None
    best_err = float("inf")

    for a in allowed_rad:
        err = abs(np.sin(angle_rad - a))
        if err < best_err:
            best_err = err
            best = a

    return best


def fit_line_pca(points: np.ndarray) -> Line:
    """
    Fit a line to points using PCA and return endpoints.
    """
    mean = points.mean(axis=0)
    centered = points - mean

    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    direction = eigvecs[:, np.argmax(eigvals)]

    proj = centered @ direction
    p1 = mean + direction * proj.min()
    p2 = mean + direction * proj.max()

    return (float(p1[0]), float(p1[1])), (float(p2[0]), float(p2[1]))


# -------------------------------------------------
# Global grid estimation
# -------------------------------------------------

def estimate_global_grid_angle(road_mask: np.ndarray) -> float | None:
    """
    Estimate dominant global road orientation using PCA
    over all road pixels.
    """
    ys, xs = np.nonzero(road_mask)
    if len(xs) < 1000:
        return None

    pts = np.column_stack([xs, ys]).astype(np.float32)
    pts -= pts.mean(axis=0)

    cov = np.cov(pts.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    dominant = eigvecs[:, np.argmax(eigvals)]

    return float(np.arctan2(dominant[1], dominant[0]))


def global_grid_axes(angle_rad: float) -> List[float]:
    """
    Return two orthogonal grid angles (radians).
    """
    a = angle_rad % np.pi
    return [a, (a + np.pi / 2) % np.pi]


# -------------------------------------------------
# Tile orientation
# -------------------------------------------------

def estimate_tile_orientation(edge_pts: np.ndarray) -> float | None:
    """
    Estimate dominant orientation inside a tile using PCA.
    """
    if len(edge_pts) < 50:
        return None

    pts = edge_pts.astype(np.float32)
    pts -= pts.mean(axis=0)

    cov = np.cov(pts.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    dominant = eigvecs[:, np.argmax(eigvals)]

    return float(np.arctan2(dominant[1], dominant[0]))


# -------------------------------------------------
# Core curb generation (Plan D+++)
# -------------------------------------------------

def generate_curbs_from_road_multi(
    road_mask: np.ndarray,
    curb_mask: np.ndarray,
    curb_offset: float,
    allowed_rad: List[float],
    street_band_gap: float = 80.0
) -> List[Line]:
    """
    Generate curb lines inside one tile using
    snapped global grid orientation.
    """

    ys, xs = np.nonzero(road_mask)
    if len(xs) < 100:
        return []

    edge_pts = np.column_stack([xs, ys])

    tile_angle = estimate_tile_orientation(edge_pts)
    if tile_angle is None:
        return []

    tile_angle = snap_angle(tile_angle, allowed_rad)

    # normal + tangent
    t = np.array([np.cos(tile_angle), np.sin(tile_angle)])
    n = np.array([-t[1], t[0]])

    # project points onto normal to find street bands
    proj = edge_pts @ n
    proj_sorted = np.sort(proj)

    bands = []
    current = [proj_sorted[0]]

    for v in proj_sorted[1:]:
        if abs(v - current[-1]) < street_band_gap:
            current.append(v)
        else:
            bands.append(current)
            current = [v]
    bands.append(current)

    lines: List[Line] = []

    for band in bands:
        center = np.mean(band)

        for side in (-1, 1):
            offset = center + side * curb_offset
            mask = np.abs((edge_pts @ n) - offset) < curb_offset

            pts = edge_pts[mask]
            if len(pts) < 10:
                continue

            line = fit_line_pca(pts)
            lines.append(line)

    return lines


# -------------------------------------------------
# Tiled wrapper (Plan D+++++)
# -------------------------------------------------

def generate_curbs_tiled(
    road_mask: np.ndarray,
    curb_mask: np.ndarray,
    curb_offset: float,
    tile_size: int = 512,
    stride: int = 512,
    min_road_pixels: int = 1500,
    street_band_gap: float = 80.0
) -> List[Line]:
    """
    Run curb extraction tile-by-tile using
    a globally locked grid orientation.
    """

    global_angle = estimate_global_grid_angle(road_mask)
    if global_angle is None:
        return []

    grid_angles = global_grid_axes(global_angle)

    H, W = road_mask.shape
    results: List[Line] = []

    for y0 in range(0, H, stride):
        for x0 in range(0, W, stride):
            y1 = min(y0 + tile_size, H)
            x1 = min(x0 + tile_size, W)

            road_tile = road_mask[y0:y1, x0:x1]
            curb_tile = curb_mask[y0:y1, x0:x1]

            if int((road_tile > 0).sum()) < min_road_pixels:
                continue

            tile_lines = generate_curbs_from_road_multi(
                road_mask=road_tile,
                curb_mask=curb_tile,
                curb_offset=curb_offset,
                allowed_rad=grid_angles,
                street_band_gap=street_band_gap
            )

            for (p1, p2) in tile_lines:
                gp1 = (p1[0] + x0, p1[1] + y0)
                gp2 = (p2[0] + x0, p2[1] + y0)
                results.append((gp1, gp2))

    return results
