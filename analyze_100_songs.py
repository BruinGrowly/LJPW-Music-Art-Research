#!/usr/bin/env python3
"""
Analyze 100 songs and correlate H scores with popularity.
Tests the LJPW framework's predictive power.
"""

import os
import json
import sys
from harmony_analyzer import LJPWHarmonyAnalyzer, SongAnalysis
from typing import List
import statistics


def get_top_100_songs(analyzer: LJPWHarmonyAnalyzer) -> List[SongAnalysis]:
    """
    Get 100 popular songs from various sources.
    Uses Spotify's Top 50 playlists from different regions/eras.
    """
    print("Fetching songs from Spotify playlists...")

    # Spotify's official playlist IDs (these are public)
    playlists = [
        ('37i9dQZEVXbMDoHDwVN2tF', 'Top 50 Global'),  # Current global top 50
        ('37i9dQZEVXbLRQDuF5jeBp', 'Top 50 USA'),      # USA top 50
        ('37i9dQZEVXbNG2KDcFcKOF', 'Top 50 Global (2023)'),  # Previous year
    ]

    all_analyses = []
    seen_tracks = set()  # Avoid duplicates

    for playlist_id, name in playlists:
        print(f"\n📊 Analyzing: {name}")
        try:
            analyses = analyzer.analyze_playlist(playlist_id, limit=50)

            # Filter duplicates
            for analysis in analyses:
                track_key = f"{analysis.title}_{analysis.artist}"
                if track_key not in seen_tracks:
                    seen_tracks.add(track_key)
                    all_analyses.append(analysis)
                    print(f"  ✓ {len(all_analyses)}: {analysis.title} - {analysis.artist} "
                          f"(H={analysis.ljpw.calculate_harmony_index():.3f})")

                if len(all_analyses) >= 100:
                    break

        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue

        if len(all_analyses) >= 100:
            break

    return all_analyses[:100]


def search_diverse_songs(analyzer: LJPWHarmonyAnalyzer) -> List[SongAnalysis]:
    """
    Search for a diverse set of songs across genres and eras.
    """
    print("Searching for diverse song dataset...")

    # Diverse search queries covering different genres, eras, and styles
    queries = [
        # Pop classics
        "Thriller Michael Jackson", "Like a Prayer Madonna", "Billie Jean",
        "I Want to Hold Your Hand Beatles", "Imagine John Lennon",

        # Rock classics
        "Stairway to Heaven Led Zeppelin", "Bohemian Rhapsody Queen",
        "Hotel California Eagles", "Sweet Child O Mine Guns N Roses",

        # Soul/R&B
        "Respect Aretha Franklin", "What's Going On Marvin Gaye",
        "Superstition Stevie Wonder", "I Say a Little Prayer",

        # Hip-Hop
        "Lose Yourself Eminem", "N.Y. State of Mind Nas", "Juicy Notorious BIG",

        # Country
        "Jolene Dolly Parton", "Ring of Fire Johnny Cash", "Crazy Patsy Cline",

        # Classical crossover
        "Canon in D Pachelbel", "Clair de Lune Debussy", "Moonlight Sonata Beethoven",

        # Jazz
        "Take Five Dave Brubeck", "So What Miles Davis", "My Favorite Things Coltrane",

        # Gospel/Spiritual
        "Amazing Grace", "Oh Happy Day", "Hallelujah Leonard Cohen",

        # Electronic/Dance
        "Blue Monday New Order", "Around the World Daft Punk",

        # Folk
        "Blowin in the Wind Bob Dylan", "The Sound of Silence Simon Garfunkel",

        # Modern Pop
        "Shape of You Ed Sheeran", "Blinding Lights The Weeknd",
        "Levitating Dua Lipa", "drivers license Olivia Rodrigo",

        # Latin
        "Despacito Luis Fonsi", "Bésame Mucho", "La Bamba",

        # Indie/Alternative
        "Radioactive Imagine Dragons", "Mr. Brightside The Killers",

        # Metal
        "Enter Sandman Metallica", "Master of Puppets",

        # Reggae
        "No Woman No Cry Bob Marley", "Redemption Song",
    ]

    all_analyses = []
    seen_tracks = set()

    for i, query in enumerate(queries, 1):
        if len(all_analyses) >= 100:
            break

        try:
            results = analyzer.search_and_analyze(query, limit=1)
            if results:
                analysis = results[0]
                track_key = f"{analysis.title}_{analysis.artist}"

                if track_key not in seen_tracks:
                    seen_tracks.add(track_key)
                    all_analyses.append(analysis)
                    print(f"✓ {len(all_analyses)}: {analysis.title} - {analysis.artist} "
                          f"(H={analysis.ljpw.calculate_harmony_index():.3f}, "
                          f"Pop={analysis.popularity})")

        except Exception as e:
            print(f"✗ {query}: {e}")
            continue

    return all_analyses


