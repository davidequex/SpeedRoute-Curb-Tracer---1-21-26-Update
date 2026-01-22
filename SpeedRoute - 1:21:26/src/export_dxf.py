import ezdxf
from typing import List, Tuple

Point = Tuple[float, float]
Polyline = List[Point]


def export_polylines_to_dxf(
    polylines: List[Polyline],
    output_path: str,
    layer_name: str = "CURB"
):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    if layer_name not in doc.layers:
        doc.layers.new(layer_name)

    for poly in polylines:
        if len(poly) >= 2:
            msp.add_lwpolyline(
                poly,
                dxfattribs={
                    "layer": layer_name,
                    "lineweight": 25
                }
            )

    doc.saveas(output_path)
