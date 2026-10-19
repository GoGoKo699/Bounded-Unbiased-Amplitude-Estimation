# Finite precision

The [ideal estimator](model-and-estimator.md) is exactly unbiased. A finite gate sequence with rounded classical outputs generally has a small bias. This page gives a quantitative implementation that keeps the output in $`[0,1]`$, preserves variance proportional to $`p(1-p)/M^2`$, and fixes both endpoints exactly in the compiled, noiseless circuit model. Its precision requirement is independent of any minimum nonzero value of $`p`$.

The construction uses the same compiled clock transform for preparation and its exact reversed gate sequence for readout. One independent Bernoulli sample chooses whether to estimate the event or its complement. Hardware faults and inaccuracies in the intended input model require separate budgets.

## 1. Circuit assumptions and the full output map

Use the notation of [Model and estimator](model-and-estimator.md): $`A`$ is the actual compiled sampler unitary, including its work registers,

```math
|\psi\rangle=A|0\rangle,\qquad
p=\langle\psi|\Pi|\psi\rangle,\qquad
G=(2|\psi\rangle\langle\psi|-I)(I-2\Pi).
```

For now, the compiled gates execute without additional noise. The success reflection and initial-state reflection are exact, and every use of $`A^\dagger`$ is the exact inverse of the same compiled $`A`$. A success flag computed within $`A`$ is one way to meet the success-reflection assumption. Independently approximating a nominal inverse or using an approximate non-involutory reflection is outside these assumptions.

Let $`M\ge2`$, $`L=M+1`$, $`\alpha=\pi/L`$, and

```math
z_j=\frac{1-\cos(j\alpha)/\cos\alpha}{2},\qquad
\kappa_M=\frac{M-1}{M+1}\tan^2\alpha.
```

The clock implementation has a full retained Hilbert space $`\mathcal C`$, including every ancillary register that can remain occupied after its transform. Scratch that both the ideal and compiled transforms return to zero exactly can be restricted to that invariant zero subspace. Such scratch is still charged in the circuit width, but may be borrowed by the controlled reflections while clean; no behavior on its unreachable dirty states is assumed. Any retained synthesis garbage and the high clock bit remain in $`\mathcal C`$. Its canonical path states are $`|0_{\mathrm{aux}},r\rangle`$, $`1\le r\le M`$. Write

```math
|u\rangle=|0_{\mathrm{aux}},1\rangle.
```

The ideal full unitary $`V`$ preserves the canonical path subspace and implements the sine transform there, possibly with a common global phase. The compiled unitary $`\widetilde V`$ obeys

```math
\|\widetilde V-V\|\le\eta_V.
\tag{1}
```

An irrelevant global phase may be chosen when evaluating (1). Readout uses the exact inverse $`\widetilde V^\dagger`$, not a separately synthesized approximation to $`V^\dagger`$.

Specify the controlled power on **every** clock basis state. We require orthogonal projectors $`P_0,\ldots,P_M`$, summing to the identity on $`\mathcal C`$, such that it applies $`G^r`$ on $`P_r`$. On the canonical path, $`P_r`$ selects label $`r`$. For the efficient family $`L=2^\ell`$, the low $`\ell`$ clock bits encode $`r\in\{0,\ldots,M\}`$; all auxiliary bits are ignored by the power ladder. Thus leakage into a spare or auxiliary state still receives an exponent between $`0`$ and $`M`$. For another binary encoding, its unused labels must be assigned exponents in this same range, or the degree bound below must be changed.

Define the ideal output function on every measurement label $`b`$ by

```math
z(b)=
\begin{cases}
z_j,&b=(0_{\mathrm{aux}},j),\quad 1\le j\le M,\\
0,&\text{otherwise.}
\end{cases}
\tag{2}
```

Use a deterministic classical output map $`\widetilde z`$ satisfying

```math
0\le\widetilde z(b)\le1,\qquad
|\widetilde z(b)-z(b)|\le\rho,\qquad
\widetilde z(u)=0.
\tag{3}
```

In particular, set all auxiliary-label outputs to zero and set the canonical endpoint outputs to exactly zero and one. Evaluate the other values with certified error at most $`\rho`$, then clip to $`[0,1]`$; clipping cannot increase their error. No amplitude lookup table is required.

