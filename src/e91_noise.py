"""
Funzioni didattiche per simulare rumore nel protocollo E91.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from e91 import (
        check_basis,
        measure_e91_qubit,
        measure_in_angle,
        prepare_bell_phi_plus,
        random_bases,
    )
    from noise_models import (
        build_bit_flip_noise_model,
        build_amplitude_damping_noise_model,
        check_probability,
        compute_jc_damping_probability_from_distance,
    )
    from chsh import (
        build_chsh_result,
        compute_chsh_s,
        compute_correlation_from_counts,
        get_chsh_angles,
    )
except ImportError:
    from .e91 import (
        check_basis,
        measure_e91_qubit,
        measure_in_angle,
        prepare_bell_phi_plus,
        random_bases,
    )
    from .noise_models import (
        build_bit_flip_noise_model,
        build_amplitude_damping_noise_model,
        check_probability,
        compute_jc_damping_probability_from_distance,
    )
    from .chsh import (
        build_chsh_result,
        compute_chsh_s,
        compute_correlation_from_counts,
        get_chsh_angles,
    )


def check_channel_mode(channel_mode):
    """Controlla il modo con cui il rumore agisce sul canale."""
    if channel_mode != "one_arm" and channel_mode != "two_arm":
        raise ValueError("channel_mode deve essere 'one_arm' oppure 'two_arm'.")


def get_noisy_qubits(channel_mode):
    """Restituisce i qubit attraversati dal canale rumoroso."""
    check_channel_mode(channel_mode)

    if channel_mode == "one_arm":
        return [1]

    return [0, 1]


def insert_channel_identity_gates(circuit, channel_mode):
    """Inserisce gate id sui qubit attraversati dal canale."""
    noisy_qubits = get_noisy_qubits(channel_mode)

    for qubit in noisy_qubits:
        circuit.id(qubit)

    return circuit


def _get_seed(base_seed, offset):
    """Calcola un seed derivato, se il seed di base esiste."""
    if base_seed is None:
        return None

    return base_seed + offset


def _run_noisy_e91_round(
    alice_basis,
    bob_basis,
    noise_model,
    channel_mode,
    seed=None,
    seed_offset=0,
    metadata=None,
):
    """Esegue un round E91 rumoroso generico."""
    check_basis(alice_basis)
    check_basis(bob_basis)
    check_channel_mode(channel_mode)

    circuit = QuantumCircuit(2, 2)
    prepare_bell_phi_plus(circuit)
    insert_channel_identity_gates(circuit, channel_mode)
    measure_e91_qubit(circuit, alice_basis, qubit=0, cbit=0)
    measure_e91_qubit(circuit, bob_basis, qubit=1, cbit=1)

    simulator_seed = _get_seed(seed, seed_offset)

    if simulator_seed is None:
        simulator = AerSimulator(noise_model=noise_model)
    else:
        simulator = AerSimulator(noise_model=noise_model, seed_simulator=simulator_seed)

    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    for bitstring in counts:
        # Qiskit mostra i bit classici come c1 c0.
        alice_bit = int(bitstring[-1])
        bob_bit = int(bitstring[-2])

    round_result = {
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "alice_bit": alice_bit,
        "bob_bit": bob_bit,
    }

    if metadata is not None:
        for key in metadata:
            round_result[key] = metadata[key]

    return round_result


def _run_noisy_e91_protocol(
    n_rounds,
    round_function,
    channel_mode,
    seed=None,
    round_seed_offset=0,
    **round_kwargs,
):
    """Esegue piu round E91 rumorosi usando una funzione di round."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    check_channel_mode(channel_mode)

    alice_bases_seed = seed
    bob_bases_seed = _get_seed(seed, 1)

    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)

    results = []

    for i in range(n_rounds):
        alice_basis = alice_bases[i]
        bob_basis = bob_bases[i]
        round_seed = _get_seed(seed, round_seed_offset + i)

        round_result = round_function(
            alice_basis,
            bob_basis,
            channel_mode=channel_mode,
            seed=round_seed,
            **round_kwargs,
        )

        result = {
            "round": i,
        }

        for key in round_result:
            result[key] = round_result[key]

        result["keep"] = alice_basis == bob_basis
        results.append(result)

    return results


