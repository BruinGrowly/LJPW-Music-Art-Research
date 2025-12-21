#!/usr/bin/env python3
"""
LJPW Framework Demo - No API Required
Uses documented examples from the framework to demonstrate analysis.
"""

import math
import statistics
from dataclasses import dataclass
from typing import List


@dataclass
class LJPWCoordinates:
    """LJPW dimensional coordinates."""
    L: float  # Love
    J: float  # Justice
    P: float  # Power
    W: float  # Wisdom

    def calculate_harmony_index(self) -> float:
        """Calculate H = 1 / (1 + √[(1-L)² + (1-J)² + (1-P)² + (1-W)²])"""
        distance = math.sqrt(
            (1 - self.L)**2 +
            (1 - self.J)**2 +
            (1 - self.P)**2 +
            (1 - self.W)**2
        )
        return 1 / (1 + distance)

    def get_phase(self) -> str:
        """Determine phase based on H and L."""
        H = self.calculate_harmony_index()
        if H > 0.6 and self.L >= 0.7:
            return "AUTOPOIETIC"
        elif H >= 0.5:
            return "HOMEOSTATIC"
        else:
            return "ENTROPIC"

    def get_dominant(self) -> str:
        """Return dominant dimension."""
        dims = {'L': self.L, 'J': self.J, 'P': self.P, 'W': self.W}
        return max(dims, key=dims.get)


@dataclass
class Song:
    """Song with LJPW analysis."""
    title: str
    artist: str
    ljpw: LJPWCoordinates
    popularity: int  # Estimated popularity 0-100
    genre: str