Ancillas cannot be discarded between $`\widetilde V`$ and $`\widetilde V^\dagger`$. They may be reused as clean workspace only if the actual compiled preparation returns them to zero exactly. The specified [QFT-based circuit](circuits-and-resources.md) has this property for its reversible arithmetic scratch: only its QFT rotations are approximated, using ancilla-free synthesis, and its exact arithmetic uncomputes its scratch for every data label. Its potentially occupied high clock bit remains part of $`\mathcal C`$.

## 2. Uniform errors in the first two moments

For a Grover eigenphase $`\phi`$, let

```math
P(\phi)=\sum_{r=0}^{M}e^{ir\phi}P_r.
```

The ideal and compiled readout states are

```math
|\chi_\phi\rangle=V^\dagger P(\phi)V|u\rangle,
\qquad
|\widetilde\chi_\phi\rangle
=\widetilde V^\dagger P(\phi)\widetilde V|u\rangle.
```

Unitary invariance and the triangle inequality give

```math
\|\,|\widetilde\chi_\phi\rangle-|\chi_\phi\rangle\,\|
\le2\eta_V.
\tag{4}
```

The total variation distance between the corresponding measurement distributions is at most $`2\eta_V`$: measurement cannot increase trace distance, and pure-state trace distance is at most the Euclidean distance between state vectors. This also bounds the equal mixture of the $`+\phi`$ and $`-\phi`$ distributions.

For $`x=(1-\cos\phi)/2`$, denote the compiled primitive's output by $`\widetilde Z_x`$, and write

```math
\begin{aligned}
\mathbb E\widetilde Z_x&=x+e_1(x),\\
\mathbb E\widetilde Z_x^2
&=x^2+\kappa_M x(1-x)+e_2(x).
\end{aligned}
\tag{5}
```

The [ideal moment identities](variance-proof.md), (2)–(4), and boundedness give

```math
\boxed{\quad
\|e_1\|_{\infty,[0,1]}\le\sigma_1:=2\eta_V+\rho,
\qquad
\|e_2\|_{\infty,[0,1]}\le\sigma_2:=2\eta_V+2\rho.
\quad}
\tag{6}
```

For the second inequality, use
$`|\widetilde z^2-z^2|\le2|\widetilde z-z|`$.
The statistical contribution is $`2\eta_V`$, rather than twice that value, because an expectation of a function in $`[0,1]`$ changes by at most the total variation distance.

## 3. Endpoint stability from a polynomial bound

**Lemma.** Under the assumptions above, $`e_1,e_2`$ are real polynomials of degree at most $`M`$, they vanish at zero, and

```math
|e_i(x)|\le d_i x,
\qquad d_i:=2M^2\sigma_i,
\qquad 0\le x\le1.
\tag{7}
```

**Proof.** The prepared target state $`A|0\rangle`$ has equal squared weight on the two Grover eigenphases. This remains true for a complex sampler circuit. Consequently every compiled clock moment averages the $`+\phi`$ and $`-\phi`$ contributions with equal weights, even though $`\widetilde V`$ need not be real.

Expanding a moment in the projectors $`P_r,P_s`$ gives phase factors $`e^{i(r-s)\phi}`$. The equal mixture replaces these by

```math
\cos((r-s)\phi)=T_{|r-s|}(1-2x),
```

where $`T_k`$ is the degree-$`k`$ Chebyshev polynomial. The observable is Hermitian, so the resulting polynomial has real coefficients. Since $`0\le r,s\le M`$, both raw moments have degree at most $`M`$. Subtracting the ideal moments in (5) preserves this bound because $`M\ge2`$. This explains why spare-label exponents and the equal phase weights are part of the assumptions.

At $`x=0`$, the phase operator is the identity, so the paired circuits cancel:

```math
\widetilde V^\dagger P(0)\widetilde V|u\rangle=|u\rangle.
```

Equation (3) then makes both raw moments exactly zero. Hence $`e_i(0)=0`$.

Markov's polynomial inequality on $`[0,1]`$ states that a degree-$`M`$ real polynomial $`q`$ satisfies

```math
\|q'\|_{\infty,[0,1]}
\le2M^2\|q\|_{\infty,[0,1]}.
```