def _run_noisy_chsh_counts(
    angle_a,
    angle_b,
    noise_model,
    channel_mode,
    shots=1000,
    seed=None,
    seed_offset=0,
):
    """Esegue conteggi CHSH rumorosi generici."""
    if shots <= 0:
        raise ValueError("shots deve essere maggiore di 0.")

    check_channel_mode(channel_mode)

    circuit = QuantumCircuit(2, 2)
    prepare_bell_phi_plus(circuit)
    insert_channel_identity_gates(circuit, channel_mode)
    measure_in_angle(circuit, angle_a, qubit=0, cbit=0)
    measure_in_angle(circuit, angle_b, qubit=1, cbit=1)

    simulator_seed = _get_seed(seed, seed_offset)

    if simulator_seed is None:
        simulator = AerSimulator(noise_model=noise_model)
    else:
        simulator = AerSimulator(noise_model=noise_model, seed_simulator=simulator_seed)

    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    return counts


def _run_noisy_chsh_experiment(
    counts_function,
    shots=1000,
    seed=None,
    metadata=None,
    **counts_kwargs,
):
    """Esegue un esperimento CHSH rumoroso generico."""
    a, a_prime, b, b_prime = get_chsh_angles()

    seed_ab = seed
    seed_ab_prime = _get_seed(seed, 1)
    seed_a_prime_b = _get_seed(seed, 2)
    seed_a_prime_b_prime = _get_seed(seed, 3)

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
        extra_metadata=metadata,
    )


def run_e91_round_with_bit_flip_noise(
    alice_basis,
    bob_basis,
    noise_probability=0.0,
    channel_mode="one_arm",
    seed=None,
):
    """Simula un round E91 con rumore bit-flip."""
    check_probability(noise_probability)

    noise_model = build_bit_flip_noise_model(noise_probability)
    metadata = {
        "noise_type": "bit_flip",
        "noise_probability": noise_probability,
        "channel_mode": channel_mode,
    }

    return _run_noisy_e91_round(
        alice_basis,
        bob_basis,
        noise_model,
        channel_mode,
        seed=seed,
        seed_offset=9000,
        metadata=metadata,
    )


def run_e91_protocol_with_bit_flip_noise(
    n_rounds,
    noise_probability=0.0,
    channel_mode="one_arm",
    seed=None,
):
    """Simula piu round E91 con rumore bit-flip."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    check_probability(noise_probability)

    return _run_noisy_e91_protocol(
        n_rounds,
        run_e91_round_with_bit_flip_noise,
        channel_mode,
        seed=seed,
        round_seed_offset=100,
        noise_probability=noise_probability,
    )


def run_chsh_counts_with_bit_flip_noise(
    angle_a,
    angle_b,
    noise_probability=0.0,
    channel_mode="one_arm",
    shots=1000,
    seed=None,
):
    """Esegue conteggi CHSH con rumore bit-flip."""
    if shots <= 0:
        raise ValueError("shots deve essere maggiore di 0.")

    check_probability(noise_probability)

    noise_model = build_bit_flip_noise_model(noise_probability)

    return _run_noisy_chsh_counts(
        angle_a,
        angle_b,
        noise_model,
        channel_mode,
        shots=shots,
        seed=seed,
        seed_offset=9100,
    )


def run_chsh_experiment_with_bit_flip_noise(
    noise_probability=0.0,
    channel_mode="one_arm",
    shots=1000,
    seed=None,
):
    """Simula CHSH per E91 con rumore bit-flip."""
    metadata = {
        "noise_type": "bit_flip",
        "noise_probability": noise_probability,
        "channel_mode": channel_mode,
    }

    return _run_noisy_chsh_experiment(
        run_chsh_counts_with_bit_flip_noise,
        shots=shots,
        seed=seed,
        metadata=metadata,
        noise_probability=noise_probability,
        channel_mode=channel_mode,
    )


def run_e91_round_with_amplitude_damping(
    alice_basis,
    bob_basis,
    damping_probability=0.0,
    channel_mode="one_arm",
    seed=None,
):
    """Simula un round E91 con amplitude damping."""
    check_probability(damping_probability)

    noise_model = build_amplitude_damping_noise_model(damping_probability)
    metadata = {
        "noise_type": "amplitude_damping",
        "damping_probability": damping_probability,
        "channel_mode": channel_mode,
    }

    return _run_noisy_e91_round(
        alice_basis,
        bob_basis,
        noise_model,
        channel_mode,
        seed=seed,
        seed_offset=9200,
        metadata=metadata,
    )


def run_e91_protocol_with_amplitude_damping(
    n_rounds,
    damping_probability=0.0,
    channel_mode="one_arm",
    seed=None,
):
    """Simula piu round E91 con amplitude damping."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    check_probability(damping_probability)

    return _run_noisy_e91_protocol(
        n_rounds,
        run_e91_round_with_amplitude_damping,
        channel_mode,
        seed=seed,
        round_seed_offset=200,
        damping_probability=damping_probability,
    )