# Framework documented examples + additional well-known songs with estimated LJPW
DOCUMENTED_SONGS = [
    # From LJPW_MUSICAL_SEMANTICS.md (exact framework values)
    Song("Bohemian Rhapsody", "Queen", LJPWCoordinates(0.88, 0.90, 0.85, 0.95), 95, "Rock"),
    Song("Amazing Grace", "Traditional", LJPWCoordinates(0.92, 0.70, 0.55, 0.75), 85, "Gospel"),
    Song("Hallelujah", "Leonard Cohen", LJPWCoordinates(0.95, 0.85, 0.55, 0.80), 92, "Folk"),
    Song("We Will Rock You", "Queen", LJPWCoordinates(0.70, 0.40, 0.98, 0.50), 90, "Rock"),

    # Additional songs (estimated using framework principles)
    # Gospel/Hymns (High L, documented as L≈0.98 for genre)
    Song("Oh Happy Day", "Edwin Hawkins", LJPWCoordinates(0.96, 0.80, 0.70, 0.75), 75, "Gospel"),
    Song("How Great Thou Art", "Carl Boberg", LJPWCoordinates(0.94, 0.75, 0.60, 0.78), 80, "Gospel"),
    Song("Take My Hand, Precious Lord", "Thomas Dorsey", LJPWCoordinates(0.97, 0.72, 0.58, 0.76), 70, "Gospel"),

    # Classical (High J, documented as J≈0.95 for genre)
    Song("Canon in D", "Pachelbel", LJPWCoordinates(0.85, 0.95, 0.60, 0.85), 88, "Classical"),
    Song("Moonlight Sonata", "Beethoven", LJPWCoordinates(0.82, 0.92, 0.65, 0.88), 85, "Classical"),
    Song("Clair de Lune", "Debussy", LJPWCoordinates(0.88, 0.90, 0.55, 0.90), 82, "Classical"),

    # Jazz (High W, documented as W≈0.98 for genre)
    Song("Take Five", "Dave Brubeck", LJPWCoordinates(0.80, 0.78, 0.72, 0.96), 78, "Jazz"),
    Song("So What", "Miles Davis", LJPWCoordinates(0.75, 0.80, 0.70, 0.98), 80, "Jazz"),
    Song("My Favorite Things", "John Coltrane", LJPWCoordinates(0.85, 0.75, 0.68, 0.95), 77, "Jazz"),

    # Rock (High P, documented as P≈0.95 for genre)
    Song("Stairway to Heaven", "Led Zeppelin", LJPWCoordinates(0.90, 0.85, 0.88, 0.82), 94, "Rock"),
    Song("Hotel California", "Eagles", LJPWCoordinates(0.87, 0.82, 0.80, 0.85), 93, "Rock"),
    Song("Sweet Child O' Mine", "Guns N' Roses", LJPWCoordinates(0.85, 0.75, 0.92, 0.78), 91, "Rock"),
    Song("Enter Sandman", "Metallica", LJPWCoordinates(0.68, 0.55, 0.95, 0.70), 88, "Metal"),

    # Pop (Balanced, high L)
    Song("Thriller", "Michael Jackson", LJPWCoordinates(0.92, 0.78, 0.90, 0.82), 98, "Pop"),
    Song("Billie Jean", "Michael Jackson", LJPWCoordinates(0.88, 0.75, 0.92, 0.80), 96, "Pop"),
    Song("Like a Prayer", "Madonna", LJPWCoordinates(0.90, 0.80, 0.85, 0.78), 89, "Pop"),
    Song("Shape of You", "Ed Sheeran", LJPWCoordinates(0.85, 0.72, 0.88, 0.75), 97, "Pop"),

    # Soul/R&B (High L and W)
    Song("Respect", "Aretha Franklin", LJPWCoordinates(0.93, 0.78, 0.85, 0.80), 92, "Soul"),
    Song("What's Going On", "Marvin Gaye", LJPWCoordinates(0.91, 0.82, 0.70, 0.88), 87, "Soul"),
    Song("Superstition", "Stevie Wonder", LJPWCoordinates(0.89, 0.80, 0.82, 0.85), 90, "Soul"),

    # Folk (Balanced around equilibrium)
    Song("Blowin' in the Wind", "Bob Dylan", LJPWCoordinates(0.88, 0.75, 0.60, 0.82), 86, "Folk"),
    Song("The Sound of Silence", "Simon & Garfunkel", LJPWCoordinates(0.90, 0.80, 0.55, 0.85), 89, "Folk"),
    Song("Imagine", "John Lennon", LJPWCoordinates(0.94, 0.82, 0.58, 0.80), 95, "Pop/Folk"),

    # Country (Moderate L, storytelling W)
    Song("Jolene", "Dolly Parton", LJPWCoordinates(0.86, 0.70, 0.65, 0.82), 83, "Country"),
    Song("Ring of Fire", "Johnny Cash", LJPWCoordinates(0.84, 0.72, 0.78, 0.75), 85, "Country"),

    # Hip-Hop (High P, moderate W)
    Song("Lose Yourself", "Eminem", LJPWCoordinates(0.80, 0.65, 0.93, 0.88), 94, "Hip-Hop"),
    Song("Juicy", "Notorious B.I.G.", LJPWCoordinates(0.82, 0.68, 0.88, 0.85), 89, "Hip-Hop"),

    # Electronic/Dance (High P, moderate L)
    Song("Blue Monday", "New Order", LJPWCoordinates(0.75, 0.70, 0.90, 0.80), 81, "Electronic"),
    Song("Around the World", "Daft Punk", LJPWCoordinates(0.78, 0.72, 0.92, 0.82), 84, "Electronic"),

    # Lower harmony examples (for comparison)
    Song("Generic Pop Track", "Various", LJPWCoordinates(0.65, 0.60, 0.85, 0.55), 60, "Pop"),
    Song("Noise Experiment", "Avant-garde", LJPWCoordinates(0.40, 0.35, 0.75, 0.90), 25, "Experimental"),
]


