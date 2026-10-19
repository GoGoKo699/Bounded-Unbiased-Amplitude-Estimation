# Circuits and logical resources

The sine estimator can be built from an explicit sampler, its reversed gate sequence, two reflections, two Fourier transforms, and reversible integer arithmetic. No quantum random-access memory or amplitude table is required. The counts below include the input circuit and its work qubits. They are logical circuit counts, not a prediction of physical running time or a speedup over a specialized classical solver.

The ideal statistical theorem is developed in [the model and estimator](model-and-estimator.md) and [the variance proof](variance-proof.md). [Finite precision](finite-precision.md) specifies which claims survive gate synthesis and why the same compiled circuit must be paired with its exact inverse. The optional [restoration construction](restoration.md) has a different runtime guarantee and is not included in the fixed-budget ledger here.

## Circuit conventions

Let $`A`$ act on $`W`$ qubits, including every sampler work qubit, and put $`|\psi\rangle=A|0^W\rangle`$. The success projector is $`\Pi`$, with $`p=\langle\psi|\Pi|\psi\rangle`$. Define

```math
S_0=I-2|0^W\rangle\langle0^W|,\qquad
S_g=I-2\Pi,\qquad
G=-A S_0 A^\dagger S_g.
```

On the two-dimensional good/bad subspace, $`G`$ has phases $`\pm\phi`$, where $`\cos\phi=1-2p`$. The input $`|\psi\rangle`$ has equal weights in these two eigenspaces. This statement holds for complex input amplitudes; an eigenstate preparation is unnecessary. At $`p=0`$ and $`p=1`$, the relevant eigenvalue is respectively $`+1`$ and $`-1`$.

A controlled $`G`$ is executed in the following order:

1. Controlled $`S_g`$.
2. Unconditional $`A^\dagger`$.
3. Controlled $`S_0`$.
4. Unconditional $`A`$.
5. $`Z`$ on the control, to implement the displayed minus sign.

When the control is zero, $`A^\dagger`$ and $`A`$ cancel. Thus the construction does not assume a free controlled version of an unknown unitary. It needs the explicit circuit $`A`$, its exact reversed sequence, and the two controlled reflections. A gate of $`A`$ is counted on each invocation, including each inverse.

## Odd embedding and the type-I sine transform

Choose $`\ell\ge2`$, $`L=2^\ell`$, and $`M=L-1`$. Use an $`\ell`$-bit register $`r`$, a high bit $`h`$, and $`\ell-1`$ clean arithmetic work bits. The ideal path is $`h=0`$, $`1\le r\le L-1`$; $`r=0`$ is a spare label. All circuits below are nevertheless defined on every value of $`(h,r)`$.

The embedding $`E`$ applies $`H_h`$, then $`Z_h`$, then negates $`r`$ modulo $`L`$ if $`h=1`$. For a nonzero path label,

```math
E|0,r\rangle=\frac{|r\rangle-|2L-r\rangle}{\sqrt2}.
```

Let $`F_{2L}`$ be the positive-exponent Fourier transform. Grouping its terms at $`s`$ and $`2L-s`$ gives

```math
F_{2L}E|0,r\rangle
=i\sum_{s=1}^{L-1}\sqrt{\frac2L}\sin\!\left(\frac{\pi rs}{L}\right)E|0,s\rangle.
```

Consequently $`V=E^\dagger F_{2L}E`$ acts as $`iD`$ on the path subspace, where $`D`$ is the orthogonal, symmetric type-I discrete sine transform. Its high bit returns to zero. Initialize $`|h,r\rangle=|0,1\rangle`$ using one $`X`$ gate, prepare with $`V`$, and read out with $`V^\dagger`$. These operations prepare the sine amplitudes and measure the path-adjacency eigenbasis. The irrelevant factor $`i`$ cancels. Fast quantum sine transforms are established prior art; see `klappenecker2001dct` in [the bibliography](../references/bibliography.bib).

### A counted controlled-negation circuit

The arithmetic operation in $`E`$ has a direct implementation with clean work bits $`q_0,\ldots,q_{\ell-2}`$:

