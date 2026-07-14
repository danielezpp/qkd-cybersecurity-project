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


def compute_lambda_from_attenuation(
    attenuation_db_per_km,
    fiber_speed_km_s=203390,
):
    """Calcola lambda a partire dall'attenuazione della fibra."""
    if attenuation_db_per_km < 0:
        raise ValueError("attenuation_db_per_km deve essere maggiore o uguale a 0.")

    if fiber_speed_km_s <= 0:
        raise ValueError("fiber_speed_km_s deve essere maggiore di 0.")

    lambda_parameter = fiber_speed_km_s * attenuation_db_per_km * np.log(10) / 10

    return lambda_parameter


def compute_time_from_distance(distance_km, fiber_speed_km_s=203390):
    """Calcola il tempo di propagazione dalla distanza."""
    if distance_km < 0:
        raise ValueError("distance_km deve essere maggiore o uguale a 0.")

    if fiber_speed_km_s <= 0:
        raise ValueError("fiber_speed_km_s deve essere maggiore di 0.")

    time_s = distance_km / fiber_speed_km_s

    return time_s


def compute_c1_amplitude(time_s, lambda_parameter, coupling_ratio):
    """Calcola l'ampiezza C1(t) del modello semplificato."""
    if time_s < 0:
        raise ValueError("time_s deve essere maggiore o uguale a 0.")

    if lambda_parameter < 0:
        raise ValueError("lambda_parameter deve essere maggiore o uguale a 0.")

    if coupling_ratio < 0:
        raise ValueError("coupling_ratio deve essere maggiore o uguale a 0.")

    if time_s == 0 or lambda_parameter == 0:
        return 1.0

    sqrt_term = np.sqrt(1 - 2 * coupling_ratio + 0j)

    if abs(sqrt_term) < 1e-12:
        raise ValueError(
            "coupling_ratio troppo vicino al valore critico 0.5 "
            "per questa formula semplificata."
        )

    time_factor = lambda_parameter * time_s / 2
    argument = time_factor * sqrt_term

    c1 = np.exp(-time_factor) * (
        np.cosh(argument)
        + (1 / sqrt_term) * np.sinh(argument)
    )

    return c1


def compute_jc_damping_probability(
    time_s,
    lambda_parameter,
    coupling_ratio,
):
    """Calcola la probabilita di damping dal modello semplificato."""
    c1 = compute_c1_amplitude(
        time_s,
        lambda_parameter,
        coupling_ratio,
    )

    survival_probability = abs(c1) ** 2
    damping_probability = 1 - survival_probability

    if damping_probability < 0.0:
        damping_probability = 0.0

    if damping_probability > 1.0:
        damping_probability = 1.0

    return float(damping_probability)


def compute_jc_damping_probability_from_distance(
    distance_km,
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
):
    """Calcola il damping a partire dalla distanza del canale."""
    lambda_parameter = compute_lambda_from_attenuation(
        attenuation_db_per_km,
        fiber_speed_km_s=fiber_speed_km_s,
    )
    time_s = compute_time_from_distance(
        distance_km,
        fiber_speed_km_s=fiber_speed_km_s,
    )
    damping_probability = compute_jc_damping_probability(
        time_s,
        lambda_parameter,
        coupling_ratio,
    )

    return damping_probability


def run_bb84_protocol_with_jc_amplitude_damping(
    n_rounds,
    distance_km,
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
    seed=None,
):
    """Simula BB84 con damping dipendente dalla distanza."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if distance_km < 0:
        raise ValueError("distance_km deve essere maggiore o uguale a 0.")

    damping_probability = compute_jc_damping_probability_from_distance(
        distance_km,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )

    results = run_bb84_protocol_with_amplitude_damping(
        n_rounds=n_rounds,
        damping_probability=damping_probability,
        seed=seed,
    )

    for result in results:
        result["distance_km"] = distance_km
        result["attenuation_db_per_km"] = attenuation_db_per_km
        result["coupling_ratio"] = coupling_ratio
        result["fiber_speed_km_s"] = fiber_speed_km_s

    return results
