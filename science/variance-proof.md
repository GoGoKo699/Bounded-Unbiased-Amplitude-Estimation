# Proof of boundedness, unbiasedness, and variance

Use the [model and estimator](model-and-estimator.md): $|\psi\rangle=A|0\rangle$, $p=\langle\psi|\Pi|\psi\rangle$, and

$$
G=(2|\psi\rangle\langle\psi|-I)(I-2\Pi).
$$

For $M\ge2$, set $L=M+1$, $\alpha=\pi/L$, $c=\cos\alpha$, and

$$
a_r=\sqrt{\frac2L}\sin(r\alpha),
\qquad D_{jr}=\sqrt{\frac2L}\sin(jr\alpha),
\qquad 1\le r,j\le M.
$$

The algorithm prepares $a$, applies controlled $G^r$, measures in the sine basis, and returns

$$
z_j=\frac{1-\cos(j\alpha)/c}{2}.
$$

We prove

$$
Z\in[0,1],\qquad
\mathbb EZ=p,\qquad
\operatorname{Var}(Z)
=\frac{M-1}{M+1}\tan^2\alpha\,p(1-p).
$$

## 1. Reduce the target dynamics to a clock phase

First suppose $0<p<1$. Define normalized good and bad states

$$
|b\rangle=\frac{(I-\Pi)|\psi\rangle}{\sqrt{1-p}},
\qquad
|g\rangle=\frac{\Pi|\psi\rangle}{\sqrt p}.
$$

They are orthogonal and span a space preserved by both reflections. In the ordered basis $(|b\rangle,|g\rangle)$,

$$
|\psi\rangle=
\begin{pmatrix}\sqrt{1-p}\\\sqrt p\end{pmatrix},
\qquad
G=\begin{pmatrix}
1-2p&-2\sqrt{p(1-p)}\\
2\sqrt{p(1-p)}&1-2p
\end{pmatrix}
=\begin{pmatrix}
\cos\phi&-\sin\phi\\
\sin\phi&\cos\phi
\end{pmatrix},
$$

where $\phi\in(0,\pi)$, $\cos\phi=1-2p$, and $\sin\phi=2\sqrt{p(1-p)}$.

The eigenvectors $|\pm\rangle=(|b\rangle\mp i|g\rangle)/\sqrt2$ have eigenvalues $e^{\pm i\phi}$. Each occurs in $|\psi\rangle$ with squared weight $1/2$. After the controlled powers, tracing out the target therefore gives the clock state

$$
\rho_C=\frac12|v(\phi)\rangle\langle v(\phi)|
+\frac12|v(-\phi)\rangle\langle v(-\phi)|,
\qquad v(\phi)_r=a_re^{ir\phi}.
$$

The readout matrix $D$ is real, and $v(-\phi)=\overline{v(\phi)}$. Consequently the two pure clock states have the same outcome probabilities. It suffices to analyze $v(\phi)$.

At $p=0$, $G|\psi\rangle=|\psi\rangle$; at $p=1$, $G|\psi\rangle=-|\psi\rangle$. These give the same clock expression with $\phi=0$ or $\phi=\pi$, so the clock calculation below also covers both endpoints without dividing by $p$ or $1-p$.

## 2. Identify the measured observable

Let $H$ be the $M\times M$ path adjacency matrix:

$$
H_{r,s}=\begin{cases}1,&|r-s|=1,\\0,&\text{otherwise.}\end{cases}
$$

Set $a_0=a_L=0$. The sine addition identity gives

$$
a_{r-1}+a_{r+1}=2c\,a_r,\qquad 1\le r\le M.
$$

Thus $Ha=2ca$. More generally the $j$-th sine vector is an eigenvector of $H$ with eigenvalue $2\cos(j\alpha)$. Orthogonality of these vectors gives

$$
DHD=\operatorname{diag}_{j=1}^{M}\bigl(2\cos(j\alpha)\bigr).
$$

Applying $D$, measuring $j$, and returning $z_j$ is therefore a projective measurement of the clock observable

$$
B=\frac12\left(I-\frac{H}{2c}\right).
$$

In particular, its first and second measurement moments are $\langle B\rangle$ and $\langle B^2\rangle$. Since $j\alpha\in[\alpha,\pi-\alpha]$,

$$
-c\le\cos(j\alpha)\le c.
$$

Every eigenvalue $z_j$ of $B$ lies in $[0,1]$. This proves boundedness directly from the measurement spectrum.

## 3. Compute the expectation

The eigenvector identity and normalization imply

$$
2\sum_{r=1}^{M-1}a_ra_{r+1}=\langle a|H|a\rangle=2c.
$$

For the phased clock,

