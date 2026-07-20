import numpy as np
from qiskit_aer.noise import NoiseModel, amplitude_damping_error, pauli_error


def check_probability(probability):
    """Controlla che una probabilita sia tra 0 e 1."""
    if probability < 0.0 or probability > 1.0:
        raise ValueError("La probabilita deve essere tra 0.0 e 1.0.")


def build_bit_flip_noise_model(noise_probability):
    """Crea un noise model Qiskit per rumore bit-flip."""
    check_probability(noise_probability)

    # Bit-flip: con probabilita p il canale applica X,
    # altrimenti lascia invariato il qubit.
    noise_model = NoiseModel()
    error = pauli_error([
        ("X", noise_probability),
        ("I", 1 - noise_probability),
    ])
    noise_model.add_all_qubit_quantum_error(error, ["id"])

    return noise_model


def apply_bit_flip_noise(circuit, qubit, noise_probability, seed=None):
    """Applica un possibile errore bit-flip al qubit."""
    check_probability(noise_probability)

    # Versione esplicita del bit-flip: utile nei round singoli
    # per sapere se l'errore X e' stato applicato.
    rng = np.random.default_rng(seed)
    random_number = rng.random()

    if random_number < noise_probability:
        circuit.x(qubit)
        noise_applied = True
    else:
        noise_applied = False

    return circuit, noise_applied


def build_amplitude_damping_noise_model(damping_probability):
    """Crea un noise model con amplitude damping."""
    check_probability(damping_probability)

    # Amplitude damping: il NoiseModel rappresenta un canale dissipativo
    # che puo far decadere la componente eccitata del qubit.
    noise_model = NoiseModel()
    error = amplitude_damping_error(damping_probability)

    # L'istruzione id rappresenta in modo semplice il passaggio nel canale.
    noise_model.add_all_qubit_quantum_error(error, ["id"])

    return noise_model


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

    # Modello Jaynes-Cummings semplificato: C1(t) descrive la
    # sopravvivenza dell'ampiezza eccitata durante la propagazione.
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
    # La probabilita di damping e' il complemento della probabilita
    # di sopravvivenza della componente eccitata.
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
    # Catena distanza -> tempo di propagazione -> probabilita di damping,
    # usata poi come parametro del canale di amplitude damping.
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
