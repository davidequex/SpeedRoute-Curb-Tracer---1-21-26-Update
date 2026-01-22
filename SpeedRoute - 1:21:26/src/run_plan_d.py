# src/run_plan_d.py

import numpy as np
import cv2


from export_dxf import export_polylines_to_dxf

from simplify import generate_curbs_tiled




def load_mask(path: str) -> np.ndarray:
    """
    Load a binary mask image (white = mask).
    """
    mask = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Could not load mask: {path}")
    return (mask > 0).astype(np.uint8)


def main():
    # ------------------------------------------------------------------
    # INPUTS (temporary scaffolding)
    # ------------------------------------------------------------------

    road_mask = load_mask("data/road_mask.png")

    # TEMP: use road mask as curb mask until real curb mask is wired in
    curb_mask = road_mask.copy()

    # Offset from road centerline to curb (pixels for now)
    curb_offset = 15.0

    # ------------------------------------------------------------------
    # PLAN D: generate straight curb lines from road geometry
    # ------------------------------------------------------------------

    curb_lines = generate_curbs_tiled(
        road_mask=road_mask,
        curb_mask=curb_mask,
        curb_offset=15.0,
        tile_size=512,
        stride=512,
        street_band_gap=80.0
    )





    print(f"Generated {len(curb_lines)} curb lines")

    # ------------------------------------------------------------------
    # EXPORT
    # ------------------------------------------------------------------

    export_polylines_to_dxf(
        [list(line) for line in curb_lines],
        "data/planD_curbs.dxf"
    )

    print("✅ planD_curbs.dxf written")


if __name__ == "__main__":
    main()
