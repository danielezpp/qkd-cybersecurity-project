"""
Funzioni comuni per gli esperimenti CHSH.
"""

import numpy as np

try:
    from metrics import (
        CHSH_CLASSICAL_LIMIT,
        CHSH_TSIRELSON_BOUND,
        compute_chsh_gap,
        compute_chsh_strength,
    )
except ImportError:
    from .metrics import (
        CHSH_CLASSICAL_LIMIT,
        CHSH_TSIRELSON_BOUND,
        compute_chsh_gap,
        compute_chsh_strength,
    )


def get_chsh_angles():
    """Restituisce gli angoli standard usati nel test CHSH."""
    a = 0
    a_prime = np.pi / 2
    b = np.pi / 4
    b_prime = -np.pi / 4

    return a, a_prime, b, b_prime


def compute_correlation_from_counts(counts):
    """Calcola la correlazione E dai conteggi."""
    total_shots = 0
    weighted_sum = 0

    for bitstring in counts:
        count = counts[bitstring]

        # Qiskit mostra i bit classici come c1 c0.
        alice_bit = int(bitstring[-1])
        bob_bit = int(bitstring[-2])

        if alice_bit == 0:
            alice_value = 1
        else:
            alice_value = -1

        if bob_bit == 0:
            bob_value = 1
        else:
            bob_value = -1

        product = alice_value * bob_value
        weighted_sum = weighted_sum + product * count
        total_shots = total_shots + count

    return float(weighted_sum / total_shots)


def compute_chsh_s(E_ab, E_ab_prime, E_a_prime_b, E_a_prime_b_prime):
    """Calcola il parametro S del test CHSH."""
    S = E_ab + E_ab_prime + E_a_prime_b - E_a_prime_b_prime

    return S


def build_chsh_result(
    E_ab,
    E_ab_prime,
    E_a_prime_b,
    E_a_prime_b_prime,
    S,
    shots,
    extra_metadata=None,
):
    """Costruisce il dizionario finale per un esperimento CHSH."""
    abs_S = abs(S)

    result = {
        "E_ab": E_ab,
        "E_ab_prime": E_ab_prime,
        "E_a_prime_b": E_a_prime_b,
        "E_a_prime_b_prime": E_a_prime_b_prime,
        "S": S,
        "abs_S": abs_S,
        "classical_limit": CHSH_CLASSICAL_LIMIT,
        "quantum_limit": CHSH_TSIRELSON_BOUND,
        "violates_chsh": abs_S > CHSH_CLASSICAL_LIMIT,
        "chsh_gap": compute_chsh_gap(abs_S),
        "chsh_strength": compute_chsh_strength(abs_S),
        "shots": shots,
    }

    if extra_metadata is not None:
        for key in extra_metadata:
            result[key] = extra_metadata[key]

    return result


def run_chsh_experiment_from_counts_function(
    counts_function,
    shots=1000,
    seed=None,
    extra_metadata=None,
    **counts_kwargs,
):
    """Esegue un esperimento CHSH usando una funzione di conteggio."""
    a, a_prime, b, b_prime = get_chsh_angles()

    if seed is None:
        seed_ab = None
        seed_ab_prime = None
        seed_a_prime_b = None
        seed_a_prime_b_prime = None
    else:
        seed_ab = seed
        seed_ab_prime = seed + 1
        seed_a_prime_b = seed + 2
        seed_a_prime_b_prime = seed + 3

    counts_ab = counts_function(
        a,
        b,
        shots=shots,
        seed=seed_ab,
        **counts_kwargs,
    )
    E_ab = compute_correlation_from_counts(counts_ab)

    counts_ab_prime = counts_function(
        a,
        b_prime,
        shots=shots,
        seed=seed_ab_prime,
        **counts_kwargs,
    )
    E_ab_prime = compute_correlation_from_counts(counts_ab_prime)

    counts_a_prime_b = counts_function(
        a_prime,
        b,
        shots=shots,
        seed=seed_a_prime_b,
        **counts_kwargs,
    )
    E_a_prime_b = compute_correlation_from_counts(counts_a_prime_b)

    counts_a_prime_b_prime = counts_function(
        a_prime,
        b_prime,
        shots=shots,
        seed=seed_a_prime_b_prime,
        **counts_kwargs,
    )
    E_a_prime_b_prime = compute_correlation_from_counts(counts_a_prime_b_prime)

    S = compute_chsh_s(E_ab, E_ab_prime, E_a_prime_b, E_a_prime_b_prime)

    return build_chsh_result(
        E_ab,
        E_ab_prime,
        E_a_prime_b,
        E_a_prime_b_prime,
        S,
        shots,
        extra_metadata=extra_metadata,
    )
