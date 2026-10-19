# Reproduce the finite checks

Run from the repository root with Python 3.10 or newer:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The suite was executed with Python 3.12.14 and NumPy 2.3.5 on 2026-10-19. All four programs passed their internal checks and matched the committed [reference outputs](expected). NumPy is used only for the finite classical matrix calculations. No quantum SDK, QRAM service, account, network access during the checks, or quantum device is required.

Expected runner summary:

```json
{
  "status": "passed",
  "scripts": ["check_circuits", "check_statistics", "check_precision", "resource_table"],
  "reference_mode": "compared",
  "scope": "finite ideal-circuit, perturbation, statistics and resource checks"
}
```

Do not use Python's `-O` option. The verification programs use assertions, and the runner rejects optimized execution. Every program can also be run individually with `python3 verification/PROGRAM.py`; each emits one JSON document. The first three expose a `run_checks()` function for local use.

## What is checked

| Program | Independent calculation | Tested scope |
|---|---|---|
| [check_circuits.py](check_circuits.py) | Elementary reversible gates, gate-by-gate QFT, odd embedding, direct joint clock/target evolution and an exact Toffoli decomposition | 2,594 reversible basis cases; Fourier implementations for $`M=3,7,15,31,63`$; complex Grover inputs; gate counts and workspace |
| [check_statistics.py](check_statistics.py) | Direct sine-law probabilities, enumerated products, finite-state transition flow and an algebraic endpoint expression | 66 moment cases; an 84-outcome independent product; an 11-state positive-weight chain; convex-order obstruction, posterior perturbation and rounding |
| [check_precision.py](check_precision.py) | Full complex unitary perturbations, paired readout, polynomial interpolation, density-matrix Kraus evolution | Ten perturbed-clock cases at 77 probabilities, including $`10^{-14}`$; 28 ideal-restoration cases; spare/sign leakage and a retained auxiliary qubit |
| [resource_table.py](resource_table.py) | Evaluation of the exact variance coefficient and sampler-call counts | The six-row variance-equivalence table in [Interpretation](../science/interpretation.md) |

The circuit checker does not insert a discrete sine transform as an elementary gate. It constructs the Fourier circuit, implements the odd embedding with reversible prefix-OR arithmetic, and compares that operation with the independently calculated sine matrix. Its direct Grover calculation uses genuinely complex good/bad states and verifies the equal-eigenphase mixture as well as the harmless shift between physical exponents $`r`$ and $`r-1`$.

The Boolean checks verify clause truth values, uncomputation, the success flag and the all-zero reflection. Empty formulas, empty clauses, repeated literals, tautologies and invalid inputs are included. The closed-form 3CNF resource ledger is used only under its stated distinct-variable, at-least-three-clause assumptions. The general gate-list implementation handles the other cases separately.

The statistical checker verifies detailed balance and the marginal of a small extended target. This is a finite check of the target identity, not a mixing or convergence benchmark. Its convex-order example compares specified distributions; it is not an application-level runtime comparison.

The precision checker uses dense deterministic complex perturbations that populate noncanonical labels. They are mathematical unitary errors, not returned sequences from a Clifford+$`T`$ compiler. It checks the first two raw moments against their degree-$`M`$ polynomial structure at independent points and verifies the stated orientation inequalities. Negative controls demonstrate endpoint or polynomial failures when the paired inverse, orientation, or equal phase mixture is removed. The restoration calculation propagates the target density matrix through the actual ideal Kraus operators for 32 rounds, then closes the remaining geometric tail analytically. It does not claim to simulate an infinite stopping time.

## Tolerances and recorded results

Reversible Boolean values and gate counts are exact. The matrix checks use double-precision complex arithmetic and explicitly bounded residuals. The observed maximum QFT/sine-circuit residual was below $`8\times10^{-15}`$. The statistical moment errors were below $`2\times10^{-15}`$, and the finite-state detailed-balance residual was below $`4\times10^{-18}`$. The compiled-moment polynomial residual was below $`4\times10^{-15}`$. The ideal restoration identities and stopping-moment checks had residuals below $`2\times10^{-14}`$.

Each script states and enforces its own scientific tolerances. In particular, endpoint-scaled perturbation checks allow a relative tolerance of $`2\times10^{-7}`$ times the relevant endpoint factor, plus a $`5\times10^{-25}`$ cancellation floor. This accommodates division by probabilities as small as $`10^{-14}`$ in double precision. Absolute raw-moment and polynomial residuals use a tighter $`5\times10^{-12}`$ tolerance. These numerical tolerances are not physical error budgets.

The runner additionally compares JSON structure, exact integer/string values and floating-point results with the committed reference files. Its floating-point comparison uses absolute tolerance $`10^{-10}`$ and relative tolerance $`10^{-7}`$ to allow small platform differences. The scripts' internal assertions remain responsible for the stronger mathematical checks. A different BLAS implementation can change the last few reported digits without changing the tested conclusion.

To deliberately regenerate reference files after reviewing a scientific change, run:

```bash
python3 verification/run_all.py --record
python3 verification/run_all.py
```

The first command runs every script successfully before replacing any reference output. Review the resulting changes. Regenerating reference files is not evidence that a changed scientific claim is correct.

## Proof and implementation boundaries

The [review record](REVIEW.md) identifies the inspected scientific revision and the actual GitHub mathematical-rendering checks.

The universal moment identities are proved in [Variance proof](../science/variance-proof.md). The endpoint-aware synthesis guarantee is proved in [Finite precision](../science/finite-precision.md), and the unbounded-tail restoration law in [Ideal restoration](../science/restoration.md). Finite enumeration cannot replace those proofs.

The [logical resource ledger](../science/circuits-and-resources.md) specifies explicit gates before rotation synthesis and a cost interface for a certified native compiler. This suite does not run that compiler, choose an error-correcting code, emulate physical noise, or establish a wall-clock advantage. Dense state-vector calculations are small-instance verification methods, not efficient classical replacements for the general quantum task. The scientific source and attribution comparisons are documented in [Related work](../references/related-work.md), independently of the numerical suite.