1. Compute $`q_0=r_0`$ with one CNOT. For each $`i=1,\ldots,\ell-2`$, compute $`q_i=q_{i-1}\lor r_i`$ using CNOT$`(q_{i-1},q_i)`$, CNOT$`(r_i,q_i)`$, and Toffoli$`(q_{i-1},r_i;q_i)`$.
2. For each $`i=1,\ldots,\ell-1`$, flip $`r_i`$ with Toffoli$`(h,q_{i-1};r_i)`$. Leave $`r_0`$ unchanged.
3. Reverse the prefix computation.

Modulo negation leaves the least significant one unchanged and flips all more significant bits. It also preserves whether every low-bit prefix is zero. The work bits therefore contain the same prefix-OR values before and after step 2, which justifies step 3 on every input, including $`r=0`$ and superpositions. This is not an assumption that the arithmetic is used only on the sine state.

For $`\ell\ge2`$, each controlled negation uses exactly

```math
3\ell-5\ \text{Toffoli},\qquad 4\ell-6\ \text{CNOT},\qquad \ell-1\ \text{clean work bits}.
```

Each $`E`$ or $`E^\dagger`$ also uses one $`H`$ and one $`Z`$. The complete preparation and readout contain four embeddings. Their arithmetic work always returns to zero.

### Fourier gates, including synthesis positions

A QFT on $`b=\ell+1`$ qubits uses $`b`$ Hadamards, $`b(b-1)/2`$ controlled phases, and $`\lfloor b/2\rfloor`$ swaps in the conventional binary circuit. No approximate-QFT truncation is assumed. The two Fourier transforms together therefore use

| Gate | Count |
|---|---:|
| Hadamard | $`2(\ell+1)`$ |
| Controlled phase | $`\ell(\ell+1)`$ |
| SWAP | $`2\lfloor(\ell+1)/2\rfloor`$ |

Up to a global phase, each controlled phase is two CNOTs and three single-qubit $`R_z`$ rotations, with angles $`\theta/2,\theta/2,-\theta/2`$. A SWAP is three CNOTs. Thus one $`V`$ has

```math
N_{R_z,V}=\frac32\ell(\ell+1)
```

rotation positions. The reversed compiled $`\widetilde V^\dagger`$ reuses their exact inverses. Some angles are exactly Clifford or Clifford+$`T`$; counting every position as requiring synthesis is a conservative upper bound.

Only these rotations are approximated in the specified implementation. The embeddings use exact Clifford/Toffoli gates and uncompute their work for every $`(h,r)`$. Ancilla-free rotation compilation therefore leaves all arithmetic work exactly clean after $`\widetilde V`$, even if the high bit or spare label acquires amplitude. This fact permits the work reuse in the width ledger. If a different compiler retains synthesis garbage, that garbage must be kept until the inverse and cannot be borrowed as clean reflection work.

## Controlled powers and the exact call convention

The binary ladder applies $`G^{2^j}`$ controlled by bit $`r_j`$, for $`j=0,\ldots,\ell-1`$. Implementing every power by repeated controlled $`G`$ uses

```math
\sum_{j=0}^{\ell-1}2^j=2^\ell-1=M
```

physical controlled-$`G`$ calls. The phase exponent is $`r`$. An equivalent shifted convention indexes the sine vector and phase exponent by $`k=r-1`$; the common phase within each Grover eigenspace does not affect any clock probability. Both conventions and their equivalence are checked numerically. If synthesis leaks outside the path, the exponent is still the low-register value $`0\le r\le M`$, independent of $`h`$ and any other clock ancilla. This bounded exponent is used by the finite-precision polynomial argument.

Exactly $`M-1`$ calls are possible in the ideal path subspace by applying one $`G`$ controlled by each predicate $`r-1\ge t`$, $`t=1,\ldots,M-1`$. Reversible comparisons and their inverses then cost $`O(M\ell)`$ gates rather than the binary ladder's absence of comparison gates. This alternative is not the resource baseline. The phrase “maximum exponent $`M-1`$” does not by itself establish a physical call count of $`M-1`$ for a binary ladder.

## An explicit input: a hard-coded 3CNF satisfying fraction

Consider $`n\ge3`$ input bits and $`c\ge3`$ clauses, each containing three distinct variables. A signed literal list is compiled classically into a fixed circuit; clause addresses are gate operands, not a quantum memory query. Let $`P`$ be the total number of positive literals, so $`0\le P\le3c`$.

