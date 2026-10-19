# Ideal state restoration

For odd $`M`$, a centered version of the sine estimator can return its first output and then restore the target state exactly. It takes two rounds on average for every $`0<p<1`$, but has no deterministic bound on the number of rounds. This is a separate ideal-unitary extension of the [fixed-work estimator](model-and-estimator.md).

The restoration proof uses exact reflection symmetries of the sine preparation and readout. Generic finite synthesis does not preserve those symmetries, so the [finite-precision moment theorem](finite-precision.md) does not by itself establish a compiled restoration guarantee.

## 1. Center the physical clock powers

Use the common notation

```math
L=M+1,\qquad \alpha=\pi/L,\qquad
a_r=\sqrt{2/L}\sin(r\alpha),\qquad
D_{jr}=\sqrt{2/L}\sin(jr\alpha),
```

with physical clock labels $`r,j\in\{1,\ldots,M\}`$. Assume $`M\ge3`$ is odd, and put

```math
h=L/2.
```

A restoration round performs one ideal estimator round using controlled $`G^r`$, and applies the target correction $`G^{-h}`$. Apply this correction in every round, including the final round. It may be applied before or after the clock measurement because it commutes with the target Kraus operators.

The effective powers are $`G^{r-h}`$, with integer exponents symmetric about zero. The correction is $`G^{-(M+1)/2}`$. If instead the clock implementation uses powers $`G^{r-1}`$, its correction is $`G^{-(M-1)/2}`$. Those two conventions have the same destructive clock statistics, but their uncorrected target states differ. The resource count below uses the physical $`G^r`$ convention throughout.

## 2. Every outcome applies one of two target unitaries

For $`0<p<1`$, let $`\mathcal H_\phi`$ be the Grover invariant plane with eigenvectors $`|+\rangle,|-\rangle`$ and eigenvalues $`e^{i\phi},e^{-i\phi}`$, where

```math
\phi\in(0,\pi),\qquad \cos\phi=1-2p.
```

Define the involution

```math
J_\phi=|+\rangle\langle+|-|-\rangle\langle-|,
\qquad J_\phi^2=I_{\mathcal H_\phi}.
```

The corrected Kraus coefficient for measurement label $`j`$ and eigenphase $`\phi`$ is

```math
k_j(\phi)=\sum_{r=1}^{M}D_{jr}a_r e^{i(r-h)\phi}.
\tag{1}
```

The exact sine identities are

```math
a_{L-r}=a_r,
\qquad D_{j,L-r}=(-1)^{j+1}D_{jr}.
```

Substituting $`r\mapsto L-r`$ in (1) gives

```math
k_j(-\phi)=(-1)^{j+1}k_j(\phi).
\tag{2}
```

Since the coefficients $`D_{jr}a_r`$ are real, odd $`j`$ has a real $`k_j`$, and even $`j`$ has a purely imaginary $`k_j`$. The more useful consequence of (2) is the target Kraus operator restricted to the plane:

```math
\boxed{\displaystyle
K_j\big|_{\mathcal H_\phi}
=\begin{cases}
k_j(\phi) I,&j\text{ odd},\\
k_j(\phi) J_\phi,&j\text{ even}.
\end{cases}}
\tag{3}
```

Thus

```math
K_j^\dagger K_j=|k_j(\phi)|^2 I
\quad\text{on }\mathcal H_\phi.
\tag{4}
```

Every outcome probability is independent of the input density operator supported on this plane. An odd label leaves that state unchanged; an even label conjugates it by the same involution $`J_\phi`$. No direct implementation of $`J_\phi`$ is assumed or needed.

For the usual prepared state $`|\psi\rangle=A|0\rangle`$, its two eigenphase weights are equal, so $`J_\phi|\psi\rangle`$ is orthogonal to $`|\psi\rangle`$. Orthogonality is not required for the restoration argument; $`J_\phi^2=I`$ suffices.

## 3. Repeat until the label parity returns

Initialize a classical parity bit to zero. Perform the following procedure.

1. Run a corrected round, measure its clock label $`j`$, and save the first round's number
   ```math
   Z_{\mathrm{first}}=\frac{1-\cos(j\alpha)/\cos\alpha}{2}.
   ```
2. Toggle the parity bit exactly when $`j`$ is even.
3. If the bit is zero, stop. Otherwise reset the clock and perform another corrected round on the same target state.

Equivalently, an odd first label stops immediately. An even first label is followed by rounds until the next even label. The target is retained coherently throughout the procedure; measuring and resetting the clock does not end that target's coherent computation.

At every terminating history, the product of Kraus operators in (3) is a scalar multiple of the identity on $`\mathcal H_\phi`$. Therefore the final normalized target state is exactly its initial state, conditional on every terminating history of nonzero probability. The same statement holds for a target entangled with an external reference, provided the target's support lies in this one invariant plane: the conditional operator is a scalar multiple of $`I_{\mathcal H_\phi}\otimes I_{\mathrm{ref}}`$.

By (4), fresh clock rounds have the same outcome distribution regardless of the current parity state. Their labels are independent and identically distributed. Consequently the first number is unchanged by the later restoration procedure and has the ideal moments

