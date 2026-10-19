#!/usr/bin/env python3
"""Deterministic finite-distribution checks for science/positive-weights.md.

Run from any directory with Python >= 3.9. No third-party dependencies.
Public entry point: run_checks() -> dict. Assertions fail with nonzero exit.
The direct clock kernel uses physical labels r=1,...,M; no random sampling.
This is a statistical verification, not a gate-synthesis or mixing simulation.
"""

import cmath
import itertools
import json
import math


def sine_distribution(m, p):
    """Return (outputs, probabilities) from the direct sine-DST amplitude sum."""
    assert isinstance(m, int) and m >= 2
    assert 0.0 <= p <= 1.0
    alpha = math.pi / (m + 1)
    phase = 2.0 * math.asin(math.sqrt(p))
    outputs = [
        (1.0 - math.cos(j * alpha) / math.cos(alpha)) / 2.0
        for j in range(1, m + 1)
    ]
    # These labels are exactly the endpoints in the mathematical output rule.
    outputs[0], outputs[-1] = 0.0, 1.0
    probabilities = []
    for j in range(1, m + 1):
        amplitude = sum(
            math.sin(r * alpha)
            * math.sin(j * r * alpha)
            * cmath.exp(1j * r * phase)
            for r in range(1, m + 1)
        ) * (2.0 / (m + 1))
        probabilities.append(abs(amplitude) ** 2)
    # Do not normalize or force endpoint probabilities: normalization and
    # endpoint concentration are tested independently from the amplitude sum.
    return outputs, probabilities


def kappa(m):
    return (m - 1) / (m + 1) * math.tan(math.pi / (m + 1)) ** 2


def expectation(values, probabilities):
    return math.fsum(v * q for v, q in zip(values, probabilities))


def assert_close(actual, expected, absolute=2e-12, relative=2e-10):
    assert math.isclose(actual, expected, abs_tol=absolute, rel_tol=relative), (
        actual, expected, abs(actual - expected)
    )


def metric(value):
    """Stable compact numeric formatting; no dependence on random seeds."""
    return float(format(value, ".12g"))


def check_moments():
    max_normalization = max_mean = max_variance = 0.0
    cases = 0
    for m in (2, 3, 4, 7, 15, 31):
        for p in (0.0, 1e-9, 1e-5, 0.001, 0.1, 0.37, 0.5,
                  0.83, 1.0 - 1e-5, 1.0 - 1e-9, 1.0):
            z, q = sine_distribution(m, p)
            total = math.fsum(q)
            mean = expectation(z, q)
            mse = expectation([(x - p) ** 2 for x in z], q)
            expected_variance = kappa(m) * p * (1.0 - p)
            assert_close(total, 1.0)
            assert_close(mean, p, absolute=1e-14)
            assert_close(mse, expected_variance, absolute=1e-14)
            assert min(z) >= 0.0 and max(z) <= 1.0
            max_normalization = max(max_normalization, abs(total - 1.0))
            max_mean = max(max_mean, abs(mean - p))
            max_variance = max(max_variance, abs(mse - expected_variance))
            cases += 1
    return {
        "cases": cases,
        "max_normalization_error": metric(max_normalization),
        "max_mean_error": metric(max_mean),
        "max_variance_error": metric(max_variance),
    }


