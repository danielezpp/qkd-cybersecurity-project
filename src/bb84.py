"""
Funzioni semplici per simulare il protocollo BB84 ideale.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from qkd_core import (
        check_basis,
        check_bit,
        compute_qber,
        random_bases,
        random_bits,
        sift_keys,
    )
except ImportError:
    from .qkd_core import (
        check_basis,
        check_bit,
        compute_qber,
        random_bases,
        random_bits,
        sift_keys,
    )


def prepare_bb84_state(circuit, bit, basis, qubit=0):
    """Prepara uno dei quattro stati BB84."""
    check_bit(bit)
    check_basis(basis)

    if basis == "Z":
        if bit == 1:
            circuit.x(qubit)

    if basis == "X":
        if bit == 1:
            circuit.x(qubit)
        circuit.h(qubit)

    return circuit


def measure_bb84_state(circuit, basis, qubit=0, cbit=0):
    """Misura un qubit nella base scelta."""
    check_basis(basis)

    # Per misurare in base X, prima riportiamo lo stato nella base Z.
    if basis == "X":
        circuit.h(qubit)

    circuit.measure(qubit, cbit)

    return circuit


def _run_bb84_round(
    alice_bit,
    alice_basis,
    bob_basis,
    attack_mode=None,
    intercept_probability=0.0,
    seed=None,
):
    """Esegue un round BB84, con o senza attacco."""
    check_bit(alice_bit)
    check_basis(alice_basis)
    check_basis(bob_basis)

    if attack_mode is None:
        circuit = QuantumCircuit(1, 1)
        prepare_bb84_state(circuit, alice_bit, alice_basis)
        measure_bb84_state(circuit, bob_basis)

        simulator = AerSimulator()
        result = simulator.run(circuit, shots=1).result()
        counts = result.get_counts(circuit)

        # Con shots=1 esiste un solo risultato.
        for measured_bit in counts:
            bob_bit = int(measured_bit)

        return bob_bit

    if attack_mode != "intercept_resend":
        raise ValueError("attack_mode non riconosciuto.")

    try:
        from attacks import eve_intercept_resend
    except ImportError:
        from .attacks import eve_intercept_resend

    if intercept_probability < 0.0 or intercept_probability > 1.0:
        raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    rng = np.random.default_rng(seed)
    eve_intercepted = rng.random() < intercept_probability

    if not eve_intercepted:
        bob_bit = _run_bb84_round(alice_bit, alice_basis, bob_basis)
        return {
            "alice_bit": alice_bit,
            "alice_basis": alice_basis,
            "bob_basis": bob_basis,
            "bob_bit": bob_bit,
            "eve_intercepted": False,
            "eve_basis": None,
            "eve_bit": None,
        }

    eve_result = eve_intercept_resend(alice_bit, alice_basis, seed=seed)
    eve_basis = eve_result["eve_basis"]
    eve_bit = eve_result["eve_bit"]

    circuit = QuantumCircuit(1, 1)
    prepare_bb84_state(circuit, eve_bit, eve_basis)
    measure_bb84_state(circuit, bob_basis)

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    # Con shots=1 Bob ottiene un solo bit.
    for measured_bit in counts:
        bob_bit = int(measured_bit)

    return {
        "alice_bit": alice_bit,
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "bob_bit": bob_bit,
        "eve_intercepted": True,
        "eve_basis": eve_basis,
        "eve_bit": eve_bit,
    }


def _run_bb84_protocol(
    n_rounds,
    attack_mode=None,
    intercept_probability=0.0,
    seed=None,
):
    """Esegue piu round BB84, con o senza attacco."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if attack_mode is not None and attack_mode != "intercept_resend":
        raise ValueError("attack_mode non riconosciuto.")

    if attack_mode == "intercept_resend":
        if intercept_probability < 0.0 or intercept_probability > 1.0:
            raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    if seed is None:
        alice_bits_seed = None
        alice_bases_seed = None
        bob_bases_seed = None
    else:
        alice_bits_seed = seed
        alice_bases_seed = seed + 1
        bob_bases_seed = seed + 2

    alice_bits = random_bits(n_rounds, seed=alice_bits_seed)
    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)

    results = []

    for i in range(n_rounds):
        alice_bit = alice_bits[i]
        alice_basis = alice_bases[i]
        bob_basis = bob_bases[i]

        if seed is None:
            round_seed = None
        else:
            round_seed = seed + 10 + i

        round_result = _run_bb84_round(
            alice_bit,
            alice_basis,
            bob_basis,
            attack_mode=attack_mode,
            intercept_probability=intercept_probability,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        if attack_mode is None:
            result = {
                "round": i + 1,
                "alice_bit": alice_bit,
                "alice_basis": alice_basis,
                "bob_basis": bob_basis,
                "bob_bit": round_result,
                "keep": keep,
            }
        else:
            result = {
                "round": i + 1,
                "alice_bit": round_result["alice_bit"],
                "alice_basis": round_result["alice_basis"],
                "bob_basis": round_result["bob_basis"],
                "bob_bit": round_result["bob_bit"],
                "keep": keep,
                "eve_intercepted": round_result["eve_intercepted"],
                "eve_basis": round_result["eve_basis"],
                "eve_bit": round_result["eve_bit"],
            }

        results.append(result)

    return results


def run_bb84_round(alice_bit, alice_basis, bob_basis):
    """Simula un singolo round BB84 ideale."""
    return _run_bb84_round(alice_bit, alice_basis, bob_basis)


def run_bb84_protocol(n_rounds, seed=None):
    """Simula piu round del protocollo BB84 ideale."""
    return _run_bb84_protocol(n_rounds, seed=seed)


def run_bb84_round_with_eve(
    alice_bit,
    alice_basis,
    bob_basis,
    intercept_probability=1.0,
    seed=None,
):
    """Simula un singolo round BB84 con Eve."""
    return _run_bb84_round(
        alice_bit,
        alice_basis,
        bob_basis,
        attack_mode="intercept_resend",
        intercept_probability=intercept_probability,
        seed=seed,
    )


def run_bb84_protocol_with_eve(n_rounds, intercept_probability=1.0, seed=None):
    """Simula piu round BB84 con Eve."""
    return _run_bb84_protocol(
        n_rounds,
        attack_mode="intercept_resend",
        intercept_probability=intercept_probability,
        seed=seed,
    )
