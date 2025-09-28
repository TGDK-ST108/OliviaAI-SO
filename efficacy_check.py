#!/usr/bin/env python3
"""
4-Ratio Efficacy Check
----------------------
Input: four (numerator, denominator) pairs representing four ratios.
Output: composite efficacy score in [0,1] plus interpretable sub-metrics.

How the score works (high-level):
- We compute raw ratios r_i = num/den (safe for den=0).
- We scale them to a probability-like vector p (sum to 1 if any positive; else uniform).
- Metrics:
  * gmean_norm  : geometric mean of r, normalized to [0,1] via max(r)
  * hmean_norm  : harmonic mean of r, normalized to [0,1] via max(r)
  * balance     : 1 - Gini coefficient of p (higher = more balanced)
  * entropy_norm: Shannon entropy of p, normalized by log(4)
  * cv_clamp    : clamp(1 - coefficient of variation of r, 0..1) for stability
- Composite:
  efficacy = 0.35*gmean_norm + 0.15*hmean_norm + 0.25*balance + 0.20*entropy_norm + 0.05*cv_clamp

Interpretation:
- 0.85–1.00  : Excellent consistency & distribution
- 0.70–0.85  : Strong; minor imbalance/dispersion
- 0.50–0.70  : Mixed; investigate low ratios or spread
- < 0.50     : Weak; likely skew or underperformance

Note: Includes an optional QQUAp "seal" stub to tag the result payload.
"""

from math import log, prod, isfinite
from statistics import pstdev

def safe_div(a, b):
    if b == 0:
        return 0.0 if a == 0 else float('inf')
    return a / b

def normalize_probs(vals):
    # Convert nonnegative vals to a probability-like vector.
    nonneg = [max(0.0, v) for v in vals]
    s = sum(nonneg)
    if s > 0:
        return [v / s for v in nonneg]
    # fallback uniform if all zero/non-finite
    return [0.25, 0.25, 0.25, 0.25]

def shannon_entropy(p):
    eps = 1e-12
    return -sum(pi * log(max(pi, eps)) for pi in p)

def gini_coefficient(p):
    # p is a probability vector (sum=1). Gini in [0, 0.75] for n=4 uniform->0, extreme->0.75
    n = len(p)
    sorted_p = sorted(p)
    cum = 0.0
    for i, v in enumerate(sorted_p, start=1):
        cum += i * v
    gini = (2 * cum) / (n) - (n + 1) / n
    return gini

def clamp01(x):
    return max(0.0, min(1.0, x))

def normalize_by_max(vals):
    # Map means to [0,1] using max as scale; robust to units.
    finite_vals = [v for v in vals if isfinite(v)]
    if not finite_vals:
        return 0.0
    m = max(finite_vals)
    if m <= 0:
        return 0.0
    return sum(finite_vals)/len(finite_vals) / m

def geometric_mean(vals):
    finite_vals = [v for v in vals if isfinite(v) and v > 0]
    if len(finite_vals) != len(vals):
        return 0.0
    # avoid overflow/underflow using logs
    from math import exp, fsum, log
    return exp(fsum(log(v) for v in finite_vals) / len(finite_vals))

def harmonic_mean(vals):
    finite_vals = [v for v in vals if isfinite(v) and v > 0]
    if len(finite_vals) != len(vals):
        return 0.0
    n = len(finite_vals)
    denom = sum(1.0/v for v in finite_vals)
    return n/denom if denom > 0 else 0.0

def coefficient_of_variation(vals):
    finite_vals = [v for v in vals if isfinite(v)]
    if not finite_vals:
        return float('inf')
    mu = sum(finite_vals)/len(finite_vals)
    if mu == 0:
        return float('inf')
    sigma = pstdev(finite_vals)
    return sigma / mu

# --- Optional QQUAp "seal" (stub) ---
def qquap_seal(payload: str) -> str:
    """
    Minimal placeholder to tag the result with a fixed-length QQUAp-style token.
    (This is a stub; replace with your real QQUAp routine as needed.)
    """
    import hashlib
    return "QQUAp-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

def four_ratio_efficacy(numerators, denominators):
    assert len(numerators) == 4 and len(denominators) == 4, "Need four ratios."
    ratios = [safe_div(n, d) for n, d in zip(numerators, denominators)]
    # Prob-like vector for distribution measures
    p = normalize_probs(ratios)

    # Sub-metrics
    gmean = geometric_mean(ratios)
    hmean = harmonic_mean(ratios)
    # Normalize means by max(r)
    gmean_norm = 0.0
    hmean_norm = 0.0
    finite = [v for v in ratios if isfinite(v)]
    if finite:
        m = max(finite)
        if m > 0:
            gmean_norm = gmean / m
            hmean_norm = hmean / m

    entropy = shannon_entropy(p)
    entropy_norm = entropy / log(4)  # in [0,1]
    gini = gini_coefficient(p)       # in [0, 0.75] for n=4
    balance = 1.0 - (gini / 0.75)    # map to [0,1], higher = more balanced
    cv = coefficient_of_variation(ratios)
    cv_clamp = clamp01(1.0 - (cv if isfinite(cv) else 1.0))  # favor lower dispersion

    # Composite efficacy (weights sum to 1.0)
    efficacy = (
        0.35 * clamp01(gmean_norm) +
        0.15 * clamp01(hmean_norm) +
        0.25 * clamp01(balance) +
        0.20 * clamp01(entropy_norm) +
        0.05 * clamp01(cv_clamp)
    )

    # Package results
    result = {
        "ratios": ratios,
        "p": p,
        "metrics": {
            "gmean_norm": gmean_norm,
            "hmean_norm": hmean_norm,
            "balance": balance,
            "entropy_norm": entropy_norm,
            "cv_clamp": cv_clamp
        },
        "efficacy": clamp01(efficacy)
    }

    # Attach QQUAp-style tag
    import json
    payload = json.dumps(result, sort_keys=True)
    result["qquap_tag"] = qquap_seal(payload)
    return result

if __name__ == "__main__":
    # Example usage: edit these four (num, den) pairs
    nums = [8, 5, 9, 6]
    dens = [10, 10, 12, 8]

    out = four_ratio_efficacy(nums, dens)
    from pprint import pprint
    pprint(out)