def check_products():
    specifications = ((3, 0.13), (4, 0.61), (7, 0.28))
    distributions = [sine_distribution(m, p) for m, p in specifications]
    first_terms, second_terms = [], []
    for indices in itertools.product(*(range(m) for m, _ in specifications)):
        value = math.prod(distributions[i][0][j] for i, j in enumerate(indices))
        mass = math.prod(distributions[i][1][j] for i, j in enumerate(indices))
        first_terms.append(mass * value)
        second_terms.append(mass * value * value)
    actual_mean, actual_second = math.fsum(first_terms), math.fsum(second_terms)
    target = math.prod(p for _, p in specifications)
    expected_second = math.prod(
        p * p + kappa(m) * p * (1.0 - p) for m, p in specifications
    )
    relative_variance = actual_second / (target * target) - 1.0
    formula = math.prod(
        1.0 + kappa(m) * (1.0 - p) / p for m, p in specifications
    ) - 1.0
    assert_close(actual_mean, target)
    assert_close(actual_second, expected_second)
    assert_close(relative_variance, formula)
    exponent = math.fsum(kappa(m) * (1.0 - p) / p for m, p in specifications)
    assert relative_variance <= math.expm1(exponent) + 1e-12
    # A zero factor leaves only roundoff-sized probability outside output zero.
    z0, q0 = sine_distribution(7, 0.0)
    assert expectation(z0, q0) < 1e-25
    return {
        "enumerated_outcomes": math.prod(m for m, _ in specifications),
        "likelihood": metric(target),
        "relative_variance": metric(relative_variance),
        "mean_error": metric(abs(actual_mean - target)),
        "second_moment_error": metric(abs(actual_second - expected_second)),
    }


def check_pseudo_marginal_balance():
    prior = (0.2, 0.5, 0.3)
    probabilities = (0.07, 0.3, 0.83)
    budgets = (3, 4, 7)
    proposal = ((0.4, 0.4, 0.2), (0.1, 0.6, 0.3), (0.2, 0.3, 0.5))
    distributions = [sine_distribution(m, p) for m, p in zip(budgets, probabilities)]
    # Zero-weight proposals are excluded from the invariant support and retained
    # in the rejection probability by the row construction below.
    states = [(theta, j) for theta, m in enumerate(budgets) for j in range(1, m)]
    normalizer = math.fsum(a * p for a, p in zip(prior, probabilities))
    stationary = [
        prior[t] * distributions[t][1][j] * distributions[t][0][j] / normalizer
        for t, j in states
    ]
    transition = [[0.0 for _ in states] for _ in states]
    for i, (t, j) in enumerate(states):
        weight = distributions[t][0][j]
        for h, (u, k) in enumerate(states):
            if i == h:
                continue
            proposed_weight = distributions[u][0][k]
            ratio = prior[u] * proposal[u][t] * proposed_weight / (
                prior[t] * proposal[t][u] * weight
            )
            transition[i][h] = proposal[t][u] * distributions[u][1][k] * min(1.0, ratio)
        transition[i][i] = 1.0 - math.fsum(transition[i])
        assert transition[i][i] >= -1e-14
    balance_error = max(
        abs(stationary[i] * transition[i][j] - stationary[j] * transition[j][i])
        for i in range(len(states)) for j in range(len(states))
    )
    marginal_error = max(
        abs(math.fsum(stationary[i] for i, (t, _) in enumerate(states) if t == theta)
            - prior[theta] * probabilities[theta] / normalizer)
        for theta in range(len(prior))
    )
    invariant_error = max(
        abs(math.fsum(stationary[i] * transition[i][j] for i in range(len(states)))
            - stationary[j])
        for j in range(len(states))
    )
    assert balance_error < 1e-13 and marginal_error < 1e-13 and invariant_error < 1e-13
    assert_close(math.fsum(stationary), 1.0)
    return {
        "positive_weight_states": len(states),
        "max_detailed_balance_error": metric(balance_error),
        "max_posterior_marginal_error": metric(marginal_error),
        "max_invariance_error": metric(invariant_error),
    }