The factor two comes from rescaling the interval $`[-1,1]`$. Apply this inequality to (6) and integrate from zero to $`x`$. This proves (7). $`\square`$

A generic absolute-error comparison alone would leave a variance floor of order $`\eta_V+\rho`$. Equation (7) instead makes the moment errors vanish at least linearly with the estimated probability. It does not, by itself, fix the endpoint $`x=1`$.

## 4. One Bernoulli sample fixes both endpoints

Obtain an independent sample $`X\sim\mathrm{Bernoulli}(p)`$ by preparing $`A|0\rangle`$ and measuring success. Reset the quantum registers. Then run one fresh compiled primitive:

- if $`X=0`$, estimate the original event and return $`W=\widetilde Z_p`$;
- if $`X=1`$, estimate the complementary event and return $`W=1-\widetilde Z_{1-p}`$.

The clock transform and output map are unchanged in the second branch. Complementing $`\Pi`$ changes the Grover operator to $`-G`$, which is implemented by an additional phase on the power-ladder control. No value of $`p`$ is needed. The Bernoulli sample must use the same actual sampler and success definition as the subsequent primitive, and its randomness must be independent of that fresh run.

**Theorem: compiled moment guarantee.** The output satisfies $`W\in[0,1]`$ and

```math
\boxed{\displaystyle
|\mathbb EW-p|
\le4M^2\sigma_1\,p(1-p),
}
\tag{8}
```

```math
\boxed{\displaystyle
\mathrm{Var}(W)
\le\mathbb E(W-p)^2
\le\bigl[\kappa_M+4M^2(\sigma_1+\sigma_2)\bigr]p(1-p).
}
\tag{9}
```

At $`p=0`$ and $`p=1`$, the output is respectively zero and one with certainty.

**Proof.** Conditioning on the independent orientation sample gives

```math
\mathbb EW-p=(1-p)e_1(p)-p e_1(1-p).
```

Using (7) bounds its magnitude by $`2d_1p(1-p)`$, proving (8). For the mean-square error, direct expansion gives the useful exact identity

```math
\begin{aligned}
\mathbb E(W-p)^2
={}&\kappa_M p(1-p)
 +(1-p)e_2(p)+p e_2(1-p)\\
 &-2p(1-p)\,[e_1(p)+e_1(1-p)].
\end{aligned}
```

The two second-moment errors contribute at most $`2d_2p(1-p)`$. The last line contributes at most $`2d_1p(1-p)`$, because $`|e_1(p)|+|e_1(1-p)|\le d_1`$. Substituting the definitions of $`d_i`$ proves (9). At either endpoint the orientation is deterministic and selects the primitive for a zero-probability event. Its paired transforms return $`|u\rangle`$ exactly. $`\square`$

The endpoint statement concerns the actual compiled probability $`p`$. It does not imply exact endpoints for a different intended model, or under arbitrary hardware faults. Exact unbiasedness is recovered when $`\eta_V=\rho=0`$; (8) is the bias guarantee at finite precision.

## 5. Explicit precision choices and confidence bounds

If both $`\eta_V\le s`$ and $`\rho\le s`$, equations (8)–(9) simplify to

```math
|\mathbb EW-p|\le12M^2s\,p(1-p),
\qquad
\mathbb E(W-p)^2
\le(\kappa_M+28M^2s)\,p(1-p).
\tag{10}
```

For a desired bias bound $`\beta p(1-p)`$ and variance inflation at most $`1+\lambda`$, it is sufficient to choose

```math
s\le
\min\!\left\{\frac{\beta}{12M^2},
\frac{\lambda\kappa_M}{28M^2}\right\},
\qquad \beta,\lambda>0.
\tag{11}
```

This conditional moment statement is useful in [positive-weight compositions](positive-weights.md).

Here is a simple choice using only rational functions of $`M`$ and an additive accuracy $`0<\varepsilon<1`$:

```math
\boxed{\displaystyle
s=\min\!\left\{\frac{1}{28M^4},
\frac{\varepsilon}{12M^2}\right\},
\qquad \eta_V\le s,\quad\rho\le s.
}
\tag{12}
```

For $`M\ge2`$, $`\kappa_M\ge M^{-2}`$. Indeed, $`\tan\alpha\ge\alpha`$, $`(M-1)/(M+1)\ge1/3`$, and $`M/(M+1)\ge2/3`$ imply $`M^2\kappa_M\ge4\pi^2/27>1`$. Thus (12) guarantees

