# Project understanding map

This map follows one question: how can an explicitly implemented quantum sampler produce a bounded probability estimate with exact ideal moments, and what remains true after charging for its implementation? The thirty milestones describe scientific understanding targets and their dependencies. The authoritative statements and proofs remain in [the scientific account](../science/model-and-estimator.md).

The single educational anchor is **Lin Lin, _Lecture Notes on Quantum Algorithms for Scientific Computation_, author-hosted revision dated March 3, 2022** ([PDF][lin], [author's course page](https://math.berkeley.edu/~linlin/qasc/)). Section numbers below refer to that revision; page numbers are the printed pages. The January 20, 2022 arXiv version and the later Lin–Wiebe live notes are different versions. The anchor supplies quantum-computing foundations. The project supplies the sine-observable moment proof, implementation details and extensions; primary research citations establish their attribution and imported proof ingredients.

| Phase | Milestones | Scientific role |
|---|---|---|
| Background/preliminaries | M01–M11 | Connect probability, reversible circuits, Grover dynamics, spectral measurement, Fourier clocks, approximation and cost into the estimation problem. |
| Narrative/innovation | M12–M30 | Follow the calibrated measurement through its exact moments, circuit realization, finite precision, statistical uses, optional restoration and end-to-end interpretation. |

The 11/19 allocation reflects the prerequisite structure: ten foundational connections culminate in the baseline estimation problem, while the larger second phase develops and integrates the estimator's mathematical, computational and statistical branches. It does not follow the anchor's chapter order. Prerequisites listed for each milestone are earlier milestones; independent branches rejoin in M28–M30. M11 and M30 synthesize their respective phases.

The [Lin-to-project bridge](LIN_BRIDGE.md) follows this map with a complete small example and the missing derivations. Each scientific page linked below remains authoritative for its assumptions and proof details.

## Phase I: background/preliminaries

### M01. A success probability is an operational quantity

- **Central question:** What probability is the algorithm actually being asked to estimate?
- **Understanding target:** Interpret a normalized quantum state, a unitary preparation $`A`$, and a success projector $`\Pi`$ through $`|\psi\rangle=A|0\rangle`$ and $`p=\langle\psi|\Pi|\psi\rangle`$. Distinguish the probability $`p`$ from the amplitude $`\sqrt p`$ and from a classical description of the state.
- **Prerequisites and story role:** None within this map. Establishes the input, measurement and scalar target before introducing an estimation algorithm.
- **Conceptual connection:** Every later theorem concerns this operational probability; changing the implemented sampler can change the target itself.
- **Sources:** [Lin][lin], §§1.1 and 1.5 (pp. 7 and 16); [Model and estimator](../science/model-and-estimator.md), “Input and access model.”

### M02. An estimate has several distinct guarantees

- **Central question:** Why are boundedness, unbiasedness, variance and confidence separate properties?
- **Understanding target:** Relate direct success measurements to a Bernoulli variable of variance $`p(1-p)`$. Distinguish an estimator's mean, variance, mean-square error and tail probability; understand why independent averaging reduces variance and why a nonlinear summary can change the mean.
- **Prerequisites and story role:** M01. Introduces the statistical quantities that the quantum construction must control.
- **Conceptual connection:** The project's value lies in a conjunction of output and moment guarantees, rather than an error bar alone.
- **Sources:** [Lin][lin], §1.5 (p. 16); [Model and estimator](../science/model-and-estimator.md), “Repetition and statistical guarantees”; [Interpretation](../science/interpretation.md), “A useful probability estimate.”

### M03. A reversible sampler includes its work

- **Central question:** What must be available to turn a sampler into a coherent subroutine?
- **Understanding target:** Explain circuit reversal, clean workspace, retained garbage and uncomputation. Distinguish an explicit unitary circuit with its inverse from a source of state copies or destructive experimental observations. A classical input compiled into gates is not free coherent memory access.
- **Prerequisites and story role:** M01. Expands the preparation symbol into a complete computational object.
- **Conceptual connection:** Counting every register and inverse prevents hidden QRAM, data-loading and erasure assumptions in both the theorem and the resource ledger.
- **Sources:** [Lin][lin], §§1.3 and 1.7–1.8 (pp. 13, 20–23); [Circuits and resources](../science/circuits-and-resources.md), “Circuit conventions” and “An explicit input: a hard-coded 3CNF satisfying fraction.”

### M04. Reflections make the sampler controllable

- **Central question:** How can the algorithm control a reflection about a prepared state without assuming a free controlled sampler?
- **Understanding target:** Relate $`R_\psi=2|\psi\rangle\langle\psi|-I`$ to an initial-state reflection conjugated by $`A`$. Track the order of $`A^\dagger`$, the controlled reflection and $`A`$, including the control phase required by the sign convention. Reflect about the full initial register, including sampler work.
- **Prerequisites and story role:** M01 and M03. Identifies the coherent operations used to interrogate the probability.
- **Conceptual connection:** This construction connects an executable sampler to controlled Grover steps and exposes their nonzero cost.
- **Sources:** [Lin][lin], §§2.2–2.3 (pp. 30–33); [Model and estimator](../science/model-and-estimator.md), “Input and access model”; [Circuits and resources](../science/circuits-and-resources.md), “Circuit conventions.”

### M05. Two reflections encode probability as a phase

- **Central question:** Why does a possibly large sampler reduce to a two-dimensional rotation?
- **Understanding target:** Resolve the prepared state into orthogonal good and bad components and derive the invariant Grover plane. Interpret the eigenphases $`\pm\phi`$, the relation $`\cos\phi=1-2p`$, and the equal eigenphase weights of the prepared state, including complex sampler amplitudes. Treat $`p=0,1`$ without dividing by vanishing probabilities.
- **Prerequisites and story role:** M01 and M04. Converts the scalar estimation problem into a phase-dependent dynamics problem.
- **Conceptual connection:** The equal phase mixture is needed by both the ideal readout and the finite-precision polynomial argument.
- **Sources:** [Lin][lin], §2.3 and §4.2 (pp. 33 and 57–58); [Variance proof](../science/variance-proof.md), §1. The project's $`\phi`$ is the Grover eigenphase, not the state-vector angle $`\phi/2`$.

### M06. A measurement can expose moments directly

- **Central question:** How does assigning numbers to measurement outcomes define an observable?
- **Understanding target:** Connect a Hermitian matrix's eigenbasis and eigenvalues to a projective measurement. Explain why the assigned output's first two moments are expectations of $`B`$ and $`B^2`$, and why its range is determined by the spectrum of $`B`$.
- **Prerequisites and story role:** M01 and M02. Supplies the language for designing the readout around a desired mean and variance.
- **Conceptual connection:** The project measures a calibrated cosine observable; it does not need to estimate a phase bin and then infer its moments through a nonlinear conversion.
- **Sources:** [Lin][lin], §§1.1 and 1.5; [Variance proof](../science/variance-proof.md), §2.

### M07. Controlled powers write phase into a clock

- **Central question:** What information is stored by a coherent superposition of different evolution times?
- **Understanding target:** Follow phase kickback from controlled $`G^r`$ to clock amplitudes proportional to $`e^{ir\phi}`$. Relate this to the quantum Fourier transform and conventional phase estimation. For the prepared target, retain the mixture of the two eigenphases when ignoring the target register.
- **Prerequisites and story role:** M03 and M05. Connects coherent query time to a measurable clock state.
- **Conceptual connection:** Both conventional phase estimation and this estimator use phase kickback; their clock preparation and measurement statistics differ.
- **Sources:** [Lin][lin], §§3.3–3.5 (pp. 45–50) and §4.2; [Variance proof](../science/variance-proof.md), §1; [Circuits and resources](../science/circuits-and-resources.md), “Controlled powers and the exact call convention.”

### M08. A finite path links sine waves and Fourier circuits

- **Central question:** Why do sine vectors appear in both a matrix spectrum and a quantum circuit?
- **Understanding target:** Interpret the finite path adjacency matrix with zero boundary values, its sine eigenvectors and its eigenvalues $`2\cos(j\pi/(M+1))`$. Connect the type-I discrete sine transform to the odd subspace of a Fourier transform. Separate this established transform structure from the project's choice of probe and output calibration.
- **Prerequisites and story role:** M06 and M07. Provides the spectral and computational ingredients used together in the main mechanism.
- **Conceptual connection:** The same sine transform will prepare the probe and diagonalize the measured path observable without an amplitude table.
- **Sources:** [Lin][lin], §3.3 supplies the Fourier foundation; [Variance proof](../science/variance-proof.md), §2; [Circuits and resources](../science/circuits-and-resources.md), “Odd embedding and the type-I sine transform”; [Related work](../references/related-work.md), “The measurement and circuit ingredients are established.”

### M09. Approximation changes circuits and probabilities differently

- **Central question:** What does a small unitary error guarantee about a measured scalar?
- **Understanding target:** Relate operator-norm error, state error and measurement total variation; use bounded outputs to control moment changes. Distinguish a compiled unitary followed by its exact inverse from separately approximated forward and inverse operations. Separate approximation of an intended input model from additional execution noise.
- **Prerequisites and story role:** M01, M02 and M03. Introduces the error notions required to connect ideal algebra with finite circuits.
- **Conceptual connection:** A uniform absolute error bound is insufficient by itself to protect probabilities arbitrarily close to zero; the later endpoint argument needs additional structure.
- **Sources:** [Lin][lin], §§1.2, 1.6–1.9 (pp. 11 and 19–23); [Finite precision](../science/finite-precision.md), §§1–2, 6 and 8.

### M10. A query budget is only one resource model

- **Central question:** What has to be counted before a probability-estimation advantage becomes operational?
- **Understanding target:** Distinguish controlled-Grover queries, native logical gates, circuit depth, live qubits, classical work and physical time. Include preparation, inverse computation, reflections, clock gates, precision, measurement and reset. Understand why independent repetition reduces variance while multiplying total work.
- **Prerequisites and story role:** M02–M04 and M07–M09. Joins the statistical and circuit descriptions into a common accounting framework.
- **Conceptual connection:** A no-QRAM implementation still needs an explicit input model and a complete cost ledger.
- **Sources:** [Lin][lin], §§1.8–1.10 (pp. 23–24); [Circuits and resources](../science/circuits-and-resources.md), “Full per-sample ledger” and “Precision, readout, and repetitions”; [Interpretation](../science/interpretation.md), “Physical resource boundary.”

### M11. The complete probability-estimation problem

- **Central question:** What does conventional amplitude estimation provide, and what additional specification motivates this project?
- **Understanding target:** Combine the executable sampler, Grover phase, clock measurement and resource model into one task. Explain why a phase-accuracy guarantee does not automatically specify an exactly unbiased bounded probability output or its second moment. Identify the different roles of ideal operations, finite synthesis and physical execution.
- **Prerequisites and story role:** M01–M10. Synthesizes the background into the input, output, statistical and implementation contract that the narrative must meet.
- **Conceptual connection:** This is the transition from established amplitude-estimation machinery to the particular calibrated measurement studied here.
- **Sources:** [Lin][lin], §4.2 together with §§3.3–3.5; [Model and estimator](../science/model-and-estimator.md); [Related work](../references/related-work.md), “The object being compared.”

## Phase II: narrative/innovation

### M12. Design the probe and readout as one measurement

- **Central question:** Which preparation and output values jointly produce a bounded probability estimate?
- **Understanding target:** Connect $`a_r=\sqrt{2/(M+1)}\sin(r\alpha)`$, the sine-transform readout and $`z_j=(1-\cos(j\alpha)/\cos\alpha)/2`$, where $`\alpha=\pi/(M+1)`$. Identify their observable as $`B=(I-H/(2\cos\alpha))/2`$ and use its spectrum to establish the output interval.
- **Prerequisites and story role:** M06, M08 and M11. Introduces the complete local measurement mechanism before proving its moments.
- **Conceptual connection:** Preparation and calibration are matched to one finite-path eigenvalue; neither boundedness nor the moment identities come from a sine probe alone.
- **Sources:** [Model and estimator](../science/model-and-estimator.md), “Clock and readout”; [Variance proof](../science/variance-proof.md), §2. The Fourier and measurement foundations are [Lin][lin], §§1.5 and 3.3.

### M13. Adjacent phase coherence gives the exact mean

- **Central question:** Why is the expected output exactly $`p`$ at every clock size?
- **Understanding target:** Use $`Ha=2\cos\alpha\,a`$ to normalize the nearest-neighbor overlap. Show how phase kickback multiplies its real part by $`\cos\phi`$, giving $`\langle H\rangle=2\cos\alpha\cos\phi`$ and hence $`\mathbb EZ=p`$ for both eigenphase branches.
- **Prerequisites and story role:** M05, M07 and M12. Establishes the first moment through the mechanism of the measurement.
- **Conceptual connection:** Exact unbiasedness follows from the finite spectral identity, without a preliminary estimate of $`p`$ or a limiting phase-resolution argument.
- **Sources:** [Variance proof](../science/variance-proof.md), §§1–3; [Model and estimator](../science/model-and-estimator.md), “Ideal sampling theorem.”

### M14. A discrete derivative determines the entire variance

- **Central question:** Why does the variance vanish at both endpoints while decreasing quadratically with clock size?
- **Understanding target:** Interpret the residual $`(B-pI)v(\phi)`$ as a discrete derivative of the sine profile multiplied by $`\sin\phi`$. Connect its squared norm to $`\mathrm{Var}(Z)=\kappa_Mp(1-p)`$, with $`\kappa_M=\frac{M-1}{M+1}\tan^2\alpha`$. Understand the deterministic endpoints and the $`M=2,3`$ distributions as consequences of the same law.
- **Prerequisites and story role:** M12 and M13. Completes the exact moment calculation and identifies its rare-event scale.
- **Conceptual connection:** The variance has no additive probability-independent term; its asymptotic coefficient does not establish finite-size minimax optimality.
- **Sources:** [Variance proof](../science/variance-proof.md), §§4–5; [Model and estimator](../science/model-and-estimator.md), “Ideal sampling theorem.”

### M15. Compose fixed blocks into a statistical guarantee

- **Central question:** How does the single-shot law support an executable estimation procedure?
- **Understanding target:** Combine boundedness, exact mean and variance in a fixed ideal block. Distinguish an arithmetic mean, which preserves unbiasedness, from a median-of-means confidence wrapper. Use a known bound $`v\ge p(1-p)`$ to choose repetitions, and distinguish an admissible block-size cap from a formula involving unknown $`p`$.
- **Prerequisites and story role:** M02, M10 and M14. Integrates the ideal statistical result before implementation details are charged.
- **Conceptual connection:** The resulting hybrid query scaling is established territory; the explicit output law and its moment identity are the object being composed.
- **Sources:** [Model and estimator](../science/model-and-estimator.md), “Repetition and statistical guarantees”; [Interpretation](../science/interpretation.md), “Repetition and gate precision”; [Lin][lin], §1.5 for the sampling background.

### M16. Realize the complete clock without an amplitude table

- **Central question:** How does the abstract sine measurement become a circuit on binary registers?
- **Understanding target:** Follow the odd embedding $`E`$, Fourier transform $`F_{2L}`$ and $`V=E^\dagger F_{2L}E`$, which acts as $`iD`$ on the path. Include controlled modular negation, its clean scratch, the spare label and high bit. For $`L=2^\ell`$, account for the binary ladder's exactly $`M=2^\ell-1`$ controlled Grover calls and distinguish physical powers $`G^r`$ from shifted powers.
- **Prerequisites and story role:** M03, M08, M12 and M15. Turns the ideal measurement into a fully specified unitary implementation.
- **Conceptual connection:** Efficient transform structure removes a table-loading assumption, while the full binary action prepares the finite-precision analysis.
- **Sources:** [Lin][lin], §§1.7–1.8 and 3.3; [Circuits and resources](../science/circuits-and-resources.md), “Odd embedding and the type-I sine transform” through “Controlled powers and the exact call convention.”

### M17. Make input preparation and reflection explicit

- **Central question:** What does the access model cost for a concrete, finite computational task?
- **Understanding target:** Follow the hard-coded 3CNF satisfying-fraction sampler from uniform input through clause bits and a success flag. Understand why clause garbage is retained, what the exact inverse removes, and why the controlled zero reflection includes all sampler qubits. Separate the stated distinct-variable clause baseline from its edge cases.
- **Prerequisites and story role:** M03, M04 and M16. Instantiates the access assumptions in a counted reversible example.
- **Conceptual connection:** The example demonstrates no-QRAM semantics and accounting; it does not establish an advantage over classical satisfiability or counting algorithms.
- **Sources:** [Lin][lin], §1.7; [Circuits and resources](../science/circuits-and-resources.md), “An explicit input: a hard-coded 3CNF satisfying fraction” and “Controlled reflections and live width.”

### M18. Assemble the native per-sample ledger

- **Central question:** Which costs survive after every oracle and clock operation is expanded?
- **Understanding target:** Combine the $`2M+1`$ sampler/inverse calls with controlled reflections, both transforms, classical output arithmetic and the peak live workspace. Interpret the Clifford+$`T`$ expansion and its rotation-compiler cost interface. Explain when clock scratch and reflection scratch can share a clean pool, and include initialization, measurement and reset in an eventual timing model.
- **Prerequisites and story role:** M10, M16 and M17. Integrates the local circuit components into one logical resource statement.
- **Conceptual connection:** This ledger makes a coherent-gate cap meaningful and identifies the additional information required for a physical cost comparison.
- **Sources:** [Circuits and resources](../science/circuits-and-resources.md), “Full per-sample ledger” and “Precision, readout, and repetitions”; [Interpretation](../science/interpretation.md), “The cost of one coherent run”; [Lin][lin], §§1.9–1.10.

### M19. Full-space synthesis errors retain polynomial structure

- **Central question:** What structure remains when the compiled clock leaks into unused labels?
- **Understanding target:** Keep every clock ancilla, assign all labels bounded outputs, and restrict every phase exponent to $`0,\ldots,M`$. Understand why paired preparation/readout gives an exact zero output at $`p=0`$ and why the equal eigenphase mixture makes both raw moment errors real polynomials of degree at most $`M`$. Connect uniform bounds $`\sigma_1=2\eta_V+\rho`$ and $`\sigma_2=2\eta_V+2\rho`$ to an endpoint bound through Markov's polynomial derivative inequality.
- **Prerequisites and story role:** M05, M09, M14 and M16. Supplies the structural argument that improves on a generic absolute perturbation bound.
- **Conceptual connection:** The proof uses the actual full unitary and output map, not an assumption that compilation stays inside the ideal path.
- **Sources:** [Finite precision](../science/finite-precision.md), §§1–3; [Lin][lin], §1.6 for accumulated unitary error. Markov's inequality is a separate research-level ingredient cited in the scientific page.

### M20. A Bernoulli orientation protects both endpoints

- **Central question:** How can one-sided compiled stability become a bound proportional to $`p(1-p)`$?
- **Understanding target:** Use an independent Bernoulli sample from the same compiled sampler to select the event or its complement, returning the complemented estimate when appropriate. Explain the resulting bounded output $`W`$, its exact endpoint behavior, and the bounds $`|\mathbb EW-p|\le4M^2\sigma_1p(1-p)`$ and $`\mathrm{Var}(W)\le[\kappa_M+4M^2(\sigma_1+\sigma_2)]p(1-p)`$.
- **Prerequisites and story role:** M02, M05 and M19. Converts the polynomial endpoint control into a uniform two-endpoint implementation guarantee.
- **Conceptual connection:** The additional preparation is a charged, independent operation. The finite circuit has controlled bias, rather than exact ideal unbiasedness.
- **Sources:** [Finite precision](../science/finite-precision.md), §4; [Circuits and resources](../science/circuits-and-resources.md), “Precision, readout, and repetitions.”

### M21. Close the compiled accuracy and resource budget

- **Central question:** How can finite synthesis, output arithmetic and statistical repetition meet one requested tolerance?
- **Understanding target:** Connect the precision allocation to $`O(M^{-2})p(1-p)`$ variance and a bounded bias, then choose repetitions using a justified variance promise. Distinguish the compiled probability from an intended-model probability, and logical synthesis error from execution faults. Explain why increasing final accuracy can keep the expensive sampler-call count per block fixed while increasing native precision cost.
- **Prerequisites and story role:** M09, M15, M18 and M20. Integrates the finite implementation theorem with the complete ledger.
- **Conceptual connection:** The rare-event guarantee needs no minimum compiled probability, but an absolute model or hardware error does not inherit that relative protection.
- **Sources:** [Finite precision](../science/finite-precision.md), §§5–8; [Circuits and resources](../science/circuits-and-resources.md), “Precision, readout, and repetitions”; [Lin][lin], §§1.6 and 1.8–1.10.

### M22. Independent positive factors form likelihood weights

- **Central question:** What survives when several probability estimates are multiplied?
- **Understanding target:** Derive nonnegativity, exact ideal product mean and the complete product second moment under conditional independence. Interpret the relative-variance factors $`1+\kappa_{M_i}(1-p_i)/p_i`$, the cost of small factor probabilities, and the role of a justified probability lower bound when choosing budgets. Distinguish independent factor draws from reusing one estimate as a power.
- **Prerequisites and story role:** M02, M14, M15 and M18. Develops the first statistical composition of the single-factor interface.
- **Conceptual connection:** Sequential factor circuits can reuse workspace without QRAM, but every factor's data access, preparation and classical arithmetic remains part of the evaluation cost.
- **Sources:** [Positive weights](../science/positive-weights.md), §§1, 3 and 4; [Lin][lin], §1.5 supplies the sampling foundation, while the product argument is supplied locally.

### M23. Unbiased nonnegative weights preserve a target marginal

- **Central question:** Why can a random likelihood weight define the correct invariant posterior?
- **Understanding target:** Interpret the extended target proportional to $`\rho(\theta)wD_\theta(dw)`$ and recover its intended marginal by integrating over the weight. Connect the Metropolis–Hastings acceptance ratio to symmetric pair flow. Understand why the current weight is retained after rejection and why zero weights and initialization require explicit treatment.
- **Prerequisites and story role:** M02, M15 and M22. Connects the moment interface to a larger statistical construction.
- **Conceptual connection:** This application uses the established pseudo-marginal identity. Correct invariance does not imply an independent posterior draw after finitely many steps or a favorable mixing time.
- **Sources:** [Positive weights](../science/positive-weights.md), §2 and its Andrieu–Roberts attribution; [Related work](../references/related-work.md), “Positive weights and restoration.” This statistical construction is beyond the selected anchor and is derived in the project.

### M24. Relative bias controls the perturbed target

- **Central question:** What posterior statement remains when each nonnegative estimate has a small implementation bias?
- **Understanding target:** Connect the endpoint-scaled factor bias to a multiplicative likelihood comparison, then to the stated total-variation bound after normalization. Separate the invariant target of rounded weights from finite-run chain error. Include correct acceptance arithmetic and explain why intended-model error needs its own suitable relative comparison.
- **Prerequisites and story role:** M20–M23. Carries the finite-circuit guarantee through the positive-weight application.
- **Conceptual connection:** The orientation theorem can prevent division by a minimum likelihood probability in the target bound; it does not make exact acceptance decisions uniformly finite-time or remove sampler-model error.
- **Sources:** [Positive weights](../science/positive-weights.md), §§6–7; [Finite precision](../science/finite-precision.md), §§4 and 6.

### M25. Lower variance does not order every statistical use

- **Central question:** Why is the exact variance identity insufficient for a universal inference-speed claim?
- **Understanding target:** Distinguish variance comparison from convex order, stationary acceptance from mixing, and independent factor averaging from correlated classical alternatives. Understand the role of the explicit $`M=7`$ convex-order obstruction and the narrower equilibrium acceptance bound.
- **Prerequisites and story role:** M22–M24. Delimits what the positive-weight branch has and has not established.
- **Conceptual connection:** A useful estimator interface can support correct compositions without determining the best application-level algorithm.
- **Sources:** [Positive weights](../science/positive-weights.md), §5; [Interpretation](../science/interpretation.md), “A useful probability estimate”; [Related work](../references/related-work.md), “Positive weights and restoration.”

### M26. Centered clock symmetry gives a restoration instrument

- **Central question:** How can the same measurement have a simple, reversible effect on its target?
- **Understanding target:** For odd $`M`$, center the physical powers using $`G^{-(M+1)/2}`$. Relate the sine reflection symmetry to Kraus operators proportional to either the identity or one involution, according to the measured label parity. Understand why the outcome probabilities are state-independent within one Grover plane and why returning to even parity restores states supported on that plane, including entanglement with a reference.
- **Prerequisites and story role:** M05–M08, M14 and M16. Opens the optional state-reuse branch through the measurement's target action.
- **Conceptual connection:** Equal clock statistics under shifted exponents do not imply equal target disturbance; the correction depends on the physical convention.
- **Sources:** [Restoration](../science/restoration.md), §§1–3; [Lin][lin], §§1.2 and 1.5 provide density-operator and measurement foundations. The parity-instrument derivation is local to the project.

### M27. Restoration exchanges a deterministic cap for a stopping law

- **Central question:** What does an expected two restoration rounds actually cost?
- **Understanding target:** Interpret the geometric return mechanism, $`\mathbb EN=2`$, $`\mathbb EN^2=2+2/s`$ and $`\Pr(N>n)=s(1-s)^{n-1}`$ for interior probabilities. Include each round's controlled powers and target correction. Distinguish clock resets from loss of target coherence, and a bounded mean from a deterministic cap or uniformly bounded second moment.
- **Prerequisites and story role:** M10, M18 and M26. Completes the ideal restoration branch with its exact operational boundary.
- **Conceptual connection:** Restoration preserves the first ideal estimate, but its unbounded tail cannot be combined with the destructive block's fixed-work claim. Generic finite synthesis is not covered by the exact parity argument.
- **Sources:** [Restoration](../science/restoration.md), §§4–5; [Interpretation](../science/interpretation.md), “The cost of one coherent run.”

### M28. Locate the result among established ingredients

- **Central question:** Which conjunction of properties is being studied, and which components already have close predecessors?
- **Understanding target:** Compare probability versus amplitude targets, bounded versus signed outputs, exact versus small bias, endpoint-dependent versus additive variance, and deterministic versus expected cost. Attribute cosine observables, sine probes, fast sine transforms, pseudo-marginal inference and restoration to their established literature. Identify the calibrated joint moment identity and endpoint-sensitive finite-synthesis analysis precisely.
- **Prerequisites and story role:** M11, M15, M21, M25 and M27. Reunites the statistical and implementation branches in a properly delimited comparison.
- **Conceptual connection:** The claim concerns the combined interface and its construction; it is not a new generic estimation exponent, the first unbiased estimator, or a finite-size optimality theorem.
- **Sources:** [Related work](../references/related-work.md), all comparison sections; [Interpretation](../science/interpretation.md), “Repetition and gate precision.” The selected anchor remains [Lin][lin], §4.2; the comparison sources are primary research, not additional educational anchors.

### M29. Compare complete implementations at equal statistical accuracy

- **Central question:** When could the variance reduction pay for the extra coherent work?
- **Understanding target:** Interpret the ideal independent-averaging criterion $`\kappa_M\tau_Q<\tau_B`$ using complete elapsed costs in the same units. Distinguish the sampler-call equivalence table from a native-gate or physical-runtime claim. Include compilation, input work, repetitions, precision and the relevant classical competitor; keep restoration's cost model separate.
- **Prerequisites and story role:** M18, M21, M22, M25, M27 and M28. Combines the established statistical benefit with its operational price and comparison assumptions.
- **Conceptual connection:** No QRAM removes one possible hidden cost. It does not by itself demonstrate advantage over direct sampling, structural classical methods or a particular physical architecture.
- **Sources:** [Interpretation](../science/interpretation.md), “Comparing variances at the same sampler-call budget” and “Physical resource boundary”; [Circuits and resources](../science/circuits-and-resources.md), “Full per-sample ledger”; [Positive weights](../science/positive-weights.md), §4.

### M30. Integrate the estimator's complete scientific contract

- **Central question:** What can be claimed for a specified sampler, implementation and downstream use after every assumption is made explicit?
- **Understanding target:** Connect the full chain: executable input and success event; Grover phase; calibrated path measurement; exact ideal moments; explicit no-QRAM circuit; compiled endpoint-aware bias and variance; statistical repetition or positive-weight composition; optional ideal restoration; and a fair cost comparison. Locate the authoritative argument for each link and distinguish a proved guarantee from an application or hardware condition still requiring evidence.
- **Prerequisites and story role:** M01–M29. Synthesizes the narrative into one account of mechanism, meaning, resources and scope.
- **Conceptual connection:** The global result is an explicit bounded estimation primitive with a controlled implementation route. Its usefulness in any larger task depends on preserving the stated access, error, independence and cost conditions.
- **Sources:** [Model and estimator](../science/model-and-estimator.md); [Variance proof](../science/variance-proof.md); [Circuits and resources](../science/circuits-and-resources.md); [Finite precision](../science/finite-precision.md); [Positive weights](../science/positive-weights.md); [Restoration](../science/restoration.md); [Interpretation](../science/interpretation.md); [Related work](../references/related-work.md).

[lin]: https://math.berkeley.edu/~linlin/qasc/qasc_notes.pdf
