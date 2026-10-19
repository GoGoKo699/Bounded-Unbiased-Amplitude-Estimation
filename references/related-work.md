# Related work and scope of the contribution

Primary sources were checked on 2026-10-19. The comparisons below refer to the indicated theorem and version, rather than to an informal use of “unbiased.” Citation keys refer to [bibliography.bib](bibliography.bib).

## The object being compared

The [ideal theorem](../science/model-and-estimator.md) concerns the probability $p=\|\Pi A|0\rangle\|^2$. For every $M\ge2$, a fixed circuit returns

$$
Z\in[0,1],\qquad \mathbb EZ=p,\qquad
\operatorname{Var}(Z)=\kappa_Mp(1-p),\qquad
\kappa_M=\frac{M-1}{M+1}\tan^2\!\frac{\pi}{M+1}.
$$

There is no additive variance floor at either endpoint. The binary implementation for $M+1=2^\ell$ uses exactly $M$ controlled Grover steps, or $2M+1$ sampler/inverse calls including initial preparation. This is a destructive estimator: it makes no state-restoration promise.

The distinction under examination is the **conjunction** of an exact first moment, bounded nonnegative outputs, an explicit variance identity uniform in $p$, and a deterministic $O(M)$ expensive-call budget independent of the requested bias tolerance. None of exact unbiasedness, low bias, positive outputs, fixed query budgets, sine probes, or efficient sine transforms is individually new. Finite gate synthesis gives an approximately unbiased estimator, under the separate assumptions in [Finite precision](../science/finite-precision.md).

## Closest estimation results

In this table, “fixed” means a deterministic query bound for the stated accuracy parameters; it does not mean that the bound is independent of those parameters. A reflection query and a sampler query are different primitives. When $A$ is explicitly available, a state reflection costs an $A^\dagger$, a full-register zero reflection, and an $A$; the native costs must still be charged.

| Source and result | Target and output | Moment or error guarantee | Budget and relevant distinction |
|---|---|---|---|
| Cornelissen–Hamoudi, arXiv:2207.08643, Theorem 2.4 (`corneli2023partition`) | Probability $p$; output in $[-2\pi,2\pi]$ | Bias at most $\nu$; variance at most $91p/t^2+\nu$ | Expected $O(t\log\log t\log(t/\nu))$ reflections; restores the supplied state with probability at least $1-\nu$ |
| Miyamoto, arXiv:2406.01889v2, Theorem 2 (`miyamoto2025dividing`) | Probability, called $a$ there; real output, with no $[0,1]$ guarantee in the theorem | Bias at most $\delta$; MSE at most $\epsilon^2+\delta$ | **Deterministic** $O(\epsilon^{-1}\log\log(1/\epsilon)\log(1/(\delta\epsilon)))$ calls to $A$; prepares fresh states instead of restoring one |
| Rall–Fuller, Theorem 23 (`rall2023qsp`) | Amplitude $a=\|\Pi\psi\|$; interval-refinement output in $[0,1]$ | Failure probability at most $\delta$ for error $\epsilon$; bias at most $\epsilon\eta+\delta$ | Fixed $O(\epsilon^{-1}(\eta^{-1}+\log(1/\delta)))$ query bound; bounded low-bias output is already available |
| van Apeldoorn et al., arXiv:2207.08800, §§6.2–6.4 (`vanapeldoorn2023tomography`) | Probability $p$; estimates can fall outside $[0,1]$ | Ideal exact unbiasedness; variance $O(p(1-p)/M^2+M^{-4}+e^{-m/4})$ after boosting | Random phase shift, $2m+1$ phase samples, normalization by a clock-dependent scalar; finite-precision treatment is separate |
| Ambainis–Gilyén–Kokainis, arXiv:2610.06803v1, Corollary 5 (`ambainis2026hybrid`) | Probability $p$ in the large-$q$ branch; no $[0,1]$ restriction | Ideal exact unbiasedness; variance $O(p(1-p)/q^2+q^{-4})$ | Fixed $O(q)$ query block with nine phase-clock copies in the stated regime $q\ge\max\{270,[p(1-p)]^{-1/2}\}$; intermediate-depth branch permits bias |
| This repository, ideal destructive block | Probability $p$; $[0,1]$ | Exact mean $p$ and exact variance $\kappa_Mp(1-p)$ | Fixed $M$ controlled Grover steps for the efficient clock family; no preliminary estimate of $p$ |

### What these comparisons rule out

