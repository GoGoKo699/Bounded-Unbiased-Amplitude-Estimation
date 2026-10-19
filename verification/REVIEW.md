# Verification and rendering review

Reviewed on October 19, 2026. The scientific and learning content inspected is commit [`e7ec09ce05cbab841dd8ace944baf409cb9055cf`](https://github.com/GoGoKo699/Bounded-Unbiased-Amplitude-Estimation/tree/e7ec09ce05cbab841dd8ace944baf409cb9055cf). This record and its incoming links are documentation added after that inspection; they do not change the inspected mathematics or verification programs.

## Scientific and learning checks

The consistency review compared the headline, exact moment theorem, proof, circuit ledger, finite-precision assumptions, positive-weight application and separate restoration mode. It checked the sampler/inverse and reflection costs, clean-work sharing, compiled bias constants, confidence allocation, and the distinction between deterministic destructive work and expected restoration work. The small clarifications from this review are incorporated in the scientific pages.

The learning route uses one selected educational anchor: Lin Lin's March 3, 2022 author revision. Section pointers and the Grover basis/angle conventions were checked against that source. The map contains exactly M01–M30, allocated as 11 background and 19 narrative milestones, with backward prerequisites and a final synthesis in each phase. The bridge's three-outcome example was checked algebraically. Personal teaching instructions and learner records are outside this repository.

## Reproduction

`python3 verification/run_all.py` passed all four programs and their saved-reference comparisons under Python 3.12.14 and NumPy 2.3.5. The programs check finite circuit identities, moments and statistical compositions, structured precision perturbations and ideal restoration, and the resource table. See [the verification guide](README.md) for commands, tolerances and exact scope.

Local navigation, Markdown fences, protected inline-math pairs and milestone fields were also checked. Hosted file blobs were compared with the local source. The verification code and expected outputs are unchanged by the documentation and rendering repairs.

## Actual hosted rendering

GitHub Preview was inspected in a browser, beyond source-level delimiter checks. At the content revision above, every mathematical expression counted in each source page had a corresponding rendered math element, and no macro or delimiter errors were present:

| Page | Rendered expressions |
|---|---:|
| [README](../README.md) | 10 |
| [Source bridge](../learning/LIN_BRIDGE.md) | 149 |
| [Milestone map](../learning/MILESTONES.md) | 67 |
| [Model and estimator](../science/model-and-estimator.md) | 90 |
| [Variance proof](../science/variance-proof.md) | 97 |
| [Circuits and resources](../science/circuits-and-resources.md) | 233 |
| [Finite precision](../science/finite-precision.md) | 195 |
| [Positive weights](../science/positive-weights.md) | 170 |
| [Restoration](../science/restoration.md) | 97 |
| [Interpretation](../science/interpretation.md) | 28 |
| [Related work](../references/related-work.md) | 67 |
| [Verification guide](README.md) | 17 |

Visual inspection included the README theorem and results table; bridge matrices, outcome table and spectral derivation; milestone phase table; ideal theorem and output procedure; variance residual; live-width formula and gate ledger; compiled moment and precision bounds; product moments; and restoration procedure and stopping law. Inline subscripts, bra–ket notation, equation references and table boundaries were included in these samples.

The hosted checks exposed and resolved rejected operator-name macros, Markdown consumption of mathematical escapes, collapsed numbered-equation layouts and formulas displayed as code inside numbered lists. The corrected files use protected inline expressions, top-level math fences, supported roman labels and equation numbers within the formula row. This is a check of the observed hosting renderer, not a restriction on LaTeX in other formats.

The review is an internal consistency and reproducibility check. It is not external peer review, a proof of novelty, a hardware execution test or a physical resource estimate. The universal claims depend on the written proofs and their stated assumptions.
