#!/usr/bin/env python3
"""
visualize_hub_constellation.py
LJPW Research Division — Harmonic Geometry Protocol

Visualizes the AlphaHub triplet and candidate Hubs in the Gaussian Plane.
Saves to docs/hub_constellation.png

The visualization reveals the "resonant corridor" — the angular band in ℤ[i]
where 8-fold locked primes cluster, pointing toward φ.
"""

import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

PHI = (1 + math.sqrt(5)) / 2

# ── The AlphaHub Triplet (from research document) ──────────────
TRIPLET = [
    {
        'p': 100_003_829,
        'a': 8302, 'b': 5575,
        'label': 'AlphaHub\n100,003,829',
        'color': '#ff6b6b',
        'size': 220,
        'is_alpha': True,
    },
    {
        'p': 100_011_029,
        'a': 8270, 'b': 5623,
        'label': '100,011,029\n(Hub 2)',
        'color': '#ffd93d',
        'size': 160,
        'is_alpha': False,
    },
    {
        'p': 100_017_761,
        'a': 8356, 'b': 5495,
        'label': '100,017,761\n(Hub 3)',
        'color': '#4ecdc4',
        'size': 160,
        'is_alpha': False,
    },
]

# Compute phases and ratios
for hub in TRIPLET:
    hub['phase'] = math.degrees(math.atan2(hub['b'], hub['a']))
    hub['ratio'] = hub['a'] / hub['b']
    hub['r'] = math.sqrt(hub['p'])  # radial distance = sqrt(p)

# ── φ Reference line ───────────────────────────────────────────
PHI_ANGLE = math.degrees(math.atan(1 / PHI))  # atan(b/a) where a/b = φ → b/a = 1/φ
# If a/b → φ, then angle from x-axis = atan(b/a) = atan(1/φ) ≈ 31.72°