[Cornelissen–Hamoudi](https://arxiv.org/pdf/2207.08643) already obtain variance proportional to a small success probability, together with arbitrarily suppressed bias and state reuse. Their theorem is a stronger access-model result in one respect: it starts with one supplied state and reflections, rather than assuming repeated inexpensive preparations. Its expected-work restoration cannot be compared to a destructive fixed block without noting that difference. Choosing the smaller event can also turn a $p$ dependence into a dependence comparable to $p(1-p)$; this does not by itself provide an unknown-$p$, exact bounded estimator.

[Miyamoto's 2025 paper](https://arxiv.org/html/2406.01889v2#S2.SS5) explicitly modifies the Cornelissen–Hamoudi construction by omitting unbounded restoration loops. Thus **fixed-budget nearly unbiased amplitude estimation is already established**. The comparison here is against its bias-dependent expensive-call overhead and stated moment guarantee, not against a purported absence of fixed budgets. The paper also already uses low bias to control accumulated errors in a stochastic-process application. Separately, [Miyamoto's 2024 iterative-estimation paper](https://arxiv.org/html/2311.16560v2) (`miyamoto2024bias`) studies bias from adaptive termination and a mitigation that reruns the final round with fixed parameters; it is not the 2025 theorem.

[Rall–Fuller](https://arxiv.org/pdf/2207.08628) already supply positive bounded low-bias estimates. Their target is a square-root amplitude, but this alone is not a substantive separation: a probability can be represented as a suitable overlap amplitude using a state-preparation unitary and its inverse. The material differences are the exact first moment, the uniform explicit second moment, and the dependence of costly queries on bias tolerance.

The exact probability estimator in [van Apeldoorn et al.](https://arxiv.org/html/2207.08800v1#S6.SS3) is an especially close predecessor. It debiases a circular phase estimate by dividing its real part by a normalization smaller than one, allowing values outside the probability interval. The $M^{-4}$ term matters when $p(1-p)\ll M^{-2}$. The finite-precision subsection proves a discretization bound for the basic shifted-phase algorithm and expressly leaves part of the boosted symmetry analysis unresolved; it should not be cited as an exact finite-gate unbiasedness theorem.

[Ambainis–Gilyén–Kokainis](https://arxiv.org/html/2610.06803v1#S8) sharpen that route and establish the optimal hybrid query tradeoff. With a known upper bound $v$ on the Bernoulli variance and in their stated precision regime, the tradeoff is

$$
\Theta\!\left(\frac{\sqrt v}{\epsilon}+\frac{v}{q\epsilon^2}\right).
$$

Their exact large-$q$ construction already matches the same scaling when its additive $q^{-4}$ variance term is dominated. Their intermediate regime uses amplification and a potentially biased inversion. The present fixed clock handles both regimes with the same bounded output law; it does **not** improve the general query exponent, prove a new hybrid lower bound, or establish a better finite-$M$ optimal constant.

[Vu–Cheng–Rebentrost](https://arxiv.org/html/2410.01173v1) (`vu2025lowdepth`) already explain how averaging suitably low-bias quantum estimators produces parallel low-depth algorithms. Averaging a better-specified estimator is therefore a consequence of its moments, not a new general parallelization principle. The older amplitude-amplification and estimation framework is [Brassard–Høyer–Mosca–Tapp](https://arxiv.org/abs/quant-ph/0005055) (`brassard2002amplitude`).

## Suruga's generalized Hadamard test

[Suruga, arXiv:2509.05710v2](https://arxiv.org/html/2509.05710v2) (`suruga2025hadamard`), Proposition 1 and the proof in §4, already construct exact unbiased estimators for polynomial functions of a unitary. Its generalized Hadamard test uses $2m$ controlled-unitary calls for the represented degree-$m$ inner product. The resulting generic complex estimator can take values such as $3-i$ and $-1-i$; Proposition 1's PAC complexity depends on the squared trace norm of the representing matrix and on $\epsilon^{-2}$. Theorem 1's main approximation criterion is Haar-averaged squared bias.

A success probability is itself a polynomial in matrix entries, so **exact unbiasedness of a polynomial function is not a distinction from this work**. What its stated construction does not supply is the present family of $[0,1]$ outputs with variance exactly $\kappa_Mp(1-p)$ and a specified polylogarithmic clock implementation. Deriving that family from the general representation theorem would require a new choice of measurement and a sharper per-instance second-moment analysis; the theorem's norm bound alone does not give it.

## The measurement and circuit ingredients are established

The key observable is a finite path adjacency matrix, or a finite-dimensional cosine-of-phase operator. [Susskind–Glogower](https://journals.aps.org/ppf/pdf/10.1103/PhysicsPhysiqueFizika.1.49) (`susskind1964phase`), pp. 58–59, derive the fixed-total-excitation recurrence and its sine eigenvectors in Eq. (41). This is the same finite-path spectral structure, up to scaling and labels. Their Eqs. (43)–(45) analyze a flat-coefficient phase state. The cosine observable and its sine diagonalization should therefore be attributed to this established construction; the repository studies a particular sine probe, affine output calibration, and its exact Bernoulli-variance identity.

Sine-shaped probes are also established in phase estimation. [Berry–Wiseman](https://arxiv.org/abs/quant-ph/0009117) (`berry2000phase`) study optimal interferometric states for a phase cost. [Babbush et al.](https://arxiv.org/pdf/1805.03662), §II.B (`babbush2018spectra`), use a sine clock and give an efficient preparation method. [Najafi–Costa–Berry](https://arxiv.org/abs/2303.12503) (`najafi2023phase`) implement optimum phase estimation with two control qubits. These works make neither the sine profile nor efficient preparation a new ingredient. Their phase readouts and costs do not directly imply the exact moments of the calibrated path-observable readout used here.

[Klappenecker–Roetteler](https://arxiv.org/html/quant-ph/0111038v1), Theorem 1 (`klappenecker2001dct`), already implement type-I sine and cosine transforms with $O(\log^2N)$ elementary gates by embedding them in a Fourier transform. The [explicit circuit](../science/circuits-and-resources.md) specializes that known transform structure, tracks unused labels and phases, and counts the preparation/readout pair. It is not a new quantum sine-transform algorithm. The standard compiler ingredients are [Ross–Selinger](https://arxiv.org/abs/1403.2975) (`ross2014zrotations`), with its stated number-theoretic/expected-runtime qualifications, and [Dawson–Nielsen](https://arxiv.org/abs/quant-ph/0505030) (`dawson2005solovay`) for a general polylogarithmic Solovay–Kitaev bound. [Selinger](https://arxiv.org/abs/1210.0974) (`selinger2013tdepth`) supplies standard Clifford+$T$ circuit background.

## Finite synthesis is a distinct result

The [finite-precision analysis](../science/finite-precision.md) does not claim exact unbiasedness from a finite approximate QFT. It uses an approximate transform and its exactly reversed circuit to preserve one endpoint, then an independent Bernoulli draw to choose whether to estimate the event or its complement. Polynomial moment stability gives bias and mean-square-error bounds proportional to $p(1-p)$; the linked theorem states the constants and separate transform/readout error parameters. Its derivative step uses the classical first-derivative inequality of A. A. Markov. A modern research source stating the sharp $n^2$ bound is [Bun–Thaler](https://arxiv.org/html/1302.6191v3#S5), §5 (`bun2015dual`); their work supplies new duality proofs of related inequalities, not the historical origin of the bound.

This preserves the rare-event scale without inserting a positive lower bound on $p$. The comparison is with the **compiled sampler's probability**. A generic additive approximation bound for a different intended sampler does not become a relative bound near zero. The sampler-call count stays fixed as the requested bias decreases, but rotation synthesis and classical output precision increase. Consequently, there is no claim of unlimited accuracy from one fixed finite native circuit or at a nonzero uncontrolled hardware-noise floor.

## Positive weights and restoration

The use of a nonnegative unbiased estimate in an extended target is the established [Andrieu–Roberts pseudo-marginal construction](https://arxiv.org/pdf/0903.5480), §2 (`andrieu2009pseudomarginal`). The [positive-weight note](../science/positive-weights.md) applies that identity and derives product-error consequences of the estimator's moments. Correct stationary marginals do not prove fast mixing. In particular, [Deligiannidis–Doucet–Pitt](https://doi.org/10.1111/rssb.12280) (`deligiannidis2018correlated`) correlate successive likelihood estimates; this is a relevant classical competitor to any application-level comparison based only on independent factor averaging. The repository makes no universal pseudo-marginal runtime claim.

Witness-preserving amplification and state recovery have substantial prior art, including [Marriott–Watrous](https://arxiv.org/abs/cs/0506068) (`marriott2005amplification`) and [Nagaj–Wocjan–Zhang](https://arxiv.org/abs/0904.1549) (`nagaj2009fast`). More directly, [Harrow–Wei](https://arxiv.org/html/1907.09965v2#S4), Algorithm 5 and Theorem 18 (`harrow2020annealing`), restore the input following amplitude estimation through repeated projections, with an expected constant number of restoration attempts and a high-probability nondestructive estimation guarantee. Generic restoration is therefore not a new claim.

The separate [ideal restoration note](../science/restoration.md) identifies a particularly simple parity law for this instrument and retains the first estimate while returning the target state. Its repeat-until-return tail is unbounded. It must not be combined with the destructive block's deterministic budget, and approximate synthesis is not asserted to preserve its exact parity law.

## What is established here, and what is not

The mathematical contribution tested in this repository is the explicit joint moment identity for the calibrated sine/DST measurement and its endpoint-sensitive finite-synthesis implementation. The primary comparisons above identify the concrete gap between that conjunction and the cited constructions; they also identify the ingredients and broader estimation tradeoffs that are already established.

This account does not turn an oracle-call saving into a practical speedup. [Circuits and resources](../science/circuits-and-resources.md) charges the reversible sampler, its inverse, reflections, clock, precision and readout, including a compiled Boolean example without QRAM. [Interpretation](../science/interpretation.md) states the additional condition needed for a runtime advantage and the remaining hardware and classical-competitor costs. No physical runtime advantage, universal MCMC improvement, finite-size minimax theorem, or first-ever unbiased quantum estimator is claimed.
