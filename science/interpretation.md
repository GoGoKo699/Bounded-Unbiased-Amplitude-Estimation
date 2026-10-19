# What the estimator changes and what it costs

The task is to estimate the success probability of an explicitly implementable sampler. A direct observation produces a Bernoulli variable with variance $`p(1-p)`$. The sine-clock construction replaces that observation with a bounded real output whose variance is $`\kappa_M p(1-p)`$. Its expectation remains exactly $`p`$ in the ideal circuit model.

The mechanism is a measurement choice. The sine clock is the top eigenvector of a finite path adjacency matrix. Measuring that matrix in its sine-transform eigenbasis converts adjacent phase coherence into the desired first moment. The same eigenvector recurrence makes the centered second moment a discrete derivative norm, yielding the exact coefficient $`\kappa_M`$. The [variance proof](variance-proof.md) supplies this connection without a phase-bin estimate or a nonlinear inversion of an estimated phase.

## A useful probability estimate

An output in $`[0,1]`$ can be averaged without clipping and can serve as a nonnegative likelihood weight. Exact unbiasedness is useful when the target of a larger statistical construction depends on a first-moment identity. The [positive-weight account](positive-weights.md) makes that statement precise for pseudo-marginal targets and independent products.

These are structural guarantees. They do not establish faster mixing for every Markov chain, and smaller variance does not imply domination in convex order. The explicit counterexample in that account prevents such an inference. Likewise, the product comparison is against independent classical factor averaging; correlated classical methods require a separate comparison.

## The cost of one coherent run

Write $`g_A`$ for the cost of the actual sampler, $`g_R`$ for the combined controlled reflections and control phase, and $`g_V`$ for one clock transform in a specified logical gate convention. The binary implementation with $`M+1=2^\ell`$ has cost

```math
g_{\mathrm{shot}}=(2M+1)g_A+Mg_R+2g_V+g_{\mathrm{init}},
```

where $`g_{\mathrm{init}}`$ includes setting the clock label to one, a single $`X`$ gate in the specified circuit. State initialization, measurement, reset and classical readout must also be included in the chosen hardware cost model. The orientation correction for finite synthesis adds one independent sampler preparation and success measurement. The exact width and the full hard-coded reversible 3CNF example are in [circuits and resources](circuits-and-resources.md).

The number of sampler calls is deterministic for the destructive estimator. The separate [restoration protocol](restoration.md) has at most two expected rounds, but an unbounded tail. Its expected-cost guarantee cannot be used as a strict coherent-work cap.

## Comparing variances at the same sampler-call budget

For $`0<p<1`$, one ideal sine-clock output has the same variance as the average of $`1/\kappa_M`$ independent Bernoulli samples, if fractional sample counts are used only as a numerical equivalence. An actual average needs an integer number of samples. The following table isolates sampler calls and omits reflection, clock, measurement and reset costs.

| $`M`$ | $`\kappa_M`$ | Sampler or inverse calls | Equivalent Bernoulli count $`1/\kappa_M`$ | Equivalence divided by sampler calls |
|---:|---:|---:|---:|---:|
| 3 | 0.500000000 | 7 | 2.000 | 0.286 |
| 7 | 0.128679656 | 15 | 7.771 | 0.518 |
| 15 | 0.034620364 | 31 | 28.885 | 0.932 |
| 31 | 0.009094272 | 63 | 109.959 | 1.745 |
| 63 | 0.002338027 | 127 | 427.711 | 3.368 |
| 127 | 0.000593219 | 255 | 1685.719 | 6.611 |

The first entry in this implemented family with a ratio greater than one is $`M=31`$. This is a sampler-call comparison, not a hardware speedup. At $`M=3`$, the output law is exactly that of the average of two Bernoulli samples, despite the seven sampler/inverse calls used by the binary circuit.

For a genuine runtime comparison, let $`\tau_Q`$ be the full elapsed cost of one coherent estimator shot and $`\tau_B`$ the elapsed cost of one direct Bernoulli draw in the competing implementation. Matching the variance of independent averages favors the ideal estimator only if

```math
\kappa_M\tau_Q<\tau_B.
```

Both sides must use the same physical cost unit. A classical Bernoulli draw can be much cheaper than a reversible quantum sampler call. In the 3CNF example, a classical program can evaluate clauses and stop after failure; the coherent circuit maintains reversibility and must later uncompute. Structure-specific counting algorithms are additional competitors. The table supplies no evidence against them.

## Repetition and gate precision

Independent ideal outputs preserve exact unbiasedness under an ordinary sample mean. A median-of-means construction gives high-probability error bounds from the variance guarantee, but the median itself is generally biased. For a known bound $`v\geq p(1-p)`$, additive error $`\varepsilon`$ and failure probability $`\zeta`$, the familiar repetition scale is

```math
R=O\!\left[\left(1+\frac{\kappa_M v}{\varepsilon^2}\right)
\left(1+\log\frac1\zeta\right)\right].
```

The [finite-precision theorem](finite-precision.md) allocates part of the error to bias and supplies an analogous bound. Paired synthesis plus one Bernoulli orientation sample protects the endpoint behavior, giving a variance and bias proportional to $`p(1-p)`$ without a minimum-probability assumption. The target is the actual compiled sampler; an intended-model discrepancy is a separate term.

At fixed $`M`$, the costly sampler-call budget per run does not grow as the final requested accuracy improves. Clock synthesis and output arithmetic still require increasing precision. Thus a fixed costly-call budget is compatible with increasing native gate cost, and a genuinely fixed finite circuit has a bias floor. No claim of arbitrary final accuracy at a fixed total native-gate budget follows.

Existing amplitude-estimation and hybrid quantum-classical results already establish quadratic variance and precision advantages in appropriate access models. The [related-work comparison](../references/related-work.md) identifies the closer positive, nearly unbiased and exactly unbiased constructions. The present scientific distinction is the combined output, moment and budget guarantee and its explicit implementation, not a new general estimation exponent.

## Physical resource boundary

The circuit ledger counts logical gates and live qubits. A physical implementation also needs a hardware connectivity model, gate durations, a chosen error-correcting code and decoder, magic-state production where applicable, and an allocation of failure probability across repeated shots. Those choices can change both time and space substantially.

No numerical physical-qubit or wall-clock advantage is asserted here. Coherent synthesis error is bounded in the written theorem; stochastic hardware faults are a different error source. Arbitrary faults can destroy exact endpoint behavior, so the uniform rare-event guarantee is not asserted at a nonzero uncontrolled fault floor.

No QRAM is assumed. The explicit example uses a compiled clause list, ordinary reversible Boolean operations and direct classical calculation of the final scalar. More general applications must provide their own equally explicit state preparation, success test, inverse, input precision and classical processing costs.
