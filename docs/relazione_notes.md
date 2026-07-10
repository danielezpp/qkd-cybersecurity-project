# Appunti per relazione finale

## Titolo provvisorio

Quantum Key Distribution per la cybersecurity: simulazione di BB84 ed E91 con intercettazione, QBER e rumore di canale

## Obiettivo del progetto

Il progetto analizza protocolli di Quantum Key Distribution in ambito cybersecurity, con particolare attenzione a BB84 ed E91.

## Collegamento con il corso

Concetti derivati dal corso:

- qubit;
- bra/ket;
- misura;
- collasso;
- basi di misura;
- gate unitari;
- Hadamard;
- Pauli X/Z;
- CNOT;
- prodotto tensoriale;
- entanglement;
- Bell states;
- osservabili;
- Hamiltoniana;
- valore atteso.

## Integrazioni esterne

- BB84;
- E91;
- Quantum Bit Error Rate;
- intercept-resend attack;
- sicurezza QKD;
- amplitude damping;
- decoerenza;
- rumore del canale.

## Struttura provvisoria relazione

1. Introduzione
2. Fondamenti teorici
3. Quantum Key Distribution e cybersecurity
4. BB84 ideale
5. Intercept-resend e QBER
6. E91
7. Confronto BB84 vs E91
8. Rumore e decoerenza
9. Risultati
10. Conclusioni

## Unità 1 — BB84 ideale

### Obiettivo dell'unità

L'unità introduce e simula il protocollo BB84 in condizioni ideali, senza intercettazione da parte di Eve e senza rumore di canale. Lo scopo è verificare il comportamento atteso del protocollo quando Alice e Bob preparano e misurano qubit nelle basi `Z` e `X`, applicano il sifting e calcolano il QBER.

### Funzioni implementate

- `random_bits(n, seed=None)`: genera bit casuali `0` e `1`.
- `random_bases(n, seed=None)`: genera basi casuali `Z` e `X`.
- `prepare_bb84_state(circuit, bit, basis, qubit=0)`: prepara gli stati BB84 `|0>`, `|1>`, `|+>`, `|->`.
- `measure_bb84_state(circuit, basis, qubit=0, cbit=0)`: misura nella base `Z` o `X`.
- `run_bb84_round(alice_bit, alice_basis, bob_basis, simulator=None, shots=1)`: simula un singolo round Alice-Bob.
- `run_bb84_protocol(n_rounds, seed=None)`: simula il protocollo su piu round e restituisce un DataFrame.
- `sift_keys(results_df)`: estrae le chiavi sifted di Alice e Bob.
- `compute_qber(alice_key, bob_key)`: calcola il Quantum Bit Error Rate.
- `save_table(df, path)`: salva i risultati in CSV.
- `plot_keep_discard(results_df, path=None)`: crea il grafico round mantenuti/scartati.

### Risultati prodotti

- Tabella completa della simulazione ideale BB84 salvata in `results/tables/bb84_ideal_results.csv`.
- Grafico dei round mantenuti e scartati salvato in `results/figures/bb84_ideal_keep_discard.png`.
- Simulazione principale: `n_rounds = 200`, `seed = 123`.
- Metriche calcolate: round totali, round mantenuti, round scartati, lunghezza della chiave sifted, QBER.

### Interpretazione dei risultati

Quando Alice e Bob scelgono la stessa base, il round viene conservato per la chiave sifted. Quando scelgono basi diverse, il round viene scartato perche la misura di Bob non e confrontabile in modo deterministico con la preparazione di Alice.

Nel caso ideale, dopo il sifting Alice e Bob condividono la stessa chiave e il QBER risulta nullo. Questo conferma il funzionamento del protocollo in assenza di intercettazione e rumore.

### Elementi da usare nella relazione finale

- Descrivere la codifica dei bit nelle basi `Z` e `X`.
- Spiegare il ruolo del gate Hadamard per preparare e misurare nella base `X`.
- Presentare il sifting come confronto pubblico delle basi, non dei bit.
- Usare la tabella CSV come evidenza dei singoli round.
- Usare il grafico keep/discard per mostrare che circa meta dei round viene conservata in media.
- Collegare il QBER nullo al caso ideale senza Eve e senza rumore.

### Possibili domande orali

1. Perche BB84 usa due basi?
2. Che cos'e il sifting?
3. Perche nel caso ideale il QBER e nullo?
