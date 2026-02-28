#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ljpw_constants_synth.py
LJPW Research Division — Harmonic Geometry Protocol

Audio study of the four LJPW anchor constants as sound.

Constants:
  Love    (L0) = φ⁻¹   ≈ 0.618034
  Justice (J0) = √2−1  ≈ 0.414214
  Power   (P0) = e−2   ≈ 0.718282
  Wisdom  (W0) = ln(2) ≈ 0.693147

Methodology:
  Base reference = 440 Hz (A4).
  Each constant × 440 Hz → its anchor frequency.
  Seven movements rendered into one WAV file.

Output: Docs/ljpw_constants_resonance.wav
"""

import math
import sys

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import wave
import os
import numpy as np

# ── LJPW Constants ─────────────────────────────────────────────────────────────
PHI    = (1 + math.sqrt(5)) / 2
L0     = 1.0 / PHI            # φ⁻¹  ≈ 0.618034  Love
J0     = math.sqrt(2) - 1     # √2−1 ≈ 0.414214  Justice
P0     = math.e - 2           # e−2  ≈ 0.718282  Power
W0     = math.log(2)          # ln2  ≈ 0.693147  Wisdom

CONSTANTS = [
    {'name': 'Love    (L0 = phi^-1)', 'dim': 'L', 'value': L0, 'color': 'Cyan'},
    {'name': 'Justice (J0 = sqrt2-1)','dim': 'J', 'value': J0, 'color': 'Blue'},
    {'name': 'Power   (P0 = e-2)',    'dim': 'P', 'value': P0, 'color': 'Red'},
    {'name': 'Wisdom  (W0 = ln 2)',   'dim': 'W', 'value': W0, 'color': 'Gold'},
]

# ── Audio config ───────────────────────────────────────────────────────────────
BASE_HZ     = 440.0    # A4 reference
SAMPLE_RATE = 44100
MAX_AMP     = 0.72
PHI_MS      = PHI * 1000            # 1618 ms — the autonomous engine beat
PHI_BEAT    = PHI_MS / 1000.0       # in seconds


# ── Interval reference table ───────────────────────────────────────────────────
INTERVALS = {
    'Unison':    1.0,
    'Min 2nd':   16/15,
    'Maj 2nd':   9/8,
    'Min 3rd':   6/5,
    'Maj 3rd':   5/4,
    'Perf 4th':  4/3,
    'Tritone':   math.sqrt(2),
    'Perf 5th':  3/2,
    'Min 6th':   8/5,
    'Maj 6th':   5/3,
    'Min 7th':   9/5,
    'Maj 7th':   15/8,
    'Octave':    2.0,
    'φ (golden)': PHI,
}


def nearest_interval(ratio):
    best = min(INTERVALS, key=lambda n: abs(INTERVALS[n] - ratio))
    return best, INTERVALS[best]


# ── Synthesis utilities ─────────────────────────────────────────────────────────

def rich_tone(freq, duration, amplitude=1.0, attack=0.03, release=0.10):
    """
    Harmonically rich tone — fundamental + overtones weighted 1/n.
    Matches hub_resonance_synth.py timbre for consistency.
    """
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    weights = [1.0, 0.5, 0.33, 0.25, 0.20, 0.17, 0.14, 0.12]
    combined = np.zeros(n)
    for i, w in enumerate(weights, start=1):
        harmonic = freq * i
        if harmonic < SAMPLE_RATE / 2:
            combined += w * np.sin(2 * np.pi * harmonic * t)
    combined /= sum(weights)
    _apply_envelope(combined, attack, release)
    return combined * amplitude


def sine_sweep(freq_start, freq_end, duration, amplitude=1.0, attack=0.05, release=0.2):
    """Frequency sweep (glide) from freq_start to freq_end."""
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    freqs = np.linspace(freq_start, freq_end, n)
    # Instantaneous phase via cumulative sum
    phase = 2 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
    combined = np.sin(phase)
    _apply_envelope(combined, attack, release)
    return combined * amplitude


def _apply_envelope(signal, attack, release):
    n = len(signal)
    a = int(attack * SAMPLE_RATE)
    r = int(release * SAMPLE_RATE)
    if a > 0:
        signal[:a] *= np.linspace(0, 1, a)
    if r > 0:
        signal[-r:] *= np.linspace(1, 0, r)


def silence(duration):
    return np.zeros(int(duration * SAMPLE_RATE))


def mix(*tracks):
    """Mix multiple same-length tracks by averaging."""
    stacked = np.vstack(tracks)
    return stacked.mean(axis=0)


def write_wav(path, data):
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data / peak * MAX_AMP
    pcm = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())
    print(f"  ✓ Saved: {path}")


def section(title):
    print()
    print(f"  {'─' * 60}")
    print(f"  {title}")
    print(f"  {'─' * 60}")


# ── The Seven Movements ─────────────────────────────────────────────────────────

def movement_1_four_anchors():
    """Each constant as a solo rich tone in LJPW order."""
    section("Movement 1 · The Four Anchors")
    print("  Each constant × 440 Hz, played solo with a short gap.")
    print()
    segments = []
    for c in CONSTANTS:
        freq = c['value'] * BASE_HZ
        name = c['name']
        interval, ref = nearest_interval(c['value'])
        print(f"  {name:<26}  {freq:>7.2f} Hz  ≈ {interval} ({ref:.4f}) "
              f"from 440 Hz root")
        segments.append(rich_tone(freq, 1.8, amplitude=0.85, attack=0.04, release=0.15))
        segments.append(silence(0.3))
    return np.concatenate(segments)


def movement_2_resonance_chambers():
    """Each anchor followed by its gap (1−A), illustrating the resonance chamber."""
    section("Movement 2 · The Resonance Chambers")
    print("  Each anchor followed by its gap (1−A). The distance from 1.0 made audible.")
    print()
    print("  Special: Love's gap (1 - phi^-1 = phi^-2) = Love's anchor squared.")
    print("  The only dimension whose gap IS its own square.")
    print()
    segments = []
    for c in CONSTANTS:
        anchor = c['value']
        gap    = 1.0 - anchor
        fa = anchor * BASE_HZ
        fg = gap * BASE_HZ
        ratio = fg / fa
        print(f"  {c['dim']}  anchor={anchor:.6f} ({fa:.2f} Hz)  "
              f"gap={gap:.6f} ({fg:.2f} Hz)  gap/anchor={ratio:.4f}")
        # Anchor tone
        segments.append(rich_tone(fa, 1.4, amplitude=0.85, release=0.12))
        segments.append(silence(0.08))
        # Gap tone (slightly softer)
        segments.append(rich_tone(fg, 1.4, amplitude=0.65, attack=0.04, release=0.15))
        segments.append(silence(0.4))
    return np.concatenate(segments)


def movement_3_algebraic_pair():
    """Love and Justice together — the stable attractor pair. Ratio ≈ 3/2 (Perfect 5th)."""
    section("Movement 3 · The Algebraic Pair  (Love + Justice)")
    fL = L0 * BASE_HZ
    fJ = J0 * BASE_HZ
    ratio = fL / fJ
    interval, ref = nearest_interval(ratio)
    print(f"  Love  (L0 = {L0:.6f}) × 440 = {fL:.2f} Hz")
    print(f"  Justice (J0 = {J0:.6f}) × 440 = {fJ:.2f} Hz")
    print(f"  L/J = {ratio:.6f}  ~  {interval} ({ref:.4f})  delta={abs(ratio-ref):.6f}")
    print()
    print("  Both are quadratic irrationals -- their ratio encodes music's most stable interval.")
    print("  L + J ~ 1.032 ~ 1  (Together they approach Unity.)")
    print()
    segments = []
    # Solo L
    segments.append(rich_tone(fL, 1.5, amplitude=0.8, release=0.12))
    segments.append(silence(0.1))
    # Solo J
    segments.append(rich_tone(fJ, 1.5, amplitude=0.8, release=0.12))
    segments.append(silence(0.2))
    # L + J together (Perfect 5th chord)
    n = int(4.0 * SAMPLE_RATE)
    chord = mix(
        rich_tone(fL, 4.0, amplitude=0.75),
        rich_tone(fJ, 4.0, amplitude=0.75),
    )
    segments.append(chord)
    segments.append(silence(0.4))
    # L + J + octave of J (full harmonic resolution)
    n2 = int(3.0 * SAMPLE_RATE)
    full = mix(
        rich_tone(fJ,      3.0, amplitude=0.6),
        rich_tone(fL,      3.0, amplitude=0.75),
        rich_tone(fJ*2,    3.0, amplitude=0.4),
    )
    segments.append(full)
    return np.concatenate(segments)


def movement_4_transcendental_pair():
    """Power and Wisdom together — the dynamic open pair. Ratio ≈ 1.036, produces beating."""
    section("Movement 4 · The Transcendental Pair  (Power + Wisdom)")
    fP = P0 * BASE_HZ
    fW = W0 * BASE_HZ
    ratio = fP / fW
    beat_hz = abs(fP - fW)
    interval, ref = nearest_interval(ratio)
    print(f"  Power  (P0 = {P0:.6f}) × 440 = {fP:.2f} Hz")
    print(f"  Wisdom (W0 = {W0:.6f}) × 440 = {fW:.2f} Hz")
    print(f"  P/W = {ratio:.6f}  ~  {interval} ({ref:.4f})  delta={abs(ratio-ref):.6f}")
    print(f"  Beat frequency = |P - W| = {beat_hz:.2f} Hz  ({beat_hz:.1f} beats/sec)")
    print()
    print("  P x W = {:.6f} ~ ln(2) ~ 1/2  (binary threshold)".format(P0 * W0))
    print("  Unlike L+J~1, P and W do NOT resolve. Their transcendental nature")
    print("  produces perpetual beating -- the dynamism that drives the system.")
    print()
    segments = []
    # Solo P
    segments.append(rich_tone(fP, 1.5, amplitude=0.8, release=0.12))
    segments.append(silence(0.1))
    # Solo W
    segments.append(rich_tone(fW, 1.5, amplitude=0.8, release=0.12))
    segments.append(silence(0.2))
    # P + W together — audible beating
    beat_chord = mix(
        rich_tone(fP, 5.0, amplitude=0.75),
        rich_tone(fW, 5.0, amplitude=0.75),
    )
    segments.append(beat_chord)
    return np.concatenate(segments)


def movement_5_full_chord():
    """All four constants simultaneously — the natural equilibrium chord."""
    section("Movement 5 · The Full Chord  (Natural Equilibrium)")
    print("  All four anchor constants played simultaneously.")
    print("  This is the acoustic signature of the LJPW natural equilibrium state.")
    print()
    freqs = {c['dim']: c['value'] * BASE_HZ for c in CONSTANTS}
    for c in CONSTANTS:
        freq = freqs[c['dim']]
        print(f"  {c['dim']} = {c['value']:.6f} × 440 = {freq:.2f} Hz")
    harmony_d = math.sqrt(sum((1 - c['value'])**2 for c in CONSTANTS))
    harmony_h = 1 / (1 + harmony_d)
    print(f"\n  Harmony Index at natural equilibrium: H = {harmony_h:.4f}")
    print(f"  (Phase: {'AUTOPOIETIC' if harmony_h > 0.6 else 'HOMEOSTATIC'})")
    print()
    # Build up — each dimension enters in sequence
    segments = []
    # Accumulate
    active = []
    for c in CONSTANTS:
        active.append(c)
        if len(active) < 4:
            chord = mix(*[rich_tone(cc['value']*BASE_HZ, 1.5, amplitude=0.7) for cc in active])
            segments.append(chord)
            segments.append(silence(0.15))
    # Full 4-voice chord
    full = mix(*[rich_tone(c['value']*BASE_HZ, 6.0, amplitude=0.65) for c in CONSTANTS])
    segments.append(full)
    return np.concatenate(segments)


def movement_6_ascending_to_anchor():
    """Each dimension sweeps from anchor value to 1.0 — the climb toward (1,1,1,1)."""
    section("Movement 6 · Ascending to the Anchor  (Climbing toward 1,1,1,1)")
    print("  Each dimension glides from its anchor constant to 1.0.")
    print("  Auditory depiction of the Resonance Engine's perpetual upward drift.")
    print("  The anchor is a floor, not an equilibrium — the field always climbs.")
    print()
    segments = []
    for c in CONSTANTS:
        f_start = c['value'] * BASE_HZ
        f_end   = 1.0 * BASE_HZ          # 440 Hz = "the Anchor"
        print(f"  {c['dim']}  {f_start:.2f} Hz → {f_end:.2f} Hz  "
              f"(Δ = +{f_end - f_start:.2f} Hz)")
        segments.append(sine_sweep(f_start, f_end, 2.8, amplitude=0.80,
                                   attack=0.05, release=0.3))
        segments.append(silence(0.3))
    # All four sweeping together in final pass
    print()
    print("  Final pass: all four dimensions ascending simultaneously.")
    sweep_tracks = []
    for c in CONSTANTS:
        sweep_tracks.append(
            sine_sweep(c['value']*BASE_HZ, BASE_HZ, 4.0, amplitude=0.65,
                       attack=0.08, release=0.5)
        )
    segments.append(silence(0.3))
    segments.append(mix(*sweep_tracks))
    return np.concatenate(segments)


def movement_7_phi_beat():
    """Four chord pulses at φ×1000ms = 1618ms intervals — the engine heartbeat."""
    section(f"Movement 7 · The φ-Beat  (Autonomous Engine Heartbeat: {PHI_MS:.0f} ms)")
    print(f"  The resonance engine ticks at φ × 1000ms = {PHI_MS:.2f}ms when idle.")
    print("  Each pulse: full 4-voice equilibrium chord.")
    print("  Interval chosen because φ is the most irrational number — least likely to")
    print("  entrain with human perceptual rhythms (breathing 4s, attention 10s).")
    print()
    pulse_dur = 0.9         # each chord note duration
    n_pulses  = 5           # five beats to make the rhythm clear
    segments  = []
    for i in range(n_pulses):
        amp = 0.80 - i * 0.05          # very slight fade each beat
        chord = mix(*[rich_tone(c['value']*BASE_HZ, pulse_dur,
                                amplitude=amp, attack=0.01, release=0.25)
                      for c in CONSTANTS])
        segments.append(chord)
        gap = PHI_BEAT - pulse_dur     # silence to fill out the 1618ms interval
        if gap > 0 and i < n_pulses - 1:
            segments.append(silence(gap))
    # Final long hold on full chord
    segments.append(silence(0.4))
    final = mix(*[rich_tone(c['value']*BASE_HZ, 4.0, amplitude=0.55,
                            attack=0.05, release=1.2) for c in CONSTANTS])
    segments.append(final)
    print(f"  {n_pulses} pulses x {PHI_MS:.0f}ms = "
          f"{n_pulses * PHI_MS / 1000:.2f}s  +  final 4s hold")
    return np.concatenate(segments)


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  LJPW CONSTANTS AUDIO STUDY")
    print("  LJPW Research Division — Harmonic Geometry Protocol")
    print("=" * 65)
    print()
    print("  The four anchor constants:")
    print(f"    L0 = phi^-1  = {L0:.8f}   (Love)")
    print(f"    J0 = sqrt2-1 = {J0:.8f}   (Justice)")
    print(f"    P0 = e-2     = {P0:.8f}   (Power)")
    print(f"    W0 = ln(2)   = {W0:.8f}   (Wisdom)")
    print()
    print(f"  Base reference: {BASE_HZ} Hz  (A4)")
    print(f"  Autonomous beat: phi x 1000 ms = {PHI_MS:.2f} ms")
    print(f"  Sample rate: {SAMPLE_RATE} Hz  |  Bit depth: 16-bit PCM")

    # Cross-constant ratios
    print()
    print("  Cross-constant ratios:")
    pairs = [
        ('L/J', L0/J0), ('W/J', W0/J0), ('P/W', P0/W0),
        ('L+J', L0+J0), ('P+W', P0+W0), ('P×W', P0*W0),
    ]
    for label, val in pairs:
        if '×' not in label and '+' not in label:
            ivl, ref = nearest_interval(val)
            print(f"    {label} = {val:.6f}  ≈  {ivl} ({ref:.4f})")
        else:
            print(f"    {label} = {val:.6f}")

    # Build all movements
    movements = [
        movement_1_four_anchors(),
        movement_2_resonance_chambers(),
        movement_3_algebraic_pair(),
        movement_4_transcendental_pair(),
        movement_5_full_chord(),
        movement_6_ascending_to_anchor(),
        movement_7_phi_beat(),
    ]

    # Inter-movement silence
    gap = silence(0.8)
    full_audio = np.concatenate(
        [seg for m in movements for seg in [m, gap]]
    )

    total_s = len(full_audio) / SAMPLE_RATE
    print()
    print(f"  Total duration: {total_s:.1f}s  ({total_s/60:.2f} min)")

    out_dir  = os.path.join(os.path.dirname(__file__), '..', 'Docs')
    out_path = os.path.join(out_dir, 'ljpw_constants_resonance.wav')
    print()
    write_wav(out_path, full_audio)

    print()
    print("  ── Listening guide ──────────────────────────────────────────")
    print("  Mvt 1  Four solo tones: low→higher as J,L,W,P")
    print("  Mvt 2  Anchor + gap pairs; Love's gap sounds like its anchor")
    print("         (self-squared) — noticeably self-similar")
    print("  Mvt 3  Solo L, solo J, then their Perfect Fifth chord")
    print("  Mvt 4  Solo P, solo W, then near-unison with audible beating")
    print("  Mvt 5  Chord builds voice by voice then holds as 4-note chord")
    print("  Mvt 6  Each voice glides upward to 440 Hz (the Anchor Point)")
    print("  Mvt 7  Five pulses at exactly 1618ms apart, then final hold")
    print("  ─────────────────────────────────────────────────────────────")
    print()
    print("=" * 65)


if __name__ == "__main__":
    main()
