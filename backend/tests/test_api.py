"""
Simple test script to verify the random palette generation API endpoint.
"""

import requests
import json


def test_random_palette_endpoint():
    """Test the /generate/random endpoint."""
    base_url = "http://localhost:8000"

    # Test basic random generation
    print("🧪 Testing basic random palette generation...")
    response = requests.post(f"{base_url}/generate/random", json={})

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Generated colors: {data['colors']}")
        print(f"📝 Color names: {data['names']}")
        print(f"🎨 Harmony info: {data['harmony_info']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

    # Test with specific harmony type
    print("\n🧪 Testing complementary harmony...")
    response = requests.post(
        f"{base_url}/generate/random", json={"harmony_type": "complementary"}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Complementary colors: {data['colors']}")
        print(f"🎯 Harmony confidence: {data['harmony_info']['confidence']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

    # Test with locked colors
    print("\n🧪 Testing with locked colors...")
    response = requests.post(
        f"{base_url}/generate/random",
        json={"locked_colors": ["#ff0000", "#00ff00"], "harmony_type": "triadic"},
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Palette with locked colors: {data['colors']}")
        print(f"🔒 First two colors should be red and green: {data['colors'][:2]}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    try:
        test_random_palette_endpoint()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to server. Make sure it's running on localhost:8000"
        )
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
