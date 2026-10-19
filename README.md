# Bounded Unbiased Amplitude Estimation

**Can one coherent run estimate a probability without bias, keep every output between zero and one, and reduce its variance quadratically in the coherent work?** A sine clock and a discrete sine transform give an explicit ideal-circuit construction with all three properties.

Let an available unitary sampler prepare a state whose success probability is $p$. For an integer $M\geq2$, one run returns $Z\in[0,1]$ with

```math
\mathbb E Z=p,\qquad
\operatorname{Var}(Z)=\kappa_M p(1-p),\qquad
\kappa_M=\frac{M-1}{M+1}\tan^2\!\left(\frac{\pi}{M+1}\right)
\sim\frac{\pi^2}{M^2}.
```

The implemented family uses $M+1=2^\ell$. Its clock requires two quantum Fourier transforms, reversible arithmetic and $O(\log M)$ clock storage, with **no QRAM or amplitude lookup table**. The direct binary schedule uses exactly $M$ controlled Grover steps, hence $2M+1$ sampler or inverse calls, before optional finite-precision orientation correction. Reflections, clock gates, workspace, measurement and classical readout are additional charged resources.

| Result | Conditions and meaning | Scientific account |
|---|---|---|
| Bounded, exactly unbiased output with uniform variance | Ideal rotations and exact real-valued readout; every $p\in[0,1]$ | [Model and estimator](science/model-and-estimator.md), [proof](science/variance-proof.md) |
| Explicit circuit and reversible counting example | Available sampler and exact inverse; computable success reflection; no QRAM | [Circuits and resources](science/circuits-and-resources.md) |
| Controlled relative bias after gate synthesis | Paired clock circuit and inverse; an independent Bernoulli orientation sample; faithful execution of compiled gates | [Finite precision](science/finite-precision.md) |
| Nonnegative likelihood weights and independent products | Exact target identity in the ideal model; quantified target perturbation after synthesis | [Positive weights](science/positive-weights.md) |
| Separate state-restoration extension | Ideal circuit; almost-sure restoration in at most two expected rounds, with an unbounded tail | [Restoration](science/restoration.md) |

The contribution is the conjunction of positivity, exact ideal unbiasedness, a deterministic costly-call budget and a variance proportional to $p(1-p)$. Sine probe states, cosine observables, quantum sine transforms and general amplitude-estimation speedups are established ingredients. The [related-work comparison](references/related-work.md) identifies those ingredients and distinguishes this construction from existing nearly unbiased and hybrid estimators. No new generic precision exponent is claimed.

## Read the science

Begin with the [model and operational construction](science/model-and-estimator.md), then follow the [variance proof](science/variance-proof.md). The [circuit ledger](science/circuits-and-resources.md) explains how the mathematical measurement is realized and what it costs. [Finite precision](science/finite-precision.md) connects that ideal result to compiled gates. The [resource interpretation](science/interpretation.md) joins these results and explains the relevant comparisons.

The [positive-weight application](science/positive-weights.md) and [ideal restoration mode](science/restoration.md) can be read independently after the core construction. [Primary references](references/related-work.md) and the [structured bibliography](references/bibliography.bib) support attribution and further checking. The [LLM reading guide](llms.txt) maps questions to authoritative files.

## Reproduce the finite checks

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The [verification guide](verification/README.md) explains the tested identities, deterministic outputs and numerical tolerances. Finite simulations support the circuit and algebraic account; the written proofs establish the universal claims. The scripts are small-instance classical checks, not a quantum implementation benchmark or an efficient classical method for large samplers.

## Scope

Exact unbiasedness refers to the ideal circuit model. Finite gate synthesis and finite output arithmetic introduce a controlled bias. The precision theorem targets the probability of the actual compiled sampler; approximation of an intended continuous model needs its own error budget. Hardware faults require a separate fault-tolerance model.

The construction estimates a probability when an explicit reversible sampler and the required reflections are available. Lower estimator variance does not establish faster Markov-chain mixing, and a query advantage does not establish a physical runtime advantage over the best classical algorithm. The [resource comparison](science/interpretation.md) keeps those distinctions explicit.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
