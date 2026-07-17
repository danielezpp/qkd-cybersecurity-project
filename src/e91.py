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
    from chsh import (
        build_chsh_result,
        compute_chsh_s,
        compute_correlation_from_counts,
        get_chsh_angles,
    )
    from attacks import choose_eve_basis, prepare_single_qubit_from_bit_basis
except ImportError:
    from .qkd_core import (
        check_basis,
        check_bit,
        compute_qber,
        random_bases,
        random_bits,
        sift_keys,
    )
    from .chsh import (
        build_chsh_result,
        compute_chsh_s,
        compute_correlation_from_counts,
        get_chsh_angles,
    )
    from .attacks import choose_eve_basis, prepare_single_qubit_from_bit_basis


def prepare_bell_phi_plus(circuit):
    """Prepara lo stato di Bell Phi+."""
    circuit.h(0)
    circuit.cx(0, 1)

    return circuit


def measure_e91_qubit(circuit, basis, qubit, cbit):
    """Misura un qubit nella base scelta."""
    check_basis(basis)

    if basis == "X":
        circuit.h(qubit)

    circuit.measure(qubit, cbit)

    return circuit


def run_e91_round(alice_basis, bob_basis):
    """Simula un singolo round E91 ideale."""
    check_basis(alice_basis)
    check_basis(bob_basis)

    circuit = QuantumCircuit(2, 2)
    prepare_bell_phi_plus(circuit)
    measure_e91_qubit(circuit, alice_basis, qubit=0, cbit=0)
    measure_e91_qubit(circuit, bob_basis, qubit=1, cbit=1)

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    for measured_bits in counts:
        bit_string = measured_bits

    # Qiskit mostra i bit classici come c1 c0.
    alice_bit = int(bit_string[-1])
    bob_bit = int(bit_string[-2])

    return {
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "alice_bit": alice_bit,
        "bob_bit": bob_bit,
    }


