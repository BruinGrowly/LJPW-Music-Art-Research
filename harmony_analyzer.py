#!/usr/bin/env python3
"""
LJPW Harmony Analyzer
Extracts audio features and calculates Harmony Index (H) scores based on the LJPW framework.
"""

import json
import math
import statistics
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import os

# Try to import optional dependencies
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("Warning: librosa not available. Install with: pip install librosa numpy")

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False
    print("Warning: spotipy not available. Install with: pip install spotipy")


# LJPW Framework Constants
PHI = 1.618034  # Golden Ratio
EQUILIBRIUM = {
    'L': 0.618034,  # φ⁻¹ (Love equilibrium)
    'J': 0.414214,  # √2-1 (Justice equilibrium)
    'P': 0.718282,  # e-2 (Power equilibrium)
    'W': 0.693147,  # ln(2) (Wisdom equilibrium)
}

# Key signature LJPW mappings from framework
KEY_MAPPINGS = {
    0: {'name': 'C',  'L': 0.75, 'J': 0.90, 'P': 0.70, 'W': 0.65},  # Justice Key
    1: {'name': 'C#', 'L': 0.98, 'J': 0.75, 'P': 0.72, 'W': 0.85},  # THE LOVE KEY
    2: {'name': 'D',  'L': 0.85, 'J': 0.80, 'P': 0.90, 'W': 0.75},  # Power Key
    3: {'name': 'D#', 'L': 0.70, 'J': 0.75, 'P': 0.85, 'W': 0.80},
    4: {'name': 'E',  'L': 0.88, 'J': 0.82, 'P': 0.78, 'W': 0.70},
    5: {'name': 'F',  'L': 0.72, 'J': 0.85, 'P': 0.65, 'W': 0.75},
    6: {'name': 'F#', 'L': 0.85, 'J': 0.60, 'P': 0.70, 'W': 0.95},  # Wisdom Key
    7: {'name': 'G',  'L': 0.80, 'J': 0.75, 'P': 0.80, 'W': 0.70},
    8: {'name': 'G#', 'L': 0.78, 'J': 0.70, 'P': 0.75, 'W': 0.85},
    9: {'name': 'A',  'L': 0.92, 'J': 0.78, 'P': 0.80, 'W': 0.75},  # Joyful
    10: {'name': 'A#', 'L': 0.75, 'J': 0.72, 'P': 0.82, 'W': 0.78},
    11: {'name': 'B',  'L': 0.82, 'J': 0.77, 'P': 0.75, 'W': 0.80},
}

# Mode mappings (major = 1, minor = 0 in Spotify)
MODE_MODIFIERS = {
    'major': {'L': 0.15, 'J': 0.05, 'P': 0.05, 'W': 0.0},   # Major = Love
    'minor': {'L': -0.10, 'J': 0.05, 'P': -0.05, 'W': 0.10},  # Minor = Wisdom/Justice
}


@dataclass
class LJPWCoordinates:
    """LJPW dimensional coordinates for a song."""
    L: float  # Love (Melody)
    J: float  # Justice (Harmony)
    P: float  # Power (Rhythm)
    W: float  # Wisdom (Timbre)

    def calculate_harmony_index(self) -> float:
        """Calculate the Harmony Index (H) using LJPW framework formula."""
        # H = 1 / (1 + √[(1-L)² + (1-J)² + (1-P)² + (1-W)²])
        distance = math.sqrt(
            (1 - self.L)**2 +
            (1 - self.J)**2 +
            (1 - self.P)**2 +
            (1 - self.W)**2
        )
        return 1 / (1 + distance)

    def get_phase(self) -> str:
        """Determine the phase based on H and L values."""
        H = self.calculate_harmony_index()
        if H > 0.6 and self.L >= 0.7:
            return "AUTOPOIETIC"
        elif H >= 0.5:
            return "HOMEOSTATIC"
        else:
            return "ENTROPIC"

    def get_dominant_dimension(self) -> str:
        """Return the dominant LJPW dimension."""
        dims = {'L': self.L, 'J': self.J, 'P': self.P, 'W': self.W}
        return max(dims, key=dims.get)

    def to_dict(self) -> dict:
        """Convert to dictionary with H score and phase."""
        return {
            'L': round(self.L, 3),
            'J': round(self.J, 3),
            'P': round(self.P, 3),
            'W': round(self.W, 3),
            'H': round(self.calculate_harmony_index(), 3),
            'phase': self.get_phase(),
            'dominant': self.get_dominant_dimension(),
        }


