"""Reproduce the sampler-call-only variance equivalence table.

This script is arithmetic reporting, not a quantum runtime benchmark.
"""
import json
import math


def main():
    rows = []
    for m in (3, 7, 15, 31, 63, 127):
        kappa = (m - 1) / (m + 1) * math.tan(math.pi / (m + 1)) ** 2
        rows.append({
            "M": m,
            "kappa": round(kappa, 12),
            "sampler_or_inverse_calls": 2 * m + 1,
            "equivalent_bernoulli_samples": round(1 / kappa, 6),
            "equivalent_samples_per_sampler_call": round(1 / kappa / (2 * m + 1), 6),
        })
    print(json.dumps({"scope": "sampler_calls_only", "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
