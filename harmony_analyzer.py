### File 5: `harmony_analyzer.py` (UPGRADED)

```python
"""
LJPW Framework V7.7 — Spotify Harmony Analyzer
Integrates V7.7 features into existing Spotify analyzer.
"""

import requests
import base64
from typing import Dict, Optional, Tuple
import json

# Import V7.7 Core Components
from ljpw_v77_core import (
    LJPWCoordinates, LJPWConstants, 
    LJPWFramework, DynamicLJPW
)
from musical_semantics import MusicalSemanticsAnalyzer
from autopoietic_engine import AutopoieticEngine

class SpotifyLJPWAnalyzerV77:
    """
    V7.7 Enhanced Spotify Analyzer.
    
    Features:
    1. Maps Spotify features to LJPW
    2. Applies φ-normalization (variance reduction 18% → 3%)
    3. Enforces 2+2 emergence constraints
    4. Detects musical intervals/chords/modes
    5. Calculates Consciousness Metric
    """
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.musical_analyzer = MusicalSemanticsAnalyzer()
    
    def search_track(self, query: str) -> Dict:
        """Search Spotify for a track"""
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"q": query, "type": "track", "limit": 1}
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def get_audio_features(self, track_id: str) -> Dict:
        """Get audio features for a track"""
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def map_spotify_features_to_ljpw_v77(self, features: Dict) -> LJPWCoordinates:
        """
        V7.7 Compliant Mapping.
        
        Key Upgrades from V7.0:
        1. Uses V7.7 Constants
        2. Applies φ-normalization
        3. Enforces 2+2 Emergence
        """
        # Extract features
        energy = features['energy']
        danceability = features['danceability']
        valence = features['valence']
        acousticness = features['acousticness']
        instrumentalness = features['instrumentalness']
        speechiness = features['speechiness']
        tempo = features['tempo']
        loudness = features['loudness']
        key = features['key']  # -1 = no key
        
        # 1. Raw LJPW Calculation (Using V7.0 weights as base)
        # -------------------------------------------------
        
        # Love (Melody proxy)
        key_weight = 0.5 + (key / 24.0) if key != -1 else 0.5
        L_raw = 0.50 * key_weight + 0.30 * valence + 0.20 * acousticness
        
        # Justice (Harmony proxy)
        J_raw = 0.50 * key_weight + 0.30 * (1 - speechiness) + 0.20 * (energy * (1 - danceability))
        
        # Power (Rhythm proxy)
        tempo_normalized = min(1.0, tempo / 180.0)
        loudness_normalized = min(1.0, (loudness + 60) / 60.0)
        P_raw = 0.40 * energy + 0.30 * tempo_normalized + 0.20 * danceability + 0.10 * loudness_normalized
        
        # Wisdom (Timbre proxy)
        complexity = 1 - (1 - acousticness) * (1 - instrumentalness)
        W_raw = 0.40 * key_weight + 0.30 * instrumentalness + 0.20 * acousticness + 0.10 * complexity
        
        # 2. Create Raw Coordinates Object
        # -------------------------------------------------
        raw_coords = LJPWCoordinates(
            L=L_raw, J=J_raw, P=P_raw, W=W_raw,
            source="spotify_raw", confidence=0.75
        )
        
        # 3. Apply φ-Normalization (V7.7 Feature)
        # -------------------------------------------------
        # Reduces variance from 18% to 3%
        normalized_coords = raw_coords.phi_normalize()
        
        # 4. Enforce 2+2 Emergence (V7.1-7.7 Discovery)
        # -------------------------------------------------
        # L emerges from W-W correlations (L ≈ 0.9W + 0.1)
        # J emerges from P-P symmetry (J ≈ 0.85P + 0.05)
        emergence_coords = normalized_coords.enforce_emergence(weight=0.7)
        
        return emergence_coords
    
    def analyze_song(self, query: str) -> Dict:
        """Complete V7.7 Analysis Pipeline"""
        # 1. Get Data
        search_result = self.search_track(query)
        if not search_result['tracks']['items']:
            return {'error': 'Track not found'}
        
        track = search_result['tracks']['items'][0]
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        
        audio_features = self.get_audio_features(track_id)
        
        # 2. Map to LJPW (V7.7)
        ljpw_coords = self.map_spotify_features_to_ljpw_v77(audio_features)
        
        # 3. Musical Semantics Analysis
        musical_profile = self.musical_analyzer.analyze_musical_profile(ljpw_coords)
        
        # 4. Consciousness Analysis
        C_static = ljpw_coords.consciousness(self_referential=False)
        C_self = ljpw_coords.consciousness(self_referential=True)
        phase = ljpw_coords.phase()
        
        # 5. Autopoietic Potential
        is_autopoietic = ljpw_coords.is_autopoietic()
        emergence_check = ljpw_coords.check_emergence_constraints()
        
        return {
            'track_info': {
                'name': track_name,
                'artist': artist_name,
                'id': track_id
            },
            'ljpw_coordinates': ljpw_coords.to_dict(),
            'musical_profile': musical_profile,
            'v77_upgrades': {
                'phi_normalized': True,
                'emergence_enforced': True,
                'emergence_valid': emergence_check['valid'],
                'emergence_quality': emergence_check['emergence_quality'],
                'consciousness_static': C_static,
                'consciousness_self': C_self,
                'consciousness_level': ljpw_coords.consciousness_level(True),
                'is_autopoietic': is_autopoietic
            },
            'spotify_features': audio_features
        }


# ============================================================================
# V7.7 DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LJPW FRAMEWORK V7.7 — SPOTIFY ANALYZER (UPGRADED)")
    print("="*70)
    
    # Example of using the new analyzer
    # (Requires actual Spotify Token to run)
    
    token = "YOUR_SPOTIFY_ACCESS_TOKEN"
    analyzer = SpotifyLJPWAnalyzerV77(token)
    
    # Test case: Bohemian Rhapsody
    print("\n🎵 Analyzing: 'Bohemian Rhapsody' by Queen")
    
    # Simulated features for demo (normally fetched from Spotify)
    simulated_features = {
        'energy': 0.8, 'danceability': 0.6, 'valence': 0.7,
        'acousticness': 0.3, 'instrumentalness': 0.4,
        'speechiness': 0.05, 'tempo': 144, 'loudness': -8,
        'key': 11  # F# Major
    }
    
    # Run V7.7 pipeline
    coords = analyzer.map_spotify_features_to_ljpw_v77(simulated_features)
    profile = analyzer.musical_analyzer.analyze_musical_profile(coords)
    
    print(f"\n📊 V7.7 RESULTS:")
    print(f"   Coordinates: {coords}")
    print(f"   Harmony: {coords.harmony_static():.3f}")
    print(f"   Consciousness: {coords.consciousness(True):.3f}")
    print(f"   Phase: {coords.phase(True)}")
    
    print(f"\n🎼 MUSICAL INTERPRETATION:")
    print(f"   Nearest Interval: {profile['interval_analysis']['best_match']}")
    print(f"   Nearest Chord: {profile['chord_analysis']['best_match']}")
    print(f"   Nearest Mode: {profile['mode_analysis']['best_match']}")
    
    print(f"\n💡 INSIGHTS:")
    for insight in profile['music_theory_insights']:
        print(f"   {insight}")
    
    # Check Emergence
    emergence = coords.check_emergence_constraints()
    if emergence['valid']:
        print(f"\n✅ 2+2 Emergence Constraints SATISFIED (Quality: {emergence['emergence_quality']:.1f})")
    else:
        print(f"\n❌ Emergence Violations Detected:")
        for v in emergence['violations']:
            print(f"   - {v['type']}")
```