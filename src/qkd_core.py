"""
Funzioni comuni per i protocolli QKD simulati.
"""

import numpy as np


def check_bit(bit):
    """Controlla che il bit sia 0 oppure 1."""
    if bit not in (0, 1):
        raise ValueError("Il bit deve essere 0 oppure 1.")


def check_basis(basis):
    """Controlla che la base sia Z oppure X."""
    if basis not in ("Z", "X"):
        raise ValueError("La base deve essere 'Z' oppure 'X'.")


def random_bits(n, seed=None):
    """Genera una lista di n bit casuali."""
    if n <= 0:
        raise ValueError("n deve essere maggiore di 0.")

    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, size=n)

    return bits.tolist()


def random_bases(n, seed=None):
    """Genera una lista di n basi casuali."""
    if n <= 0:
        raise ValueError("n deve essere maggiore di 0.")

    rng = np.random.default_rng(seed)
    bases = rng.choice(["Z", "X"], size=n)

    return bases.tolist()


def sift_keys(results):
    """Estrae le chiavi sifted dai risultati."""
    alice_key = []
    bob_key = []

    for result in results:
        if result["keep"] is True:
            alice_key.append(result["alice_bit"])
            bob_key.append(result["bob_bit"])

    return alice_key, bob_key


def compute_qber(alice_key, bob_key):
    """Calcola il QBER tra due chiavi."""
    if len(alice_key) != len(bob_key):
        raise ValueError("Le due chiavi devono avere la stessa lunghezza.")

    if len(alice_key) == 0:
        return np.nan

    errors = 0

    for i in range(len(alice_key)):
        if alice_key[i] != bob_key[i]:
            errors = errors + 1

    return errors / len(alice_key)
