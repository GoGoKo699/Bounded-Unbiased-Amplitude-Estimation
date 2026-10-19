# From amplitude estimation to a bounded unbiased measurement

Suppose a reversible program prepares a quantum state and sets a flag when a specified event occurs. Measuring the flag gives a random zero or one. Repeating the program estimates its success probability. This project asks whether one longer coherent execution can return a number between zero and one with the same mean and a smaller variance, while making the entire circuit and its cost explicit.

The [30-milestone map](MILESTONES.md) fixes the understanding route. This bridge supplies the connections between the selected source and the project's proofs. It is useful to read the opening example before following every technical branch. The exact assumptions and universal arguments remain in [science/](../science/model-and-estimator.md).

## The selected source and where to enter

The single educational anchor is **Lin Lin, _Lecture Notes on Quantum Algorithms for Scientific Computation_, March 3, 2022 author revision**: [PDF](https://math.berkeley.edu/~linlin/qasc/qasc_notes.pdf), [course page](https://math.berkeley.edu/~linlin/qasc/). All section and page references below use that revision. Its January 2022 arXiv record is an earlier version; the later Lin–Wiebe live notes have different authorship and numbering. The bibliography identifies this source as `lin2022qasc`.

| Anchor sections; printed pages | Use here | Milestones |
|---|---|---|
| §1.1.3, pp. 9–10; §1.5, pp. 16–19 | Measurements, moments and sampling | M01–M02, M06 |
| §§1.6–1.10, pp. 19–25 | Reversible gates, approximation and costs | M03–M04, M09–M10 |
| §§2.2–2.3, pp. 30–34 | Reflections and the Grover plane | M04–M05 |
| §§3.3–3.5, pp. 45–52 | Fourier circuits and phase kickback | M07–M08 |
| §4.2, pp. 57–58 | Probability estimation through Grover phases | M11 |

These are entry points, not an assignment to read the whole source. The path-observable calculation, explicit sine-transform circuit, compiled endpoint argument and statistical applications are supplied below and in the linked scientific pages. Their primary research references remain separate from the educational anchor.

| Source notation | Project notation and convention |
|---|---|
| Preparation $`U_{\psi_0}`$, state $`\psi_0`$, probability $`p_0`$ | $`A`$, $`\psi`$, $`p`$ |
| Grover angle $`\theta`$ in §4.2 | $`\phi`$, with $`p=\sin^2(\phi/2)`$ |
| Fractional eigenphase in Chapter 3 | $`\pm\phi/(2\pi)`$ modulo one |
| Basis ordered good, bad in Eq. (4.23) | Basis ordered bad, good in the project proof |

Reversing that basis order reverses the signs of the off-diagonal matrix entries; it does not change the eigenphase pair. The reflection convention itself agrees: $`G=(2|\psi\rangle\langle\psi|-I)(I-2\Pi)`$. The source's simplified exact-binary-phase examples are not hypotheses here. Nor do we restrict $`p`$ to be small: the project theorem holds throughout $`[0,1]`$.

## 1. A complete three-outcome example

**Route: M01–M07, then M12–M15.** Take two input bits in uniform superposition and compute their AND into a flag with a Toffoli gate. The sampler $`A`$ is two Hadamards followed by that Toffoli. The success projector tests whether the flag is one. Exactly one of the four inputs succeeds, so $`p=1/4`$. The flag and both input qubits belong to the sampler register. This small example is classically transparent; its purpose is to expose the operation.

A direct flag measurement returns a Bernoulli variable: one with probability $`p`$, zero otherwise. Its mean is $`p`$ and its variance is $`p(1-p)`$. Unbiasedness means that mean identity, not that each realized output equals $`p`$.

Now choose $`M=3`$, so $`L=4`$ and $`\alpha=\pi/4`$. On the three valid clock labels, prepare

```math
a=\begin{pmatrix}1/2\\1/\sqrt2\\1/2\end{pmatrix},
\qquad
D=\begin{pmatrix}
1/2&1/\sqrt2&1/2\\
1/\sqrt2&0&-1/\sqrt2\\
1/2&-1/\sqrt2&1/2
\end{pmatrix}.
```

Apply $`G`$, $`G^2`$ or $`G^3`$ coherently according to the clock label, apply $`D`$, and measure the clock. The three labels are assigned outputs $`0,1/2,1`$. Nothing is rejected, and the success flag itself is not measured during this coherent run.

Here is the full outcome law. On one Grover eigenphase branch the clock is $`v_r=a_r e^{ir\phi}`$, where $`\cos\phi=1-2p`$. Multiplying by $`D`$ gives

```math
Dv=e^{2i\phi}
\begin{pmatrix}
(1+\cos\phi)/2\\
-i\sin\phi/\sqrt2\\
(\cos\phi-1)/2
\end{pmatrix}.
```

The other branch is its complex conjugate and has the same probabilities. Squaring the three absolute values therefore gives the actual distribution:

| Output $`Z`$ | Probability | At $`p=1/4`$ |
|---:|---:|---:|
| $`0`$ | $`(1-p)^2`$ | $`9/16`$ |
| $`1/2`$ | $`2p(1-p)`$ | $`6/16`$ |
| $`1`$ | $`p^2`$ | $`1/16`$ |

Its mean is $`p(1-p)+p^2=p`$. Its second moment is $`p(1-p)/2+p^2`$, so its variance is $`p(1-p)/2`$, equal to $`3/32`$ in this example. The output is bounded and exactly unbiased in the ideal circuit.

This law is also the law of the mean of two independent Bernoulli samples. Yet the direct binary quantum schedule costs three controlled Grover steps, each using $`A`$ and $`A^\dagger`$, plus the initial $`A`$: **seven sampler or inverse calls**. It also needs reflections and both clock transforms. Two direct measurements obtain the same variance with two sampler calls. This example illustrates the mechanism and its guarantees; it does not give a computational saving.

## 2. Why the clock carries the probability

**Route: M04–M07, integrated in M11.** For $`0<p<1`$, normalize the good and bad parts of $`A|0\rangle`$ to obtain orthogonal states $`|g\rangle`$ and $`|b\rangle`$. In the ordered basis $`(|b\rangle,|g\rangle)`$,

```math
|\psi\rangle=\begin{pmatrix}\sqrt{1-p}\\\sqrt p\end{pmatrix},
\qquad
G=\begin{pmatrix}
1-2p&-2\sqrt{p(1-p)}\\
2\sqrt{p(1-p)}&1-2p
\end{pmatrix}.
```

This is a rotation with eigenvalues $`e^{\pm i\phi}`$. The prepared state has equal squared overlap with the two eigenvectors. Consequently ignoring the target after controlled powers gives an equal mixture of the two phased clocks $`a_re^{ir\phi}`$ and $`a_re^{-ir\phi}`$. No Grover eigenstate needs to be prepared. The argument also allows complex amplitudes inside the good and bad states.

At $`p=0`$ or $`1`$, use the direct statement $`G|\psi\rangle=|\psi\rangle`$ or $`- |\psi\rangle`$ instead of dividing by a zero probability. These endpoint phases will force deterministic outputs.

The source's phase-estimation route motivates using controlled powers. A phase estimate followed by a nonlinear function does not automatically have the right mean. This project instead chooses a clock observable whose expectation is exactly $`(1-\cos\phi)/2`$. That changes what must be proved: the spectrum determines the output range, and the observable's first two moments determine its statistics.

## 3. The missing spectral step

**Route: M06, M08, M12–M15.** A path adjacency matrix $`H`$ connects neighboring labels and has zero elsewhere. With zero boundary values $`a_0=a_{M+1}=0`$, choose

```math
\alpha=\frac{\pi}{M+1},\qquad c=\cos\alpha,
\qquad a_r=\sqrt{\frac{2}{M+1}}\sin(r\alpha).
```

The sine addition identity gives $`a_{r-1}+a_{r+1}=2ca_r`$, or $`Ha=2ca`$. The other sine vectors diagonalize the same matrix, with eigenvalues $`2\cos(j\alpha)`$. Thus applying the sine transform and assigning the scalar $`z_j`$ measures

```math
B=\frac12\left(I-\frac{H}{2c}\right),
\qquad z_j=\frac{1-\cos(j\alpha)/c}{2}.
```

Because $`-c\le\cos(j\alpha)\le c`$ on $`1\le j\le M`$, every possible output lies in $`[0,1]`$. The normalization by $`c`$ matters: omitting it would change the mean.

The relation $`Ha=2ca`$ also implies $`\sum_{r=1}^{M-1}a_ra_{r+1}=c`$. Adding phase $`e^{ir\phi}`$ multiplies the real part of this neighboring overlap by $`\cos\phi`$. Therefore

```math
\langle v|H|v\rangle=2c\cos\phi,
\qquad \mathbb EZ=\langle v|B|v\rangle
=\frac{1-\cos\phi}{2}=p.
```

For the variance, subtract the mean before taking a norm. The terms proportional to $`a_r`$ cancel, leaving a discrete derivative:

```math
[(B-pI)v]_r
=\frac{i\sin\phi}{4c}e^{ir\phi}(a_{r-1}-a_{r+1}),
\qquad
\sum_{r=1}^{M}(a_{r-1}-a_{r+1})^2
=4\frac{M-1}{M+1}\sin^2\alpha.
```

The squared norm is the variance. Using $`\sin^2\phi=4p(1-p)`$ gives

```math
\mathrm{Var}(Z)=\kappa_Mp(1-p),\qquad
\kappa_M=\frac{M-1}{M+1}\tan^2\alpha
\sim\frac{\pi^2}{M^2}.
```

The factor $`p(1-p)`$ explains both exact endpoints. The remaining factor explains the quadratic variance reduction with coherent clock size. [The proof](../science/variance-proof.md) evaluates the finite trigonometric sum and covers every $`M\ge2`$; the small example is not its justification.

Independent averaging divides this variance by the number of executions and preserves unbiasedness. A median-of-means wrapper gives a stronger confidence guarantee but is generally biased. Its repetition schedule needs a known variance bound, such as $`p(1-p)\le1/4`$, not the unknown value it is meant to estimate. See [the statistical contract](../science/model-and-estimator.md#repetition-and-statistical-guarantees).

## 4. Turn the sine transform into counted gates

**Route: M03, M07–M10, M16–M18.** A list of desired amplitudes is not yet an implementation. Choose the efficient family $`L=M+1=2^\ell`$. An odd embedding on $`\ell+1`$ data qubits maps a valid path label to

```math
E|0,r\rangle=\frac{|r\rangle-|2L-r\rangle}{\sqrt2}.
```

For the positive-exponent Fourier transform $`F_{2L}`$, the amplitude at $`s`$ after this embedding is

```math
\frac{e^{i\pi rs/L}-e^{-i\pi rs/L}}{2\sqrt L}
=\frac{i}{\sqrt L}\sin\!\left(\frac{\pi rs}{L}\right).
```

The amplitudes at $`s`$ and $`2L-s`$ have opposite signs. Pairing them in the odd basis adds the factor $`\sqrt2`$, yielding exactly $`iD_{sr}`$. Hence $`V=E^\dagger F_{2L}E`$ implements $`iD`$ on the path. Prepare with $`V`$ and read with $`V^\dagger`$; the common phase cancels. The high bit, spare label and reversible negation workspace all have specified behavior in [the circuit construction](../science/circuits-and-resources.md#odd-embedding-and-the-type-i-sine-transform).

The binary ladder uses $`1+2+\cdots+2^{\ell-1}=M`$ controlled Grover steps. A controlled step executes controlled success reflection, $`A^\dagger`$, controlled zero reflection, $`A`$, and a control $`Z`$. The last phase implements the minus sign in $`G=-AS_0A^\dagger S_g`$. A global sign on an uncontrolled unitary becomes a relative phase when controlled, so it cannot be dropped here.

This produces $`2M+1`$ sampler or inverse calls and two transforms. The [logical ledger](../science/circuits-and-resources.md#full-per-sample-ledger) additionally counts reflections, initialization, clean-work sharing, Fourier rotations and a hard-coded reversible 3CNF sampler. Output arithmetic evaluates only the measured cosine ratio with certified precision. There is no table of $`M`$ amplitudes to load and no QRAM assumption.

## 5. Preserve the useful structure at finite precision

**Route: M09, M19–M21.** Finite gate synthesis generally changes the exact mean. The implementation theorem therefore states a bias bound, while retaining bounded outputs. Its target is the probability of the actual fixed compiled sampler $`A`$, always paired with its exact reversed gate sequence $`A^\dagger`$. Both success and initial-state reflections are exact in this noiseless compiled model.

For the clock, pair one compiled transform $`\widetilde V`$ with its exact inverse. Retain any ancillary state that can remain occupied, give every output label a bounded scalar, and ensure that every phase exponent stays in $`0,\ldots,M`$. Exactly clean borrowed scratch may be restricted to its zero subspace, while still being charged in the width.

The rounded output must stay in $`[0,1]`$ and approximate the specified ideal output map within $`\rho`$. In particular, the starting label $`u=|0_{\mathrm{aux}},1\rangle`$ has output exactly zero. Assign the other canonical endpoint exactly one and every auxiliary or spare label zero; round only the interior values. Cancellation at zero phase then implies zero measured output, not merely a return to the starting state.

Why does this help near an endpoint? At zero phase the two compiled transforms cancel exactly. For other phases, equal averaging of $`+\phi`$ and $`-\phi`$ turns $`e^{i(r-s)\phi}`$ into $`\cos((r-s)\phi)`$, a polynomial of degree at most $`M`$ in $`x=(1-\cos\phi)/2`$. The first two moment errors are therefore polynomials $`e_i(x)`$ with $`e_i(0)=0`$. If their uniform bounds are $`\sigma_i`$, Markov's derivative inequality gives

```math
|e_i(x)|\le 2M^2\sigma_i x,
\qquad \sigma_1=2\eta_V+\rho,\quad \sigma_2=2\eta_V+2\rho,
```

where $`\eta_V`$ bounds transform operator error and $`\rho`$ bounds scalar rounding error. This is the extra step beyond a generic absolute perturbation estimate.

An independent direct success sample $`X`$ now selects the orientation. If $`X=0`$, estimate the event; if $`X=1`$, estimate its complement and return one minus that output. Writing the resulting estimate as $`W`$, its bias is

```math
\mathbb EW-p=(1-p)e_1(p)-pe_1(1-p),
```

so both terms carry $`p(1-p)`$. The complete result is

```math
|\mathbb EW-p|\le4M^2\sigma_1p(1-p),
\qquad
\mathrm{Var}(W)\le
[\kappa_M+4M^2(\sigma_1+\sigma_2)]p(1-p).
```

At either endpoint the orientation chooses a zero-probability primitive, making the final output exact in this noiseless compiled model. The orientation sample costs one extra preparation, measurement and reset. [Finite precision](../science/finite-precision.md) supplies the second-moment derivation, explicit precision choices and confidence allocation. Approximation of a separate intended sampler and hardware faults have additional budgets; arbitrary noise does not preserve the exact endpoints.

## 6. Read the application branches with their conditions

**Route: M22–M27.** Two distinct uses become available after the core theorem.

For independent nonnegative estimates of factors $`p_i`$, the product has mean $`\prod_i p_i`$. This identity can supply an unbiased random likelihood weight. In pseudo-marginal sampling, augmenting the state by the current weight gives a target density proportional to $`\rho(\theta)wD_\theta(dw)`$. Integrating out the weight yields $`\rho(\theta)\mathbb Ew`$, the desired marginal. Retaining that weight after a rejection is part of the algorithm. The [positive-weight account](../science/positive-weights.md) derives the product variance, perturbed target bounds and exact acceptance requirements. These claims do not establish faster mixing: a lower variance need not give a more favorable distribution for every use.

The compiled bias bound also has a useful relative meaning. If $`|\mu_i-p_i|\le\beta_i p_i(1-p_i)`$ with $`0\le\beta_i<1`$, then for $`p_i>0`$ the mean ratio $`\mu_i/p_i`$ lies in $`[1-\beta_i,1+\beta_i]`$. Conditional independence multiplies these intervals for a likelihood product. Controlling the ratio before and after normalization then bounds the perturbed target distribution, without dividing by a minimum positive compiled probability. Zero factors remain zero by endpoint exactness. The scientific page supplies the sharp normalization bound and its separate intended-model conditions.

For ideal state restoration, the measurement's action on the target matters as well as its clock probabilities. Centering the physical powers for odd $`M`$ makes each outcome operator proportional to either the identity or a fixed involution on one Grover plane. Tracking the parity of involution outcomes allows restoration while keeping the first estimate. The [restoration proof](../science/restoration.md) gives an interior mean of two rounds, but an unbounded stopping tail. This is a separate ideal extension; it does not inherit the destructive estimator's deterministic work cap or a generic finite-synthesis guarantee.

## 7. Join the result to a fair comparison

**Route: M28–M30.** Sine probes, finite cosine observables, fast sine transforms and amplitude-estimation speedups all have predecessors. The [primary-source comparison](../references/related-work.md) distinguishes the joint guarantee here: bounded output, exact ideal unbiasedness, uniform variance proportional to $`p(1-p)`$, and deterministic costly calls, together with an explicit implementation and a qualified finite-precision route.

For ideal independent averaging, let $`\tau_Q`$ be the complete cost of one quantum output and $`\tau_B`$ the cost of one direct Bernoulli sample in the same units. Comparing cost to attain the same variance gives the criterion $`\kappa_M\tau_Q<\tau_B`$. Counting only sampler calls is one partial comparison. Physical time also needs synthesis, connectivity, error correction, measurements, resets, classical work and an appropriate classical competitor.

The final understanding target is to connect the executable input to its measured probability, its estimator law, its compiled error budget and the total cost of its intended use. The [resource interpretation](../science/interpretation.md) joins these statements. The [verification guide](../verification/README.md) shows which finite examples can be reproduced and where the written universal proofs remain necessary.