```math
0\le Z_{\mathrm{first}}\le1,\qquad
\mathbb EZ_{\mathrm{first}}=p,\qquad
\mathrm{Var}(Z_{\mathrm{first}})=\kappa_Mp(1-p).
\tag{5}
```

After termination, further independent executions can reuse the restored target. The state is the same conditional on the complete earlier record, so retaining that classical record does not introduce a hidden target disturbance.

## 4. Exact stopping-time law

Let

```math
s=\sum_{j\text{ even}}|k_j(\phi)|^2
```

be the probability of an even label, and let $`N`$ be the number of rounds. If $`s>0`$, then

```math
\Pr(N=1)=1-s,
\qquad
\Pr(N=n)=s^2(1-s)^{n-2},\quad n\ge2.
\tag{6}
```

Indeed, after an even first label the number of additional rounds is geometric on $`\{1,2,\ldots\}`$ with success probability $`s`$. It follows that

```math
\boxed{\displaystyle
\mathbb EN=2,\qquad
\mathbb EN^2=2+\frac2s,\qquad
\Pr(N>n)=s(1-s)^{n-1}\quad(n\ge1).
}
\tag{7}
```

If $`s=0`$, then $`N=1`$ with certainty.

For completeness, let $`R|r\rangle=|L-r\rangle`$ be reflection of the path. Its eigenvalue on the $`j`$-th sine vector is $`(-1)^{j+1}`$. Applying its odd-parity projector to the centered phase clock gives

```math
s=\sum_{r=1}^{M}a_r^2\sin^2((r-h)\phi).
\tag{8}
```

All $`a_r`$ are nonzero, and the labels $`r=h\pm1`$ exist for $`M\ge3`$. Thus $`s=0`$ implies $`\sin\phi=0`$. Conversely $`\phi=0`$ and $`\phi=\pi`$ make every term zero. Hence $`s>0`$ for every $`0<p<1`$, and restoration occurs almost surely.

At $`p=0`$, the clock returns $`j=1`$. At $`p=1`$, it returns $`j=M`$, which is odd. Both endpoints therefore stop in one round and preserve the target up to an irrelevant global phase. They can be handled directly without defining distinct $`+\phi`$ and $`-\phi`$ eigenvectors.

There is no uniform second-moment bound: (7) diverges as $`s\downarrow0`$. Nor is there a deterministic round cap. For $`n\ge2`$, maximizing the tail over $`s\in[0,1]`$ gives

```math
s(1-s)^{n-1}
\le\frac1n\left(1-\frac1n\right)^{n-1}.
```

By continuity of (8) near an endpoint, arbitrarily small positive $`s`$ occur, so the worst-case tail is asymptotically of order $`1/n`$. Stopping after a fixed number of rounds and discarding a nonzero parity state would not be exact restoration. Conditioning the reported estimate on early successful restoration could also change its distribution, because the first output and stopping time are correlated.

## 5. Resource accounting and scope

For the efficient family $`L=2^\ell`$, a round uses:

- $`M`$ controlled applications of $`G`$ from the binary power ladder;
- $`L/2`$ applications of $`G^\dagger`$ for centering;
- one ideal sine preparation and one ideal sine readout;
- clock initialization, measurement, reset, and a classical parity update.

Thus each round contains $`(3M+1)/2`$ Grover applications when controlled and uncontrolled applications are each counted as one query. For an interior probability, the expected number is $`3M+1`$; at an endpoint it is $`(3M+1)/2`$. These are query counts, not equal native costs for controlled and uncontrolled operations.

More explicitly, if $`g_G^{(c)}`$ and $`g_{G^{-1}}`$ are their respective native costs, and $`g_V`$ is a sine-transform cost in the chosen ideal-gate convention, a round costs

```math
C_{\mathrm{round}}
=M g_G^{(c)}+\frac L2 g_{G^{-1}}+2g_V
+g_{\mathrm{clock\ init/readout/reset}}+g_{\mathrm{classical}}.
```

The expected total is $`2C_{\mathrm{round}}`$ for $`0<p<1`$, plus any initial preparation of the target. The target is prepared once and reused through the restoration rounds. Every application of $`G`$ or $`G^\dagger`$ still contains its sampler, inverse, and reflection work. The [native circuit ledger](circuits-and-resources.md) supplies those components.

This expectation does not satisfy a deterministic cap on the total coherent work before the target is discarded. It therefore does not replace the fixed-block construction in the main estimator theorem. Measurement reversal and repeated state restoration are established techniques; the [related-work discussion](../references/related-work.md) gives the relevant amplitude-estimation and state-restoration references. The calculation here supplies the particular sine-clock parity identity and its stopping law.

The invariant-space restriction also matters. For a superposition across different problem instances or different eigenphase pairs, the terminating scalar Kraus factor can depend on the instance. Learning an amplitude can then disturb the superposition even though each individual plane has an identity Kraus operator up to its own scalar. No coherent preservation across different probabilities is asserted.

Finally, a generic approximate $`\widetilde V`$ may violate (2). Its outcome operators need not be scalar multiples of $`I`$ or the same involution, and an imperfect first round can change the eigenphase weights. The destructive finite-precision theorem controls moments for fresh prepared states; it does not justify applying the present stopping argument after such a disturbance. A finite-gate restoration theorem would require an exactly symmetry-preserving implementation or a separate analysis of accumulated disturbance and stopping. Neither is assumed here.