def run_e91_protocol(n_rounds, seed=None):
    """Simula piu round del protocollo E91 ideale."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if seed is None:
        alice_bases_seed = None
        bob_bases_seed = None
    else:
        alice_bases_seed = seed
        bob_bases_seed = seed + 1

    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)

    results = []

    for i in range(n_rounds):
        alice_basis = alice_bases[i]
        bob_basis = bob_bases[i]

        round_result = run_e91_round(alice_basis, bob_basis)
        keep = alice_basis == bob_basis

        result = {
            "round": i + 1,
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "alice_bit": round_result["alice_bit"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
        }
        results.append(result)

    return results

def run_e91_round_with_eve(
    alice_basis,
    bob_basis,
    intercept_probability=1.0,
    seed=None,
):
    """Simula un singolo round E91 con Eve."""
    check_basis(alice_basis)
    check_basis(bob_basis)

    if intercept_probability < 0.0 or intercept_probability > 1.0:
        raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    rng = np.random.default_rng(seed)
    eve_intercepted = rng.random() < intercept_probability

    if not eve_intercepted:
        round_result = run_e91_round(alice_basis, bob_basis)

        return {
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "alice_bit": round_result["alice_bit"],
            "bob_bit": round_result["bob_bit"],
            "eve_intercepted": False,
            "eve_basis": None,
            "eve_bit": None,
        }

    eve_basis = choose_eve_basis(seed)

    entangled_circuit = QuantumCircuit(2, 2)
    prepare_bell_phi_plus(entangled_circuit)

    # Eve misura il qubit destinato a Bob e rompe l'entanglement.
    measure_e91_qubit(entangled_circuit, eve_basis, qubit=1, cbit=1)
    measure_e91_qubit(entangled_circuit, alice_basis, qubit=0, cbit=0)

    if seed is None:
        simulator = AerSimulator()
    else:
        simulator = AerSimulator(seed_simulator=seed + 3000)

    result = simulator.run(entangled_circuit, shots=1).result()
    counts = result.get_counts(entangled_circuit)

    for bitstring in counts:
        measured_bits = bitstring

    # Qiskit mostra i bit classici come c1 c0.
    alice_bit = int(measured_bits[-1])
    eve_bit = int(measured_bits[-2])

    bob_circuit = QuantumCircuit(1, 1)
    prepare_single_qubit_from_bit_basis(
        bob_circuit,
        eve_bit,
        eve_basis,
        qubit=0,
    )
    measure_e91_qubit(bob_circuit, bob_basis, qubit=0, cbit=0)

    if seed is None:
        bob_simulator = AerSimulator()
    else:
        bob_simulator = AerSimulator(seed_simulator=seed + 4000)

    bob_result = bob_simulator.run(bob_circuit, shots=1).result()
    bob_counts = bob_result.get_counts(bob_circuit)

    for measured_bit in bob_counts:
        bob_bit = int(measured_bit)

    return {
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "alice_bit": alice_bit,
        "bob_bit": bob_bit,
        "eve_intercepted": True,
        "eve_basis": eve_basis,
        "eve_bit": eve_bit,
    }


def run_e91_protocol_with_eve(
    n_rounds,
    intercept_probability=1.0,
    seed=None,
):
    """Simula piu round E91 con Eve."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if intercept_probability < 0.0 or intercept_probability > 1.0:
        raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    if seed is None:
        alice_bases_seed = None
        bob_bases_seed = None
    else:
        alice_bases_seed = seed
        bob_bases_seed = seed + 1

    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)

    results = []

    for i in range(n_rounds):
        alice_basis = alice_bases[i]
        bob_basis = bob_bases[i]

        if seed is None:
            round_seed = None
        else:
            round_seed = seed + 10 + i

        round_result = run_e91_round_with_eve(
            alice_basis,
            bob_basis,
            intercept_probability=intercept_probability,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        result = {
            "round": i + 1,
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "alice_bit": round_result["alice_bit"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
            "eve_intercepted": round_result["eve_intercepted"],
            "eve_basis": round_result["eve_basis"],
            "eve_bit": round_result["eve_bit"],
        }
        results.append(result)

    return results


def measure_in_angle(circuit, angle, qubit, cbit):
    """Misura un qubit lungo una direzione ruotata."""
    # La rotazione RY(-angle) permette di ricondurre la misura lungo
    # una direzione ruotata a una misura standard in base computazionale.
    circuit.ry(-angle, qubit)
    circuit.measure(qubit, cbit)

    return circuit


def run_chsh_counts(angle_a, angle_b, shots=1000, seed=None):
    """Esegue una misura CHSH per una coppia di angoli."""
    circuit = QuantumCircuit(2, 2)
    prepare_bell_phi_plus(circuit)
    measure_in_angle(circuit, angle_a, qubit=0, cbit=0)
    measure_in_angle(circuit, angle_b, qubit=1, cbit=1)

    if seed is None:
        simulator = AerSimulator()
    else:
        simulator = AerSimulator(seed_simulator=seed)

    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    return counts


def run_chsh_experiment(shots=1000, seed=None):
    """Simula CHSH: per uno stato ideale ci aspettiamo |S| vicino a 2*sqrt(2), oltre il limite classico 2."""
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

    counts_ab = run_chsh_counts(a, b, shots=shots, seed=seed_ab)
    E_ab = compute_correlation_from_counts(counts_ab)

    counts_ab_prime = run_chsh_counts(a, b_prime, shots=shots, seed=seed_ab_prime)
    E_ab_prime = compute_correlation_from_counts(counts_ab_prime)

    counts_a_prime_b = run_chsh_counts(a_prime, b, shots=shots, seed=seed_a_prime_b)
    E_a_prime_b = compute_correlation_from_counts(counts_a_prime_b)

    counts_a_prime_b_prime = run_chsh_counts(
        a_prime,
        b_prime,
        shots=shots,
        seed=seed_a_prime_b_prime,
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
    )


def run_chsh_counts_with_eve(
    angle_a,
    angle_b,
    intercept_probability=1.0,
    shots=1000,
    seed=None,
):
    """Esegue conteggi CHSH con Eve intercept-resend."""
    if shots <= 0:
        raise ValueError("shots deve essere maggiore di 0.")

    if intercept_probability < 0.0 or intercept_probability > 1.0:
        raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    rng = np.random.default_rng(seed)
    counts = {}

    for shot_index in range(shots):
        eve_intercepted = rng.random() < intercept_probability

        if not eve_intercepted:
            if seed is None:
                ideal_seed = None
            else:
                ideal_seed = seed + 7000 + shot_index

            ideal_counts = run_chsh_counts(
                angle_a,
                angle_b,
                shots=1,
                seed=ideal_seed,
            )

            for bitstring in ideal_counts:
                if bitstring not in counts:
                    counts[bitstring] = 0
                counts[bitstring] = counts[bitstring] + ideal_counts[bitstring]

        else:
            if seed is None:
                eve_seed = None
            else:
                eve_seed = seed + 1000 + shot_index

            eve_basis = choose_eve_basis(seed=eve_seed)

            entangled_circuit = QuantumCircuit(2, 2)
            prepare_bell_phi_plus(entangled_circuit)

            # Eve misura il qubit destinato a Bob e rompe l'entanglement.
            measure_e91_qubit(entangled_circuit, eve_basis, qubit=1, cbit=1)
            measure_in_angle(entangled_circuit, angle_a, qubit=0, cbit=0)

            if seed is None:
                simulator = AerSimulator()
            else:
                simulator = AerSimulator(seed_simulator=seed + 5000 + shot_index)

            result = simulator.run(entangled_circuit, shots=1).result()
            eve_counts = result.get_counts(entangled_circuit)

            for bitstring in eve_counts:
                measured_bits = bitstring

            # Qiskit mostra i bit classici come c1 c0.
            alice_bit = int(measured_bits[-1])
            eve_bit = int(measured_bits[-2])

            bob_circuit = QuantumCircuit(1, 1)
            prepare_single_qubit_from_bit_basis(
                bob_circuit,
                eve_bit,
                eve_basis,
                qubit=0,
            )
            measure_in_angle(bob_circuit, angle_b, qubit=0, cbit=0)

            if seed is None:
                bob_simulator = AerSimulator()
            else:
                bob_simulator = AerSimulator(seed_simulator=seed + 6000 + shot_index)

            bob_result = bob_simulator.run(bob_circuit, shots=1).result()
            bob_counts = bob_result.get_counts(bob_circuit)

            for measured_bit in bob_counts:
                bob_bit = int(measured_bit)

            final_bitstring = f"{bob_bit}{alice_bit}"

            if final_bitstring not in counts:
                counts[final_bitstring] = 0
            counts[final_bitstring] = counts[final_bitstring] + 1

    return counts


def run_chsh_experiment_with_eve(
    intercept_probability=1.0,
    shots=1000,
    seed=None,
):
    """Simula CHSH con Eve intercept-resend."""
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

    counts_ab = run_chsh_counts_with_eve(
        a,
        b,
        intercept_probability=intercept_probability,
        shots=shots,
        seed=seed_ab,
    )
    E_ab = compute_correlation_from_counts(counts_ab)

    counts_ab_prime = run_chsh_counts_with_eve(
        a,
        b_prime,
        intercept_probability=intercept_probability,
        shots=shots,
        seed=seed_ab_prime,
    )
    E_ab_prime = compute_correlation_from_counts(counts_ab_prime)

    counts_a_prime_b = run_chsh_counts_with_eve(
        a_prime,
        b,
        intercept_probability=intercept_probability,
        shots=shots,
        seed=seed_a_prime_b,
    )
    E_a_prime_b = compute_correlation_from_counts(counts_a_prime_b)

    counts_a_prime_b_prime = run_chsh_counts_with_eve(
        a_prime,
        b_prime,
        intercept_probability=intercept_probability,
        shots=shots,
        seed=seed_a_prime_b_prime,
    )
    E_a_prime_b_prime = compute_correlation_from_counts(counts_a_prime_b_prime)

    S = compute_chsh_s(E_ab, E_ab_prime, E_a_prime_b, E_a_prime_b_prime)

    metadata = {
        "intercept_probability": intercept_probability,
    }

    return build_chsh_result(
        E_ab,
        E_ab_prime,
        E_a_prime_b,
        E_a_prime_b_prime,
        S,
        shots,
        extra_metadata=metadata,
    )


def prepare_classically_correlated_pair(circuit, source_bit):
    """Prepara una coppia classica |00> oppure |11>."""
    if source_bit not in (0, 1):
        raise ValueError("source_bit deve essere 0 oppure 1.")

    # Questa preparazione crea correlazione classica, non entanglement.
    if source_bit == 1:
        circuit.x(0)
        circuit.x(1)

    return circuit


def choose_classical_source_bit(seed=None):
    """Sceglie il bit della sorgente classica."""
    rng = np.random.default_rng(seed)
    source_bit = rng.integers(0, 2)

    return int(source_bit)


def run_e91_round_with_classical_source(
    alice_basis,
    bob_basis,
    source_bit=None,
    seed=None,
):
    """Simula un round E91 con sorgente classica."""
    check_basis(alice_basis)
    check_basis(bob_basis)

    if source_bit is None:
        source_bit = choose_classical_source_bit(seed)
    else:
        if source_bit not in (0, 1):
            raise ValueError("source_bit deve essere 0 oppure 1.")

    circuit = QuantumCircuit(2, 2)
    prepare_classically_correlated_pair(circuit, source_bit)
    measure_e91_qubit(circuit, alice_basis, qubit=0, cbit=0)
    measure_e91_qubit(circuit, bob_basis, qubit=1, cbit=1)

    if seed is None:
        simulator = AerSimulator()
    else:
        simulator = AerSimulator(seed_simulator=seed + 7000)

    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    for bitstring in counts:
        measured_bits = bitstring

    # Qiskit mostra i bit classici come c1 c0.
    alice_bit = int(measured_bits[-1])
    bob_bit = int(measured_bits[-2])

    return {
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "alice_bit": alice_bit,
        "bob_bit": bob_bit,
        "source_type": "classical_correlated",
        "source_bit": source_bit,
    }


def run_e91_protocol_with_classical_source(n_rounds, seed=None):
    """Simula piu round E91 con sorgente classica."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if seed is None:
        alice_bases_seed = None
        bob_bases_seed = None
    else:
        alice_bases_seed = seed
        bob_bases_seed = seed + 1

    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)

    results = []

    for i in range(n_rounds):
        alice_basis = alice_bases[i]
        bob_basis = bob_bases[i]

        if seed is None:
            round_seed = None
        else:
            round_seed = seed + 20 + i

        round_result = run_e91_round_with_classical_source(
            alice_basis,
            bob_basis,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        result = {
            "round": i,
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "alice_bit": round_result["alice_bit"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
            "source_type": round_result["source_type"],
            "source_bit": round_result["source_bit"],
        }
        results.append(result)

    return results


def run_chsh_counts_with_classical_source(
    angle_a,
    angle_b,
    shots=1000,
    seed=None,
):
    """Esegue conteggi CHSH con sorgente classica."""
    if shots <= 0:
        raise ValueError("shots deve essere maggiore di 0.")

    rng = np.random.default_rng(seed)
    counts = {}

    for shot_index in range(shots):
        source_bit = int(rng.integers(0, 2))

        circuit = QuantumCircuit(2, 2)
        prepare_classically_correlated_pair(circuit, source_bit)
        measure_in_angle(circuit, angle_a, qubit=0, cbit=0)
        measure_in_angle(circuit, angle_b, qubit=1, cbit=1)

        if seed is None:
            simulator = AerSimulator()
        else:
            simulator = AerSimulator(seed_simulator=seed + 8000 + shot_index)

        result = simulator.run(circuit, shots=1).result()
        shot_counts = result.get_counts(circuit)

        for bitstring in shot_counts:
            measured_bits = bitstring

        if measured_bits not in counts:
            counts[measured_bits] = 0
        counts[measured_bits] = counts[measured_bits] + 1

    return counts


def run_chsh_experiment_with_classical_source(shots=1000, seed=None):
    """Simula CHSH con una sorgente classicamente correlata."""
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

    counts_ab = run_chsh_counts_with_classical_source(
        a,
        b,
        shots=shots,
        seed=seed_ab,
    )
    E_ab = compute_correlation_from_counts(counts_ab)

    counts_ab_prime = run_chsh_counts_with_classical_source(
        a,
        b_prime,
        shots=shots,
        seed=seed_ab_prime,
    )
    E_ab_prime = compute_correlation_from_counts(counts_ab_prime)

    counts_a_prime_b = run_chsh_counts_with_classical_source(
        a_prime,
        b,
        shots=shots,
        seed=seed_a_prime_b,
    )
    E_a_prime_b = compute_correlation_from_counts(counts_a_prime_b)

    counts_a_prime_b_prime = run_chsh_counts_with_classical_source(
        a_prime,
        b_prime,
        shots=shots,
        seed=seed_a_prime_b_prime,
    )
    E_a_prime_b_prime = compute_correlation_from_counts(counts_a_prime_b_prime)

    S = compute_chsh_s(E_ab, E_ab_prime, E_a_prime_b, E_a_prime_b_prime)

    metadata = {
        "source_type": "classical_correlated",
    }

    return build_chsh_result(
        E_ab,
        E_ab_prime,
        E_a_prime_b,
        E_a_prime_b_prime,
        S,
        shots,
        extra_metadata=metadata,
    )
