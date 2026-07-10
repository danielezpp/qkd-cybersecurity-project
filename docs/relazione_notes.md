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

### Obiettivo dell’unità

L’obiettivo dell’Unità 1 è simulare il protocollo BB84 in condizioni ideali, cioè in assenza di intercettazione da parte di Eve e in assenza di rumore o decoerenza del canale.

Questa unità rappresenta il livello base del progetto: prima di introdurre attacchi, rumore o protocolli entanglement-based come E91, è necessario verificare che Alice e Bob riescano a costruire correttamente una chiave condivisa nel caso ideale.

### File coinvolti

I file principali utilizzati o prodotti nell’Unità 1 sono:

- `notebooks/01_bb84_ideal.ipynb`
- `src/bb84.py`
- `src/plots.py`
- `src/utils.py`
- `src/qkd_utils.py`
- `results/tables/bb84_ideal_results.csv`
- `results/figures/bb84_ideal_keep_discard.png`

Il file `qkd_utils.py` è mantenuto come file di compatibilità, mentre la logica principale è stata separata in moduli più leggibili: `bb84.py` per il protocollo BB84, `plots.py` per i grafici e `utils.py` per funzioni generali.

### Funzioni implementate

Le principali funzioni implementate sono:

- `random_bits(n, seed=None)`: genera una sequenza casuale di bit classici 0/1;
- `random_bases(n, seed=None)`: genera una sequenza casuale di basi, `"Z"` oppure `"X"`;
- `prepare_bb84_state(circuit, bit, basis, qubit=0)`: prepara nel circuito Qiskit uno dei quattro stati BB84;
- `measure_bb84_state(circuit, basis, qubit=0, cbit=0)`: misura il qubit nella base scelta;
- `run_bb84_round(alice_bit, alice_basis, bob_basis, simulator=None, shots=1)`: esegue un singolo round del protocollo BB84 ideale;
- `run_bb84_protocol(n_rounds, seed=None)`: simula più round del protocollo;
- `sift_keys(results_df)`: applica il sifting, mantenendo solo i round in cui Alice e Bob hanno scelto la stessa base;
- `compute_qber(alice_key, bob_key)`: calcola il Quantum Bit Error Rate;
- `plot_keep_discard(results_df, path=None)`: produce il grafico dei round mantenuti e scartati;
- `save_table(df, path)`: salva una tabella dei risultati in formato CSV.

### Convenzioni usate

Nel protocollo BB84 simulato sono state adottate le seguenti convenzioni:

| Bit classico | Base | Stato quantistico | Implementazione Qiskit |
|---:|---|---|---|
| 0 | Z | `|0⟩` | nessun gate |
| 1 | Z | `|1⟩` | gate `X` |
| 0 | X | `|+⟩` | gate `H` |
| 1 | X | `|-⟩` | gate `X` seguito da `H` |

La misura in base `Z` viene realizzata tramite misura diretta.  
La misura in base `X` viene realizzata applicando prima un gate `H` e poi misurando in base computazionale.

### Strumenti Qiskit utilizzati

In questa unità sono stati usati solo strumenti elementari di Qiskit:

- `QuantumCircuit(1, 1)`;
- gate `X`;
- gate `H`;
- `measure`;
- `AerSimulator`.

Questa scelta è coerente con l’obiettivo dell’unità: simulare BB84 ideale usando circuiti a singolo qubit e misure in basi differenti.

### Risultati prodotti

Il notebook `01_bb84_ideal.ipynb` produce:

- una simulazione di pochi round per verificare il comportamento del protocollo;
- una simulazione su più round;
- una tabella dei risultati dei round;
- il processo di sifting;
- il calcolo del QBER;
- un grafico che confronta round mantenuti e round scartati.

I risultati vengono salvati in:

- `results/tables/bb84_ideal_results.csv`;
- `results/figures/bb84_ideal_keep_discard.png`.

### Risultato principale

Nel caso ideale, dopo il sifting, Alice e Bob condividono la stessa chiave.

Il risultato numerico atteso è: `QBER = 0.0`.

Questo risultato conferma che, in assenza di intercettazione e rumore, i bit mantenuti dopo il confronto delle basi coincidono.

### Interpretazione fisica

BB84 si basa sull’uso di due basi di misura incompatibili: la base computazionale `Z` e la base Hadamard `X`.

Se Alice e Bob scelgono la stessa base, Bob recupera correttamente il bit preparato da Alice.

Se invece scelgono basi diverse, il risultato della misura non è affidabile per la costruzione della chiave e il round viene scartato durante il sifting.

Nel caso ideale simulato in questa unità non è presente alcun attaccante e non è presente rumore nel canale. Pertanto, dopo il sifting, non compaiono errori tra la chiave di Alice e quella di Bob.

### Collegamento con il materiale del corso

Questa unità utilizza direttamente diversi concetti teorici trattati nel corso:

- qubit;
- stati `|0⟩` e `|1⟩`;
- sovrapposizione;
- base computazionale;
- gate unitari;
- gate `X`;
- gate `H`;
- misura quantistica;
- collasso dello stato;
- probabilità di misura.

La parte specifica relativa al protocollo BB84, al sifting e al QBER costituisce invece un’integrazione esterna rispetto ai fondamenti del corso, collegata al tema del progetto finale sulla Quantum Key Distribution.

### Limiti dell’Unità 1

L’Unità 1 considera solo il caso ideale. In particolare, non sono ancora presenti:

- Eve;
- attacco intercept-resend;
- rumore del canale;
- decoerenza;
- amplitude damping;
- confronto con E91.

Inoltre, la generazione casuale dei bit e delle basi è realizzata con generatori pseudocasuali standard, utili per la riproducibilità degli esperimenti. In un’applicazione crittografica reale sarebbe necessario utilizzare sorgenti di casualità crittograficamente sicure o sorgenti quantistiche di numeri casuali.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- introdurre il funzionamento base di BB84;
- mostrare la corrispondenza tra bit classici, basi e stati quantistici;
- spiegare il ruolo del gate Hadamard nel passaggio tra base `Z` e base `X`;
- introdurre il sifting;
- definire operativamente il QBER;
- mostrare il caso di riferimento ideale rispetto al quale confrontare intercettazione e rumore.

### Possibili domande orali

1. Perché BB84 usa due basi diverse?
2. Che cosa succede se Bob misura in una base diversa da quella usata da Alice?
3. Che cos’è il sifting?
4. Perché nel caso ideale il QBER è nullo?
5. Qual è il ruolo del gate Hadamard nel protocollo BB84?
6. La generazione casuale usata nella simulazione è equivalente a quella richiesta in un sistema crittografico reale?
