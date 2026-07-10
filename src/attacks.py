"""
Funzioni semplici per l'attacco intercept-resend di Eve su BB84.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from bb84 import check_basis, measure_bb84_state, prepare_bb84_state
except ImportError:
    from .bb84 import check_basis, measure_bb84_state, prepare_bb84_state


def choose_eve_basis(seed=None):
    """Sceglie casualmente la base di Eve."""
    rng = np.random.default_rng(seed)
    eve_basis = rng.choice(["Z", "X"])

    return str(eve_basis)


def eve_measure(alice_bit, alice_basis, eve_basis):
    """Misura il qubit di Alice nella base scelta da Eve."""
    circuit = QuantumCircuit(1, 1)
    prepare_bb84_state(circuit, alice_bit, alice_basis)
    measure_bb84_state(circuit, eve_basis)

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts(circuit)

    # Con un solo shot Eve ottiene un solo bit.
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
