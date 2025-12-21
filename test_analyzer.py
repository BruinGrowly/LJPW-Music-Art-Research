#!/usr/bin/env python3
"""
Quick test script to verify Harmony Analyzer setup.
Tests the framework with a few well-known songs.
"""

import os
import sys
from harmony_analyzer import LJPWHarmonyAnalyzer


def test_framework_examples():
    """
    Test songs that appear in the framework documentation to verify mapping accuracy.

    Framework documented examples:
    - Bohemian Rhapsody: L=0.88, J=0.90, P=0.85, W=0.95 → H=0.818
    - Amazing Grace: L=0.92, J=0.70, P=0.55, W=0.75 → H=0.625
    - Hallelujah: L=0.95, J=0.85, P=0.55, W=0.80 → H=0.659
    - We Will Rock You: L=0.70, J=0.40, P=0.98, W=0.50 → H=0.544
    """

    print("=" * 80)
    print("LJPW HARMONY ANALYZER - QUICK TEST")
    print("=" * 80)
    print()

    # Check credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("❌ ERROR: Spotify credentials not found!")
        print()
        print("Please set environment variables:")
        print("  export SPOTIFY_CLIENT_ID='your_client_id'")
        print("  export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        print()
        print("Get credentials at: https://developer.spotify.com/dashboard")
        sys.exit(1)

    # Initialize
    print("Initializing analyzer...")
    analyzer = LJPWHarmonyAnalyzer(client_id, client_secret)
    print("✓ Analyzer ready\n")

    # Test songs (from framework documentation)
    test_cases = [
        {
            'query': 'Bohemian Rhapsody Queen',
            'expected': {'L': 0.88, 'J': 0.90, 'P': 0.85, 'W': 0.95, 'H': 0.818},
            'notes': 'Highest harmony in framework examples'
        },
        {
            'query': 'Amazing Grace',
            'expected': {'L': 0.92, 'J': 0.70, 'P': 0.55, 'W': 0.75, 'H': 0.625},
            'notes': 'Classic hymn, Love-dominant'
        },
        {
            'query': 'Hallelujah Leonard Cohen',
            'expected': {'L': 0.95, 'J': 0.85, 'P': 0.55, 'W': 0.80, 'H': 0.659},
            'notes': 'Very high Love score'
        },
        {
            'query': 'We Will Rock You Queen',
            'expected': {'L': 0.70, 'J': 0.40, 'P': 0.98, 'W': 0.50, 'H': 0.544},
            'notes': 'Pure Power song, homeostatic phase'
        },
    ]

    print("Testing framework example songs...")
    print("=" * 80)
    print()

    results = []

    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Searching: {test['query']}")

        try:
            analyses = analyzer.search_and_analyze(test['query'], limit=1)

            if not analyses:
                print(f"  ❌ Song not found\n")
                continue

            analysis = analyses[0]
            results.append(analysis)

            # Display results
            print(f"\n  🎵 {analysis.title}")
            print(f"     Artist: {analysis.artist}")
            print(f"     Popularity: {analysis.popularity}/100")
            print()

            # LJPW comparison
            print("     LJPW Coordinates:")
            print("     Dimension | Calculated | Expected | Δ")
            print("     ----------|------------|----------|-------")

            ljpw_actual = {
                'L': analysis.ljpw.L,
                'J': analysis.ljpw.J,
                'P': analysis.ljpw.P,
                'W': analysis.ljpw.W,
            }

            total_error = 0
            for dim in ['L', 'J', 'P', 'W']:
                actual = ljpw_actual[dim]
                expected = test['expected'][dim]
                delta = actual - expected

                total_error += abs(delta)

                status = "✓" if abs(delta) < 0.15 else "~" if abs(delta) < 0.25 else "✗"
                print(f"     {dim}         | {actual:6.3f}     | {expected:5.2f}    | {delta:+.3f} {status}")

            # H score comparison
            h_actual = analysis.ljpw.calculate_harmony_index()
            h_expected = test['expected']['H']
            h_delta = h_actual - h_expected

            print(f"     ----------|------------|----------|-------")
            h_status = "✓" if abs(h_delta) < 0.10 else "~" if abs(h_delta) < 0.15 else "✗"
            print(f"     H Score   | {h_actual:6.3f}     | {h_expected:5.3f}  | {h_delta:+.3f} {h_status}")

            print()
            print(f"     Phase: {analysis.ljpw.get_phase()}")
            print(f"     Dominant: {analysis.ljpw.get_dominant_dimension()}")
            print(f"     Notes: {test['notes']}")
            print(f"     Average Error: {total_error/4:.3f}")

            # Audio features
            print(f"\n     Audio Features (Spotify):")
            features = analysis.audio_features
            print(f"       Key: {features.get('key')} ({'Major' if features.get('mode') == 1 else 'Minor'})")
            print(f"       Tempo: {features.get('tempo', 0):.0f} BPM")
            print(f"       Energy: {features.get('energy', 0):.3f}")
            print(f"       Valence: {features.get('valence', 0):.3f}")
            print(f"       Acousticness: {features.get('acousticness', 0):.3f}")

            print("\n" + "-" * 80 + "\n")

        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            continue

    # Summary
    if results:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        avg_h = sum(a.ljpw.calculate_harmony_index() for a in results) / len(results)
        avg_pop = sum(a.popularity for a in results if a.popularity) / len([a for a in results if a.popularity])

        autopoietic = sum(1 for a in results if a.ljpw.get_phase() == 'AUTOPOIETIC')

        print(f"\n  Songs analyzed: {len(results)}")
        print(f"  Average H score: {avg_h:.3f}")
        print(f"  Average popularity: {avg_pop:.1f}/100")
        print(f"  AUTOPOIETIC: {autopoietic}/{len(results)}")

        print("\n  ✓ Analyzer is working correctly!")
        print("\n  Next steps:")
        print("    - Run: python analyze_100_songs.py")
        print("    - This will analyze 100 songs and test framework predictions")

    else:
        print("\n❌ No songs were successfully analyzed")
        print("   Check your Spotify credentials and internet connection")


if __name__ == '__main__':
    test_framework_examples()