def check_convex_order_obstruction():
    m, p, n, threshold = 7, 0.1, 6, 19.0 / 20.0
    z, q = sine_distribution(m, p)
    endpoint_exact = (1324.0 - 936.0 * math.sqrt(2.0)) / 15625.0
    endpoint_classical = p ** n
    assert_close(q[-1], endpoint_exact, absolute=2e-16)
    assert endpoint_exact > 8.0 / 546875.0 > endpoint_classical
    classical_values = [k / n for k in range(n + 1)]
    classical_masses = [math.comb(n, k) * p ** k * (1.0 - p) ** (n - k)
                        for k in range(n + 1)]
    assert z[-2] < threshold and classical_values[-2] < threshold
    stop_loss_quantum = expectation([max(x - threshold, 0.0) for x in z], q)
    stop_loss_classical = expectation(
        [max(x - threshold, 0.0) for x in classical_values], classical_masses
    )
    quantum_variance = kappa(m) * p * (1.0 - p)
    classical_variance = p * (1.0 - p) / n
    assert stop_loss_quantum > stop_loss_classical
    assert quantum_variance < classical_variance
    # More direct samples further suppress this endpoint; no equal native-cost
    # claim is made about either n=6 or these illustrative sample counts.
    for larger_n in (7, 15):
        assert q[-1] > p ** larger_n
    return {
        "M": m, "p": p, "classical_samples": n,
        "quantum_endpoint_probability": metric(q[-1]),
        "classical_endpoint_probability": metric(endpoint_classical),
        "quantum_variance": metric(quantum_variance),
        "classical_variance": metric(classical_variance),
        "convex_test_threshold": threshold,
        "quantum_stop_loss": metric(stop_loss_quantum),
        "classical_stop_loss": metric(stop_loss_classical),
    }


def check_acceptance_bound():
    m, p, m_prime, p_prime = 7, 0.1, 4, 0.63
    z, q = sine_distribution(m, p)
    z_prime, q_prime = sine_distribution(m_prime, p_prime)
    variance_sum = kappa(m) * (1.0 - p) / p + kappa(m_prime) * (1.0 - p_prime) / p_prime
    factor = max(0.0, 1.0 - 0.5 * math.sqrt(variance_sum))
    slacks = []
    for ratio in (0.01, 0.2, 1.0, 3.0, 100.0):
        actual = math.fsum(
            qi * qj * min(x / p, ratio * y / p_prime)
            for x, qi in zip(z, q) for y, qj in zip(z_prime, q_prime)
        )
        bound = min(1.0, ratio) * factor
        assert actual + 1e-13 >= bound
        slacks.append(actual - bound)
    return {"proposal_pair_ratios_checked": 5, "bound_factor": metric(factor),
            "minimum_bound_slack": metric(min(slacks))}


def total_variation(first, second):
    return 0.5 * math.fsum(abs(a - b) for a, b in zip(first, second))


def check_posterior_perturbation():
    prior = (0.1, 0.2, 0.3, 0.4)
    factor_probabilities = ((1e-8, 0.7), (0.03, 0.2), (0.6, 0.9), (0.85, 0.4))
    etas = (0.03, 0.07)
    signs = ((-1, 1), (1, -1), (-1, -1), (1, 1))
    targets, perturbed_targets = [], []
    for weight, factors, factor_signs in zip(prior, factor_probabilities, signs):
        targets.append(weight * math.prod(factors))
        perturbed_targets.append(weight * math.prod(
            p + sign * eta * p * (1.0 - p)
            for p, eta, sign in zip(factors, etas, factor_signs)
        ))
    posterior = [x / math.fsum(targets) for x in targets]
    perturbed_posterior = [x / math.fsum(perturbed_targets) for x in perturbed_targets]
    a = math.prod(1.0 - eta for eta in etas)
    b = math.prod(1.0 + eta for eta in etas)
    bound = (math.sqrt(b) - math.sqrt(a)) / (math.sqrt(b) + math.sqrt(a))
    hyperbolic_bound = math.tanh(0.5 * math.fsum(math.atanh(eta) for eta in etas))
    assert_close(bound, hyperbolic_bound)
    actual = total_variation(posterior, perturbed_posterior)
    assert actual <= bound + 1e-13
    for base, changed in zip(posterior, perturbed_posterior):
        assert a / b - 1e-13 <= changed / base <= b / a + 1e-13
    # Sharpness of the general reweighting lemma, independently of the stronger
    # oriented-bias constraint on individual probability factors.
    mass_at_b = (math.sqrt(a * b) - a) / (b - a)
    sharp_base = [1.0 - mass_at_b, mass_at_b]
    raw = [sharp_base[0] * a, sharp_base[1] * b]
    sharp_changed = [x / math.fsum(raw) for x in raw]
    sharp_tv = total_variation(sharp_base, sharp_changed)
    assert_close(sharp_tv, bound)
    # Small absolute sampler error alone need not imply small posterior error.
    t = 1e-6
    model_tv = total_variation((0.5, 0.5), (1.0 / (1.0 + t), t / (1.0 + t)))
    assert t - t * t < 1.1e-6 and model_tv > 0.49999
    return {
        "actual_total_variation": metric(actual),
        "reweighting_bound": metric(bound),
        "sharp_example_error": metric(abs(sharp_tv - bound)),
        "absolute_model_error_example": metric(t - t * t),
        "model_example_total_variation": metric(model_tv),
    }


