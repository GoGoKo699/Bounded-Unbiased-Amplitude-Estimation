#!/usr/bin/env python3
"""Finite-dimensional checks of the compiled moment and ideal restoration claims.

Run ``python verification/check_precision.py`` from the repository root.  The
only nonstandard dependency is NumPy.  ``run_checks()`` returns JSON-compatible
data and raises AssertionError on a failed check; stdout is one JSON document.

These are deterministic floating-point experiments, not proofs, gate-synthesis
certificates, stochastic fault simulations, or tests of approximate restoration.
Dense complex unitary errors deliberately mix the full clock's canonical,
spare, and sign labels; one case also retains an extra auxiliary qubit.  The
power ladder always uses the low clock bits, including on leaked states.

The tested bounds are those in science/finite-precision.md, equations (6)--(9).
Operator/normalization and polynomial residual tolerances are 5e-12.  Endpoint
probability tolerance is 5e-25 (squared floating-point cancellation errors).
Endpoint-scaled comparisons allow 2e-7 times x or p(1-p), plus that endpoint
floor, because relative errors amplify cancellation near p=1e-14.  Ordinary
raw-moment and polynomial checks retain their stricter absolute tolerance.
"""

import json
import math

import numpy as np
from numpy.polynomial import chebyshev as cheb


ABS_TOL = 5e-12
ENDPOINT_TOL = 5e-25
SCALED_TOL = 2e-7


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def full_clock(ell, extra_auxiliary=False):
    """Construct E^dagger F_(2L) E, without using a DST as a primitive.

    Label = r + L*sign + 2L*aux, and u=1.  E is the complete H/Z and
    controlled-negation unitary, including its action at r=0 and sign=1.
    The added auxiliary, when present, is initially zero and never discarded.
    """
    L = 1 << ell
    dimension = 2 * L
    E = np.zeros((dimension, dimension), complex)
    for column in range(dimension):
        r, sign = column % L, column // L
        E[r, column] = 1 / math.sqrt(2)
        E[L + (-r) % L, column] = -(-1) ** sign / math.sqrt(2)
    labels = np.arange(dimension)
    F = np.exp(2j * math.pi * np.outer(labels, labels) / dimension) / math.sqrt(dimension)
    V = E.conj().T @ F @ E
    if extra_auxiliary:
        V = np.kron(np.eye(2), V)
    labels = np.arange(V.shape[0])
    path = np.arange(1, L)
    alpha = math.pi / L
    outputs = np.zeros(V.shape[0])
    outputs[path] = (1 - np.cos(path * alpha) / math.cos(alpha)) / 2
    outputs[1], outputs[L - 1] = 0.0, 1.0
    D = math.sqrt(2 / L) * np.sin(alpha * np.outer(path, path))
    require(np.max(abs(V[np.ix_(path, path)] - 1j * D)) < ABS_TOL,
            "full ideal transform does not implement the sine transform")
    return V, labels % L, outputs


