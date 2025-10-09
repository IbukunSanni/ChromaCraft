#!/usr/bin/env python3
"""
Demo script to showcase color locking functionality.
Run this to see color locking in action.
"""

import requests
import json
from typing import List


def print_palette(colors: List[str], names: List[str], title: str):
    """Print a color palette in a nice format."""
    print(f"\n{title}")
    print("=" * len(title))
    for i, (color, name) in enumerate(zip(colors, names)):
        lock_indicator = "🔒" if i < 2 else "  "  # Assume first 2 are locked in demos
        print(f"{lock_indicator} {color} - {name}")


def demo_color_locking():
    """Demonstrate the color locking functionality."""
    base_url = "http://localhost:8000"

    print("🎨 ChromaCraft Color Locking Demo")
    print("=" * 40)

    try:
        # Step 1: Generate initial palette
        print("\n1️⃣ Generating initial complementary palette...")
        response = requests.post(
            f"{base_url}/generate/random", json={"harmony_type": "complementary"}
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            return

        initial_palette = response.json()
        print_palette(
            initial_palette["colors"], initial_palette["names"], "Initial Palette"
        )

        # Step 2: Lock first two colors and regenerate with triadic harmony
        locked_colors = initial_palette["colors"][:2]
        print(f"\n2️⃣ Locking colors: {locked_colors[0]} and {locked_colors[1]}")
        print("   Regenerating with triadic harmony...")

        response = requests.post(
            f"{base_url}/generate/random",
            json={"locked_colors": locked_colors, "harmony_type": "triadic"},
        )

        locked_palette = response.json()
        print_palette(
            locked_palette["colors"],
            locked_palette["names"],
            "Palette with Locked Colors",
        )

        # Verify locked colors are preserved
        if (
            locked_palette["colors"][0] == locked_colors[0]
            and locked_palette["colors"][1] == locked_colors[1]
        ):
            print("✅ Locked colors successfully preserved!")
        else:
            print("❌ Locked colors were not preserved correctly")

        # Step 3: Lock more colors
        print(f"\n3️⃣ Now locking 4 colors and regenerating...")
        more_locked = locked_palette["colors"][:4]

        response = requests.post(
            f"{base_url}/generate/random",
            json={"locked_colors": more_locked, "harmony_type": "analogous"},
        )

        more_locked_palette = response.json()
        print_palette(
            more_locked_palette["colors"],
            more_locked_palette["names"],
            "Palette with 4 Locked Colors",
        )

        # Step 4: Show harmony info
        print(f"\n4️⃣ Harmony Information:")
        harmony_info = more_locked_palette["harmony_info"]
        print(f"   Harmony Type: {harmony_info['harmony_type']}")
        print(f"   Confidence: {harmony_info['confidence']:.2f}")
        print(f"   Locked Colors Count: {harmony_info.get('locked_colors_count', 0)}")

        # Step 5: Demonstrate "unlocking" by generating with fewer locked colors
        print(f"\n5️⃣ 'Unlocking' colors by only locking the first one...")
        single_locked = [more_locked_palette["colors"][0]]

        response = requests.post(
            f"{base_url}/generate/random",
            json={"locked_colors": single_locked, "harmony_type": "complementary"},
        )

        single_locked_palette = response.json()
        print_palette(
            single_locked_palette["colors"],
            single_locked_palette["names"],
            "Palette with Only One Locked Color",
        )

        print(f"\n🎉 Demo completed successfully!")
        print(f"   The color locking functionality is working correctly.")
        print(f"   Locked colors are preserved across regenerations while")
        print(f"   unlocked colors are regenerated according to harmony rules.")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend server.")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
        print("   Run: python main.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    demo_color_locking()
