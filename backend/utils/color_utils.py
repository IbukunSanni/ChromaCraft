"""
Common color utility functions used across the application.
Centralizes color format conversion and common operations.
"""

import colorsys
from typing import Tuple
from math import sqrt
from constants.color_constants import ColorConstants


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert HEX color to RGB tuple (0-255).
    
    Args:
        hex_color: Color in hex format (e.g., "#FF5733" or "FF5733")
    
    Returns:
        Tuple of RGB values (0-255)
    """
    hex_color = hex_color.lstrip("#")
    return tuple(
        int(hex_color[i:i + ColorConstants.HEX_COMPONENT_LENGTH], 16) 
        for i in (0, ColorConstants.HEX_COMPONENT_LENGTH, ColorConstants.HEX_COMPONENT_LENGTH * 2)
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values (0-255) to HEX color string.
    
    Args:
        r, g, b: RGB values (0-255)
    
    Returns:
        HEX color string (e.g., "#FF5733")
    """
    return f"#{r:0{ColorConstants.HEX_COMPONENT_LENGTH}x}{g:0{ColorConstants.HEX_COMPONENT_LENGTH}x}{b:0{ColorConstants.HEX_COMPONENT_LENGTH}x}"


def hex_to_rgb_normalized(hex_color: str) -> Tuple[float, float, float]:
    """
    Convert HEX color to normalized RGB tuple (0.0-1.0).
    
    Args:
        hex_color: Color in hex format (e.g., "#FF5733")
    
    Returns:
        Tuple of normalized RGB values (0.0-1.0)
    """
    r, g, b = hex_to_rgb(hex_color)
    return r / ColorConstants.RGB_MAX_VALUE, g / ColorConstants.RGB_MAX_VALUE, b / ColorConstants.RGB_MAX_VALUE


def rgb_normalized_to_hex(r: float, g: float, b: float) -> str:
    """
    Convert normalized RGB values (0.0-1.0) to HEX color string.
    
    Args:
        r, g, b: Normalized RGB values (0.0-1.0)
    
    Returns:
        HEX color string (e.g., "#FF5733")
    """
    return f"#{int(r * ColorConstants.RGB_MAX_VALUE):0{ColorConstants.HEX_COMPONENT_LENGTH}x}{int(g * ColorConstants.RGB_MAX_VALUE):0{ColorConstants.HEX_COMPONENT_LENGTH}x}{int(b * ColorConstants.RGB_MAX_VALUE):0{ColorConstants.HEX_COMPONENT_LENGTH}x}"


def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
    """
    Convert HEX color to HSL values.
    
    Args:
        hex_color: Color in hex format (e.g., "#FF5733")
    
    Returns:
        Tuple of HSL values: (hue, saturation, lightness) all in 0.0-1.0 range
    """
    r, g, b = hex_to_rgb_normalized(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """
    Convert HSL values to HEX color.
    
    Args:
        h: Hue (0.0-1.0)
        s: Saturation (0.0-1.0)
        l: Lightness (0.0-1.0)
    
    Returns:
        HEX color string (e.g., "#FF5733")
    """
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_normalized_to_hex(r, g, b)


def color_distance_rgb(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.
    
    Args:
        color1, color2: RGB tuples (0-255)
    
    Returns:
        Distance value (lower = more similar)
    """
    return sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))


def color_distance_hex(hex1: str, hex2: str) -> float:
    """
    Calculate Euclidean distance between two HEX colors.
    
    Args:
        hex1, hex2: HEX color strings
    
    Returns:
        Distance value (lower = more similar)
    """
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    return color_distance_rgb(rgb1, rgb2)


def normalize_hue(hue: float) -> float:
    """
    Normalize hue to 0-1 range.
    
    Args:
        hue: Hue value (can be outside 0-1 range)
    
    Returns:
        Normalized hue (0.0-1.0)
    """
    while hue < 0:
        hue += 1
    while hue >= 1:
        hue -= 1
    return hue


def adjust_hue(r: float, g: float, b: float, shift: float) -> Tuple[float, float, float]:
    """
    Adjust the hue of normalized RGB values.
    
    Args:
        r, g, b: Normalized RGB values (0.0-1.0)
        shift: Hue shift amount (-1.0 to 1.0)
    
    Returns:
        Adjusted normalized RGB values
    """
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = normalize_hue(h + shift)
    return colorsys.hls_to_rgb(h, l, s)


def adjust_saturation(r: float, g: float, b: float, factor: float) -> Tuple[float, float, float]:
    """
    Adjust the saturation of normalized RGB values.
    
    Args:
        r, g, b: Normalized RGB values (0.0-1.0)
        factor: Saturation multiplier (1.0 = no change, >1.0 = more saturated)
    
    Returns:
        Adjusted normalized RGB values
    """
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = max(0.0, min(1.0, s * factor))
    return colorsys.hls_to_rgb(h, l, s)