def draw_constellation():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor('#0d1117')

    # ── LEFT: Full Gaussian plane view ─────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor('#0d1117')
    ax1.set_title('Hub Constellation in Gaussian Plane\n(a + bi where p = a² + b²)',
                  color='white', fontsize=13, pad=12)

    # Draw φ-angle reference line
    max_r = max(hub['a'] for hub in TRIPLET) * 1.05
    phi_x = max_r
    phi_y = phi_x / PHI
    ax1.plot([0, phi_x], [0, phi_y], '--',
             color='#6c5ce7', alpha=0.5, linewidth=1.5,
             label=f'φ-line (a/b = φ, angle ≈ {PHI_ANGLE:.1f}°)')

    # Draw resonant corridor (31° – 36°)
    corridor_lo = math.radians(31)
    corridor_hi = math.radians(36)
    theta_fill = np.linspace(corridor_lo, corridor_hi, 50)
    fill_r = max_r * 1.02
    ax1.fill_between(
        fill_r * np.cos(theta_fill),
        np.zeros(50),
        fill_r * np.sin(theta_fill),
        alpha=0.12, color='#ff6b6b',
        label='Resonant Corridor (31°–36°)'
    )
    # Corridor boundary lines
    for angle_deg, style in [(31, ':'), (36, ':')]:
        angle_rad = math.radians(angle_deg)
        ax1.plot([0, fill_r * math.cos(angle_rad)],
                 [0, fill_r * math.sin(angle_rad)],
                 style, color='#ff6b6b', alpha=0.4, linewidth=1)

    # Plot each hub
    for hub in TRIPLET:
        a, b = hub['a'], hub['b']
        ax1.scatter(a, b,
                   s=hub['size'],
                   c=hub['color'],
                   edgecolors='white',
                   linewidths=1.5,
                   zorder=5)
        # Phase angle arc
        arc_r = 1200
        arc_angle = math.radians(hub['phase'])
        ax1.annotate('',
                     xy=(a, b),
                     xytext=(a + 300, b - 200),
                     arrowprops=dict(arrowstyle='->', color=hub['color'], lw=1.2))
        # Label
        offset_x = 150 if hub['is_alpha'] else 120
        offset_y = 150 if hub['is_alpha'] else -300
        ax1.annotate(
            hub['label'] + f"\nphase: {hub['phase']:.2f}°\na/b: {hub['ratio']:.3f}",
            xy=(a, b),
            xytext=(a + offset_x, b + offset_y),
            color=hub['color'],
            fontsize=8,
            ha='left',
            va='center',
        )

    # Axes styling
    ax1.set_xlim(7800, 8700)
    ax1.set_ylim(5200, 6000)
    ax1.set_xlabel('Re(z) = a', color='#aaa')
    ax1.set_ylabel('Im(z) = b', color='#aaa')
    ax1.tick_params(colors='#888')
    ax1.spines['bottom'].set_color('#444')
    ax1.spines['left'].set_color('#444')
    ax1.spines['top'].set_color('#222')
    ax1.spines['right'].set_color('#222')
    ax1.grid(True, alpha=0.15, color='#444')
    ax1.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#444',
               labelcolor='white', fontsize=8)

    # ── RIGHT: Phase angle comparison ─────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#0d1117')
    ax2.set_title('Phase Angles & φ-Distance\nHub Triplet Comparison',
                  color='white', fontsize=13, pad=12)

    phases = [hub['phase'] for hub in TRIPLET]
    ratios = [hub['ratio'] for hub in TRIPLET]
    colors = [hub['color'] for hub in TRIPLET]
    labels = [f"p={hub['p']:,}\na/b={hub['ratio']:.3f}\nΔφ={abs(hub['ratio']-PHI):.3f}"
              for hub in TRIPLET]
    x_pos = np.arange(len(TRIPLET))

    # Phase bar chart
    bars = ax2.bar(x_pos, phases, color=colors, alpha=0.85,
                   edgecolor='white', linewidth=0.8, width=0.45)

    # φ-angle reference line
    ax2.axhline(y=PHI_ANGLE, color='#6c5ce7', linestyle='--', linewidth=1.5, alpha=0.8,
                label=f'φ-angle ({PHI_ANGLE:.1f}°)')

    # Resonant corridor
    ax2.axhspan(31, 36, alpha=0.15, color='#ff6b6b', label='Resonant Corridor (31°–36°)')

    # Labels on bars
    for i, (bar, hub) in enumerate(zip(bars, TRIPLET)):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1,
                 f"{hub['phase']:.2f}°",
                 ha='center', va='bottom',
                 color='white', fontsize=9)
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() / 2,
                 labels[i],
                 ha='center', va='center',
                 color='#111', fontsize=7.5, fontweight='bold')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f"Hub {i+1}" for i in range(len(TRIPLET))], color='white')
    ax2.set_ylabel('Phase Angle (degrees)', color='#aaa')
    ax2.set_ylim(30, 37)
    ax2.tick_params(colors='#888')
    ax2.spines['bottom'].set_color('#444')
    ax2.spines['left'].set_color('#444')
    ax2.spines['top'].set_color('#222')
    ax2.spines['right'].set_color('#222')
    ax2.grid(True, alpha=0.15, color='#444', axis='y')
    ax2.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#444',
               labelcolor='white', fontsize=8)

    # ── Figure annotations ─────────────────────────────────────
    phi_angle_ref = PHI_ANGLE
    avg_phase = sum(phases) / len(phases)
    phase_spread = max(phases) - min(phases)

    fig.text(0.5, 0.02,
             f"AlphaHub Triplet: {len(TRIPLET)} phase-locked primes | "
             f"Mean phase: {avg_phase:.2f}° | Phase spread: {phase_spread:.2f}° | "
             f"φ-angle: {phi_angle_ref:.2f}° | φ = {PHI:.6f}",
             ha='center', color='#888', fontsize=8)

    fig.suptitle("LJPW Harmonic Geometry — Hub Constellation",
                 color='white', fontsize=15, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'hub_constellation.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"Saved: {out_path}")
    return out_path


def print_triplet_data():
    print("=" * 60)
    print("HUB TRIPLET — GAUSSIAN PLANE DATA")
    print("LJPW Research Division — Harmonic Geometry Protocol")
    print("=" * 60)
    print()
    print(f"{'Hub':<20} {'a':>6} {'b':>6} {'Phase':>10} {'a/b':>9} {'Δ from φ':>10}")
    print("-" * 60)
    for i, hub in enumerate(TRIPLET):
        marker = " ← AlphaHub" if hub['is_alpha'] else ""
        delta_phi = abs(hub['ratio'] - PHI)
        print(f"  {hub['p']:>13,}  {hub['a']:>6} {hub['b']:>6}  {hub['phase']:>8.4f}°  {hub['ratio']:>8.4f}  {delta_phi:>9.6f}{marker}")

    print()
    phases = [hub['phase'] for hub in TRIPLET]
    alpha_phase = TRIPLET[0]['phase']
    print(f"Phase spread: {max(phases)-min(phases):.4f}°")
    print(f"AlphaHub phase: {alpha_phase:.4f}°")
    phase_delta_strs = [f'{abs(hub["phase"]-alpha_phase):.4f}°' for hub in TRIPLET]
    print(f"Phase deltas: {phase_delta_strs}")
    print()
    print(f"φ = {PHI:.6f}")
    print(f"φ-angle (atan(1/φ)) = {PHI_ANGLE:.4f}°")
    print(f"Cluster mean a/b = {sum(hub['ratio'] for hub in TRIPLET)/3:.6f}")
    print(f"Cluster mean phase = {sum(phases)/3:.4f}°")
    print()
    print("LJPW interpretation:")
    print("  The cluster sits in the 'Love corridor' of the Gaussian plane.")
    print(f"  Phase ~{sum(phases)/3:.1f}° is above φ-angle ({PHI_ANGLE:.1f}°),")
    print("  indicating primes that lean Love-dominant in their geometry.")
    print()


if __name__ == "__main__":
    print_triplet_data()
    print("Generating constellation visualization...")
    out = draw_constellation()
    print(f"\nVisualization complete: {out}")