```math
|\mathbb EW-p|\le\varepsilon/4,
\qquad
\mathrm{Var}(W)\le2\kappa_M p(1-p).
\tag{13}
```

There is no hidden $`\log(1/p)`$ precision cost. To use a smaller variance promise, however, the repetition count still needs a known bound $`v\ge p(1-p)`$.

For example, reserve $`\varepsilon/4`$ for intended-model error as described next. With (12), form groups of

```math
b=\max\!\left\{1,
\left\lceil\frac{32\kappa_M v}{\varepsilon^2}\right\rceil\right\}
```

independent outputs $`W`$, and return the median of an odd number $`K\ge8\ln(2/\delta)`$ of group means. By Chebyshev, each group deviates from $`\mathbb EW`$ by more than $`\varepsilon/2`$ with probability at most $`1/4`$. Hoeffding's inequality then bounds the median's failure probability by $`e^{-K/8}\le\delta/2`$. The remaining $`\delta/2`$ can cover execution faults. The median remains bounded, but is not generally unbiased.

## 6. Actual compiled probability versus the intended model

Let $`A_\star`$ be the intended sampler and $`A`$ its fixed compiled implementation, with the same success projector. Define

```math
p_\star=\|\Pi A_\star|0\rangle\|^2,
\qquad p=\|\Pi A|0\rangle\|^2.
```

If $`\|A-A_\star\|\le\eta_A`$, then

```math
|p-p_\star|
\le\tfrac12\bigl\|
|\psi\rangle\langle\psi|-|\psi_\star\rangle\langle\psi_\star|
\bigr\|_1
\le\|\,|\psi\rangle-|\psi_\star\rangle\,\|
\le\eta_A.
\tag{14}
```

Using $`\eta_A\le\varepsilon/4`$ completes the accuracy allocation in the preceding confidence construction. The bias in (14) is **not multiplied by $`M`$**: the Grover operator is exactly the reflection product for the actual $`A|0\rangle`$, and its probability is $`p`$. This reasoning relies on reusing the same $`A`$ and its exact inverse. Errors in individual executions that do not fit that fixed unitary model belong in the noise budget below.

A variance promise for the intended probability must also be transferred. If $`v_\star\ge p_\star(1-p_\star)`$, then

```math
v=\min\{1/4,\ v_\star+\eta_A\}
```

is a valid bound for the compiled probability, because $`x(1-x)`$ is 1-Lipschitz on $`[0,1]`$. An absolute model approximation does not, in general, preserve relative error for an arbitrarily rare intended event.

## 7. Synthesis, classical output, and the gate cap

For $`L=2^\ell`$, the [explicit sine-transform circuit](circuits-and-resources.md) has $`N=O(\ell^2)`$ arbitrary single-qubit rotations after decomposing controlled phase gates, together with exact reversible arithmetic. Compile every such rotation to operator error at most $`\eta_V/N`$. Telescoping gives (1). Reverse this same sequence for readout. With a certified synthesis cost $`S(\xi)`$ per rotation at precision $`\xi`$, one transform costs

```math
g_V=O\!\left(\ell^2 S(\eta_V/\ell^2)+\ell\right).
```

Constructive Solovay–Kitaev synthesis provides unconditional polylogarithmic gate and classical compilation costs. More efficient Clifford+T rotation compilers can give logarithmic T counts, with their algorithmic assumptions stated explicitly. Either choice makes (12) a polylogarithmic clock overhead in $`M/\varepsilon`$. Ancilla-assisted synthesis requires an accounting of its retained work; it cannot silently replace the ancilla-free circuit while keeping the same width or clean-workspace assertions.

The returned cosine expression can be evaluated after measurement with certified error $`\rho`$, using classical arithmetic polynomial in $`\log M+\log(1/\rho)`$. Here is one explicit output rule for $`0<\rho\le1`$. For an interior canonical label $`j`$, compute rationals $`q_j,q_c`$ with

```math
|q_j-\cos(j\alpha)|\le\rho/16,
\qquad |q_c-\cos\alpha|\le\rho/16.
```