def run_chsh_counts_with_amplitude_damping(
    angle_a,
    angle_b,
    damping_probability=0.0,
    channel_mode="one_arm",
    shots=1000,
    seed=None,
):
    """Esegue conteggi CHSH con amplitude damping."""
    if shots <= 0:
        raise ValueError("shots deve essere maggiore di 0.")

    check_probability(damping_probability)

    noise_model = build_amplitude_damping_noise_model(damping_probability)

    return _run_noisy_chsh_counts(
        angle_a,
        angle_b,
        noise_model,
        channel_mode,
        shots=shots,
        seed=seed,
        seed_offset=9300,
    )


def run_chsh_experiment_with_amplitude_damping(
    damping_probability=0.0,
    channel_mode="one_arm",
    shots=1000,
    seed=None,
):
    """Simula CHSH per E91 con amplitude damping."""
    metadata = {
        "noise_type": "amplitude_damping",
        "damping_probability": damping_probability,
        "channel_mode": channel_mode,
    }

    return _run_noisy_chsh_experiment(
        run_chsh_counts_with_amplitude_damping,
        shots=shots,
        seed=seed,
        metadata=metadata,
        damping_probability=damping_probability,
        channel_mode=channel_mode,
    )


def compute_e91_jc_channel_parameters(
    distance_km,
    channel_mode="one_arm",
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
):
    """Calcola i parametri del canale E91 con modello distanza."""
    if distance_km < 0:
        raise ValueError("distance_km deve essere maggiore o uguale a 0.")

    check_channel_mode(channel_mode)

    if channel_mode == "one_arm":
        arm_distance_alice_km = 0.0
        arm_distance_bob_km = distance_km
        damping_probability_alice = 0.0
        damping_probability_bob = compute_jc_damping_probability_from_distance(
            distance_km,
            attenuation_db_per_km=attenuation_db_per_km,
            coupling_ratio=coupling_ratio,
            fiber_speed_km_s=fiber_speed_km_s,
        )
        effective_damping_probability = damping_probability_bob
    else:
        arm_distance_alice_km = distance_km / 2
        arm_distance_bob_km = distance_km / 2
        damping_probability_alice = compute_jc_damping_probability_from_distance(
            arm_distance_alice_km,
            attenuation_db_per_km=attenuation_db_per_km,
            coupling_ratio=coupling_ratio,
            fiber_speed_km_s=fiber_speed_km_s,
        )
        damping_probability_bob = compute_jc_damping_probability_from_distance(
            arm_distance_bob_km,
            attenuation_db_per_km=attenuation_db_per_km,
            coupling_ratio=coupling_ratio,
            fiber_speed_km_s=fiber_speed_km_s,
        )
        effective_damping_probability = damping_probability_bob

    return {
        "distance_km": distance_km,
        "channel_mode": channel_mode,
        "arm_distance_alice_km": arm_distance_alice_km,
        "arm_distance_bob_km": arm_distance_bob_km,
        "damping_probability_alice": damping_probability_alice,
        "damping_probability_bob": damping_probability_bob,
        "effective_damping_probability": effective_damping_probability,
        "attenuation_db_per_km": attenuation_db_per_km,
        "coupling_ratio": coupling_ratio,
        "fiber_speed_km_s": fiber_speed_km_s,
    }