@dataclass
class SongAnalysis:
    """Complete analysis of a song."""
    title: str
    artist: str
    ljpw: LJPWCoordinates
    audio_features: dict
    popularity: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'title': self.title,
            'artist': self.artist,
            'ljpw': self.ljpw.to_dict(),
            'audio_features': self.audio_features,
            'popularity': self.popularity,
        }


class LJPWHarmonyAnalyzer:
    """Analyzes songs and calculates LJPW Harmony Index."""

    def __init__(self, spotify_client_id: str = None, spotify_client_secret: str = None):
        """Initialize analyzer with optional Spotify credentials."""
        self.spotify = None

        if SPOTIFY_AVAILABLE and spotify_client_id and spotify_client_secret:
            try:
                credentials = SpotifyClientCredentials(
                    client_id=spotify_client_id,
                    client_secret=spotify_client_secret
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=credentials)
                print("✓ Spotify API initialized")
            except Exception as e:
                print(f"Warning: Could not initialize Spotify API: {e}")

        # Try to get from environment variables
        elif SPOTIFY_AVAILABLE:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            if client_id and client_secret:
                try:
                    credentials = SpotifyClientCredentials(
                        client_id=client_id,
                        client_secret=client_secret
                    )
                    self.spotify = spotipy.Spotify(client_credentials_manager=credentials)
                    print("✓ Spotify API initialized from environment variables")
                except Exception as e:
                    print(f"Warning: Could not initialize Spotify API: {e}")

    def map_spotify_features_to_ljpw(self, features: dict, track_info: dict = None) -> LJPWCoordinates:
        """
        Map Spotify audio features to LJPW dimensions.

        Spotify features:
        - valence: 0-1 (happiness/positivity)
        - energy: 0-1 (intensity)
        - danceability: 0-1
        - acousticness: 0-1
        - instrumentalness: 0-1
        - speechiness: 0-1
        - tempo: BPM
        - key: 0-11 (pitch class)
        - mode: 0 (minor) or 1 (major)
        - loudness: dB
        """

        # Get key mapping
        key = features.get('key', 0)
        if key == -1:  # Unknown key
            key = 0
        key_ljpw = KEY_MAPPINGS.get(key, KEY_MAPPINGS[0])

        # Mode adjustment
        mode = 'major' if features.get('mode', 1) == 1 else 'minor'
        mode_mod = MODE_MODIFIERS[mode]

        # LOVE (L) - Melody: memorability, emotional connection
        # Mapped from: valence (happiness), acousticness, key (C# = highest), mode (major boosts)
        L = (
            key_ljpw['L'] * 0.5 +  # Key contributes 50%
            features.get('valence', 0.5) * 0.3 +  # Valence 30%
            features.get('acousticness', 0.5) * 0.2  # Acoustic warmth 20%
        ) + mode_mod['L']
        L = max(0.0, min(1.0, L))  # Clamp to [0,1]

        # JUSTICE (J) - Harmony: balance, structure
        # Mapped from: key (C major = highest J), harmonic complexity (inverse of energy)
        # Higher speechiness reduces harmony (talking over music)
        harmonic_complexity = 1 - features.get('speechiness', 0.0)
        J = (
            key_ljpw['J'] * 0.5 +  # Key contributes 50%
            harmonic_complexity * 0.3 +  # Harmonic clarity 30%
            (1 - abs(features.get('energy', 0.5) - 0.5)) * 0.2  # Balance (not too extreme) 20%
        ) + mode_mod['J']
        J = max(0.0, min(1.0, J))

        # POWER (P) - Rhythm: energy, drive, intensity
        # Mapped from: energy, tempo, danceability, loudness
        tempo = features.get('tempo', 120)
        tempo_normalized = min(1.0, tempo / 180)  # Normalize tempo (180 BPM = max power)
        loudness = features.get('loudness', -10)
        loudness_normalized = min(1.0, (loudness + 60) / 60)  # Normalize loudness (-60 to 0 dB)

        P = (
            features.get('energy', 0.5) * 0.4 +  # Energy is primary 40%
            tempo_normalized * 0.3 +  # Tempo 30%
            features.get('danceability', 0.5) * 0.2 +  # Danceability 20%
            loudness_normalized * 0.1  # Loudness 10%
        ) + mode_mod['P']
        P = max(0.0, min(1.0, P))

        # WISDOM (W) - Timbre: information, complexity, richness
        # Mapped from: instrumentalness, acousticness (rich tones), key (F# = highest W)
        W = (
            key_ljpw['W'] * 0.4 +  # Key contributes 40%
            features.get('instrumentalness', 0.5) * 0.3 +  # Instrumental complexity 30%
            features.get('acousticness', 0.5) * 0.2 +  # Acoustic richness 20%
            (1 - features.get('speechiness', 0.0)) * 0.1  # Non-speech = more musical wisdom 10%
        ) + mode_mod['W']
        W = max(0.0, min(1.0, W))

        return LJPWCoordinates(L=L, J=J, P=P, W=W)

    def analyze_spotify_track(self, track_id: str) -> Optional[SongAnalysis]:
        """Analyze a single Spotify track by ID."""
        if not self.spotify:
            print("Error: Spotify API not initialized")
            return None

        try:
            # Get track info
            track = self.spotify.track(track_id)

            # Get audio features
            features = self.spotify.audio_features(track_id)[0]

            if not features:
                print(f"Warning: No audio features available for {track['name']}")
                return None

            # Map to LJPW
            ljpw = self.map_spotify_features_to_ljpw(features, track)

            # Create analysis
            analysis = SongAnalysis(
                title=track['name'],
                artist=', '.join([artist['name'] for artist in track['artists']]),
                ljpw=ljpw,
                audio_features=features,
                popularity=track.get('popularity', None)
            )

            return analysis

        except Exception as e:
            print(f"Error analyzing track {track_id}: {e}")
            return None

    def search_and_analyze(self, query: str, limit: int = 10) -> List[SongAnalysis]:
        """Search for songs and analyze them."""
        if not self.spotify:
            print("Error: Spotify API not initialized")
            return []

        try:
            results = self.spotify.search(q=query, type='track', limit=limit)
            analyses = []

            for track in results['tracks']['items']:
                analysis = self.analyze_spotify_track(track['id'])
                if analysis:
                    analyses.append(analysis)

            return analyses

        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def analyze_playlist(self, playlist_id: str, limit: int = 100) -> List[SongAnalysis]:
        """Analyze all tracks in a Spotify playlist."""
        if not self.spotify:
            print("Error: Spotify API not initialized")
            return []

        try:
            analyses = []
            offset = 0

            while len(analyses) < limit:
                results = self.spotify.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=min(100, limit - len(analyses))
                )

                if not results['items']:
                    break

                for item in results['items']:
                    if item['track']:
                        analysis = self.analyze_spotify_track(item['track']['id'])
                        if analysis:
                            analyses.append(analysis)

                offset += len(results['items'])

                if not results['next']:
                    break

            return analyses

        except Exception as e:
            print(f"Error analyzing playlist: {e}")
            return []

    def analyze_audio_file(self, file_path: str) -> Optional[LJPWCoordinates]:
        """Analyze an audio file using librosa (if available)."""
        if not LIBROSA_AVAILABLE:
            print("Error: librosa not installed. Install with: pip install librosa")
            return None

        try:
            # Load audio
            y, sr = librosa.load(file_path)

            # Extract features
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)
            zcr = librosa.feature.zero_crossing_rate(y)

            # Estimate key (simplified)
            chroma_mean = np.mean(chroma, axis=1)
            estimated_key = np.argmax(chroma_mean)

            # Create pseudo-Spotify features
            features = {
                'key': estimated_key,
                'mode': 1,  # Assume major (would need more complex detection)
                'tempo': tempo,
                'energy': float(np.mean(rms)),
                'valence': 0.5,  # Cannot determine from audio alone
                'danceability': min(1.0, tempo / 180),
                'acousticness': 1 - float(np.mean(spectral_centroid) / 8000),
                'instrumentalness': 0.5,  # Cannot determine easily
                'speechiness': 0.1,  # Assume mostly music
                'loudness': float(20 * np.log10(np.mean(rms) + 1e-10)),
            }

            return self.map_spotify_features_to_ljpw(features)

        except Exception as e:
            print(f"Error analyzing audio file: {e}")
            return None

    @staticmethod
    def calculate_correlations(analyses: List[SongAnalysis]) -> dict:
        """Calculate correlations between H scores and popularity."""
        if not analyses:
            return {}

        h_scores = [a.ljpw.calculate_harmony_index() for a in analyses]
        popularities = [a.popularity for a in analyses if a.popularity is not None]

        if len(popularities) < 2:
            return {'error': 'Not enough popularity data'}

        # Filter to only songs with popularity data
        h_with_pop = [
            a.ljpw.calculate_harmony_index()
            for a in analyses
            if a.popularity is not None
        ]

        # Calculate Pearson correlation
        if len(h_with_pop) >= 2:
            mean_h = statistics.mean(h_with_pop)
            mean_pop = statistics.mean(popularities)

            numerator = sum(
                (h - mean_h) * (pop - mean_pop)
                for h, pop in zip(h_with_pop, popularities)
            )

            denom_h = math.sqrt(sum((h - mean_h)**2 for h in h_with_pop))
            denom_pop = math.sqrt(sum((pop - mean_pop)**2 for pop in popularities))

            correlation = numerator / (denom_h * denom_pop) if denom_h * denom_pop != 0 else 0
        else:
            correlation = 0

        return {
            'h_vs_popularity_correlation': round(correlation, 3),
            'mean_h_score': round(statistics.mean(h_scores), 3),
            'mean_popularity': round(statistics.mean(popularities), 1) if popularities else None,
            'autopoietic_count': sum(1 for a in analyses if a.ljpw.get_phase() == 'AUTOPOIETIC'),
            'homeostatic_count': sum(1 for a in analyses if a.ljpw.get_phase() == 'HOMEOSTATIC'),
            'entropic_count': sum(1 for a in analyses if a.ljpw.get_phase() == 'ENTROPIC'),
            'total_songs': len(analyses),
        }