def perturbation(dimension, angle, seed):
    """A reproducible exp(i*angle*H), where H is dense Hermitian of norm one."""
    if angle == 0:
        return np.eye(dimension, dtype=complex)
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    H = (raw + raw.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    eigenvalues /= max(abs(eigenvalues))
    return (eigenvectors * np.exp(1j * angle * eigenvalues)) @ eigenvectors.conj().T


class CompiledClock:
    def __init__(self, ell, angle, bits, extra_auxiliary=False, side="left"):
        self.M = (1 << ell) - 1
        self.ideal, self.exponents, self.exact_outputs = full_clock(ell, extra_auxiliary)
        error = perturbation(len(self.exponents), angle, 9103 + 31 * ell + int(extra_auxiliary))
        self.V = error @ self.ideal if side == "left" else self.ideal @ error
        self.adjoint = self.V.conj().T  # Exact inverse of the same compiled matrix.
        self.prepared = self.V[:, 1]
        self.outputs = self.exact_outputs.copy()
        if bits is not None:
            self.outputs = np.clip(np.rint(self.outputs * 2**bits) / 2**bits, 0, 1)
        self.outputs[1], self.outputs[self.M] = 0.0, 1.0
        self.eta = float(np.linalg.norm(self.V - self.ideal, 2))
        self.rho = float(np.max(abs(self.outputs - self.exact_outputs)))
        self.kappa = (self.M - 1) / (self.M + 1) * math.tan(math.pi / (self.M + 1)) ** 2
        self.normalization_error = 0.0
        self.cache = {}
        require(np.all((0 <= self.outputs) & (self.outputs <= 1)), "output outside [0,1]")
        require(np.max(abs(self.adjoint @ self.V - np.eye(len(self.exponents)))) < ABS_TOL,
                "perturbed clock is not unitary to numerical tolerance")

    def probabilities(self, p, equal_mixture=True):
        # atan2 keeps both endpoints well conditioned; no arccos(1-2p).
        phi = 2 * math.atan2(math.sqrt(p), math.sqrt(1 - p))
        signs = np.array([1.0, -1.0]) if equal_mixture else np.array([1.0])
        phase_states = self.prepared[:, None] * np.exp(1j * self.exponents[:, None] * phi * signs)
        amplitudes = self.adjoint @ phase_states
        probabilities = np.mean(abs(amplitudes) ** 2, axis=1)
        total = float(np.sum(probabilities))
        self.normalization_error = max(self.normalization_error, abs(total - 1))
        require(abs(total - 1) < ABS_TOL, "state norm drift")
        # Correct only roundoff in a separately checked unitary calculation.
        return probabilities / total

    def moments(self, p):
        p = float(p)
        if p not in self.cache:
            probabilities = self.probabilities(p)
            mean = float(probabilities @ self.outputs)
            second = float(probabilities @ (self.outputs**2))
            mse = float(probabilities @ ((self.outputs - p) ** 2))
            self.cache[p] = (mean, second, mse)
        return self.cache[p]


def probability_grid():
    rare = [1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4]
    return np.unique(np.r_[np.linspace(0, 1, 65), rare, [1 - x for x in rare]])


def polynomial_check(clock, grid):
    """Fit at Chebyshev nodes, then test unrelated points and higher degrees."""
    degree = clock.M
    nodes = np.cos(math.pi * (np.arange(degree + 1) + 0.5) / (degree + 1))
    values = np.array([clock.moments((1 - t) / 2)[:2] for t in nodes])
    coefficients = cheb.chebfit(nodes, values, degree)
    actual = np.array([clock.moments(p)[:2] for p in grid])
    predicted = cheb.chebval(1 - 2 * grid, coefficients).T
    residual = float(np.max(abs(actual - predicted)))
    long_degree = 2 * degree + 2
    extra_nodes = np.cos(math.pi * (np.arange(long_degree + 1) + 0.5) / (long_degree + 1))
    extra_values = np.array([clock.moments((1 - t) / 2)[:2] for t in extra_nodes])
    extra_coefficients = cheb.chebfit(extra_nodes, extra_values, long_degree)
    high_degree = float(np.max(abs(extra_coefficients[degree + 1:])))
    require(max(residual, high_degree) < ABS_TOL, "raw moments failed degree-M polynomial check")
    return dict(max_off_grid_residual=residual, max_coefficient_above_M=high_degree)


def check_compiled_moments():
    cases = [(ell, angle, bits, False, side)
             for ell in (2, 3, 4)
             for angle, bits, side in ((0.0, None, "left"),
                                       (1e-6, 28, "right"),
                                       (1e-2, 12, "left"))]
    cases.append((3, 2e-3, 20, True, "left"))
    grid = probability_grid()
    records = []
    uncorrected_endpoint_witness = 0.0
    single_phase_polynomial_witness = 0.0
    for ell, angle, bits, auxiliary, side in cases:
        clock = CompiledClock(ell, angle, bits, auxiliary, side)
        M = clock.M
        sigma1, sigma2 = 2 * clock.eta + clock.rho, 2 * clock.eta + 2 * clock.rho
        d1, d2 = 2 * M**2 * sigma1, 2 * M**2 * sigma2
        polynomial = polynomial_check(clock, grid)
        max_raw_errors = [0.0, 0.0]
        max_bias_ratio = max_mse_ratio = max_identity_error = 0.0
        max_scaled_bias = max_scaled_mse = 0.0
        for p in grid:
            mean, second, mse = clock.moments(p)
            cm, cs, complement_mse = clock.moments(1 - p)
            e1, e2 = mean - p, second - p**2 - clock.kappa * p * (1 - p)
            ce1, ce2 = cm - (1 - p), cs - (1 - p) ** 2 - clock.kappa * p * (1 - p)
            max_raw_errors[0] = max(max_raw_errors[0], abs(e1))
            max_raw_errors[1] = max(max_raw_errors[1], abs(e2))
            require(abs(e1) <= sigma1 + ABS_TOL and abs(e2) <= sigma2 + ABS_TOL,
                    f"uniform moment comparison failed: M={M}, p={p}")
            tolerance = SCALED_TOL * p + ENDPOINT_TOL
            require(abs(e1) <= d1 * p + tolerance and abs(e2) <= d2 * p + tolerance,
                    f"one-sided endpoint bound failed: M={M}, p={p}")
            # Use errors and direct centered moments to avoid subtracting 1-1
            # or two nearly equal second moments at rare endpoint probabilities.
            bias = (1 - p) * e1 - p * ce1
            oriented_mse = (1 - p) * mse + p * complement_mse
            identity_mse = (clock.kappa * p * (1 - p) + (1 - p) * e2 + p * ce2
                            - 2 * p * (1 - p) * (e1 + ce1))
            identity_mean = (1 - p) * mean + p * (1 - cm)
            max_identity_error = max(max_identity_error, abs(oriented_mse - identity_mse),
                                     abs(identity_mean - p - bias))
            scale = p * (1 - p)
            bias_bound = 4 * M**2 * sigma1 * scale
            mse_bound = (clock.kappa + 4 * M**2 * (sigma1 + sigma2)) * scale
            tolerance = SCALED_TOL * scale + ENDPOINT_TOL
            require(abs(bias) <= bias_bound + tolerance,
                    f"oriented bias bound failed: M={M}, p={p}")
            require(oriented_mse <= mse_bound + tolerance,
                    f"oriented MSE bound failed: M={M}, p={p}")
            if scale:
                max_scaled_bias = max(max_scaled_bias, abs(bias) / scale)
                max_scaled_mse = max(max_scaled_mse, oriented_mse / scale)
                max_mse_ratio = max(max_mse_ratio, oriented_mse / mse_bound)
                if bias_bound:
                    max_bias_ratio = max(max_bias_ratio, abs(bias) / bias_bound)
        require(max_identity_error < ABS_TOL, "orientation conditioning identity failed")
        require(clock.moments(0)[0] <= ENDPOINT_TOL, "paired zero endpoint not restored")
        require(clock.moments(0)[2] <= ENDPOINT_TOL, "oriented endpoint MSE not zero")
        if angle:
            uncorrected_endpoint_witness = max(uncorrected_endpoint_witness,
                                               abs(clock.moments(1)[0] - 1))
            # Dropping the equal +/- eigenphase mixture should generically
            # destroy the degree-M polynomial property for a complex clock.
            nodes = np.cos(math.pi * (np.arange(M + 1) + .5) / (M + 1))
            single = np.array([clock.probabilities((1 - t) / 2, False) @ clock.outputs for t in nodes])
            fitted = cheb.chebfit(nodes, single, M)
            actual = np.array([clock.probabilities(p, False) @ clock.outputs for p in grid])
            defect = float(np.max(abs(actual - cheb.chebval(1 - 2 * grid, fitted))))
            single_phase_polynomial_witness = max(single_phase_polynomial_witness, defect)
        invalid = np.r_[0, np.arange(M + 1, len(clock.exponents))]
        leakage = float(np.sum(abs(clock.prepared[invalid]) ** 2))
        records.append(dict(M=M, dimension=len(clock.exponents), extra_auxiliary=auxiliary,
                            perturbation_side=side, perturbation_angle=angle, output_bits=bits,
                            operator_error=clock.eta, output_error=clock.rho,
                            sigma1=sigma1, sigma2=sigma2, prepared_noncanonical_weight=leakage,
                            polynomial=polynomial, max_first_raw_error=max_raw_errors[0],
                            max_second_raw_error=max_raw_errors[1],
                            max_bias_over_p_one_minus_p=max_scaled_bias,
                            max_mse_over_p_one_minus_p=max_scaled_mse,
                            max_bias_bound_ratio=max_bias_ratio, max_mse_bound_ratio=max_mse_ratio,
                            max_conditioning_identity_error=max_identity_error,
                            max_normalization_error=clock.normalization_error))
    require(uncorrected_endpoint_witness > 1e-8, "perturbations did not exercise upper endpoint failure")
    require(single_phase_polynomial_witness > 1e-8, "complex perturbations did not exercise phase-mixture requirement")

    # Independent readout error supplies a concrete failure when the inverse
    # is not paired. Rotate two output labels after an otherwise paired run.
    clock = CompiledClock(3, 1e-2, 12)
    mismatch = np.eye(len(clock.exponents), dtype=complex)
    angle = .025
    mismatch[np.ix_([1, clock.M], [1, clock.M])] = [[math.cos(angle), 1j * math.sin(angle)],
                                                   [1j * math.sin(angle), math.cos(angle)]]
    bad_state = mismatch @ clock.adjoint @ clock.prepared
    unpaired_zero_mean = float((abs(bad_state) ** 2) @ clock.outputs)
    require(unpaired_zero_mean > 1e-5, "unpaired-inverse negative control did not fail")
    return dict(cases=records, grid_points=len(grid), smallest_interior_probability=float(grid[1]),
                negative_controls=dict(unoriented_upper_endpoint_bias=uncorrected_endpoint_witness,
                                       single_phase_polynomial_residual=single_phase_polynomial_witness,
                                       unpaired_zero_endpoint_mean=unpaired_zero_mean))


def check_ideal_restoration():
    """Propagate target density matrices, rather than sampling a geometric law."""
    identity = np.eye(2, dtype=complex)
    J = np.array([[0, -1j], [1j, 0]], complex)
    vector = np.array([math.sqrt(.37), np.exp(.43j) * math.sqrt(.63)])
    initial = np.outer(vector, vector.conj())
    cutoff = 32
    records = []
    worst_kraus = worst_return = worst_tail = worst_expectation = worst_second = 0.0
    for M in (3, 5, 7, 15):
        L = M + 1
        path = np.arange(1, L)
        sine = math.sqrt(2 / L) * np.sin(math.pi * path / L)
        D = math.sqrt(2 / L) * np.sin(math.pi * np.outer(path, path) / L)
        for p in (0.0, 1e-10, .02, .2, .5, .83, 1.0):
            phi = 2 * math.atan2(math.sqrt(p), math.sqrt(1 - p))
            G = math.cos(phi) * identity + 1j * math.sin(phi) * J
            powers = np.array([np.linalg.matrix_power(G, int(r - L // 2)) for r in path])
            kraus = np.einsum("jr,r,rab->jab", D, sine, powers)
            weights = np.real(np.einsum("jab,jab->j", kraus.conj(), kraus)) / 2
            even = kraus[1::2]
            odd = kraus[::2]
            for j, K in enumerate(kraus, start=1):
                basis = identity if j % 2 else J
                scalar = np.trace(basis @ K) / 2
                worst_kraus = max(worst_kraus, float(np.max(abs(K - scalar * basis))),
                                  float(np.max(abs(K.conj().T @ K - weights[j - 1] * identity))),
                                  abs(float(scalar.imag if j % 2 else scalar.real)))
            require(abs(float(sum(weights)) - 1) < ABS_TOL, "Kraus map is not trace preserving")
            s = float(sum(weights[1::2]))
            independent_s = float(np.sum(sine**2 * np.sin((path - L // 2) * phi) ** 2))
            require(abs(s - independent_s) < ABS_TOL, "even-label probability formula failed")

            def channel(operators, state):
                return sum((K @ state @ K.conj().T for K in operators), np.zeros((2, 2), complex))

            immediate = channel(odd, initial)
            worst_return = max(worst_return, float(np.max(abs(immediate - np.trace(immediate) * initial))))
            continuing = channel(even, initial)
            tails = []
            for n in range(1, cutoff + 1):
                tail = float(np.trace(continuing).real)
                tails.append(tail)
                worst_tail = max(worst_tail, abs(tail - s * (1 - s) ** (n - 1)))
                returned = channel(even, continuing)
                worst_return = max(worst_return, float(np.max(abs(returned - np.trace(returned) * initial))))
                continuing = channel(odd, continuing)
            if p in (0.0, 1.0):
                require(s < ENDPOINT_TOL, "an ideal endpoint failed immediate restoration")
                expected, expected_second = 1.0, 1.0
            else:
                require(s > 0, "interior probability has no return event")
                # E N=sum_{n>=0}P(N>n); E N²=sum_{n>=0}(2n+1)P(N>n).
                # Close only the remaining geometric tail analytically.
                tail_next = float(np.trace(continuing).real)
                expected = 1 + sum(tails) + tail_next / s
                expected_second = (1 + sum((2 * n + 1) * tails[n - 1] for n in range(1, cutoff + 1))
                                   + tail_next * ((2 * cutoff + 3) / s + 2 * (1 - s) / s**2))
                worst_expectation = max(worst_expectation, abs(expected - 2))
                worst_second = max(worst_second, abs(expected_second / (2 + 2 / s) - 1))
            records.append(dict(M=M, p=p, even_probability=s, expected_rounds=expected,
                                second_moment_rounds=expected_second, tail_at_cutoff=tails[-1]))
    require(max(worst_kraus, worst_return, worst_tail, worst_expectation, worst_second) < ABS_TOL,
            "ideal Kraus or stopping-time check failed")
    return dict(cases=records, propagated_rounds=cutoff, max_kraus_identity_error=worst_kraus,
                max_returned_state_error=worst_return, max_tail_error=worst_tail,
                max_expected_rounds_error=worst_expectation, max_second_moment_relative_error=worst_second)


def run_checks():
    return dict(passed=True, scope="Finite-dimensional checks, not a proof or hardware simulation",
                tolerances=dict(absolute=ABS_TOL, endpoint_probability=ENDPOINT_TOL,
                                endpoint_scaled_relative=SCALED_TOL),
                finite_precision=check_compiled_moments(), ideal_restoration=check_ideal_restoration())


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2, allow_nan=False))