The sampler first applies $`H^{\otimes n}`$. It then computes each clause OR into a fresh clause bit. To compute a clause, temporarily invert each positive-literal input, compute the conjunction of the three resulting bits into the clause target, undo the input inversions, and flip the target. The three-input conjunction uses three Toffolis and one clean work bit, returned to zero. This implements the OR even on a dirty target because the target is XORed with the clause value; the intended initialization is zero.

Compute the AND of all $`c`$ clause bits into one success flag using a conjunction ladder and its uncomputation. This costs $`2c-3`$ Toffolis and $`c-2`$ clean work bits. The same work pool serves the individual clauses. Clause bits are retained as reversible garbage and must be part of the reflected sampler register. The result is

```math
A|0^W\rangle
=2^{-n/2}\sum_{x\in\{0,1\}^n}|x\rangle|\text{clauses}(x)\rangle
 |\text{CNF}(x)\rangle|0^{c-2}\rangle,
\qquad W=n+2c-1.
```

The success probability is exactly the satisfying fraction of this specified formula. The sampler inventory is

| Resource | Exact count |
|---|---:|
| Toffoli | $`5c-3`$ |
| Hadamard | $`n`$ |
| $`X`$ | $`X_A=c+2P\le7c`$ |
| Sampler qubits | $`W=n+2c-1`$ |

$`A^\dagger`$ is the exact reversed gate sequence and has the same counts. No fresh approximation of its inverse is allowed.

### Edge cases and the scope of the displayed formula

The verification implementation accepts clauses of at most three literals and handles repeated literals by removing repetitions. A clause containing both signs of a variable is a constant true clause; an empty clause is false. The empty conjunction is true. One- and two-literal ORs use a CNOT and a Toffoli respectively, plus the corresponding sign and target flips. The final conjunction for zero, one, or two clauses uses $`X`$, CNOT, or Toffoli respectively. The exact clean workspace for that general implementation is

```math
w=\max\!\left(\max(c-2,0),\ \max_j\max(k_j-2,0)\right),\qquad
W=n+c+1+w,
```

where $`k_j`$ is the number of distinct literals in a nonconstant clause, and an empty maximum is zero. Its actual gate list supplies its count. The compact $`5c-3`$ and $`n+2c-1`$ formulas are asserted only for the stated three-distinct-variable, $`c\ge3`$ baseline. Invalid literal indices and clauses longer than three are rejected. A classical simplifier might solve or greatly reduce an instance; the construction makes no complexity claim against such simplification.

## Controlled reflections and live width

A safe controlled $`S_0`$ flips all $`W`$ sampler bits, computes their conjunction into $`W-1`$ clean work bits, applies CZ between the ladder result and the clock control, uncomputes the ladder, and flips the sampler bits back. For $`W\ge1`$ its inventory is

```math
2(W-1)\ \text{Toffoli},\quad 2W\ X,\quad 1\ \text{CZ},\quad W-1\ \text{work bits}.
```

For $`W=1`$ the CZ acts directly on the flipped data bit. The conjunction construction, including its phase, is tested on every data/control basis input for widths through nine. Reflecting only the variable bits would give the wrong rank-one reflection for this sampler; all $`W`$ bits are included.

The success flag permits controlled $`S_g`$ to be one CZ. The sign convention for $`G`$ adds one $`Z`$ on the clock control. For the complementary event $`I-\Pi`$, $`S_{\bar g}=-S_g`$; its additional control phase cancels this sign correction. The counts below bound either orientation.

Sampler work is included in $`W`$ and is not borrowed by the zero-reflection ladder. Clock arithmetic work and reflection work are used at different times and can share a clean pool, under the ancilla-free synthesis choice above. The peak logical width is exactly

```math
W_{\rm peak}=W+(\ell+1)+\max(W-1,\ell-1).
```

It reduces to $`2W+\ell`$ when $`W\ge\ell`$, but that inequality is not assumed. Measurement and reset can reuse these registers for the next independent sample. Parallel execution multiplies live width and total gate work even when it shortens elapsed depth.

## Full per-sample ledger

For the baseline 3CNF input, let $`M=2^\ell-1`$ and $`X_A=c+2P`$. Include the initial $`A`$, $`M`$ controlled Grover calls, clock initialization, both Fourier transforms, and all four embeddings. Before decomposing Toffolis and controlled phases, the complete inventory is

