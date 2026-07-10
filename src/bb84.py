"""
Funzioni per la simulazione del protocollo BB84 ideale.
"""

import numpy as np
import pandas as pd
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from utils import _validate_positive_int
except ImportError:
    from .utils import _validate_positive_int


def _validate_bit(bit):
    """Verifica che il bit sia 0 oppure 1."""
    if bit not in (0, 1) or isinstance(bit, bool):
        raise ValueError("bit deve essere 0 oppure 1.")


def _validate_basis(basis):
    """Verifica che la base sia 'Z' oppure 'X'."""
    if basis not in ("Z", "X"):
        raise ValueError("basis deve essere 'Z' oppure 'X'.")


def random_bits(n, seed=None):
    """
    Genera una lista di bit classici casuali.

    Parametri
    ---------
    n : int
        Numero di bit da generare. Deve essere maggiore di 0.
    seed : int, opzionale
        Seed per rendere la generazione riproducibile.

    Restituisce
    -----------
    list[int]
        Lista contenente n interi, ciascuno uguale a 0 oppure 1.
    """
    _validate_positive_int(n)
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=n).tolist()


def random_bases(n, seed=None):
    """
    Genera una lista di basi BB84 casuali.

    Parametri
    ---------
    n : int
        Numero di basi da generare. Deve essere maggiore di 0.
    seed : int, opzionale
        Seed per rendere la generazione riproducibile.

    Restituisce
    -----------
    list[str]
        Lista contenente n stringhe, ciascuna uguale a "Z" oppure "X".
    """
    _validate_positive_int(n)
    rng = np.random.default_rng(seed)
    return rng.choice(["Z", "X"], size=n).tolist()


def prepare_bb84_state(circuit, bit, basis, qubit=0):
    """
    Prepara uno stato quantistico BB84 sul qubit selezionato.

    La corrispondenza usata e:
    - bit 0, base "Z": |0>
    - bit 1, base "Z": |1>
    - bit 0, base "X": |+>
    - bit 1, base "X": |->
    """
    _validate_bit(bit)
    _validate_basis(basis)

    if bit == 1:
        circuit.x(qubit)
    if basis == "X":
        circuit.h(qubit)

    return circuit


def measure_bb84_state(circuit, basis, qubit=0, cbit=0):
    """
    Misura uno stato BB84 nella base selezionata.

    Per la base X viene applicato un gate Hadamard prima della misura
    computazionale standard.
    """
    _validate_basis(basis)

    if basis == "X":
        circuit.h(qubit)
    circuit.measure(qubit, cbit)

    return circuit


def run_bb84_round(alice_bit, alice_basis, bob_basis, simulator=None, shots=1):
    """
    Simula un singolo round BB84 ideale da Alice a Bob.

    Alice prepara un qubit in base al suo bit e alla sua base. Bob misura lo
    stesso qubit nella base scelta. Non sono inclusi Eve o rumore.
    """
    _validate_bit(alice_bit)
    _validate_basis(alice_basis)
    _validate_basis(bob_basis)
    _validate_positive_int(shots)

    if simulator is None:
        simulator = AerSimulator()

    circuit = QuantumCircuit(1, 1)
    prepare_bb84_state(circuit, alice_bit, alice_basis, qubit=0)
    measure_bb84_state(circuit, bob_basis, qubit=0, cbit=0)

    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)
    measured_bit = max(counts, key=counts.get)

    return int(measured_bit)


def run_bb84_protocol(n_rounds, seed=None):
    """
    Simula il protocollo BB84 ideale su piu round.

    Restituisce un DataFrame con le scelte di Alice, le scelte di Bob e la
    decisione di sifting per ogni round.
    """
    _validate_positive_int(n_rounds)

    if seed is None:
        alice_bits_seed = None
        alice_bases_seed = None
        bob_bases_seed = None
        simulator_seed = None
    else:
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise TypeError("seed deve essere un intero oppure None.")
        alice_bits_seed = seed
        alice_bases_seed = seed + 1
        bob_bases_seed = seed + 2
        simulator_seed = seed + 3

    alice_bits = random_bits(n_rounds, seed=alice_bits_seed)
    alice_bases = random_bases(n_rounds, seed=alice_bases_seed)
    bob_bases = random_bases(n_rounds, seed=bob_bases_seed)
    simulator = AerSimulator(seed_simulator=simulator_seed)

    rows = []
    for index, (alice_bit, alice_basis, bob_basis) in enumerate(
        zip(alice_bits, alice_bases, bob_bases),
        start=1,
    ):
        bob_bit = run_bb84_round(
            alice_bit=alice_bit,
            alice_basis=alice_basis,
            bob_basis=bob_basis,
            simulator=simulator,
            shots=1,
        )
        keep = alice_basis == bob_basis
        rows.append(
            {
                "round": index,
                "alice_bit": alice_bit,
                "alice_basis": alice_basis,
                "bob_basis": bob_basis,
                "bob_bit": bob_bit,
                "keep": keep,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "round",
            "alice_bit",
            "alice_basis",
            "bob_basis",
            "bob_bit",
            "keep",
        ],
    )


def sift_keys(results_df):
    """
    Estrae le chiavi sifted di Alice e Bob da un DataFrame BB84.
    """
    sifted_df = results_df[results_df["keep"] == True]
    alice_key = sifted_df["alice_bit"].tolist()
    bob_key = sifted_df["bob_bit"].tolist()

    return alice_key, bob_key


def compute_qber(alice_key, bob_key):
    """
    Calcola il Quantum Bit Error Rate tra due chiavi sifted.
    """
    if len(alice_key) != len(bob_key):
        raise ValueError("alice_key e bob_key devono avere la stessa lunghezza.")
    if len(alice_key) == 0:
        return np.nan

    errors = sum(alice_bit != bob_bit for alice_bit, bob_bit in zip(alice_key, bob_key))

    return float(errors / len(alice_key))
