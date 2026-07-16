"""
Metriche comuni per i protocolli QKD simulati.
"""

import numpy as np


QBER_THRESHOLD_BB84 = 0.11
CHSH_CLASSICAL_LIMIT = 2.0
CHSH_TSIRELSON_BOUND = 2 * np.sqrt(2)


def binary_entropy(probability):
    """Calcola l'entropia binaria."""
    if probability < 0 or probability > 1:
        raise ValueError("probability deve essere tra 0 e 1.")

    if probability == 0 or probability == 1:
        return 0.0

    entropy = -probability * np.log2(probability)
    entropy = entropy - (1 - probability) * np.log2(1 - probability)

    return entropy


def bb84_asymptotic_key_rate(qber):
    """Stima didattica del key rate asintotico BB84."""
    return 1 - 2 * binary_entropy(qber)


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


def decide_qber_acceptance(qber, qber_threshold=QBER_THRESHOLD_BB84):
    """Decide se accettare la chiave in base al QBER."""
    if qber_threshold < 0 or qber_threshold > 1:
        raise ValueError("qber_threshold deve essere tra 0 e 1.")

    if qber is None:
        return False

    if np.isnan(qber):
        return False

    if qber <= qber_threshold:
        return True

    return False


def decide_key_acceptance(qber, qber_threshold=QBER_THRESHOLD_BB84):
    """Alias compatibile per la decisione basata sul QBER."""
    return decide_qber_acceptance(qber, qber_threshold)


def compute_chsh_gap(abs_s):
    """Calcola quanto |S| supera il limite classico CHSH."""
    if abs_s is None:
        return None

    if np.isnan(abs_s):
        return np.nan

    return abs_s - CHSH_CLASSICAL_LIMIT


def compute_chsh_strength(abs_s):
    """Misura normalizzata della forza della violazione CHSH rispetto al massimo quantistico ideale."""
    if abs_s is None:
        return None

    if np.isnan(abs_s):
        return np.nan

    denominator = CHSH_TSIRELSON_BOUND - CHSH_CLASSICAL_LIMIT
    strength = (abs_s - CHSH_CLASSICAL_LIMIT) / denominator

    return strength


def summarize_chsh_result(chsh_result):
    """Crea un riassunto quantitativo del risultato CHSH."""
    S = chsh_result["S"]
    abs_S = abs(S)
    violates_chsh = abs_S > CHSH_CLASSICAL_LIMIT
    chsh_gap = compute_chsh_gap(abs_S)
    chsh_strength = compute_chsh_strength(abs_S)

    return {
        "S": S,
        "abs_S": abs_S,
        "classical_limit": CHSH_CLASSICAL_LIMIT,
        "quantum_limit": CHSH_TSIRELSON_BOUND,
        "violates_chsh": violates_chsh,
        "chsh_gap": chsh_gap,
        "chsh_strength": chsh_strength,
    }


def summarize_qkd_results(
    protocol_name,
    results,
    alice_key,
    bob_key,
    qber,
    qber_threshold=QBER_THRESHOLD_BB84,
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