def run_e91_round_with_jc_amplitude_damping(
    alice_basis,
    bob_basis,
    distance_km,
    channel_mode="one_arm",
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
    seed=None,
):
    """Simula un round E91 con damping dipendente dalla distanza."""
    params = compute_e91_jc_channel_parameters(
        distance_km,
        channel_mode=channel_mode,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )

    round_result = run_e91_round_with_amplitude_damping(
        alice_basis,
        bob_basis,
        damping_probability=params["effective_damping_probability"],
        channel_mode=channel_mode,
        seed=seed,
    )

    round_result["noise_type"] = "jc_amplitude_damping"
    round_result["distance_km"] = distance_km
    round_result["arm_distance_alice_km"] = params["arm_distance_alice_km"]
    round_result["arm_distance_bob_km"] = params["arm_distance_bob_km"]
    round_result["damping_probability_alice"] = params["damping_probability_alice"]
    round_result["damping_probability_bob"] = params["damping_probability_bob"]
    round_result["attenuation_db_per_km"] = attenuation_db_per_km
    round_result["coupling_ratio"] = coupling_ratio
    round_result["fiber_speed_km_s"] = fiber_speed_km_s

    return round_result


def run_e91_protocol_with_jc_amplitude_damping(
    n_rounds,
    distance_km,
    channel_mode="one_arm",
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
    seed=None,
):
    """Simula piu round E91 con damping dipendente dalla distanza."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    compute_e91_jc_channel_parameters(
        distance_km,
        channel_mode=channel_mode,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )

    return _run_noisy_e91_protocol(
        n_rounds,
        run_e91_round_with_jc_amplitude_damping,
        channel_mode,
        seed=seed,
        round_seed_offset=300,
        distance_km=distance_km,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )


def run_chsh_counts_with_jc_amplitude_damping(
    angle_a,
    angle_b,
    distance_km,
    channel_mode="one_arm",
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
    shots=1000,
    seed=None,
):
    """Esegue conteggi CHSH con damping dipendente dalla distanza."""
    params = compute_e91_jc_channel_parameters(
        distance_km,
        channel_mode=channel_mode,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )

    counts = run_chsh_counts_with_amplitude_damping(
        angle_a,
        angle_b,
        damping_probability=params["effective_damping_probability"],
        channel_mode=channel_mode,
        shots=shots,
        seed=seed,
    )

    return counts


def run_chsh_experiment_with_jc_amplitude_damping(
    distance_km,
    channel_mode="one_arm",
    attenuation_db_per_km=0.21,
    coupling_ratio=0.1,
    fiber_speed_km_s=203390,
    shots=1000,
    seed=None,
):
    """Simula CHSH con damping dipendente dalla distanza."""
    params = compute_e91_jc_channel_parameters(
        distance_km,
        channel_mode=channel_mode,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )

    metadata = {
        "noise_type": "jc_amplitude_damping",
        "distance_km": distance_km,
        "channel_mode": channel_mode,
        "arm_distance_alice_km": params["arm_distance_alice_km"],
        "arm_distance_bob_km": params["arm_distance_bob_km"],
        "damping_probability_alice": params["damping_probability_alice"],
        "damping_probability_bob": params["damping_probability_bob"],
        "attenuation_db_per_km": attenuation_db_per_km,
        "coupling_ratio": coupling_ratio,
        "fiber_speed_km_s": fiber_speed_km_s,
    }

    return _run_noisy_chsh_experiment(
        run_chsh_counts_with_jc_amplitude_damping,
        shots=shots,
        seed=seed,
        metadata=metadata,
        distance_km=distance_km,
        channel_mode=channel_mode,
        attenuation_db_per_km=attenuation_db_per_km,
        coupling_ratio=coupling_ratio,
        fiber_speed_km_s=fiber_speed_km_s,
    )
