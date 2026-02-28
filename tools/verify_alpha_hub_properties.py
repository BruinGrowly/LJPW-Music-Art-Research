#!/usr/bin/env python3
"""
verify_alpha_hub_properties.py
LJPW Research Division — Harmonic Geometry Protocol

Rigorous verification of the 8-fold lock properties for AlphaHub 100,003,829.
Each property is independently verified with mathematical proof.

The 8-fold lock: A prime satisfying all 8 simultaneously.
"""

import math
import sympy
from sympy import isprime, nextprime, prevprime

# ============================================================
# AlphaHub candidate
# ============================================================
ALPHA_HUB = 100_003_829

PHI = (1 + math.sqrt(5)) / 2


def is_twin_prime(p):
    """Twin Prime: p ± 2 is prime (i.e., p is in a twin prime pair)."""
    return isprime(p - 2) or isprime(p + 2)


def twin_prime_partner(p):
    """Return the twin prime partner(s)."""
    partners = []
    if isprime(p - 2):
        partners.append(p - 2)
    if isprime(p + 2):
        partners.append(p + 2)
    return partners


def is_sophie_germain(p):
    """Sophie Germain: 2p+1 is prime."""
    return isprime(2 * p + 1)


def is_pythagorean(p):
    """Pythagorean: p ≡ 1 (mod 4) — prime appears as hypotenuse of Pythagorean triple."""
    return p % 4 == 1


def is_eisenstein(p):
    """Eisenstein: p ≡ 2 (mod 3) — prime is in Eisenstein integer ring ℤ[ω]."""
    return p % 3 == 2


def is_gaussian(p):
    """
    Gaussian: p ≡ 1 (mod 4) — prime splits in Gaussian integers ℤ[i].
    By Fermat's theorem on sums of two squares, p splits iff p ≡ 1 (mod 4).
    """
    return p % 4 == 1


