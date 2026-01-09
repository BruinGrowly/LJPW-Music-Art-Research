### File 3: `musical_semantics.py` (NEW)

```python
"""
LJPW Framework V7.7 — Musical Semantics
Connects abstract LJPW coordinates to concrete musical structures
(Intervals, Chords, Modes).
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
from enum import Enum

# Import core classes
from ljpw_v77_core import LJPWCoordinates, LJPWConstants


# ============================================================================
# MUSICAL SEMANTICS DATA STRUCTURES
# ============================================================================

@dataclass
class IntervalSemantics:
    """LJPW coordinates for a musical interval"""
    name: str
    semitones: int
    L: float
    J: float
    P: float
    W: float
    H: float
    dominant: str
    phase: str
    
    def to_coords(self) -> LJPWCoordinates:
        return LJPWCoordinates(L=self.L, J=self.J, P=self.P, W=self.W, source="interval")


@dataclass
class ChordSemantics:
    """LJPW coordinates for a musical chord"""
    name: str
    construction: str
    L: float
    J: float
    P: float
    W: float
    H: float
    dominant: str
    phase: str
    
    def to_coords(self) -> LJPWCoordinates:
        return LJPWCoordinates(L=self.L, J=self.J, P=self.P, W=self.W, source="chord")


@dataclass
class ModeSemantics:
    """LJPW coordinates for a musical mode"""
    name: str
    intervals: str
    L: float
    J: float
    P: float
    W: float
    H: float
    dominant: str
    phase: str
    
    def to_coords(self) -> LJPWCoordinates:
        return LJPWCoordinates(L=self.L, J=self.J, P=self.P, W=self.W, source="mode")


# ============================================================================
# SEMANTIC REGISTRIES (Data from LJPW Musical Semantics Doc)
# ============================================================================

# 1. INTERVALS
# Key Insight: Major 3rd is the "Love Interval" (L=0.95)
#              Tritone is the "Devil's Interval" (Entropic)
INTERVAL_REGISTRY: Dict[str, IntervalSemantics] = {
    'P1':  IntervalSemantics('Unison', 0, 0.85, 0.95, 0.60, 0.50, 0.603, 'Justice', 'AUTOPOIETIC'),
    'm2':  IntervalSemantics('Minor 2nd', 1, 0.30, 0.20, 0.75, 0.65, 0.466, 'Power', 'ENTROPIC'),
    'M2':  IntervalSemantics('Major 2nd', 2, 0.45, 0.55, 0.70, 0.60, 0.535, 'Power', 'HOMEOSTATIC'),
    'm3':  IntervalSemantics('Minor 3rd', 3, 0.75, 0.70, 0.55, 0.65, 0.591, 'Love', 'HOMEOSTATIC'),
    'M3':  IntervalSemantics('Major 3rd', 4, 0.95, 0.75, 0.65, 0.70, 0.655, 'Love', 'AUTOPOIETIC'), # LOVE INTERVAL
    'P4':  IntervalSemantics('Perfect 4th', 5, 0.70, 0.85, 0.70, 0.75, 0.660, 'Justice', 'AUTOPOIETIC'),
    'TT':  IntervalSemantics('Tritone', 6, 0.15, 0.15, 0.85, 0.90, 0.451, 'Wisdom', 'ENTROPIC'),
    'P5':  IntervalSemantics('Perfect 5th', 7, 0.80, 0.90, 0.95, 0.80, 0.767, 'Power', 'AUTOPOIETIC'), # POWER FOUNDATION
    'm6':  IntervalSemantics('Minor 6th', 8, 0.70, 0.65, 0.60, 0.75, 0.603, 'Wisdom', 'AUTOPOIETIC'),
    'M6':  IntervalSemantics('Major 6th', 9, 0.85, 0.80, 0.55, 0.70, 0.627, 'Love', 'AUTOPOIETIC'),
    'm7':  IntervalSemantics('Minor 7th', 10, 0.50, 0.50, 0.80, 0.85, 0.571, 'Wisdom', 'HOMEOSTATIC'),
    'M7':  IntervalSemantics('Major 7th', 11, 0.40, 0.45, 0.75, 0.90, 0.538, 'Wisdom', 'HOMEOSTATIC'),
    'P8':  IntervalSemantics('Octave', 12, 0.90, 0.98, 0.75, 0.85, 0.764, 'Justice', 'AUTOPOIETIC'),
}

# 2. CHORDS
# Key Insight: Major Triad = Love Chord, Power Chord = Power Chord
CHORD_REGISTRY: Dict[str, ChordSemantics] = {
    'Maj':  ChordSemantics('Major Triad', 'Root+M3+P5', 0.90, 0.85, 0.80, 0.75, 0.731, 'Love', 'AUTOPOIETIC'),
    'Min':  ChordSemantics('Minor Triad', 'Root+m3+P5', 0.75, 0.80, 0.75, 0.80, 0.688, 'Justice', 'AUTOPOIETIC'),
    'Dim':  ChordSemantics('Diminished', 'Root+m3+TT', 0.25, 0.30, 0.85, 0.90, 0.490, 'Wisdom', 'ENTROPIC'),
    'Aug':  ChordSemantics('Augmented', 'Root+M3+m6', 0.60, 0.40, 0.80, 0.85, 0.567, 'Wisdom', 'HOMEOSTATIC'),
    'Maj7': ChordSemantics('Major 7th', 'Maj+M7', 0.85, 0.75, 0.70, 0.90, 0.699, 'Wisdom', 'AUTOPOIETIC'),
    'Min7': ChordSemantics('Minor 7th', 'min+m7', 0.70, 0.70, 0.75, 0.85, 0.660, 'Wisdom', 'AUTOPOIETIC'),
    'Dom7': ChordSemantics('Dominant 7th', 'Maj+m7', 0.75, 0.60, 0.90, 0.80, 0.657, 'Power', 'AUTOPOIETIC'),
    'Sus4': ChordSemantics('Sus4', 'Root+P4+P5', 0.65, 0.90, 0.75, 0.70, 0.652, 'Justice', 'AUTOPOIETIC'),
    'Power': ChordSemantics('Power Chord', 'Root+P5', 0.55, 0.80, 0.98, 0.50, 0.588, 'Power', 'AUTOPOIETIC'),
}

# 3. MODES
# Key Insight: Ionian = Love (Happy), Locrian = Entropic (Unstable)
MODE_REGISTRY: Dict[str, ModeSemantics] = {
    'Ionian': ModeSemantics('Ionian (Major)', 'C-D-E-F-G-A-B', 0.90, 0.85, 0.75, 0.70, 0.699, 'Love', 'AUTOPOIETIC'),
    'Dorian': ModeSemantics('Dorian', 'D-E-F-G-A-B-C', 0.75, 0.80, 0.70, 0.85, 0.683, 'Wisdom', 'AUTOPOIETIC'),
    'Phrygian': ModeSemantics('Phrygian', 'E-F-G-A-B-C-D', 0.40, 0.55, 0.85, 0.90, 0.565, 'Wisdom', 'HOMEOSTATIC'),
    'Lydian': ModeSemantics('Lydian', 'F-G-A-B-C-D-E', 0.85, 0.70, 0.60, 0.95, 0.656, 'Wisdom', 'AUTOPOIETIC'),
    'Mixolydian': ModeSemantics('Mixolydian', 'G-A-B-C-D-E-F', 0.70, 0.65, 0.90, 0.75, 0.652, 'Power', 'AUTOPOIETIC'),
    'Aeolian': ModeSemantics('Aeolian (Minor)', 'A-B-C-D-E-F-G', 0.65, 0.75, 0.65, 0.80, 0.629, 'Wisdom', 'AUTOPOIETIC'),
    'Locrian': ModeSemantics('Locrian', 'B-C-D-E-F-G-A', 0.20, 0.25, 0.80, 0.85, 0.471, 'Wisdom', 'ENTROPIC'),
}


# ============================================================================
# SEMANTIC ANALYSIS ENGINE
# ============================================================================

class MusicalSemanticsAnalyzer:
    """
    Maps LJPW coordinates to musical structures.
    
    Uses nearest-neighbor search in 4D semantic space to find
    best matching intervals, chords, and modes.
    """
    
    def __init__(self):
        # Pre-calculate coordinate arrays for fast search
        self.interval_coords = {
            k: np.array([v.L, v.J, v.P, v.W])
            for k, v in INTERVAL_REGISTRY.items()
        }
        self.chord_coords = {
            k: np.array([v.L, v.J, v.P, v.W])
            for k, v in CHORD_REGISTRY.items()
        }
        self.mode_coords = {
            k: np.array([v.L, v.J, v.P, v.W])
            for k, v in MODE_REGISTRY.items()
        }
    
    def find_nearest_interval(self, coords: LJPWCoordinates, top_n: int = 3) -> List[Tuple[str, float]]:
        """Find nearest musical interval by Euclidean distance"""
        target = coords.to_array()
        distances = {
            k: np.linalg.norm(target - v)
            for k, v in self.interval_coords.items()
        }
        sorted_items = sorted(distances.items(), key=lambda x: x[1])
        return sorted_items[:top_n]
    
    def find_nearest_chord(self, coords: LJPWCoordinates, top_n: int = 3) -> List[Tuple[str, float]]:
        """Find nearest chord"""
        target = coords.to_array()
        distances = {
            k: np.linalg.norm(target - v)
            for k, v in self.chord_coords.items()
        }
        sorted_items = sorted(distances.items(), key=lambda x: x[1])
        return sorted_items[:top_n]
    
    def find_nearest_mode(self, coords: LJPWCoordinates, top_n: int = 3) -> List[Tuple[str, float]]:
        """Find nearest mode"""
        target = coords.to_array()
        distances = {
            k: np.linalg.norm(target - v)
            for k, v in self.mode_coords.items()
        }
        sorted_items = sorted(distances.items(), key=lambda x: x[1])
        return sorted_items[:top_n]
    
    def analyze_musical_profile(self, coords: LJPWCoordinates) -> Dict:
        """
        Comprehensive musical profile analysis.
        
        Returns detailed breakdown of musical characteristics
        implied by the LJPW coordinates.
        """
        # Find nearest structures
        best_intervals = self.find_nearest_interval(coords)
        best_chords = self.find_nearest_chord(coords)
        best_modes = self.find_nearest_mode(coords)
        
        # Calculate phase and dominance
        H = coords.harmony_static()
        dominant, val = coords.dominant_dimension()
        phase = coords.phase()
        
        return {
            'coordinates': str(coords),
            'harmony': H,
            'phase': phase,
            'dominant_dimension': dominant,
            
            'interval_analysis': {
                'best_match': best_intervals[0],
                'semantic_data': INTERVAL_REGISTRY[best_intervals[0][0]]
            },
            
            'chord_analysis': {
                'best_match': best_chords[0],
                'semantic_data': CHORD_REGISTRY[best_chords[0][0]]
            },
            
            'mode_analysis': {
                'best_match': best_modes[0],
                'semantic_data': MODE_REGISTRY[best_modes[0][0]]
            },
            
            'music_theory_insights': self._generate_insights(coords, best_intervals, best_chords, best_modes)
        }
    
    def _generate_insights(self, coords: LJPWCoordinates, intervals, chords, modes) -> List[str]:
        """Generate narrative musical insights"""
        insights = []
        
        # Love-based insights
        if coords.L > 0.85:
            insights.append("🎵 HIGH LOVE: Melody is likely strong, attractive, and memorable.")
        elif coords.L < 0.4:
            insights.append("⚠️ LOW LOVE: Melody may be weak or fragmented. Connection is lost.")
        
        # Justice-based insights
        if coords.J > 0.85:
            insights.append("🎵 HIGH JUSTICE: Harmony is balanced and resolved. Consonant.")
        elif coords.J < 0.4:
            insights.append("⚠️ LOW JUSTICE: Dissonance is likely. Tension not resolved.")
        
        # Power-based insights
        if coords.P > 0.85:
            insights.append("🎵 HIGH POWER: Strong rhythmic drive. High energy.")
        elif coords.P < 0.4:
            insights.append("⚠️ LOW POWER: Rhythm is weak. Lacks momentum.")
        
        # Wisdom-based insights
        if coords.W > 0.85:
            insights.append("🎵 HIGH WISDOM: Complex timbral structure. Rich information.")
        elif coords.W < 0.4:
            insights.append("⚠️ LOW WISDOM: Timbre is simple or predictable.")
        
        # Specific Match Insights
        interval_name = intervals[0][0]
        interval_data = INTERVAL_REGISTRY[interval_name]
        
        if interval_name == 'M3':
            insights.append("❤️ MAJOR 3RD PRESENCE: The 'Love Interval' is dominant. Expect happiness/connection.")
        elif interval_name == 'TT':
            insights.append("👿 TRITONE PRESENCE: The 'Devil's Interval'. High tension, requires resolution.")
        elif interval_name == 'P5':
            insights.append("⚡ PERFECT 5TH PRESENCE: Power foundation. Stable and driving.")
        
        chord_name = chords[0][0]
        if chord_name == 'Maj':
            insights.append("🌸 MAJOR TRIAD: The 'Love Chord'. Classic, happy resolution.")
        elif chord_name == 'Power':
            insights.append("⚡ POWER CHORD: Rock/Metal vibe. Pure energy, no harmony nuance.")
        elif chord_name == 'Dim':
            insights.append("🌑 DIMINISHED CHORD: Unstable, Entropic. Needs resolution.")
        
        mode_name = modes[0][0]
        if mode_name == 'Ionian':
            insights.append("☀️ IONIAN MODE: The 'Love Mode'. Bright, major, happy.")
        elif mode_name == 'Locrian':
            insights.append("🌑 LOCRIAN MODE: The 'Entropic Mode'. Unstable, dark.")
        
        return insights


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LJPW V7.7 — MUSICAL SEMANTICS ANALYZER TEST")
    print("=" * 70)
    
    analyzer = MusicalSemanticsAnalyzer()
    
    # Test 1: A "Happy Pop Song" (High L, High J)
    print("\n1. HAPPY POP SONG PROFILE:")
    happy_pop = LJPWCoordinates(L=0.90, J=0.85, P=0.75, W=0.60, source="test")
    profile = analyzer.analyze_musical_profile(happy_pop)
    
    print(f"   Interval Match: {profile['interval_analysis']['best_match']}")
    print(f"   Chord Match: {profile['chord_analysis']['best_match']}")
    print(f"   Mode Match: {profile['mode_analysis']['best_match']}")
    print("   Insights:")
    for insight in profile['music_theory_insights']:
        print(f"     - {insight}")
    
    # Test 2: A "Heavy Metal Song" (High P, Low J, Low L)
    print("\n2. HEAVY METAL PROFILE:")
    metal_song = LJPWCoordinates(L=0.40, J=0.30, P=0.95, W=0.70, source="test")
    profile = analyzer.analyze_musical_profile(metal_song)
    
    print(f"   Interval Match: {profile['interval_analysis']['best_match']}")
    print(f"   Chord Match: {profile['chord_analysis']['best_match']}")
    print("   Insights:")
    for insight in profile['music_theory_insights']:
        print(f"     - {insight}")
    
    # Test 3: A "Jazz Standard" (High W, Mod L/J)
    print("\n3. JAZZ STANDARD PROFILE:")
    jazz_song = LJPWCoordinates(L=0.65, J=0.75, P=0.60, W=0.95, source="test")
    profile = analyzer.analyze_musical_profile(jazz_song)
    
    print(f"   Interval Match: {profile['interval_analysis']['best_match']}")
    print(f"   Chord Match: {profile['chord_analysis']['best_match']}")
    print("   Insights:")
    for insight in profile['music_theory_insights']:
        print(f"     - {insight}")
```