def main():
    """Example usage."""
    print("=" * 60)
    print("LJPW Harmony Analyzer")
    print("=" * 60)
    print()

    # Check for Spotify credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("To use Spotify API, set environment variables:")
        print("  export SPOTIFY_CLIENT_ID='your_client_id'")
        print("  export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        print()
        print("Get credentials at: https://developer.spotify.com/dashboard")
        print()
        return

    # Initialize analyzer
    analyzer = LJPWHarmonyAnalyzer(client_id, client_secret)

    # Example: Analyze specific songs
    print("Analyzing example songs...")
    print()

    # Search for some classic songs
    test_queries = [
        "Bohemian Rhapsody Queen",
        "Hallelujah Leonard Cohen",
        "Amazing Grace",
        "We Will Rock You Queen",
    ]

    all_analyses = []
    for query in test_queries:
        results = analyzer.search_and_analyze(query, limit=1)
        if results:
            all_analyses.extend(results)
            analysis = results[0]
            print(f"🎵 {analysis.title} - {analysis.artist}")
            print(f"   LJPW: L={analysis.ljpw.L:.2f} J={analysis.ljpw.J:.2f} "
                  f"P={analysis.ljpw.P:.2f} W={analysis.ljpw.W:.2f}")
            print(f"   H Score: {analysis.ljpw.calculate_harmony_index():.3f}")
            print(f"   Phase: {analysis.ljpw.get_phase()}")
            print(f"   Dominant: {analysis.ljpw.get_dominant_dimension()}")
            print(f"   Popularity: {analysis.popularity}/100")
            print()

    # Calculate correlations
    if all_analyses:
        print("\n" + "=" * 60)
        print("STATISTICAL ANALYSIS")
        print("=" * 60)
        stats = analyzer.calculate_correlations(all_analyses)
        for key, value in stats.items():
            print(f"{key}: {value}")


if __name__ == '__main__':
    main()
