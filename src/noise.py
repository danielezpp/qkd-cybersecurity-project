"""
Funzioni semplici per simulare rumore bit-flip in BB84.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, amplitude_damping_error

try:
    from bb84 import (
        check_basis,
        check_bit,
        measure_bb84_state,
        prepare_bb84_state,
        random_bases,
        random_bits,
    )
except ImportError:
    from .bb84 import (
        check_basis,
        check_bit,
        measure_bb84_state,
        prepare_bb84_state,
        random_bases,
        random_bits,
    )


def check_probability(probability):
    """Controlla che una probabilita sia tra 0 e 1."""
    if probability < 0.0 or probability > 1.0:
        raise ValueError("La probabilita deve essere tra 0.0 e 1.0.")


def apply_bit_flip_noise(circuit, qubit, noise_probability, seed=None):
    """Applica un possibile errore bit-flip al qubit."""
    check_probability(noise_probability)

    rng = np.random.default_rng(seed)
    random_number = rng.random()

    if random_number < noise_probability:
        circuit.x(qubit)
        noise_applied = True
    else:
        noise_applied = False

    return circuit, noise_applied


def run_bb84_round_with_bit_flip_noise(
    alice_bit,
    alice_basis,
    bob_basis,
    noise_probability=0.0,
    seed=None,
):
    """Simula un singolo round BB84 con rumore bit-flip."""
    check_bit(alice_bit)
    check_basis(alice_basis)
    check_basis(bob_basis)
    check_probability(noise_probability)

    circuit = QuantumCircuit(1, 1)
    prepare_bb84_state(circuit, alice_bit, alice_basis)
    circuit, noise_applied = apply_bit_flip_noise(
        circuit,
        0,
        noise_probability,
        seed=seed,
    )
    measure_bb84_state(circuit, bob_basis)

    if seed is None:
        simulator = AerSimulator()
    else:
        simulator = AerSimulator(seed_simulator=seed + 1000)

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
        "noise_applied": noise_applied,
    }


def run_bb84_protocol_with_bit_flip_noise(
    n_rounds,
    noise_probability=0.0,
    seed=None,
):
    """Simula piu round BB84 con rumore bit-flip."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    check_probability(noise_probability)

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

        round_result = run_bb84_round_with_bit_flip_noise(
            alice_bit,
            alice_basis,
            bob_basis,
            noise_probability=noise_probability,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        result = {
            "round": i + 1,
            "alice_bit": round_result["alice_bit"],
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
            "noise_applied": round_result["noise_applied"],
        }
        results.append(result)

    return results


def build_amplitude_damping_noise_model(damping_probability):
    """Crea un noise model con amplitude damping."""
    check_probability(damping_probability)

    noise_model = NoiseModel()
    error = amplitude_damping_error(damping_probability)

    # L'istruzione id rappresenta in modo semplice il passaggio nel canale.
    noise_model.add_all_qubit_quantum_error(error, ["id"])

    return noise_model


def run_bb84_round_with_amplitude_damping(
    alice_bit,
    alice_basis,
    bob_basis,
    damping_probability=0.0,
    seed=None,
):
    """Simula un singolo round BB84 con amplitude damping."""
    check_bit(alice_bit)
    check_basis(alice_basis)
    check_basis(bob_basis)
    check_probability(damping_probability)

    circuit = QuantumCircuit(1, 1)
    prepare_bb84_state(circuit, alice_bit, alice_basis, qubit=0)
    circuit.barrier()
    circuit.id(0)
    circuit.barrier()
    measure_bb84_state(circuit, bob_basis, qubit=0, cbit=0)

    noise_model = build_amplitude_damping_noise_model(damping_probability)

    if seed is None:
        simulator = AerSimulator(noise_model=noise_model)
    else:
        simulator = AerSimulator(
            noise_model=noise_model,
            seed_simulator=seed + 2000,
        )

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
        "damping_probability": damping_probability,
    }


def run_bb84_protocol_with_amplitude_damping(
    n_rounds,
    damping_probability=0.0,
    seed=None,
):
    """Simula piu round BB84 con amplitude damping."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    check_probability(damping_probability)

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
            round_seed = seed + 20 + i

        round_result = run_bb84_round_with_amplitude_damping(
            alice_bit,
            alice_basis,
            bob_basis,
            damping_probability=damping_probability,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        result = {
            "round": i + 1,
            "alice_bit": round_result["alice_bit"],
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
            "damping_probability": round_result["damping_probability"],
        }
        results.append(result)

    return results