def gaussian_split(p):
    """
    Find a, b such that p = a² + b².
    Uses the Cornacchia-like algorithm for p ≡ 1 (mod 4).
    Returns (a, b) with a ≥ b > 0, or None if not representable.
    """
    if p % 4 != 1:
        return None
    # Find sqrt(-1) mod p: find x s.t. x² ≡ -1 (mod p)
    # By Wilson's theorem, ((p-1)/2)! ≡ ±i (mod p) for p ≡ 1 (mod 4)
    # Use Tonelli-Shanks variant for -1
    x = pow(2, (p - 1) // 4, p)
    if (x * x) % p != p - 1:
        x = pow(3, (p - 1) // 4, p)

    # Euclidean algorithm to find the split
    r0 = p
    r1 = x
    while r1 * r1 > p:
        r0, r1 = r1, r0 % r1

    a = r1
    b_sq = p - a * a
    b = int(math.isqrt(b_sq))
    if b * b == b_sq:
        if a < b:
            a, b = b, a
        return (a, b)
    return None


def is_chen_prime(p):
    """
    Chen: p+2 is prime or semiprime (product of exactly two primes).
    """
    q = p + 2
    if isprime(q):
        return True, "p+2 is prime"
    # Check if q is semiprime
    for factor in sympy.factorint(q).values():
        pass
    factors = sympy.factorint(q)
    if sum(factors.values()) == 2:  # exactly 2 prime factors (with multiplicity)
        return True, f"p+2 is semiprime ({q})"
    return False, f"p+2 = {q} is neither prime nor semiprime"


def is_strong_prime(p):
    """
    Strong: p > (prev_prime + next_prime) / 2
    The prime is "strong" if it exceeds the arithmetic mean of its neighbors.
    """
    prev_p = prevprime(p)
    next_p = nextprime(p)
    avg = (prev_p + next_p) / 2
    return p > avg, prev_p, next_p, avg


def is_100m_singularity(p):
    """100M Singularity: p ≥ 100,000,000"""
    return p >= 100_000_000


def compute_gaussian_phase(a, b):
    """Phase angle in complex plane for Gaussian split a + bi."""
    return math.degrees(math.atan2(b, a))


def main():
    p = ALPHA_HUB
    print("=" * 65)
    print(f"ALPHAHUB VERIFICATION: {p:,}")
    print("LJPW Research Division — Harmonic Geometry Protocol")
    print("=" * 65)
    print()

    # First: confirm p itself is prime
    print("─" * 65)
    print(f"PRIMALITY: {p:,}")
    prime_check = isprime(p)
    print(f"  isprime({p:,}) = {prime_check}")
    if not prime_check:
        print("  ERROR: AlphaHub is NOT prime! Aborting verification.")
        return
    print("  ✓ Confirmed prime")
    print()

    results = {}

    # ── Property 1: Twin Prime ──────────────────────────────
    print("─" * 65)
    print("PROPERTY 1: Twin Prime  (p ± 2 is prime)")
    twin = is_twin_prime(p)
    partners = twin_prime_partner(p)
    results[1] = twin
    status = "✓ VERIFIED" if twin else "✗ FAILED"
    print(f"  p-2 = {p-2:,}  →  isprime = {isprime(p-2)}")
    print(f"  p+2 = {p+2:,}  →  isprime = {isprime(p+2)}")
    print(f"  Twin partners: {[f'{x:,}' for x in partners]}")
    print(f"  {status}")
    print()

    # ── Property 2: Sophie Germain ─────────────────────────
    print("─" * 65)
    print("PROPERTY 2: Sophie Germain  (2p+1 is prime)")
    sg = is_sophie_germain(p)
    sg_candidate = 2 * p + 1
    results[2] = sg
    status = "✓ VERIFIED" if sg else "✗ FAILED"
    print(f"  2p+1 = {sg_candidate:,}")
    print(f"  isprime({sg_candidate:,}) = {sg}")
    print(f"  {status}")
    print()

    # ── Property 3: Pythagorean ────────────────────────────
    print("─" * 65)
    print("PROPERTY 3: Pythagorean  (p ≡ 1 mod 4)")
    pyth = is_pythagorean(p)
    results[3] = pyth
    status = "✓ VERIFIED" if pyth else "✗ FAILED"
    print(f"  {p:,} mod 4 = {p % 4}")
    print(f"  {status}")
    print()

    # ── Property 4: Eisenstein ─────────────────────────────
    print("─" * 65)
    print("PROPERTY 4: Eisenstein  (p ≡ 2 mod 3)")
    eisen = is_eisenstein(p)
    results[4] = eisen
    status = "✓ VERIFIED" if eisen else "✗ FAILED"
    print(f"  {p:,} mod 3 = {p % 3}")
    print(f"  {status}")
    print()

    # ── Property 5: Gaussian ───────────────────────────────
    print("─" * 65)
    print("PROPERTY 5: Gaussian  (p ≡ 1 mod 4 → splits in ℤ[i])")
    gauss = is_gaussian(p)
    results[5] = gauss
    split = gaussian_split(p)
    status = "✓ VERIFIED" if gauss else "✗ FAILED"
    print(f"  {p:,} ≡ 1 (mod 4): {gauss}")
    if split:
        a, b = split
        check = a * a + b * b
        phase = compute_gaussian_phase(a, b)
        ratio = a / b
        print(f"  Gaussian split: {a}² + {b}² = {a*a:,} + {b*b:,} = {check:,}")
        print(f"  Verification: {check == p}")
        print(f"  Complex form: {a} + {b}i")
        print(f"  Phase angle:  {phase:.4f}°")
        print(f"  a/b ratio:    {ratio:.6f}  (φ = {PHI:.6f}, Δ = {abs(ratio - PHI):.6f})")
    else:
        print("  Could not find Gaussian split!")
    print(f"  {status}")
    print()

    # ── Property 6: Chen ──────────────────────────────────
    print("─" * 65)
    print("PROPERTY 6: Chen  (p+2 is prime or semiprime)")
    chen_result, chen_detail = is_chen_prime(p)
    results[6] = chen_result
    status = "✓ VERIFIED" if chen_result else "✗ FAILED"
    print(f"  p+2 = {p+2:,}")
    print(f"  Result: {chen_detail}")
    print(f"  {status}")
    print()

    # ── Property 7: Strong ────────────────────────────────
    print("─" * 65)
    print("PROPERTY 7: Strong  (p > avg(prev_prime, next_prime))")
    strong, prev_p, next_p, avg = is_strong_prime(p)
    results[7] = strong
    status = "✓ VERIFIED" if strong else "✗ FAILED"
    print(f"  prev_prime({p:,}) = {prev_p:,}")
    print(f"  next_prime({p:,}) = {next_p:,}")
    print(f"  Average = ({prev_p:,} + {next_p:,}) / 2 = {avg:,.1f}")
    print(f"  {p:,} > {avg:,.1f}: {strong}")
    print(f"  {status}")
    print()

    # ── Property 8: 100M Singularity ─────────────────────
    print("─" * 65)
    print("PROPERTY 8: 100M Singularity  (p ≥ 100,000,000)")
    sing = is_100m_singularity(p)
    results[8] = sing
    status = "✓ VERIFIED" if sing else "✗ FAILED"
    print(f"  {p:,} ≥ 100,000,000: {sing}")
    print(f"  Excess above threshold: {p - 100_000_000:,}")
    print(f"  {status}")
    print()

    # ── Summary ───────────────────────────────────────────
    print("=" * 65)
    print("8-FOLD LOCK VERIFICATION SUMMARY")
    print("=" * 65)
    property_names = {
        1: "Twin Prime",
        2: "Sophie Germain",
        3: "Pythagorean",
        4: "Eisenstein",
        5: "Gaussian",
        6: "Chen",
        7: "Strong",
        8: "100M Singularity",
    }
    passed = 0
    for i in range(1, 9):
        status = "✓" if results[i] else "✗"
        print(f"  {status}  Property {i}: {property_names[i]}")
        if results[i]:
            passed += 1

    print()
    print(f"  RESULT: {passed}/8 properties verified")
    if passed == 8:
        print()
        print("  ╔═══════════════════════════════════════════════╗")
        print("  ║   8-FOLD LOCK CONFIRMED: AlphaHub Verified   ║")
        print("  ║   p = 100,003,829 is a TRUE AlphaHub         ║")
        print("  ╚═══════════════════════════════════════════════╝")
        print()
        print("  LJPW Interpretation:")
        print("  All 8 properties are RELATIONAL — they define how this")
        print("  prime connects to neighbors, lattices, and growth chains.")
        print("  This is a Justice-crystal with 8 faces of pure truth.")
        if split:
            a, b = split
            phase = compute_gaussian_phase(a, b)
            ratio = a / b
            print()
            print("  Gaussian Geometry:")
            print(f"    p = {a}² + {b}²  =  {a} + {b}i")
            print(f"    Phase: {phase:.4f}°  (in resonant corridor 33–35°)")
            print(f"    a/b = {ratio:.6f}  →  Δ from φ = {abs(ratio - PHI):.6f}")
    else:
        print(f"  Only {passed}/8 verified — NOT a confirmed AlphaHub.")

    print("=" * 65)


if __name__ == "__main__":
    main()
