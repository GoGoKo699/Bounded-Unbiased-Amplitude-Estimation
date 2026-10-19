# Model and estimator

This note defines an ideal quantum procedure that returns a number in $`[0,1]`$ whose expectation is a success probability $`p`$. Its variance is an explicit multiple of $`p(1-p)`$, decreasing quadratically with the clock size. The target is **the probability $`p`$**, not its square root.

The proof is in [Variance proof](variance-proof.md). Native circuits and their costs are in [Circuits and resources](circuits-and-resources.md); finite gate synthesis is treated separately in [Finite precision](finite-precision.md).

## Input and access model

Let $`A`$ be a unitary on a finite target register, including any work and garbage registers used by its implementation. Define

```math
|\psi\rangle=A|0\rangle,
\qquad \Pi=\Pi^\dagger=\Pi^2,
\qquad p=\langle\psi|\Pi|\psi\rangle\in[0,1].
```

The projector $`\Pi`$ specifies success. Often it tests a single output flag, but the mathematics allows any projector whose reflection can be implemented. Use the reflection convention

```math
R_\psi=2|\psi\rangle\langle\psi|-I,
\qquad S_\Pi=I-2\Pi,
\qquad G=R_\psi S_\Pi.
```

The algorithm needs an initial preparation of $`|\psi\rangle`$ and controlled powers of $`G`$. A controlled $`R_\psi`$ can be implemented by applying $`A^\dagger`$, a controlled reflection about $`|0\rangle`$, and $`A`$. Thus a native implementation must charge for $`A`$, $`A^\dagger`$, both reflections, and their workspace. A generic controlled version of every gate in $`A`$ is unnecessary.

On the relevant Grover invariant space, the eigenvalues of $`G`$ are $`e^{\pm i\phi}`$, where

```math
\phi\in[0,\pi],\qquad \cos\phi=1-2p.
```

This sign convention matters. Replacing $`G`$ by $`-G`$ without compensating changes the clock statistics and interchanges the roles of $`p`$ and $`1-p`$.

## Clock and readout

Choose an integer $`M\ge2`$, and set

```math
L=M+1,\qquad \alpha=\frac{\pi}{L},\qquad c=\cos\alpha>0.
```

Use clock labels $`r=1,\ldots,M`$. Define the normalized sine state and the type-I discrete sine transform by

```math
a_r=\sqrt{\frac2L}\sin(r\alpha),
\qquad |a\rangle=\sum_{r=1}^{M}a_r|r\rangle,
\qquad D_{jr}=\sqrt{\frac2L}\sin(jr\alpha).
```

Here $`D`$ is real, symmetric, and orthogonal: $`D^2=I`$. In particular, $`|a\rangle=D|1\rangle`$. An implementation in a larger binary register extends these operations unitarily on unused labels; the ideal algorithm has no support on those labels.

One sample consists of the following steps.

1. Prepare $`|a\rangle\otimes|\psi\rangle`$.
2. Apply $`\sum_{r=1}^{M}|r\rangle\langle r|\otimes G^r`$.
3. Apply $`D`$ to the clock and measure its label $`j\in\{1,\ldots,M\}`$.
4. Return the real number

   ```math
   Z=z_j=\frac{1-\cos(j\alpha)/c}{2}.
   ```

Only the clock is measured. This basic procedure need not restore the target state. It requires neither an estimate of $`p`$ nor a likelihood fit, acceptance test, or postselection.

The physical encoding above uses powers $`G^r`$, starting at $`r=1`$. Powers $`G^{r-1}`$ give the same clock distribution: the difference is a common unitary on the target. The unshifted convention is used throughout this note and in the simple binary circuit.

## Ideal sampling theorem

**Theorem.** For every $`M\ge2`$, every input unitary $`A`$, and every success projector $`\Pi`$, the exact procedure above returns $`Z`$ satisfying

```math
0\le Z\le1,
\qquad \mathbb E Z=p,
\qquad \mathrm{Var}(Z)=\kappa_M p(1-p),
```

where

```math
\boxed{\displaystyle
\kappa_M=\frac{M-1}{M+1}\tan^2\!\left(\frac{\pi}{M+1}\right)
}
\qquad\text{and}\qquad
\kappa_M=\frac{\pi^2}{M^2}\bigl(1+O(M^{-1})\bigr).
```

The identities hold at the endpoints: $`p=0`$ gives $`Z=0`$ with certainty, and $`p=1`$ gives $`Z=1`$ with certainty. There is no additive variance term independent of $`p`$.

The [proof](variance-proof.md) identifies the readout as measurement of a finite path adjacency matrix. The sine state is its largest-eigenvalue eigenvector, so its mean and variance can be evaluated directly.

