"""
Funzioni semplici per simulare il protocollo BB84 ideale.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


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


def run_bb84_round(alice_bit, alice_basis, bob_basis):
    """Simula un singolo round BB84 ideale."""
    check_bit(alice_bit)
    check_basis(alice_basis)
    check_basis(bob_basis)

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


def run_bb84_protocol(n_rounds, seed=None):
    """Simula piu round del protocollo BB84 ideale."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

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

        bob_bit = run_bb84_round(alice_bit, alice_basis, bob_basis)
        keep = alice_basis == bob_basis

        result = {
            "round": i + 1,
            "alice_bit": alice_bit,
            "alice_basis": alice_basis,
            "bob_basis": bob_basis,
            "bob_bit": bob_bit,
            "keep": keep,
        }
        results.append(result)

    return results


def run_bb84_round_with_eve(
    alice_bit,
    alice_basis,
    bob_basis,
    intercept_probability=1.0,
    seed=None,
):
    """Simula un singolo round BB84 con Eve."""
    try:
        from attacks import eve_intercept_resend
    except ImportError:
        from .attacks import eve_intercept_resend

    check_bit(alice_bit)
    check_basis(alice_basis)
    check_basis(bob_basis)

    if intercept_probability < 0.0 or intercept_probability > 1.0:
        raise ValueError("intercept_probability deve essere tra 0.0 e 1.0.")

    rng = np.random.default_rng(seed)
    eve_intercepted = rng.random() < intercept_probability

    if not eve_intercepted:
        bob_bit = run_bb84_round(alice_bit, alice_basis, bob_basis)
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


def run_bb84_protocol_with_eve(n_rounds, intercept_probability=1.0, seed=None):
    """Simula piu round BB84 con Eve."""
    if n_rounds <= 0:
        raise ValueError("n_rounds deve essere maggiore di 0.")

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

        round_result = run_bb84_round_with_eve(
            alice_bit,
            alice_basis,
            bob_basis,
            intercept_probability=intercept_probability,
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
            "eve_intercepted": round_result["eve_intercepted"],
            "eve_basis": round_result["eve_basis"],
            "eve_bit": round_result["eve_bit"],
        }
        results.append(result)

    return results


def sift_keys(results):
    """Estrae le chiavi sifted dai risultati BB84."""
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