$$
\begin{aligned}
\langle v(\phi)|H|v(\phi)\rangle
&=2\cos\phi\sum_{r=1}^{M-1}a_ra_{r+1}\\
&=2c\cos\phi.
\end{aligned}
$$

It follows that

$$
\mathbb EZ
=\langle v(\phi)|B|v(\phi)\rangle
=\frac{1-\cos\phi}{2}
=p.
$$

The same expectation holds for $v(-\phi)$, and hence for the actual mixed clock state.

## 4. Compute the variance

Because the mean is $p$, the variance on a pure clock state is

$$
\operatorname{Var}(Z)=\|(B-pI)v(\phi)\|^2.
$$

For every $r$, including the endpoints using the zero boundary values,

$$
\begin{aligned}
(Hv(\phi))_r
&=e^{ir\phi}\left(a_{r-1}e^{-i\phi}+a_{r+1}e^{i\phi}\right)\\
&=e^{ir\phi}\left(2ca_r\cos\phi
+i\sin\phi\,(a_{r+1}-a_{r-1})\right).
\end{aligned}
$$

Substituting $p=(1-\cos\phi)/2$ cancels the first term and gives the exact residual

$$
\bigl[(B-pI)v(\phi)\bigr]_r
=\frac{i\sin\phi}{4c}\,e^{ir\phi}
\left(a_{r-1}-a_{r+1}\right).
$$

The remaining norm is elementary. For $1\le r\le M$,

$$
a_{r-1}-a_{r+1}
=-2\sqrt{\frac2L}\sin\alpha\cos(r\alpha).
$$

The finite geometric sum $\sum_{r=1}^{L-1}e^{2\pi ir/L}=-1$ implies

$$
\sum_{r=1}^{M}\cos^2(r\alpha)=\frac{L-2}{2}=\frac{M-1}{2}.
$$

Hence

$$
\begin{aligned}
\sum_{r=1}^{M}(a_{r-1}-a_{r+1})^2
&=\frac8L\sin^2\alpha\sum_{r=1}^{M}\cos^2(r\alpha)\\
&=4\frac{M-1}{M+1}\sin^2\alpha.
\end{aligned}
$$

Combining these equalities and using $\sin^2\phi=4p(1-p)$ yields

$$
\begin{aligned}
\operatorname{Var}(Z)
&=\frac{\sin^2\phi}{16c^2}
\sum_{r=1}^{M}(a_{r-1}-a_{r+1})^2\\
&=\frac{\sin^2\phi}{4}\frac{M-1}{M+1}\tan^2\alpha\\
&=\boxed{\displaystyle
\frac{M-1}{M+1}\tan^2\!\left(\frac{\pi}{M+1}\right)p(1-p)}.
\end{aligned}
$$

Changing $\phi$ to $-\phi$ leaves the mean and variance unchanged. The actual mixture has this same variance, because its two components have the same mean. This completes the theorem.

## 5. Exact checks and consequences

The full ideal probability law, useful for an independent implementation check, is

$$
\Pr(Z=z_j)
=\left|\sum_{r=1}^{M}D_{jr}a_re^{ir\phi}\right|^2.
$$

It is normalized by unitarity of $D$. Several small cases and endpoints can be evaluated without numerical approximation.

| Case | Exact distribution | Variance factor |
|---|---|---|
| $p=0$ | $j=1$, so $Z=0$ surely | Variance is zero |
| $p=1$ | $j=M$, so $Z=1$ surely | Variance is zero |
| $M=2$ | $Z\sim\operatorname{Bernoulli}(p)$ | $\kappa_2=1$ |
| $M=3$ | $Z\in\{0,1/2,1\}$ with probabilities $(1-p)^2,2p(1-p),p^2$ | $\kappa_3=1/2$ |

The endpoint statements can also be read directly from the sine basis: $v(0)=a$ is the $j=1$ eigenvector, while $v(\pi)$ is the $j=M$ eigenvector up to a sign. The $M=3$ law is exactly a two-sample Bernoulli average; it does not by itself imply a resource advantage.

Finally, $\tan x=x+O(x^3)$ gives

$$
\kappa_M
=\frac{M-1}{M+1}\left(\frac{\pi^2}{(M+1)^2}+O(M^{-4})\right)
=\frac{\pi^2}{M^2}\bigl(1+O(M^{-1})\bigr).
$$

This proves the asymptotic variance reduction, but not finite-size minimax optimality. The proof uses exact sine preparation, exact readout, and exact reflections. See [Finite precision](finite-precision.md) for perturbations, [Circuits and resources](circuits-and-resources.md) for the cost of realizing these operations, [Positive weights](positive-weights.md) for compositions, [Restoration](restoration.md) for state reuse, and [Related work](../references/related-work.md) for the prior results relevant to interpretation.