For $`L=2^\ell`$, $`\ell\ge2`$, a binary power ladder uses exactly $`M=L-1`$ controlled applications of $`G`$, expanded into elementary Grover steps. Two sine transforms implement state preparation and readout. These transforms have an explicit circuit with $`O(\ell^2)`$ ideal gates and $`O(\ell)`$ reversible arithmetic gates. The resulting block has a deterministic coherent-work bound. Its native preparation, inverse, reflection, precision, and qubit costs are specified in [Circuits and resources](circuits-and-resources.md).

## Repetition and statistical guarantees

Let $`Z_1,\ldots,Z_R`$ be independent samples from fresh executions of the fixed circuit, and let

```math
\overline Z_R=\frac1R\sum_{i=1}^{R}Z_i.
```

Then

```math
\mathbb E\overline Z_R=p,
\qquad
\mathbb E(\overline Z_R-p)^2
=\mathrm{Var}(\overline Z_R)
=\frac{\kappa_M p(1-p)}R.
```

In particular, averaging preserves exact unbiasedness and boundedness. Chebyshev's inequality gives

```math
\Pr\!\left(|\overline Z_R-p|\ge\varepsilon\right)
\le \min\!\left\{1,\frac{\kappa_M p(1-p)}{R\varepsilon^2}\right\}.
```

A known bound $`v\ge p(1-p)`$ makes the choice

```math
R\ge\max\!\left\{1,\left\lceil\frac{\kappa_M v}{\delta\varepsilon^2}\right\rceil\right\}
```

sufficient for error at most $`\varepsilon`$ with failure probability at most $`\delta`$. The universal choice is $`v=1/4`$; a smaller promise can improve the resource bound. A formula involving the unknown true $`p`$ alone is not an executable sampling prescription.

### A confidence wrapper

Median-of-means reduces the failure-probability overhead. For $`\varepsilon>0`$, $`0<\delta<1`$, and known $`v\ge p(1-p)`$, take groups of size

```math
b=\max\!\left\{1,\left\lceil\frac{4\kappa_M v}{\varepsilon^2}\right\rceil\right\},
```

and an odd number $`K`$ of groups with $`K\ge8\ln(1/\delta)`$. Return the median of their sample means. Each group fails with probability at most $`1/4`$; Hoeffding's inequality bounds the probability that a majority fail by $`e^{-K/8}`$. Thus the total number of independent blocks is

```math
O\!\left(\left[1+\frac{\kappa_M v}{\varepsilon^2}\right]
\left[1+\ln\frac1\delta\right]\right).
```

The median remains in $`[0,1]`$, but it is **not generally unbiased**. Exact unbiasedness belongs to each block and to its arithmetic sample mean, not automatically to nonlinear confidence wrappers.

For the efficient clock family, the corresponding controlled-$`G`$ count is

```math
O\!\left(\left[M+\frac{v}{M\varepsilon^2}\right]
\left[1+\ln\frac1\delta\right]\right).
```

If at most $`q\ge3`$ controlled-$`G`$ applications are allowed per block, choosing the available size $`M=2^\ell-1\le q`$ near $`\min\{q,\max\{3,\sqrt v/\varepsilon\}\}`$ gives

```math
O\!\left(\left[1+\frac{\sqrt v}{\varepsilon}
+\frac{v}{q\varepsilon^2}\right]
\left[1+\ln\frac1\delta\right]\right)
```

total controlled-$`G`$ applications. This is a query-budget statement. A cap on actual coherent gates must also include the compiled sampler, reflections, clock, and synthesis costs. The asymptotic amplitude-estimation tradeoff is already established in the [related literature](../references/related-work.md); the exact bounded sample and its variance formula are the objects studied here.

For relative error $`\eta p`$, $`p>0`$, the variance-to-squared-error ratio is

```math
\frac{\mathrm{Var}(Z)}{\eta^2p^2}
=\frac{\kappa_M(1-p)}{\eta^2p}.
```

Using this for an a priori block count requires a positive lower bound on $`p`$, or a separately justified adaptive procedure. No such procedure is assumed by the theorem.

## Scope and linked extensions

- **Exact operations.** The theorem assumes exact ideal unitaries and exact evaluation of $`z_j`$. Finite rotation synthesis, output rounding, and noise require the error budget in [Finite precision](finite-precision.md). Exact ideal unbiasedness is not an exact noisy-device claim.
- **Compiled inputs.** The clock and readout require no QRAM. Any input data access, sampler construction, reversible work, or reflection implementation must be included in the native circuit; arbitrary datasets are not loaded for free.
- **Positive outputs.** Bounded nonnegative samples can be useful in products and other compositions. The relevant statements and their assumptions are developed in [Positive weights](positive-weights.md).
- **State reuse.** [Restoration](restoration.md) gives a separate ideal repeat-until-return construction. Its expected work is bounded, but its restoration time has no deterministic upper bound. It does not change the basic block's fixed-work theorem.
- **Comparison limits.** The variance identity does not establish a hardware speedup, finite-size minimax optimality, or a new precision exponent. Related estimators, sine probes, and cosine observables are compared in [Related work](../references/related-work.md).
