# Nonnegative probability estimates as likelihood weights

An exactly unbiased, nonnegative likelihood estimate can replace a likelihood evaluation in a pseudo-marginal Metropolis–Hastings algorithm while preserving its invariant posterior distribution. The sine-DST estimator supplies such a weight, with an explicit variance at a fixed coherent budget. This section establishes that application, the moments of independent products, and the effect of finite-precision bias. It does not assert a reduction in mixing time or an optimal advantage over classical inference methods.

## 1. Probability-estimation interface

Let an explicitly implemented unitary sampler and success projector define a probability

$$
p=\langle 0|A^\dagger\Pi A|0\rangle\in[0,1].
$$

For an integer $M\ge2$, set

$$
\alpha=\frac{\pi}{M+1},\qquad
a_r=\sqrt{\frac{2}{M+1}}\sin(r\alpha),\qquad r=1,\ldots,M.
$$

The physical clock labels are $r=1,\ldots,M$. With $p=\sin^2(\phi/2)$, the outcome distribution of the sine-DST measurement is

$$
D_{M,p}(j)=\left|
\frac{2}{M+1}\sum_{r=1}^{M}
\sin(r\alpha)\sin(jr\alpha)e^{ir\phi}
\right|^2,\qquad j=1,\ldots,M.
\tag{1}
$$

Changing the Grover eigenphase from $\phi$ to $-\phi$ leaves (1) unchanged. Assign the measured label the value

$$
z_j=\frac12\left(1-\frac{\cos(j\alpha)}{\cos\alpha}\right).
\tag{2}
$$

The statistical interface proved in [model-and-estimator.md](model-and-estimator.md) is

$$
0\le Z_M\le1,\qquad
\mathbb E Z_M=p,\qquad
\operatorname{Var}(Z_M)=\kappa_M p(1-p),
\quad
\kappa_M=\frac{M-1}{M+1}\tan^2\alpha.
\tag{3}
$$

In particular, $z_1=0$, $z_M=1$, and the output is deterministic at $p=0$ and $p=1$. For the clock convention in (1), the largest power is $G^M$, not $G^{M-1}$. An implementation must charge the complete controlled Grover calls, state preparation, clock operations, measurement, and classical evaluation of (2).

These statements concern the probability of the sampler actually implemented. They do not identify an approximate sampler's probability with that of an intended continuous or ideal physical model.

## 2. Exact invariant posterior

Let $(\Theta,\mu)$ be a parameter space with a reference measure. Suppose:

