import ezdxf
from typing import List, Tuple

Point = Tuple[float, float]
Polyline = List[Point]


def load_curbs_from_dxf(path: str, layer_name: str = "CURB") -> List[Polyline]:
    """
    Load curb polylines from a DXF file.

    Returns:
        List of polylines, where each polyline is a list of (x, y) points.
    """
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    polylines: List[Polyline] = []

    for entity in msp:
        if entity.dxftype() != "LWPOLYLINE":
            continue

        if entity.dxf.layer != layer_name:
            continue

        points = [(p[0], p[1]) for p in entity.get_points()]
        if len(points) >= 2:
            polylines.append(points)

    return polylines


if __name__ == "__main__":
    polylines = load_curbs_from_dxf("data/input.dxf")

    print(f"Loaded {len(polylines)} curb polylines")

    if polylines:
        print(f"First polyline has {len(polylines[0])} points")
        print("First 5 points:", polylines[0][:5])
        lengths = [len(p) for p in polylines]
        print("Min points:", min(lengths))
        print("Max points:", max(lengths))
        print("Average points:", sum(lengths) / len(lengths))