def check_rounding_and_orientation():
    eta, reporting_delta = 0.01, 0.025
    maximum_rounding_ratio = maximum_bias_ratio = 0.0
    maximum_oriented_mean_error = 0.0
    bit_counts = {}
    cases = 0
    for m in (3, 4, 7, 15, 31):
        z, _ = sine_distribution(m, 0.37)
        minimum = min(x * (1.0 - x) for x in z[1:-1])
        bits = max(0, math.ceil(math.log2(1.0 / (2.0 * eta * minimum))))
        denominator = 2 ** bits
        rounded = [round(x * denominator) / denominator for x in z]
        rounded[0], rounded[-1] = 0.0, 1.0
        bit_counts[str(m)] = bits
        for x, rounded_x in zip(z[1:-1], rounded[1:-1]):
            ratio = abs(rounded_x - x) / (eta * x * (1.0 - x))
            assert ratio <= 1.0 + 1e-12
            maximum_rounding_ratio = max(maximum_rounding_ratio, ratio)
        for p in (1e-5, 0.001, 0.1, 0.37, 0.5, 0.83, 0.999):
            _, q = sine_distribution(m, p)
            rounded_mean = expectation(rounded, q)
            oriented_budget = eta * (1.0 - kappa(m)) * p * (1.0 - p)
            assert abs(rounded_mean - p) <= oriented_budget + 2e-14
            maximum_bias_ratio = max(maximum_bias_ratio,
                                     abs(rounded_mean - p) / oriented_budget)
            # Explicit raw perturbation x -> x-delta*x*(1-x), followed by an
            # independent Bernoulli(p) orientation. This checks the orientation
            # identity, not the separate gate-synthesis/Markov-polynomial bound.
            reported = [x - reporting_delta * x * (1.0 - x) for x in z]
            _, complementary_q = sine_distribution(m, 1.0 - p)
            raw_mean = expectation(reported, q)
            complementary_mean = expectation(reported, complementary_q)
            actual_oriented_mean = (1.0 - p) * raw_mean + p * (1.0 - complementary_mean)
            expected_oriented_mean = p + reporting_delta * (1.0 - kappa(m)) * (
                p * (1.0 - p) * (2.0 * p - 1.0)
            )
            assert_close(actual_oriented_mean, expected_oriented_mean, absolute=2e-14)
            assert abs(actual_oriented_mean - p) <= (
                reporting_delta * (1.0 - kappa(m)) * p * (1.0 - p) + 2e-14
            )
            maximum_oriented_mean_error = max(
                maximum_oriented_mean_error, abs(actual_oriented_mean - expected_oriented_mean)
            )
            cases += 1
    return {
        "cases": cases, "rounding_eta": eta, "fractional_bits_by_M": bit_counts,
        "max_pointwise_rounding_fraction": metric(maximum_rounding_ratio),
        "max_mean_bias_fraction": metric(maximum_bias_ratio),
        "max_oriented_identity_error": metric(maximum_oriented_mean_error),
    }


def run_checks():
    return {
        "status": "passed",
        "physical_clock_labels": "r=1,...,M",
        "dependencies": "Python standard library",
        "moments": check_moments(),
        "products": check_products(),
        "pseudo_marginal_balance": check_pseudo_marginal_balance(),
        "convex_order_obstruction": check_convex_order_obstruction(),
        "equilibrium_acceptance_bound": check_acceptance_bound(),
        "posterior_perturbation": check_posterior_perturbation(),
        "rounding_and_orientation": check_rounding_and_orientation(),
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2, sort_keys=True, allow_nan=False))