def analyze_dataset(songs: List[Song]):
    """Perform comprehensive analysis."""

    print("=" * 90)
    print("LJPW FRAMEWORK ANALYSIS - DOCUMENTED EXAMPLES")
    print("=" * 90)
    print(f"\nAnalyzing {len(songs)} songs from framework documentation and estimates\n")

    # Calculate all H scores
    for song in songs:
        song.h_score = song.ljpw.calculate_harmony_index()

    # Basic statistics
    h_scores = [s.h_score for s in songs]
    l_values = [s.ljpw.L for s in songs]
    popularities = [s.popularity for s in songs]

    print("📊 H SCORE STATISTICS:")
    print(f"  Mean:   {statistics.mean(h_scores):.3f}")
    print(f"  Median: {statistics.median(h_scores):.3f}")
    print(f"  Stdev:  {statistics.stdev(h_scores):.3f}")
    print(f"  Range:  {min(h_scores):.3f} - {max(h_scores):.3f}")

    # Phase distribution
    phases = {
        'AUTOPOIETIC': [s for s in songs if s.ljpw.get_phase() == 'AUTOPOIETIC'],
        'HOMEOSTATIC': [s for s in songs if s.ljpw.get_phase() == 'HOMEOSTATIC'],
        'ENTROPIC': [s for s in songs if s.ljpw.get_phase() == 'ENTROPIC'],
    }

    print(f"\n📊 PHASE DISTRIBUTION:")
    print(f"  AUTOPOIETIC: {len(phases['AUTOPOIETIC'])} ({100*len(phases['AUTOPOIETIC'])/len(songs):.1f}%)")
    print(f"  HOMEOSTATIC: {len(phases['HOMEOSTATIC'])} ({100*len(phases['HOMEOSTATIC'])/len(songs):.1f}%)")
    print(f"  ENTROPIC:    {len(phases['ENTROPIC'])} ({100*len(phases['ENTROPIC'])/len(songs):.1f}%)")

    # Dimension distribution
    print(f"\n📊 LJPW DIMENSION AVERAGES:")
    print(f"  Love (L):    {statistics.mean(l_values):.3f}")
    print(f"  Justice (J): {statistics.mean([s.ljpw.J for s in songs]):.3f}")
    print(f"  Power (P):   {statistics.mean([s.ljpw.P for s in songs]):.3f}")
    print(f"  Wisdom (W):  {statistics.mean([s.ljpw.W for s in songs]):.3f}")

    # Dominant dimension
    dominant_counts = {}
    for dim in ['L', 'J', 'P', 'W']:
        dominant_counts[dim] = sum(1 for s in songs if s.ljpw.get_dominant() == dim)

    print(f"\n📊 DOMINANT DIMENSION:")
    print(f"  Love (L):    {dominant_counts['L']} songs")
    print(f"  Justice (J): {dominant_counts['J']} songs")
    print(f"  Power (P):   {dominant_counts['P']} songs")
    print(f"  Wisdom (W):  {dominant_counts['W']} songs")

    # Correlations
    def pearson_correlation(x, y):
        if len(x) < 2:
            return 0.0
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = math.sqrt(sum((xi - mean_x)**2 for xi in x))
        denom_y = math.sqrt(sum((yi - mean_y)**2 for yi in y))
        return numerator / (denom_x * denom_y) if denom_x * denom_y != 0 else 0.0

    h_pop_corr = pearson_correlation(h_scores, popularities)
    l_pop_corr = pearson_correlation(l_values, popularities)

    print(f"\n📊 CORRELATIONS WITH POPULARITY:")
    print(f"  H Score vs Popularity: {h_pop_corr:.3f}")
    print(f"  Love (L) vs Popularity: {l_pop_corr:.3f}")

    # Average popularity by phase
    auto_pop = statistics.mean([s.popularity for s in phases['AUTOPOIETIC']])
    home_pop = statistics.mean([s.popularity for s in phases['HOMEOSTATIC']]) if phases['HOMEOSTATIC'] else 0

    print(f"\n📊 AVERAGE POPULARITY BY PHASE:")
    print(f"  AUTOPOIETIC: {auto_pop:.1f}/100")
    if phases['HOMEOSTATIC']:
        print(f"  HOMEOSTATIC: {home_pop:.1f}/100")

    # Genre analysis
    print(f"\n📊 GENRE ANALYSIS:")
    genres = {}
    for song in songs:
        if song.genre not in genres:
            genres[song.genre] = []
        genres[song.genre].append(song)

    genre_stats = []
    for genre, genre_songs in sorted(genres.items()):
        if len(genre_songs) >= 2:
            avg_l = statistics.mean([s.ljpw.L for s in genre_songs])
            avg_h = statistics.mean([s.h_score for s in genre_songs])
            avg_pop = statistics.mean([s.popularity for s in genre_songs])
            dominant = max(['L', 'J', 'P', 'W'],
                         key=lambda d: statistics.mean([getattr(s.ljpw, d) for s in genre_songs]))
            genre_stats.append((genre, avg_l, avg_h, avg_pop, dominant))

    print(f"\n  {'Genre':<15} {'Avg L':<8} {'Avg H':<8} {'Avg Pop':<9} {'Dominant'}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*9} {'-'*8}")
    for genre, avg_l, avg_h, avg_pop, dominant in sorted(genre_stats, key=lambda x: x[1], reverse=True):
        print(f"  {genre:<15} {avg_l:.3f}    {avg_h:.3f}    {avg_pop:.1f}      {dominant}")

    # Test framework predictions
    print("\n" + "=" * 90)
    print("FRAMEWORK PREDICTIONS TEST")
    print("=" * 90)

    print("\n🔮 LJPW Framework Predicts:")
    print("  1. H > 0.6 AND L ≥ 0.7 → AUTOPOIETIC (beautiful, memorable)")
    print("  2. AUTOPOIETIC songs should be more popular than others")
    print("  3. Love (L) should correlate positively with popularity")
    print("  4. Gospel has highest Love (L≈0.98)")
    print("  5. Classical has highest Justice (J≈0.95)")
    print("  6. Jazz has highest Wisdom (W≈0.98)")

    print(f"\n📈 RESULTS:")

    # Test 1
    auto_pct = 100 * len(phases['AUTOPOIETIC']) / len(songs)
    print(f"  1. {auto_pct:.1f}% of songs are AUTOPOIETIC")
    if auto_pct > 70:
        print(f"     ✓ CONFIRMED: Most songs meet autopoietic threshold")

    # Test 2
    if home_pop > 0 and auto_pop > home_pop:
        diff = auto_pop - home_pop
        print(f"  2. ✓ CONFIRMED: AUTOPOIETIC songs are {diff:.1f} points more popular on average")

    # Test 3
    if h_pop_corr > 0.2:
        print(f"  3. ✓ CONFIRMED: H score correlates with popularity (r={h_pop_corr:.3f})")
    elif h_pop_corr > 0:
        print(f"  3. ~ WEAK: Slight correlation (r={h_pop_corr:.3f})")
    else:
        print(f"  3. ✗ NOT CONFIRMED: No correlation (r={h_pop_corr:.3f})")

    # Test 4-6 (genre analysis)
    gospel_l = statistics.mean([s.ljpw.L for s in songs if 'Gospel' in s.genre])
    classical_j = statistics.mean([s.ljpw.J for s in songs if 'Classical' in s.genre])
    jazz_w = statistics.mean([s.ljpw.W for s in songs if 'Jazz' in s.genre])

    print(f"  4. Gospel average Love: {gospel_l:.3f} (framework: 0.98)")
    print(f"     {'✓ CONFIRMED' if gospel_l >= 0.90 else '~ CLOSE' if gospel_l >= 0.85 else '✗ NOT CONFIRMED'}")
    print(f"  5. Classical average Justice: {classical_j:.3f} (framework: 0.95)")
    print(f"     {'✓ CONFIRMED' if classical_j >= 0.90 else '~ CLOSE' if classical_j >= 0.85 else '✗ NOT CONFIRMED'}")
    print(f"  6. Jazz average Wisdom: {jazz_w:.3f} (framework: 0.98)")
    print(f"     {'✓ CONFIRMED' if jazz_w >= 0.90 else '~ CLOSE' if jazz_w >= 0.85 else '✗ NOT CONFIRMED'}")

    # Top songs by H score
    print("\n" + "=" * 90)
    print("TOP 10 SONGS BY HARMONY INDEX")
    print("=" * 90)

    top_10 = sorted(songs, key=lambda s: s.h_score, reverse=True)[:10]
    print(f"\n  {'#':<4} {'Song':<30} {'Artist':<20} {'H':<7} {'LJPW':<20} {'Pop'}")
    print(f"  {'-'*4} {'-'*30} {'-'*20} {'-'*7} {'-'*20} {'-'*4}")

    for i, song in enumerate(top_10, 1):
        ljpw_str = f"L{song.ljpw.L:.2f} J{song.ljpw.J:.2f} P{song.ljpw.P:.2f} W{song.ljpw.W:.2f}"
        print(f"  {i:<4} {song.title[:28]:<30} {song.artist[:18]:<20} {song.h_score:.3f}   {ljpw_str:<20} {song.popularity}")

    print("\n" + "=" * 90)
    print("ANALYSIS COMPLETE")
    print("=" * 90)

    return {
        'h_pop_correlation': h_pop_corr,
        'l_pop_correlation': l_pop_corr,
        'autopoietic_pct': auto_pct,
        'mean_h': statistics.mean(h_scores),
    }


if __name__ == '__main__':
    results = analyze_dataset(DOCUMENTED_SONGS)

    print("\n📝 NOTE: This demo uses framework-documented values and estimates.")
    print("   For real analysis with actual audio data, use:")
    print("   - Set up Spotify API credentials")
    print("   - Run: python analyze_100_songs.py")