1. $\rho:\Theta\to[0,\infty)$ is a known measurable prefactor, including the prior and any exactly evaluated likelihood terms.
2. $\ell(\theta)\ge0$ is the likelihood term to be estimated, and $0<C:=\int\rho(\theta)\ell(\theta)\,\mu(d\theta)<\infty$.
3. At each parameter value, an executable probability kernel $D_\theta(dw)$ generates a finite nonnegative weight satisfying $\int wD_\theta(dw)=\ell(\theta)$.
4. The classical proposal has a measurable density $k(\theta,\theta')$ with respect to $\mu$, and the required prefactor and proposal ratios can be evaluated and sampled correctly.

For one probability likelihood, take $\ell(\theta)=p(\theta)$ and $D_\theta$ from (1)–(3). For a product likelihood, use Section 3. A density likelihood can also be used when it is expressed as a known nonnegative scale times a probability. Any parameter-dependent scale must be retained in $\rho$; it cannot be dropped as a constant.

**Proposition 1.** The probability measure

$$
\overline\pi(d\theta,dw)
=\frac{\rho(\theta)w}{C}\,\mu(d\theta)D_\theta(dw)
\tag{4}
$$

has marginal

$$
\pi(d\theta)=\frac{\rho(\theta)\ell(\theta)}{C}\,\mu(d\theta).
\tag{5}
$$

Starting from a positive-weight state, propose $\theta'\sim k(\theta,\cdot)$, generate a fresh $w'\sim D_{\theta'}$, and accept the pair with probability

$$
\mathcal A((\theta,w),(\theta',w'))
=1\wedge
\frac{\rho(\theta')k(\theta',\theta)w'}
{\rho(\theta)k(\theta,\theta')w}.
\tag{6}
$$

Use the usual Metropolis–Hastings conventions on null or one-way proposal sets. This kernel is reversible with respect to (4).

**Proof.** Integrating (4) over $w$ gives (5). The accepted pair-flow measure has, apart from the symmetric product of the two weight kernels and reference measures, the factor

$$
\frac1C\min\{
\rho(\theta)k(\theta,\theta')w,
\rho(\theta')k(\theta',\theta)w'
\},
$$

which is invariant under exchanging the two states. Rejections preserve detailed balance. $\square$

The current weight must be retained after rejection. Re-estimating both weights at every step generally defines a different, noisy algorithm. Zero proposed weights are rejected; (4) assigns zero mass to zero weights. At a fixed $\theta$ with $\ell(\theta)>0$, repeated initialization until a positive weight appears terminates almost surely, but its cost must be counted. Neither an arbitrary initialization nor a finite run is an exact independent posterior sample. Convergence still requires the relevant irreducibility and recurrence conditions.

This is an application of the standard [pseudo-marginal construction of Andrieu and Roberts (2009)](https://arxiv.org/abs/0903.5480), rather than a new convergence theorem. [Andrieu, Doucet and Holenstein (2010)](https://www.stats.ox.ac.uk/~doucet/andrieu_doucet_holenstein_PMCMC.pdf) develop the particle-MCMC setting. Nonnegative unbiased weights also arise classically. Exact unbiasedness and nonnegativity permit (4); they do not on their own improve its mixing properties.

## 3. Independent products and their complete second moment

Fix $\theta$ and suppress it from the notation. For $N$ factors, take independent $Z_i\sim D_{M_i,p_i}$ and define

$$
\ell=\prod_{i=1}^{N}p_i,\qquad
\widehat\ell=\prod_{i=1}^{N}Z_i.
$$

**Proposition 2.** The product satisfies $0\le\widehat\ell\le1$, $\mathbb E\widehat\ell=\ell$, and

$$
\mathbb E\widehat\ell^{\,2}
=\prod_{i=1}^{N}\bigl[p_i^2+\kappa_{M_i}p_i(1-p_i)\bigr].
\tag{7}
$$

If every $p_i>0$, then

$$
\frac{\operatorname{Var}(\widehat\ell)}{\ell^2}
=\prod_{i=1}^{N}
\left(1+\kappa_{M_i}\frac{1-p_i}{p_i}\right)-1.
\tag{8}
$$

**Proof.** Independence factors the first and second moments, and (3) gives the individual second moments. $\square$

If a factor vanishes, its estimate is zero almost surely, and (7) and unbiasedness still hold. Relative variance is then undefined. An estimate reused as $Z^r$ is generally biased for $p^r$. Independence must hold conditional on the parameter and the fixed budgets; common hardware memory, correlated resets, or data-dependent reuse of estimates can invalidate (7). Exact state restoration followed by independent fresh clock operations is sufficient to generate independent draws when the complete restored state has no retained memory relevant to subsequent outcomes.

A convenient sufficient condition for relative variance at most $v>0$ is

$$
\sum_{i=1}^{N}\kappa_{M_i}\frac{1-p_i}{p_i}
\le\log(1+v),
\tag{9}
$$

because $\log(1+x)\le x$. This is sufficient, not necessary. At $M\ge3$, convexity of the tangent on $[0,\pi/4]$ gives $\tan\alpha\le4\alpha/\pi$, hence $\kappa_M\le16/M^2$. If $p_i\ge p_0>0$, a shared budget obeying

$$
M\ge\max\left\{3,
4\sqrt{\frac{N(1-p_0)}{p_0\log(1+v)}}\right\}
\tag{10}
$$

therefore suffices. Rounding upward to the next admissible $M$ with $M+1$ a power of two changes this bound by at most a constant factor. A lower bound such as $p_0$ is an assumption, not information provided by the estimator. Selecting a budget using an independent pilot leaves subsequent fixed-budget unbiasedness intact; reusing the pilot outcomes needs a separate argument.

For comparison, averaging $n_i$ independent Bernoulli samples of each factor replaces $\kappa_{M_i}$ by $1/n_i$ in (7)–(9). These identities compare specified independent estimators at a given relative variance. They are not lower bounds for general classical estimators or statements about the number of MCMC iterations. [Correlated pseudo-marginal methods](https://arxiv.org/abs/1511.04992) can substantially change the relation between likelihood-estimation cost and chain efficiency.

## 4. Native implementation and classical work

The parameter and observed factor index may remain classical. Process the factors sequentially, compile or load the current observation into its circuit, and reuse the quantum work register. This arrangement does not require QRAM. It does require explicit access to every circuit that computes a factor.

For a sampler $A_{i,\theta}$, a Grover step contains the sampler, its inverse, the success reflection, and the initial-state reflection, with all controls charged. A complete likelihood evaluation has a cost of the form

$$
C_{\mathrm{eval}}(\theta)
=\sum_i\left[
C_{\mathrm{prepare},i}
+M_iC_{\mathrm{controlled\ Grover},i}
+C_{\mathrm{clock},i}
+C_{\mathrm{readout},i}
+C_{\mathrm{output},i}
\right]
+C_{\mathrm{data}}+C_{\mathrm{product}}.
\tag{11}
$$

All terms in (11) must use a common work or time unit. This is an accounting interface, not a gate bound. If the finite-precision orientation in Section 6 is used, its extra independent sampler execution is also charged. The per-step classical proposal, parameter updates, compilation, acceptance calculation, and any initialization retries are additional costs. Sequential factor processing uses at most the largest factor workspace plus the largest clock and any required ancillas. It still reads all required observation bits and carries out the classical product calculation.

A resettable unitary quantum model with an explicitly prepared input and a binary outcome projector supplies a natural factor probability. Inverse coherent access and implementable reflections are necessary. A copy-only state source or a destructive experimental device is insufficient by itself. If a reversible classical simulator supplies the factor instead, its random input preparation, trajectory computation, history or recomputation, and uncomputation belong in (11).

Small probabilities remain costly: the relative variance of one factor is $\kappa_M(1-p)/p$. A constant relative-variance target for this estimator requires $M$ of order $p^{-1/2}$ as $p\to0$. Full outcome strings may have exponentially small probabilities. A coarse binary outcome does not automatically guarantee a useful lower bound on its probability.

## 5. What the variance does and does not imply

### 5.1 An explicit failure of convex domination

For equal means, $X\le_{\mathrm{cx}}Y$ means $\mathbb E f(X)\le\mathbb E f(Y)$ for every convex function for which the expectations exist. Lower variance alone is weaker. The distinction matters for pseudo-marginal comparisons; see [Andrieu and Vihola (2016), Theorem 10 and Example 13](https://arxiv.org/pdf/1404.6909).

Take $p=1/10$, $M=7$, and let $\overline B_6$ be the average of six independent Bernoulli$(p)$ samples. Equation (1) gives the exact endpoint probability

$$
\Pr(Z_7=1)
=\frac{1324-936\sqrt2}{15625}
\simeq1.89507596021\times10^{-5},
\tag{12}
$$

whereas $\Pr(\overline B_6=1)=10^{-6}$. To verify (12), use $\cos\phi=4/5$, $\cos2\phi=7/25$, and $\cos3\phi=-44/125$. The endpoint amplitude, after removing a phase, is

$$
\frac{2-\sqrt2}{8}\cos3\phi
-\frac14\cos2\phi
+\frac{2+\sqrt2}{8}\cos\phi-\frac14
=\frac{-26+18\sqrt2}{125}.
$$

The inequality $\sqrt2<99/70$ proves that (12) is greater than $8/546875>10^{-6}$, without relying on numerical cancellation. Both penultimate support points are below $t=19/20$. Consequently

$$
\mathbb E(Z_7-t)_+
>\mathbb E(\overline B_6-t)_+,
$$

so $Z_7\not\le_{\mathrm{cx}}\overline B_6$. Nevertheless

$$
\operatorname{Var}(Z_7)
=\frac34(3-2\sqrt2)p(1-p)
<\frac16p(1-p)
=\operatorname{Var}(\overline B_6).
$$

The reverse convex order is also impossible, by this variance inequality. Six direct samples are used here to exhibit the mathematical obstruction; they are not asserted to equal the full native cost of the quantum circuit. This example does not itself construct a chain on which one estimator mixes more slowly. It prevents a universal convex-order argument based only on the variance reduction.

### 5.2 A limited equilibrium acceptance statement

For positive likelihoods write $W_\theta=\widehat\ell(\theta)/\ell(\theta)$. Suppose $\mathbb E W_\theta=1$ and $\operatorname{Var}(W_\theta)\le v_\theta$. For a fixed proposal pair, let $W_\theta,W_{\theta'}$ be independent draws from their unweighted estimation laws, and let $r$ be the ideal MH ratio. Integrating (6) over the stationary, size-biased current weight gives

$$
\overline{\mathcal A}(\theta,\theta')
=\mathbb E\min(W_\theta,rW_{\theta'}).
$$

Since $\min(x,ry)\ge\min(1,r)\min(x,y)$,

$$
\overline{\mathcal A}(\theta,\theta')
\ge\min(1,r)
\max\left\{0,1-\frac12\sqrt{v_\theta+v_{\theta'}}\right\}.
\tag{13}
$$

Here $\mathbb E\min(W,W')=1-\mathbb E|W-W'|/2$, and independence gives $\mathbb E(W-W')^2\le v_\theta+v_{\theta'}$. This controls stationary acceptance averaged over weights. It does not establish a spectral-gap bound, an autocorrelation bound, or a mixing-speed comparison.

Zero weights can make the logarithm of a likelihood estimate undefined even when its relative variance is finite. [Sherlock (2024), Section 2.4.1](https://arxiv.org/html/2411.10785v1#S2.SS4.SSS1) discusses precisely this issue for product probability estimates. That paper's Theorem 1 uses a normalized-noise law independent of the parameter; the sine-DST law generally does not satisfy that additional assumption. No such assumption is used in (4), (7), or (13).

## 6. Relative perturbations of the invariant posterior

### 6.1 A reweighting bound

**Lemma 3.** Let $\pi$ be a probability measure, and let $h$ be measurable with $0<a\le h\le b<\infty$, $\pi$-almost surely. Define $d\widetilde\pi=h\,d\pi/\mathbb E_\pi h$. Then

$$
\frac ab\le\frac{d\widetilde\pi}{d\pi}\le\frac ba,
\qquad
\|\widetilde\pi-\pi\|_{\mathrm{TV}}
\le\frac{\sqrt b-\sqrt a}{\sqrt b+\sqrt a}.
\tag{14}
$$

We use $\|P-Q\|_{\mathrm{TV}}=\tfrac12\int|dP-dQ|$.

**Proof.** Put $c=\mathbb E_\pi h\in[a,b]$. For $a<b$, the chord bound for the convex function $|x-c|$ yields

$$
\mathbb E_\pi|h-c|
\le\frac{2(b-c)(c-a)}{b-a}.
$$

Divide by $2c$ and maximize over $c$. The maximum is attained at $c=\sqrt{ab}$ and equals the right side of (14). The case $a=b$ is immediate. The bound is sharp for reweighting by a two-valued $h$ with the appropriate masses at $a,b$. $\square$

### 6.2 Oriented finite-precision bias

Suppose the implemented factor estimator remains in $[0,1]$, and its mean satisfies the uniform, pointwise condition

$$
|\mathbb E\widetilde Z_i(\theta)-p_i(\theta)|
\le\eta_i p_i(\theta)(1-p_i(\theta)),
\qquad 0\le\eta_i<1.
\tag{15}
$$

The $\eta_i$ are bounds independent of $\theta$. The finite-synthesis theorem must establish (15) for the actual circuit and output rule; an arbitrary absolute circuit error is not the same assumption. Boundedness and (15) imply deterministic correct endpoints. For every positive factor,

$$
1-\eta_i\le\frac{\widetilde p_i}{p_i}\le1+\eta_i,
\qquad \widetilde p_i:=\mathbb E\widetilde Z_i.
\tag{16}
$$

Generate the implemented factor estimates independently. Their product is exactly unbiased for $\widetilde\ell=\prod_i\widetilde p_i$, so exact pseudo-marginal acceptance targets $\widetilde\pi\propto\rho\widetilde\ell$. Zero sets of $\ell$ and $\widetilde\ell$ agree. On their positive support, use Lemma 3 with

$$
a=\prod_i(1-\eta_i),\qquad b=\prod_i(1+\eta_i).
$$

It follows that

$$
\|\widetilde\pi-\pi\|_{\mathrm{TV}}
\le\tanh\left(\frac12\sum_i\operatorname{artanh}\eta_i\right).
\tag{17}
$$

In particular this is $O(\sum_i\eta_i)$ when the sum is small, and is $O(N\eta)$ for a common small bound $\eta$. There is no division by a minimum likelihood probability. The result concerns the invariant target, not finite-run sampling error.

The interface proved in [finite-precision.md](finite-precision.md) uses a paired preparation and readout, followed by one independent Bernoulli orientation. Here $a_{\mathrm{clk}}$ bounds $\|\widetilde V-V\|$ for the full preparation transform, including ancillas, and the readout uses its exact compiled adjoint $\widetilde V^\dagger$. The quantity $r_{\mathrm{out}}$ bounds the raw output-rounding error. All outputs, including spare labels, must remain in $[0,1]$, and the initial-label output is exactly zero. Under that theorem's exponent-range $0,\ldots,M$ and equal-eigenphase-mixture hypotheses, the raw mean is a polynomial of degree at most $M$ with error at most $\sigma_1=2a_{\mathrm{clk}}+r_{\mathrm{out}}$. The oriented mean bound is

$$
|\mathbb E\widetilde Z-p|\le4M^2\sigma_1p(1-p).
\tag{18}
$$

Thus $\sigma_1\le\eta/(4M^2)$ suffices for (15), subject to those structural hypotheses. The orientation and Grover operations must use the same compiled sampler. Equation (18) is a circuit-theorem interface; the statistical proof of (17) depends only on (15).

### 6.3 Output rounding

Output rounding alone has a direct bound. Keep $z_1=0,z_M=1$ exact, and choose rounded outputs satisfying

$$
|\widetilde z_j-z_j|\le\eta z_j(1-z_j).
\tag{19}
$$

Then

$$
|\mathbb E\widetilde Z-p|
\le\eta\mathbb E[Z(1-Z)]
=\eta(1-\kappa_M)p(1-p)
\le\eta p(1-p).
\tag{20}
$$

For $M\ge3$, let $\mu_M=\min_{2\le j\le M-1}z_j(1-z_j)$. Nearest rounding to $b$ fractional bits satisfies (19) whenever $2^{-b-1}\le\eta\mu_M$. Since $\mu_M=\Theta(M^{-2})$, $b=O(\log M+\log(1/\eta))$ suffices; the leading dependence is $2\log_2M$. At $M=2$, both outputs are endpoints and need no such rounding. This argument covers the output map, not errors in the quantum measurement distribution.

## 7. Acceptance arithmetic and intended-model error

The exact-invariance claim requires sampling the acceptance probability in (6) correctly. Storing a rounded weight once and consistently retaining it defines a valid weight kernel; its mean determines the target. Rounding a ratio anew, clipping a signed estimate, replacing a product by an exponentiated noisy log-likelihood, or using uncontrolled floating-point underflow need not preserve that target.

For computable positive numerator and denominator, an exact Bernoulli decision can in principle be made by refining certified intervals for the ratio and for an independent uniform random number until the ordering is determined. It terminates almost surely under the computability assumptions, but there is no uniform deterministic precision or runtime bound: the comparison can be arbitrarily close, and a small denominator can require substantial arithmetic precision. A resource claim must count that arithmetic or give a separate error bound for a finite-precision acceptance kernel. The clock's fixed query budget does not make the complete classical acceptance step a fixed-time exact procedure.

Suppose $p_i^\star$ denotes the intended-model probability, while $p_i$ is the probability of the compiled sampler. Equations (15)–(18) control estimator bias around $p_i$. To transfer (17) to the intended model, one additionally needs a suitable model comparison, for example

$$
(1-\beta_i)p_i^\star\le p_i\le(1+\beta_i)p_i^\star,
\qquad 0\le\beta_i<1.
\tag{21}
$$

The multiplicative intervals in (16) and (21) then compose, and Lemma 3 applies with all $\eta_i$ and $\beta_i$. A uniform absolute model error alone does not give a likelihood-independent posterior bound. For example, with two equally weighted parameters and true probabilities $(t^2,t^2)$, replacing them by $(t,t^2)$ changes either probability by at most $t\to0$, but the posterior changes from $(1/2,1/2)$ to $(1/(1+t),t/(1+t))$, whose total variation tends to $1/2$. Discretization, imperfect state preparation, truncation, and sampler synthesis therefore require their own justified model-error bounds.

## 8. Relation to positive near-unbiased estimation

[Rall and Fuller, Quantum 7, 937 (2023), Theorem 23](https://arxiv.org/pdf/2207.08628), construct an estimator in $[0,1]$ with deterministic query budget and a controllably small mean error. Their target is the amplitude $a=\|\Pi\psi\|$, not its square. Their guarantee is

$$
|\mathbb E\widehat a-a|\le\epsilon\eta+\delta,
\qquad
Q=O\!\left(\epsilon^{-1}
[\eta^{-1}+\log(1/\delta)]\right).
$$

Two independent outputs give a nonnegative estimate of $p=a^2$ whose mean is $(a+b)^2$, where $b=\mathbb E\widehat a-a$; its probability bias is $2ab+b^2$. Positivity alone is therefore already available in that prior construction. Its stated finite-parameter guarantee is approximate unbiasedness, which does not itself establish (4) for the intended likelihood. Conversely, an exactly unbiased signed estimate cannot be inserted into (4) as a nonnegative weight without an additional construction.

## 9. Reproducible statistical checks

Run:

```bash
python verification/check_statistics.py
```

The script uses only the Python standard library and emits deterministic JSON. It computes (1) directly, checks the moments and independent products by finite enumeration, verifies finite-state pseudo-marginal detailed balance, checks the exact endpoint expression and the convex-order obstruction, tests the reweighting bound including an attaining two-point example, and checks rounded outputs and an explicitly specified orientation perturbation. Numerical checks support these algebraic arguments; they do not validate hardware noise, a physical sampler model, or MCMC convergence for an application.