Then $`q_c\ge7/16`$, and replacing the two cosines in $`z_j`$ by these rationals changes its value by at most $`3\rho/14`$. Round the resulting rational $`(1-q_j/q_c)/2`$ to a dyadic rational with error at most $`\rho/2`$, and clip to $`[0,1]`$. The total error is at most $`5\rho/7<\rho`$, as required by (3). Assign $`j=1`$, $`j=M`$, and every auxiliary label directly as in (2)–(3). The dyadic rounding needs $`O(\log(1/\rho))`$ fractional bits. Since $`\cos\alpha\ge1/2`$, the division is uniformly well conditioned. Only the measured label is processed, so neither an $`M`$-entry classical table nor quantum access to such a table is needed.

Let $`g_A`$ be the compiled sampler's gate count and let $`g_G^{(c)}`$ be the actual cost of a controlled Grover step. Controlled state reflections use unconditional $`A`$ and $`A^\dagger`$ around a controlled zero-state reflection; a controlled black-box $`A`$ is not presumed available. A compiled estimator block has cost

```math
g_A+M g_G^{(c)}+2g_V+g_{\mathrm{init/readout/reset}},
```

with the state initialization, measurement, and reset terms counted in the chosen hardware convention. The orientation sample adds one sampler preparation, a success measurement, and reset; it can be a separate fully discarded block. Classical orientation tracking and output evaluation must also be charged. A coherent-work cap applies to the resulting compiled block, including synthesis gates and all gates executed in parallel. The ideal count $`M`$ of controlled Grover steps alone is not that native gate cap.

## 8. Execution noise and what remains exact

The preceding theorem concerns exact execution of finite unitary gate sequences. A noisy device need not implement the inverse of its actual preparation channel, even when the nominal gate list is reversed.

Suppose the observed output law of one entire oriented sample is within total variation $`\nu`$ of its compiled, noiseless law. Because the output is clipped to $`[0,1]`$,

```math
|\mathbb EW_{\mathrm{noisy}}-p|
\le4M^2\sigma_1p(1-p)+\nu,
```

```math
\mathbb E(W_{\mathrm{noisy}}-p)^2
\le\bigl[\kappa_M+4M^2(\sigma_1+\sigma_2)\bigr]p(1-p)+\nu.
\tag{15}
```

The second statement follows directly from the bounded test function $`(w-p)^2\in[0,1]`$. A probability-independent fault rate can therefore create a variance or bias floor at an endpoint. The finite-synthesis endpoint theorem does not remove that physical effect.

For a confidence guarantee, it is enough instead to control the joint execution error. If logical operation $`t`$, including state preparation and measurement where applicable, has channel error

```math
\tfrac12\|\mathcal E_t-\mathcal U_t\|_\diamond\le\nu_t,
```

channel telescoping bounds the final output distribution's total variation distance by $`\sum_t\nu_t`$. This remains valid for the classical orientation control and other adaptive instruments when they are included in the channel description. Allocate

```math
\sum_t\nu_t\le\delta/2.
```

Together with the statistical failure probability $`\delta/2`$ above, the final estimate then has additive error at most $`\varepsilon`$ relative to $`p_\star`$ with failure probability at most $`\delta`$. A stochastic fault model with probability at most $`\delta/2`$ of any fault gives the same conclusion by a union bound. Neither formulation supplies a physical qubit or latency count without a specified error-correcting code, gate architecture, and noise model.

## References

- Mark Bun and Justin Thaler, [Dual Lower Bounds for Approximate Degree and Markov–Bernstein Inequalities](https://arxiv.org/abs/1302.6191), 2013/2015. Polynomial derivative inequalities and their approximation-theoretic role.
- Christopher M. Dawson and Michael A. Nielsen, [The Solovay–Kitaev algorithm](https://arxiv.org/abs/quant-ph/0505030), 2005/2006. Constructive polylogarithmic synthesis.
- Neil J. Ross and Peter Selinger, [Optimal ancilla-free Clifford+T approximation of z-rotations](https://arxiv.org/abs/1403.2975), 2014/2016. Rotation synthesis with explicit optimality and algorithmic qualifications.

The exact ideal estimator, the compiled moment theorem, and the noisy execution guarantee are distinct statements. Only the first is asserted to be exactly unbiased without an additional calibration argument.
