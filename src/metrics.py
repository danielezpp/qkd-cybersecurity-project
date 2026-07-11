"""
Metriche comuni per i protocolli QKD simulati.
"""

import numpy as np


def count_kept_rounds(results):
    """Conta i round mantenuti dopo il sifting."""
    kept_rounds = 0

    for result in results:
        if result["keep"] == True:
            kept_rounds = kept_rounds + 1

    return kept_rounds


def count_discarded_rounds(results):
    """Conta i round scartati dopo il sifting."""
    discarded_rounds = 0

    for result in results:
        if result["keep"] == False:
            discarded_rounds = discarded_rounds + 1

    return discarded_rounds


def compute_sifted_key_length(alice_key):
    """Restituisce la lunghezza della chiave sifted."""
    return len(alice_key)


def compute_sifted_key_rate(alice_key, n_rounds):
    """Calcola la frazione di round usati nella chiave."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    return len(alice_key) / n_rounds


def decide_key_acceptance(qber, qber_threshold=0.11):
    """Decide se accettare la chiave in base al QBER."""
    if qber_threshold < 0 or qber_threshold > 1:
        raise ValueError("qber_threshold deve essere tra 0 e 1.")

    if np.isnan(qber):
        return False

    if qber <= qber_threshold:
        return True

    return False


def summarize_qkd_results(
    protocol_name,
    results,
    alice_key,
    bob_key,
    qber,
    qber_threshold=0.11,
):
    """Crea un riassunto delle metriche QKD principali."""
    n_rounds = len(results)
    kept_rounds = count_kept_rounds(results)
    discarded_rounds = count_discarded_rounds(results)
    sifted_key_length = compute_sifted_key_length(alice_key)
    sifted_key_rate = compute_sifted_key_rate(alice_key, n_rounds)
    accepted = decide_key_acceptance(qber, qber_threshold)

    return {
        "protocol": protocol_name,
        "n_rounds": n_rounds,
        "kept_rounds": kept_rounds,
        "discarded_rounds": discarded_rounds,
        "sifted_key_length": sifted_key_length,
        "sifted_key_rate": sifted_key_rate,
        "qber": qber,
        "qber_threshold": qber_threshold,
        "accepted": accepted,
    }