| Gate | Count |
|---|---:|
| Toffoli, denoted $`N_T^{(3)}`$ below | $`(2M+1)(5c-3)+2M(W-1)+4(3\ell-5)`$ |
| CNOT | $`4(4\ell-6)`$ |
| Hadamard | $`(2M+1)n+4+2(\ell+1)`$ |
| $`X`$ | $`(2M+1)X_A+2MW+1`$ |
| CZ | $`2M`$ |
| $`Z`$ | at most $`M+4`$ |
| Controlled phase, denoted $`N_{CP}`$ | $`\ell(\ell+1)`$ |
| SWAP, denoted $`N_{SW}`$ | $`2\lfloor(\ell+1)/2\rfloor`$ |

The initial sampler is prepared once; the factor $`2M+1`$ includes all forward and inverse sampler executions. The final $`+1`$ in the $`X`$ row initializes the clock label $`r=1`$. Clock readout measures $`\ell+1`$ bits. All live qubits are initialized or reset for each independent run; these preparation, measurement, and reset operations are additional entries in a hardware timing model, not free Clifford gates.

For example, the test formula

```math
(x_1\lor x_2\lor x_3)\land
(\neg x_1\lor x_2\lor\neg x_3)\land
(x_1\lor\neg x_2\lor x_3)
```

has five satisfying assignments out of eight. With $`\ell=3`$, $`M=7`$, it uses 19 peak logical qubits, 294 Toffolis, 24 CNOTs, 57 Hadamards, 338 $`X`$ gates, 14 CZs, at most 11 $`Z`$ gates, 12 controlled phases, and four swaps before decomposition. This small example verifies accounting and semantics; it is not a useful instance on which to claim quantum advantage.

### Clifford+$`T`$ expansion

Use the exact ancilla-free Toffoli decomposition with seven $`T`$/$`T^\dagger`$, six CNOTs, and two Hadamards. Its full gate sequence and all eight computational inputs are checked in the verification script. Relative-phase Toffolis or measurement-assisted substitutions are not silently substituted.

Let $`t_z(\xi)`$ and $`g_z(\xi)`$ be the certified $`T`$ count and total one-qubit Clifford+$`T`$ count of the selected ancilla-free $`R_z`$ compiler at operator error $`\xi`$. With the table's values $`N_T^{(3)}`$, $`N_{CP}`$, and $`N_{SW}`$, a conservative total is

```math
N_T\le7N_T^{(3)}+3N_{CP}\,t_z(\xi),
```

```math
N_{\rm CNOT}=6N_T^{(3)}+4(4\ell-6)+2N_{CP}+3N_{SW}+2M.
```

The last term expands the $`2M`$ CZs as $`H`$-CNOT-$`H`$. The corresponding total native-gate bound, treating $`H,X,Z,S,T`$ and CNOT as gates, is

```math
G_{\rm shot}\le15N_T^{(3)}+4(4\ell-6)
+[(2M+1)n+4+2(\ell+1)]
+[(2M+1)X_A+2MW+1]
+6M+(M+4)+3N_{SW}+2N_{CP}+3N_{CP}g_z(\xi).
```

The compiler's actual returned sequences can replace these upper bounds. Ross–Selinger synthesis gives practical near-optimal logarithmic $`T`$ counts with its stated algorithmic qualifications. Solovay–Kitaev supplies a constructive polylogarithmic alternative without relying on the strongest practical synthesis assumptions. The chosen compiler and its classical work must be recorded for a numerical resource estimate; an unqualified unit-cost arbitrary rotation is not a fault-tolerant gate count.

## Precision, readout, and repetitions

If each of the $`N_{R_z,V}`$ compiled rotation positions has error at most $`\xi`$, the telescoping bound gives $`\|\widetilde V-V\|\le N_{R_z,V}\xi`$, after an irrelevant global phase is fixed. Allocate a clock-unitary tolerance $`\eta`$ by setting $`\xi\le\eta/N_{R_z,V}`$. Compile $`\widetilde V`$ once and reverse its gate sequence for readout.

For canonical output labels $`h=0`$, $`1\le j\le L-1`$, compute classically

```math
z_j=\frac{1-\cos(\pi j/L)/\cos(\pi/L)}2.
```