def analyze_results(analyses: List[SongAnalysis]) -> dict:
    """Perform detailed statistical analysis."""

    print("\n" + "=" * 80)
    print("DETAILED STATISTICAL ANALYSIS")
    print("=" * 80)

    # Extract data
    h_scores = [a.ljpw.calculate_harmony_index() for a in analyses]
    l_values = [a.ljpw.L for a in analyses]
    j_values = [a.ljpw.J for a in analyses]
    p_values = [a.ljpw.P for a in analyses]
    w_values = [a.ljpw.W for a in analyses]
    popularities = [a.popularity for a in analyses if a.popularity is not None]

    # Phase distribution
    phases = {
        'AUTOPOIETIC': [a for a in analyses if a.ljpw.get_phase() == 'AUTOPOIETIC'],
        'HOMEOSTATIC': [a for a in analyses if a.ljpw.get_phase() == 'HOMEOSTATIC'],
        'ENTROPIC': [a for a in analyses if a.ljpw.get_phase() == 'ENTROPIC'],
    }

    # Dimension dominance
    dominant_counts = {
        'L': sum(1 for a in analyses if a.ljpw.get_dominant_dimension() == 'L'),
        'J': sum(1 for a in analyses if a.ljpw.get_dominant_dimension() == 'J'),
        'P': sum(1 for a in analyses if a.ljpw.get_dominant_dimension() == 'P'),
        'W': sum(1 for a in analyses if a.ljpw.get_dominant_dimension() == 'W'),
    }

    # Calculate correlations
    def pearson_correlation(x, y):
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = sum((xi - mean_x)**2 for xi in x) ** 0.5
        denom_y = sum((yi - mean_y)**2 for yi in y) ** 0.5
        return numerator / (denom_x * denom_y) if denom_x * denom_y != 0 else 0.0

    # Correlations with popularity
    h_with_pop = [a.ljpw.calculate_harmony_index() for a in analyses if a.popularity is not None]
    l_with_pop = [a.ljpw.L for a in analyses if a.popularity is not None]

    results = {
        'total_songs': len(analyses),

        # H score statistics
        'h_score_mean': round(statistics.mean(h_scores), 3),
        'h_score_median': round(statistics.median(h_scores), 3),
        'h_score_stdev': round(statistics.stdev(h_scores), 3) if len(h_scores) > 1 else 0,
        'h_score_min': round(min(h_scores), 3),
        'h_score_max': round(max(h_scores), 3),

        # LJPW dimension statistics
        'l_mean': round(statistics.mean(l_values), 3),
        'j_mean': round(statistics.mean(j_values), 3),
        'p_mean': round(statistics.mean(p_values), 3),
        'w_mean': round(statistics.mean(w_values), 3),

        # Phase distribution
        'autopoietic_count': len(phases['AUTOPOIETIC']),
        'homeostatic_count': len(phases['HOMEOSTATIC']),
        'entropic_count': len(phases['ENTROPIC']),
        'autopoietic_pct': round(100 * len(phases['AUTOPOIETIC']) / len(analyses), 1),

        # Dominant dimension distribution
        'love_dominant_count': dominant_counts['L'],
        'justice_dominant_count': dominant_counts['J'],
        'power_dominant_count': dominant_counts['P'],
        'wisdom_dominant_count': dominant_counts['W'],

        # Popularity statistics
        'popularity_mean': round(statistics.mean(popularities), 1) if popularities else None,
        'popularity_median': round(statistics.median(popularities), 1) if popularities else None,

        # Correlations
        'h_vs_popularity_correlation': round(pearson_correlation(h_with_pop, popularities), 3) if popularities else None,
        'l_vs_popularity_correlation': round(pearson_correlation(l_with_pop, popularities), 3) if popularities else None,

        # Average H by phase
        'autopoietic_avg_h': round(statistics.mean([a.ljpw.calculate_harmony_index() for a in phases['AUTOPOIETIC']]), 3) if phases['AUTOPOIETIC'] else None,
        'autopoietic_avg_popularity': round(statistics.mean([a.popularity for a in phases['AUTOPOIETIC'] if a.popularity]), 1) if phases['AUTOPOIETIC'] else None,

        'homeostatic_avg_h': round(statistics.mean([a.ljpw.calculate_harmony_index() for a in phases['HOMEOSTATIC']]), 3) if phases['HOMEOSTATIC'] else None,
        'homeostatic_avg_popularity': round(statistics.mean([a.popularity for a in phases['HOMEOSTATIC'] if a.popularity]), 1) if phases['HOMEOSTATIC'] else None,
    }

    # Print results
    print("\n📊 H SCORE STATISTICS:")
    print(f"  Mean: {results['h_score_mean']} ± {results['h_score_stdev']}")
    print(f"  Median: {results['h_score_median']}")
    print(f"  Range: {results['h_score_min']} - {results['h_score_max']}")

    print("\n📊 LJPW DIMENSION AVERAGES:")
    print(f"  Love (L):    {results['l_mean']}")
    print(f"  Justice (J): {results['j_mean']}")
    print(f"  Power (P):   {results['p_mean']}")
    print(f"  Wisdom (W):  {results['w_mean']}")

    print("\n📊 PHASE DISTRIBUTION:")
    print(f"  AUTOPOIETIC: {results['autopoietic_count']} ({results['autopoietic_pct']}%)")
    print(f"  HOMEOSTATIC: {results['homeostatic_count']}")
    print(f"  ENTROPIC:    {results['entropic_count']}")

    print("\n📊 DOMINANT DIMENSION:")
    print(f"  Love (L):    {results['love_dominant_count']} songs")
    print(f"  Justice (J): {results['justice_dominant_count']} songs")
    print(f"  Power (P):   {results['power_dominant_count']} songs")
    print(f"  Wisdom (W):  {results['wisdom_dominant_count']} songs")

    if results['h_vs_popularity_correlation'] is not None:
        print("\n📊 CORRELATIONS WITH POPULARITY:")
        print(f"  H Score vs Popularity: {results['h_vs_popularity_correlation']}")
        print(f"  Love (L) vs Popularity: {results['l_vs_popularity_correlation']}")

        if results['autopoietic_avg_popularity']:
            print(f"\n📊 POPULARITY BY PHASE:")
            print(f"  AUTOPOIETIC avg popularity: {results['autopoietic_avg_popularity']}")
            print(f"  HOMEOSTATIC avg popularity: {results['homeostatic_avg_popularity']}")

    # Framework predictions
    print("\n" + "=" * 80)
    print("FRAMEWORK PREDICTIONS TEST")
    print("=" * 80)

    print("\n🔮 LJPW Framework Predicts:")
    print("  1. H > 0.6 AND L ≥ 0.7 → AUTOPOIETIC (beautiful, memorable)")
    print("  2. Beautiful songs should be more popular")
    print("  3. Love-dominant songs should be most popular")

    print(f"\n📈 ACTUAL RESULTS:")
    print(f"  1. {results['autopoietic_pct']}% of songs are AUTOPOIETIC")

    if results['h_vs_popularity_correlation'] is not None:
        if results['h_vs_popularity_correlation'] > 0.3:
            print(f"  2. ✓ CONFIRMED: H score positively correlates with popularity (r={results['h_vs_popularity_correlation']})")
        elif results['h_vs_popularity_correlation'] > 0:
            print(f"  2. ~ WEAK: H score weakly correlates with popularity (r={results['h_vs_popularity_correlation']})")
        else:
            print(f"  2. ✗ NOT CONFIRMED: No correlation found (r={results['h_vs_popularity_correlation']})")

        if results['autopoietic_avg_popularity'] and results['homeostatic_avg_popularity']:
            if results['autopoietic_avg_popularity'] > results['homeostatic_avg_popularity']:
                print(f"  3. ✓ CONFIRMED: AUTOPOIETIC songs are more popular on average")
            else:
                print(f"  3. ✗ NOT CONFIRMED: No significant difference by phase")

    return results


