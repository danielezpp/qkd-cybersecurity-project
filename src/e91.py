import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from qkd_core import (
        check_basis,
        check_bit,
        random_bases,
    )
    from chsh import run_chsh_experiment_from_counts_function
    from attacks import choose_eve_basis, prepare_single_qubit_from_bit_basis
except ImportError:
    from .qkd_core import (
        check_basis,
        check_bit,
        random_bases,
    )
    from .chsh import run_chsh_experiment_from_counts_function
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


def _run_e91_round(
    alice_basis,
    bob_basis,
    source_mode="entangled",
    attack_mode=None,
    intercept_probability=0.0,
    source_bit=None,
    seed=None,
):
    """Esegue un round E91 in uno scenario scelto."""
    check_basis(alice_basis)
    check_basis(bob_basis)

    if source_mode not in ("entangled", "classical"):
        raise ValueError("source_mode non riconosciuto.")

    if attack_mode is not None and attack_mode != "intercept_resend":
        raise ValueError("attack_mode non riconosciuto.")

    if attack_mode == "intercept_resend":
        if source_mode != "entangled":
            raise ValueError("Eve intercept-resend e' prevista solo con sorgente entangled.")

        if intercept_probability < 0.0 or intercept_probability > 1.0:
            raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

        rng = np.random.default_rng(seed)
        eve_intercepted = rng.random() < intercept_probability

        if not eve_intercepted:
            round_result = _run_e91_round(alice_basis, bob_basis)

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

    if source_mode == "entangled":
        circuit = QuantumCircuit(2, 2)
        prepare_bell_phi_plus(circuit)
    else:
        if source_bit is None:
            source_bit = choose_classical_source_bit(seed)
        else:
            check_bit(source_bit)

        circuit = QuantumCircuit(2, 2)
        prepare_classically_correlated_pair(circuit, source_bit)

    measure_e91_qubit(circuit, alice_basis, qubit=0, cbit=0)
    measure_e91_qubit(circuit, bob_basis, qubit=1, cbit=1)

    if source_mode == "classical" and seed is not None:
        simulator = AerSimulator(seed_simulator=seed + 7000)
    else:
        simulator = AerSimulator()

    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    for bitstring in counts:
        measured_bits = bitstring

    # Qiskit mostra i bit classici come c1 c0.
    alice_bit = int(measured_bits[-1])
    bob_bit = int(measured_bits[-2])

    result = {
        "alice_basis": alice_basis,
        "bob_basis": bob_basis,
        "alice_bit": alice_bit,
        "bob_bit": bob_bit,
    }

    if source_mode == "classical":
        result["source_type"] = "classical_correlated"
        result["source_bit"] = source_bit

    return result


def _run_e91_protocol(
    n_rounds,
    source_mode="entangled",
    attack_mode=None,
    intercept_probability=0.0,
    seed=None,
):
    """Esegue piu round E91 in uno scenario scelto."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

    if source_mode not in ("entangled", "classical"):
        raise ValueError("source_mode non riconosciuto.")

    if attack_mode is not None and attack_mode != "intercept_resend":
        raise ValueError("attack_mode non riconosciuto.")

    if attack_mode == "intercept_resend":
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

        if source_mode == "classical":
            if seed is None:
                round_seed = None
            else:
                round_seed = seed + 20 + i
        elif attack_mode == "intercept_resend":
            if seed is None:
                round_seed = None
            else:
                round_seed = seed + 10 + i
        else:
            round_seed = None

        round_result = _run_e91_round(
            alice_basis,
            bob_basis,
            source_mode=source_mode,
            attack_mode=attack_mode,
            intercept_probability=intercept_probability,
            seed=round_seed,
        )
        keep = alice_basis == bob_basis

        if source_mode == "classical":
            round_number = i
        else:
            round_number = i + 1

        result = {
            "round": round_number,
            "alice_basis": round_result["alice_basis"],
            "bob_basis": round_result["bob_basis"],
            "alice_bit": round_result["alice_bit"],
            "bob_bit": round_result["bob_bit"],
            "keep": keep,
        }

        if attack_mode == "intercept_resend":
            result["eve_intercepted"] = round_result["eve_intercepted"]
            result["eve_basis"] = round_result["eve_basis"]
            result["eve_bit"] = round_result["eve_bit"]

        if source_mode == "classical":
            result["source_type"] = round_result["source_type"]
            result["source_bit"] = round_result["source_bit"]

        results.append(result)

    return results


def run_e91_round(alice_basis, bob_basis):
    """Simula un singolo round E91 ideale."""
    return _run_e91_round(alice_basis, bob_basis)


def run_e91_protocol(n_rounds, seed=None):
    """Simula piu round del protocollo E91 ideale."""
    return _run_e91_protocol(n_rounds, seed=seed)


def run_e91_round_with_eve(
    alice_basis,
    bob_basis,
    intercept_probability=1.0,
    seed=None,
):
    """Simula un singolo round E91 con Eve."""
    return _run_e91_round(
        alice_basis,
        bob_basis,
        source_mode="entangled",
        attack_mode="intercept_resend",
        intercept_probability=intercept_probability,
        seed=seed,
    )


def run_e91_protocol_with_eve(
    n_rounds,
    intercept_probability=1.0,
    seed=None,
):
    """Simula piu round E91 con Eve."""
    return _run_e91_protocol(
        n_rounds,
        source_mode="entangled",
        attack_mode="intercept_resend",
        intercept_probability=intercept_probability,
        seed=seed,
    )


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
    metadata = {
        "scenario": "ideal",
    }

    return run_chsh_experiment_from_counts_function(
        run_chsh_counts,
        shots=shots,
        seed=seed,
        extra_metadata=metadata,
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
    metadata = {
        "scenario": "eve_intercept_resend",
        "intercept_probability": intercept_probability,
    }

    return run_chsh_experiment_from_counts_function(
        run_chsh_counts_with_eve,
        shots=shots,
        seed=seed,
        extra_metadata=metadata,
        intercept_probability=intercept_probability,
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
    return _run_e91_round(
        alice_basis,
        bob_basis,
        source_mode="classical",
        source_bit=source_bit,
        seed=seed,
    )


def run_e91_protocol_with_classical_source(n_rounds, seed=None):
    """Simula piu round E91 con sorgente classica."""
    return _run_e91_protocol(
        n_rounds,
        source_mode="classical",
        seed=seed,
    )


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
    metadata = {
        "scenario": "classical_source",
        "source_type": "classical_correlated",
    }

    return run_chsh_experiment_from_counts_function(
        run_chsh_counts_with_classical_source,
        shots=shots,
        seed=seed,
        extra_metadata=metadata,
    )
