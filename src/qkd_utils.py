"""
Modulo temporaneo di compatibilita per le funzioni QKD.

Le implementazioni sono state spostate in moduli piu specifici:
- `bb84.py` per il protocollo BB84 ideale;
- `plots.py` per i grafici;
- `utils.py` per funzioni generali di supporto.
"""

try:
    from bb84 import (
        compute_qber,
        measure_bb84_state,
        prepare_bb84_state,
        random_bases,
        random_bits,
        run_bb84_protocol,
        run_bb84_round,
        sift_keys,
    )
    from plots import plot_keep_discard
    from utils import save_table
except ImportError:
    from .bb84 import (
        compute_qber,
        measure_bb84_state,
        prepare_bb84_state,
        random_bases,
        random_bits,
        run_bb84_protocol,
        run_bb84_round,
        sift_keys,
    )
    from .plots import plot_keep_discard
    from .utils import save_table

__all__ = [
    "random_bits",
    "random_bases",
    "prepare_bb84_state",
    "measure_bb84_state",
    "run_bb84_round",
    "run_bb84_protocol",
    "sift_keys",
    "compute_qber",
    "plot_keep_discard",
    "save_table",
]