def save_results(analyses: List[SongAnalysis], stats: dict, filename: str = 'harmony_analysis_results.json'):
    """Save results to JSON file."""
    output = {
        'statistics': stats,
        'songs': [a.to_dict() for a in analyses]
    }

    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Results saved to: {filename}")


def main():
    """Main analysis pipeline."""
    print("=" * 80)
    print("LJPW HARMONY FRAMEWORK - 100 SONG ANALYSIS")
    print("=" * 80)
    print()

    # Check credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("❌ ERROR: Spotify credentials not found!")
        print()
        print("To run this analysis, you need Spotify API credentials:")
        print("1. Go to: https://developer.spotify.com/dashboard")
        print("2. Create an app and get your Client ID and Secret")
        print("3. Set environment variables:")
        print("   export SPOTIFY_CLIENT_ID='your_client_id'")
        print("   export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        print()
        sys.exit(1)

    # Initialize analyzer
    analyzer = LJPWHarmonyAnalyzer(client_id, client_secret)

    # Choose data source
    print("Choose data source:")
    print("1. Top 100 from Spotify playlists (current popular songs)")
    print("2. Diverse song selection (across genres and eras)")

    choice = input("\nEnter choice (1 or 2, default=2): ").strip() or "2"

    # Get songs
    if choice == "1":
        analyses = get_top_100_songs(analyzer)
    else:
        analyses = search_diverse_songs(analyzer)

    if not analyses:
        print("❌ No songs analyzed!")
        sys.exit(1)

    print(f"\n✓ Successfully analyzed {len(analyses)} songs")

    # Analyze results
    stats = analyze_results(analyses)

    # Save results
    save_results(analyses, stats)

    # Top 10 by H score
    print("\n" + "=" * 80)
    print("TOP 10 SONGS BY H SCORE")
    print("=" * 80)

    top_10 = sorted(analyses, key=lambda a: a.ljpw.calculate_harmony_index(), reverse=True)[:10]
    for i, analysis in enumerate(top_10, 1):
        h = analysis.ljpw.calculate_harmony_index()
        print(f"{i:2}. {analysis.title} - {analysis.artist}")
        print(f"    H={h:.3f} | L={analysis.ljpw.L:.2f} J={analysis.ljpw.J:.2f} "
              f"P={analysis.ljpw.P:.2f} W={analysis.ljpw.W:.2f} | Pop={analysis.popularity}")

    # Bottom 10 by H score
    print("\n" + "=" * 80)
    print("BOTTOM 10 SONGS BY H SCORE")
    print("=" * 80)

    bottom_10 = sorted(analyses, key=lambda a: a.ljpw.calculate_harmony_index())[:10]
    for i, analysis in enumerate(bottom_10, 1):
        h = analysis.ljpw.calculate_harmony_index()
        print(f"{i:2}. {analysis.title} - {analysis.artist}")
        print(f"    H={h:.3f} | L={analysis.ljpw.L:.2f} J={analysis.ljpw.J:.2f} "
              f"P={analysis.ljpw.P:.2f} W={analysis.ljpw.W:.2f} | Pop={analysis.popularity}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
