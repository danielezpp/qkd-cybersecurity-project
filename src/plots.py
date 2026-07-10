"""
Funzioni di visualizzazione per i risultati QKD.
"""

from pathlib import Path


def plot_keep_discard(results_df, path=None):
    """
    Crea un grafico dei round BB84 mantenuti e scartati.
    """
    import matplotlib.pyplot as plt

    kept = int(results_df["keep"].sum())
    discarded = int((~results_df["keep"]).sum())

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Mantenuti", "Scartati"], [kept, discarded], color=["#2f7d5b", "#b64b4b"])
    ax.set_title("BB84 ideale: round mantenuti e scartati")
    ax.set_xlabel("Esito del sifting")
    ax.set_ylabel("Numero di round")
    ax.set_ylim(0, max(kept, discarded) + 10)

    for index, value in enumerate([kept, discarded]):
        ax.text(index, value + 2, str(value), ha="center", va="bottom")

    fig.tight_layout()

    if path is not None:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)

    return fig, ax
