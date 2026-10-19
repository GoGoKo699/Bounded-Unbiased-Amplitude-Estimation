#!/usr/bin/env python3
"""Independent small-circuit checks; requires only Python 3 and NumPy.

Run from the repository root: python verification/check_circuits.py
This is an ideal state-vector/reversible-logic check, not a hardware simulation.
Qubit 0 is the least significant bit. Gates are listed in execution order.
"""
from collections import Counter
import json
import math

import numpy as np


H = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)


def basis_run(gates, bits):
    """Classical reversible circuit plus exact Z/CZ phases."""
    bits = list(bits)
    phase = 1
    for name, *q in gates:
        if name == "X":
            bits[q[0]] ^= 1
        elif name == "CX":
            bits[q[1]] ^= bits[q[0]]
        elif name == "CCX":
            bits[q[2]] ^= bits[q[0]] & bits[q[1]]
        elif name == "Z":
            phase *= 1 - 2 * bits[q[0]]
        elif name == "CZ":
            phase *= 1 - 2 * (bits[q[0]] & bits[q[1]])
        else:
            raise ValueError(name)
    return bits, phase


def vector_run(gates, state):
    """Apply actual elementary matrices, never a DST matrix primitive."""
    state = np.array(state, complex, copy=True)
    dim = state.shape[0]
    indices = np.arange(dim)
    for name, *args in gates:
        if name == "H":
            bit = args[0]
            low = indices[(indices & (1 << bit)) == 0]
            high = low | (1 << bit)
            a, b = state[low].copy(), state[high].copy()
            state[low] = (a + b) / math.sqrt(2)
            state[high] = (a - b) / math.sqrt(2)
        elif name in ("X", "CX", "CCX"):
            target = args[-1]
            mask = np.ones(dim, bool)
            for control in args[:-1]:
                mask &= (indices & (1 << control)) != 0
            permutation = indices ^ (mask.astype(int) << target)
            state = state[permutation]
        elif name == "SWAP":
            a, b = args
            flips = ((indices >> a) ^ (indices >> b)) & 1
            state = state[indices ^ (flips << a) ^ (flips << b)]
        elif name in ("Z", "CZ", "CP", "T", "TDG"):
            if name == "CP":
                control, target, angle = args
                mask = ((indices >> control) & 1) * ((indices >> target) & 1)
            elif name == "CZ":
                control, target = args
                angle = math.pi
                mask = ((indices >> control) & 1) * ((indices >> target) & 1)
            else:
                angle = {"Z": math.pi, "T": math.pi / 4, "TDG": -math.pi / 4}[name]
                mask = (indices >> args[0]) & 1
            state *= np.exp(1j * angle * mask)
        else:
            raise ValueError(name)
    return state


