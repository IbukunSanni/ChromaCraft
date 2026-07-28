from utils.color_utils import hex_to_rgb, color_distance_rgb
from typing import Dict


def find_closest_color_name(target_hex: str, xkcd_dict: Dict[str, str]) -> str:
    """
    Find the closest color name from XKCD color dictionary.
    
    Args:
        target_hex: Target color in hex format (e.g., "#FF5733")
        xkcd_dict: Dictionary of color names to hex values
    
    Returns:
        Closest color name string
    """
    target_rgb = hex_to_rgb(target_hex)
    closest_name = None
    min_dist = float("inf")

    for name, hex_value in xkcd_dict.items():
        color_rgb = hex_to_rgb(hex_value)
        dist = color_distance_rgb(target_rgb, color_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_name = name

    return closest_name