Set $`z_1=0`$ and $`z_{L-1}=1`$ exactly; assign zero to all auxiliary labels. Round other outputs within $`r_{\rm out}`$ while keeping them in $`[0,1]`$. There is no $`M`$-entry lookup table. With $`b`$ output bits, ordinary certified fixed-point arithmetic can ensure $`r_{\rm out}\le2^{-b}`$. The denominator is at least $`1/\sqrt2`$, so absolute error control is well-conditioned. A conservative direct procedure computes $`\pi`$ and bounded-argument cosine series with $`O(\ell+b)`$ working bits and $`O((\ell+b)^3)`$ bit operations per output, using schoolbook arithmetic and a linear number of terms; sharper classical implementations are optional. Shared constants can be precomputed once. Reading and storing the measurement label, computing the output, and accumulating sample sums are classical costs.

For the finite-synthesis orientation correction, first generate an independent Bernoulli sample with the same $`A`$ and success measurement. Reset the sampler, then estimate either the event or its complement as specified in [finite precision](finite-precision.md). This adds one $`A`$ execution, one success-bit measurement, and a reset per reported sample. It does not increase the peak width. The Bernoulli and estimator blocks must be independent. Their combined gate count is the baseline $`G_{\rm shot}`$ plus the sampler cost; a strict per-block coherent-volume constraint can place them in separate reset blocks.

For example, the conservative allocation

```math
\eta,\ r_{\rm out}\le
\min\!\left\{\frac{1}{256M^4},\frac{\epsilon}{256M^2}\right\}
```

is sufficient for the endpoint-aware theorem to retain variance $`K_Mp(1-p)`$ with $`K_M=O(M^{-2})`$ and clock bias smaller than $`\epsilon/4`$. This uses $`b=O(\log M+\log(1/\epsilon))`$ and a polylogarithmic clock synthesis overhead. The finite circuit has controlled bias; only the ideal circuit is exactly unbiased. In this 3CNF example the sampler itself uses exact Clifford/Toffoli gates, so there is no additional sampler-model approximation. For a different sampler, any discretization and preparation error needs a separate budget relative to the intended probability.

Given a valid bound $`v\ge p(1-p)`$, take

```math
R=\max\!\left(1,\left\lceil\frac{16K_Mv}{\epsilon^2}\right\rceil\right)
```

independent samples per group. Chebyshev's inequality bounds a group's deviation from its expectation by $`\epsilon/2`$ with failure probability at most $`1/4`$. Use an odd number $`J\ge8\log(1/\zeta)`$ of independent groups and return the median of their means. The statistical failure probability is then at most $`\zeta`$. Allocate the remaining $`\epsilon/2`$ to clock bias and any model bias. Choosing $`v=1/4`$ always works; a smaller $`v`$ requires evidence, not knowledge obtained for free.

Total gate work is $`RJ`$ times the complete per-sample count, including the orientation preparation when used. Classical readout and accumulation, measurements, resets, and the one-time circuit compilation are additional costs. Choose $`M`$ by checking this actual compiled per-block count against a coherent-gate budget; the oracle-call count alone is insufficient. If even the smallest useful clock is too costly, ordinary sampling is available.

These formulas assume faithful execution of the compiled logical circuit. Stochastic logical faults require a separate failure budget and hardware/code model. No physical-qubit count or physical wall-clock comparison follows from this ledger without that information.

## Reproducible checks and limits

Run `python verification/check_circuits.py` from the repository root. It emits deterministic JSON containing test counts and maximum numerical residuals. The checks include:

- Prefix-OR controlled negation, including zero and every high-bit input, with exact work cleanup and counted gates.
- 3CNF truth tables, retained clause bits, inverse cleanup, empty formulas, empty clauses, repeated literals, tautologies, short clauses, and invalid-input rejection.
- The controlled all-zero reflection on every data/control basis input for widths one through nine.
- The seven-$`T`$ Toffoli sequence on all basis inputs.
- Gate-by-gate QFTs and the full odd embedding, including spare/high-bit labels, for $`M=3,7,15,31,63`$; sine preparation and the exact first and second moments.
- Direct joint clock/data evolution for complex, non-eigenstate Grover inputs, compared with the independent $`\pm\phi`$ mixture, including $`p=0,1`$ and abstract $`M=2`$.

These tests support the algebra and detect implementation/counting errors. They do not establish asymptotic correctness in place of a proof, certify a compiler's approximation error, simulate fault-tolerant hardware, or compare against the best classical SAT algorithms.
