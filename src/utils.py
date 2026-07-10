"""
Funzioni generali di supporto per il progetto QKD.
"""

from pathlib import Path


def _validate_positive_int(n):
    """Verifica che n sia un intero positivo."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n deve essere un intero positivo.")
    if n <= 0:
        raise ValueError("n deve essere maggiore di 0.")


def save_table(df, path):
    """
    Salva un DataFrame in formato CSV senza indice.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