def qft_gates(n):
    gates = []
    for j in range(n - 1, -1, -1):
        gates.append(("H", j))
        for k in range(j - 1, -1, -1):
            gates.append(("CP", k, j, math.pi / (1 << (j - k))))
    gates.extend(("SWAP", j, n - 1 - j) for j in range(n // 2))
    return gates


def controlled_negation_gates(ell):
    """Negate low ell bits if high bit ell is 1, returning work to zero.

    Work bits ell+1,...,2ell-1 hold ORs of successive low-bit prefixes.
    Negation preserves whether each low-bit prefix is nonzero, which makes
    uncomputation using the changed input valid on every computational input.
    """
    if ell == 1:
        return []
    work = list(range(ell + 1, 2 * ell))
    compute = [("CX", 0, work[0])]
    for i in range(1, ell - 1):
        compute += [("CX", work[i - 1], work[i]), ("CX", i, work[i]),
                    ("CCX", work[i - 1], i, work[i])]
    change = [("CCX", ell, work[i - 1], i) for i in range(1, ell)]
    return compute + change + list(reversed(compute))


def embedding_matrix(ell):
    """Clean-work action of the H/Z/reversible-negation gate sequence."""
    n = ell + 1
    dim = 1 << n
    negation = controlled_negation_gates(ell)
    permutation = []
    for value in range(dim):
        bits = [(value >> q) & 1 for q in range(2 * ell)]
        output, phase = basis_run(negation, bits)
        assert phase == 1 and not any(output[n:])
        permutation.append(sum(output[q] << q for q in range(n)))
    hz = np.column_stack([
        vector_run([("H", ell), ("Z", ell)], np.eye(dim)[:, j])
        for j in range(dim)
    ])
    # The permutation is an involution; this row indexing applies it on output.
    assert all(permutation[permutation[j]] == j for j in range(dim))
    return hz[permutation]


def mcx(controls, target, work):
    k = len(controls)
    if k == 0:
        return [("X", target)]
    if k == 1:
        return [("CX", controls[0], target)]
    if k == 2:
        return [("CCX", *controls, target)]
    assert len(work) >= k - 2
    compute = [("CCX", controls[0], controls[1], work[0])]
    for i in range(2, k - 1):
        compute.append(("CCX", work[i - 2], controls[i], work[i - 1]))
    return compute + [("CCX", work[k - 3], controls[-1], target)] + list(reversed(compute))


def normalize_clauses(n, clauses):
    if n < 0:
        raise ValueError("negative variable count")
    result = []
    for clause in clauses:
        if len(clause) > 3:
            raise ValueError("this implementation accepts clauses of at most three literals")
        if any(type(x) is not int or x == 0 or abs(x) > n for x in clause):
            raise ValueError("literal outside 1,...,n")
        unique = tuple(dict.fromkeys(clause))
        result.append(None if any(-x in unique for x in unique) else unique)
    return result


def cnf_sampler(n, clauses):
    """Return Boolean part of A; precede it by H on the n input wires.

    Signed integers label literals. Repetitions simplify, tautologies give a
    constant-one clause, an empty clause gives zero, and an empty CNF is true.
    No input-dependent table lookup or quantum memory access is used.
    """
    clauses = normalize_clauses(n, clauses)
    c = len(clauses)
    n_work = max(max(c - 2, 0), max((max(len(x) - 2, 0) for x in clauses if x is not None), default=0))
    flag = n + c
    work = list(range(flag + 1, flag + 1 + n_work))
    gates = []
    for j, clause in enumerate(clauses):
        target = n + j
        if clause is None:
            gates.append(("X", target))
        elif clause:
            flips = [("X", x - 1) for x in clause if x > 0]
            gates += flips + mcx([abs(x) - 1 for x in clause], target, work)
            gates += list(reversed(flips)) + [("X", target)]
        # An empty clause leaves its initially clean target zero.
    gates += mcx(list(range(n, n + c)), flag, work)
    return gates, flag + 1 + n_work, flag, work, clauses


def controlled_zero_reflection(width):
    """All data wires are reflected, including clause bits and sampler work."""
    assert width >= 1
    control = width
    work = list(range(width + 1, 2 * width))
    flips = [("X", q) for q in range(width)]
    if width == 1:
        return flips + [("CZ", control, 0)] + flips, control, work
    compute = [("CCX", 0, 1, work[0])]
    for i in range(2, width):
        compute.append(("CCX", work[i - 2], i, work[i - 1]))
    gates = flips + compute + [("CZ", control, work[-1])]
    return gates + list(reversed(compute)) + flips, control, work


def check_reversible_logic():
    tests = 0
    for ell in range(1, 8):
        gates = controlled_negation_gates(ell)
        count = Counter(g[0] for g in gates)
        if ell >= 2:
            assert count["CCX"] == 3 * ell - 5 and count["CX"] == 4 * ell - 6
        L = 1 << ell
        for h in (0, 1):
            for x in range(L):
                bits = [(x >> q) & 1 for q in range(ell)] + [h] + [0] * (ell - 1)
                out, phase = basis_run(gates, bits)
                value = sum(out[q] << q for q in range(ell))
                assert value == ((-x) % L if h else x)
                assert out[ell] == h and not any(out[ell + 1:]) and phase == 1
                tests += 1
    cases = [(0, []), (0, [()]), (1, [(1,)]), (1, [(-1,)]),
             (1, [(1, 1, 1)]), (1, [(1, -1, 1)]),
             (2, [(1, 2), (-1, -2)]), (2, [(1,), (-1,)]),
             (3, [(1, 2, 3), (-1, 2, -3), (1, -2, 3)]),
             (4, [(1, -2, 3), (-1, 2, 4), (2, 3, -4), (-2, -3, -4)])]
    baseline = []
    for n, raw in cases:
        gates, width, flag, work, clauses = cnf_sampler(n, raw)
        sat = 0
        for x in range(1 << n):
            bits = [(x >> q) & 1 for q in range(n)] + [0] * (width - n)
            out, phase = basis_run(gates, bits)
            for j, clause in enumerate(raw):
                clause_truth = any(bool(bits[abs(lit) - 1]) == (lit > 0) for lit in clause)
                assert out[n + j] == clause_truth
            truth = all(any(bool(bits[abs(lit) - 1]) == (lit > 0) for lit in clause) for clause in raw)
            assert out[flag] == truth and not any(out[q] for q in work) and phase == 1
            assert out[:n] == bits[:n]
            back, phase = basis_run(list(reversed(gates)), out)
            assert back == bits and phase == 1
            sat += truth
            tests += 1
        if len(raw) >= 3 and all(len(set(abs(x) for x in cl)) == 3 for cl in raw):
            c = len(raw)
            count = Counter(g[0] for g in gates)
            assert count["CCX"] == 5 * c - 3
            assert count["X"] == c + 2 * sum(x > 0 for cl in raw for x in cl)
            assert count["CX"] == 0 and width == n + 2 * c - 1
            baseline.append(dict(n=n, clauses=c, satisfying=sat, width=width, counts=dict(count)))
    for n, raw in [(1, [(0,)]), (1, [(2,)]), (1, [(1, 1, 1, 1)])]:
        try:
            cnf_sampler(n, raw)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid clause accepted")
    for width in range(1, 10):
        gates, control, work = controlled_zero_reflection(width)
        assert Counter(g[0] for g in gates)["CCX"] == 2 * (width - 1)
        for value in range(1 << (width + 1)):
            bits = [(value >> q) & 1 for q in range(width + 1)] + [0] * len(work)
            out, phase = basis_run(gates, bits)
            expected = -1 if bits[control] and not any(bits[:width]) else 1
            assert out == bits and phase == expected
            tests += 1
    return dict(basis_cases=tests, cnf_examples=baseline)


def check_toffoli_decomposition():
    a, b, t = 0, 1, 2
    gates = [("H", t), ("CX", b, t), ("TDG", t), ("CX", a, t),
             ("T", t), ("CX", b, t), ("TDG", t), ("CX", a, t),
             ("T", b), ("T", t), ("H", t), ("CX", a, b),
             ("T", a), ("TDG", b), ("CX", a, b)]
    error = 0.0
    for j in range(8):
        actual = vector_run(gates, np.eye(8)[:, j])
        expected = vector_run([("CCX", a, b, t)], np.eye(8)[:, j])
        error = max(error, float(np.max(np.abs(actual - expected))))
    assert error < 1e-14
    return dict(max_error=error, counts=dict(Counter(g[0] for g in gates)))


def check_dst():
    results = []
    for ell in range(2, 7):
        L = 1 << ell
        dim = 2 * L
        M = L - 1
        F = np.column_stack([vector_run(qft_gates(ell + 1), np.eye(dim)[:, j]) for j in range(dim)])
        labels = np.arange(dim)
        F_exact = np.exp(2j * math.pi * np.outer(labels, labels) / dim) / math.sqrt(dim)
        E = embedding_matrix(ell)
        V = E.conj().T @ F @ E
        path = np.arange(1, L)
        D = math.sqrt(2 / L) * np.sin(math.pi * np.outer(path, path) / L)
        forbidden = np.r_[0, np.arange(L, dim)]
        qft_error = float(np.max(np.abs(F - F_exact)))
        dst_error = float(np.max(np.abs(V[np.ix_(path, path)] - 1j * D)))
        leakage = float(np.max(np.abs(V[np.ix_(forbidden, path)])))
        c = math.cos(math.pi / L)
        z = (1 - np.cos(math.pi * path / L) / c) / 2
        a = V[:, 1]
        preparation_error = float(np.max(abs(a[path] - 1j * math.sqrt(2 / L) * np.sin(math.pi * path / L))))
        mean_error = var_error = 0.0
        for p in [0, 1e-12, 1e-8, .001, .05, .25, .5, .9, 1 - 1e-8, 1]:
            phi = 2 * math.asin(math.sqrt(p))
            state = V.conj().T @ (np.exp(1j * phi * (labels % L)) * a)
            probabilities = np.abs(state[path]) ** 2
            mean_error = max(mean_error, abs(float(probabilities @ z) - p))
            variance = float(probabilities @ ((z - p) ** 2))
            exact = p * (1 - p) * (M - 1) / (M + 1) * math.tan(math.pi / L) ** 2
            var_error = max(var_error, abs(variance - exact))
        record = dict(M=M, qft_error=qft_error, dst_error=dst_error, leakage=leakage,
                      preparation_error=preparation_error, mean_error=mean_error, variance_error=var_error)
        assert max(v for k, v in record.items() if k != "M") < 1e-12
        results.append(record)
    return results


def check_grover_input():
    rng = np.random.default_rng(190026)
    worst = 0.0
    shift_error = 0.0
    # Two genuinely complex good/bad data subspaces, not an eigenstate input.
    for M in [2, 3, 7, 15]:
        r = np.arange(M)
        alpha = math.pi / (M + 1)
        sine = math.sqrt(2 / (M + 1)) * np.sin((r + 1) * alpha)
        D = math.sqrt(2 / (M + 1)) * np.sin(np.outer(r + 1, r + 1) * alpha)
        for p in [0, .00001, .13, .5, .83, 1]:
            good = rng.normal(size=2) + 1j * rng.normal(size=2)
            bad = rng.normal(size=2) + 1j * rng.normal(size=2)
            good /= np.linalg.norm(good)
            bad /= np.linalg.norm(bad)
            psi = np.zeros(4, complex)
            psi[[1, 3]], psi[[0, 2]] = math.sqrt(p) * good, math.sqrt(1 - p) * bad
            columns = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
            columns[:, 0] = psi
            A, _ = np.linalg.qr(columns)
            A[:, 0] *= np.vdot(A[:, 0], psi)
            assert np.max(abs(A[:, 0] - psi)) < 1e-14
            S0 = np.diag([-1, 1, 1, 1])
            Sg = np.diag([1, -1, 1, -1])
            G = -A @ S0 @ A.conj().T @ Sg
            assert np.max(abs(G - (2 * np.outer(psi, psi.conj()) - np.eye(4)) @ Sg)) < 1e-14
            # Circuit order Sg,A†,S0,A,minus sign. Control zero cancels A†,A.
            assert np.max(abs(A @ A.conj().T - np.eye(4))) < 1e-14
            # Physical binary ladder uses r=k+1, not the abstract index k.
            joint = np.stack([sine[k] * np.linalg.matrix_power(G, k + 1) @ psi for k in range(M)])
            actual = np.sum(np.abs(D @ joint) ** 2, axis=1)
            phi = 2 * math.asin(math.sqrt(p))
            expected = (np.abs(D @ (sine * np.exp(1j * (r + 1) * phi))) ** 2 +
                        np.abs(D @ (sine * np.exp(-1j * (r + 1) * phi))) ** 2) / 2
            abstract = (np.abs(D @ (sine * np.exp(1j * r * phi))) ** 2 +
                        np.abs(D @ (sine * np.exp(-1j * r * phi))) ** 2) / 2
            shift_error = max(shift_error, float(np.max(abs(expected - abstract))))
            worst = max(worst, float(np.max(abs(actual - expected))))
    assert max(worst, shift_error) < 1e-12
    return dict(max_distribution_error=worst, common_power_shift_error=shift_error)


def resource_ledger(n, c, ell, positive_literals):
    """Distinct-variable 3CNF baseline; pre-synthesis logical counts."""
    assert n >= 3 and c >= 3 and ell >= 2 and 0 <= positive_literals <= 3 * c
    M = (1 << ell) - 1
    W = n + 2 * c - 1
    return dict(M=M, sampler_width=W,
                peak_qubits=W + ell + 1 + max(W - 1, ell - 1),
                CCX=(2 * M + 1) * (5 * c - 3) + 2 * M * (W - 1) + 4 * (3 * ell - 5),
                CX=4 * (4 * ell - 6),
                H=(2 * M + 1) * n + 4 + 2 * (ell + 1),
                X=(2 * M + 1) * (c + 2 * positive_literals) + 2 * M * W + 1,
                CZ=2 * M, Z=M + 4, CP=ell * (ell + 1),
                SWAP=2 * ((ell + 1) // 2))


def check_resource_counts():
    raw = [(1, 2, 3), (-1, 2, -3), (1, -2, 3)]
    n, c, ell, positives = 3, 3, 3, 6
    M = (1 << ell) - 1
    sampler, W, _, _, _ = cnf_sampler(n, raw)
    reflection, _, _ = controlled_zero_reflection(W)
    gates = (sampler + [("H", q) for q in range(n)]) * (2 * M + 1)
    gates += reflection * M + [("CZ", 0, 1), ("Z", 0)] * M
    gates += (controlled_negation_gates(ell) + [("H", ell), ("Z", ell)]) * 4
    gates += qft_gates(ell + 1) * 2 + [("X", 0)]
    actual = dict(Counter(g[0] for g in gates))
    ledger = resource_ledger(n, c, ell, positives)
    expected = {k: v for k, v in ledger.items() if k not in ("M", "sampler_width", "peak_qubits")}
    assert actual == expected
    return ledger


def run_checks():
    return dict(reversible_logic=check_reversible_logic(),
                   toffoli_decomposition=check_toffoli_decomposition(),
                   fourier_embedding=check_dst(), general_grover_input=check_grover_input(),
                   illustrative_ledger=check_resource_counts(), status="passed")


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
