import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from qkd_core import check_basis, check_bit
    from bb84 import measure_bb84_state
except ImportError:
    from .qkd_core import check_basis, check_bit
    from .bb84 import measure_bb84_state


def choose_eve_basis(seed=None):
    """Sceglie casualmente la base di Eve."""
    rng = np.random.default_rng(seed)
    eve_basis = rng.choice(["Z", "X"])

    return str(eve_basis)


def prepare_single_qubit_from_bit_basis(circuit, bit, basis, qubit=0):
    """Prepara un qubit a partire da bit e base."""
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


def eve_measure(alice_bit, alice_basis, eve_basis):
    """Misura il qubit di Alice nella base scelta da Eve."""
    circuit = QuantumCircuit(1, 1)
    prepare_single_qubit_from_bit_basis(circuit, alice_bit, alice_basis)
    measure_bb84_state(circuit, eve_basis)

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    
    for measured_bit in counts:
        eve_bit = int(measured_bit)

    return eve_bit


def eve_intercept_resend(alice_bit, alice_basis, eve_basis=None, seed=None):
    """Simula il passo base dell'attacco intercept-resend."""
    if eve_basis is None:
        eve_basis = choose_eve_basis(seed)
    else:
        check_basis(eve_basis)

    eve_bit = eve_measure(alice_bit, alice_basis, eve_basis)

    return {
        "eve_basis": eve_basis,
        "eve_bit": eve_bit,
    }
