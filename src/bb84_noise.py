from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from bb84 import (
        measure_bb84_state,
        prepare_bb84_state,
    )
    from qkd_core import (
        check_basis,
        check_bit,
        random_bases,
        random_bits,
    )
    from noise_models import (
        apply_bit_flip_noise,
        build_amplitude_damping_noise_model,
        check_probability,
        compute_jc_damping_probability_from_distance,
    )
except ImportError:
    from .bb84 import (
        measure_bb84_state,
        prepare_bb84_state,
    )
    from .qkd_core import (
        check_basis,
        check_bit,
        random_bases,
        random_bits,
    )
    from .noise_models import (
        apply_bit_flip_noise,
        build_amplitude_damping_noise_model,
        check_probability,
        compute_jc_damping_probability_from_distance,
    )


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
