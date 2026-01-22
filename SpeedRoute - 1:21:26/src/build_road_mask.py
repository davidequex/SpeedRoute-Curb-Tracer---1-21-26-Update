# src/build_road_mask.py

import cv2
import numpy as np


def build_road_mask(image_path: str, output_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Roads tend to be mid-intensity, low texture
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # Adaptive threshold for lighting variation
    road_mask = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        5
    )

    # Clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    road_mask = cv2.morphologyEx(road_mask, cv2.MORPH_CLOSE, kernel)
    road_mask = cv2.morphologyEx(road_mask, cv2.MORPH_OPEN, kernel)

    cv2.imwrite(output_path, road_mask)


if __name__ == "__main__":
    build_road_mask(
        "data/input_satellite.png",
        "data/road_mask.png"
    )

    print("✅ road_mask.png written")
