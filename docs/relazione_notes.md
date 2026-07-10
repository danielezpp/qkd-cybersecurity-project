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

## Unità 2 — BB84 con Eve: attacco intercept-resend e QBER

### Obiettivo dell’unità

L’obiettivo dell’Unità 2 è estendere la simulazione del protocollo BB84 introducendo un attaccante esterno, Eve, che applica un attacco di tipo intercept-resend.

Nel caso ideale simulato nell’Unità 1, Alice e Bob ottengono la stessa chiave dopo il sifting e il QBER risulta nullo. In questa unità si studia invece cosa accade quando Eve intercetta i qubit inviati da Alice, li misura in una base scelta casualmente e poi reinvia a Bob nuovi qubit preparati sulla base dei risultati ottenuti.

Questa unità rappresenta il primo passaggio dal caso ideale a uno scenario di sicurezza più realistico, in cui la presenza di un’intercettazione può essere rivelata attraverso l’aumento del Quantum Bit Error Rate.

### File coinvolti

I file principali coinvolti nell’Unità 2 sono:

- `src/attacks.py`
- `src/bb84.py`
- `notebooks/02_bb84_intercept_resend_qber.ipynb`
- `results/tables/bb84_eve_qber_vs_interception.csv`
- `results/figures/bb84_eve_qber_vs_interception.png`

Il file `attacks.py` contiene le funzioni elementari che descrivono il comportamento di Eve.  
Il file `bb84.py` contiene invece il protocollo BB84, sia nel caso ideale sia nel caso con possibile intercettazione di Eve.  
Il notebook `02_bb84_intercept_resend_qber.ipynb` mostra in modo narrativo e didattico il funzionamento dell’attacco e il suo effetto sul QBER.

### Scelta implementativa

Per mantenere il codice semplice e spiegabile, la logica è stata separata in due livelli:

- `attacks.py`: funzioni elementari dell’attacco;
- `bb84.py`: protocollo BB84 completo, con o senza Eve.

Questa scelta permette di mantenere chiara la distinzione tra il comportamento locale di Eve e il flusso complessivo del protocollo.

In particolare, Eve non è trattata come un nuovo protocollo autonomo, ma come una modifica del canale di comunicazione tra Alice e Bob.

### Funzioni implementate in `attacks.py`

Le funzioni principali introdotte per Eve sono:

- `choose_eve_basis(seed=None)`: sceglie casualmente una base tra `Z` e `X`;
- `eve_measure(alice_bit, alice_basis, eve_basis)`: simula la misura di Eve sul qubit preparato da Alice;
- `eve_intercept_resend(alice_bit, alice_basis, eve_basis=None, seed=None)`: simula l’intercettazione e il reinvio da parte di Eve.

La funzione `eve_intercept_resend` restituisce un dizionario contenente:

- `eve_basis`;
- `eve_bit`.

Il significato fisico è che Eve, dopo aver misurato il qubit, prepara un nuovo stato coerente con il bit e la base ottenuti dalla sua misura e lo invia a Bob.

### Funzioni implementate in `bb84.py`

Nel file `bb84.py` sono state aggiunte le funzioni:

- `run_bb84_round_with_eve(alice_bit, alice_basis, bob_basis, intercept_probability=1.0, seed=None)`;
- `run_bb84_protocol_with_eve(n_rounds, intercept_probability=1.0, seed=None)`.

La prima funzione simula un singolo round BB84 con possibile intercettazione.  
La seconda funzione ripete il protocollo per più round e restituisce una lista di dizionari, senza usare direttamente DataFrame o funzioni di plotting.

Ogni round contiene informazioni come:

- bit di Alice;
- base di Alice;
- base di Bob;
- bit misurato da Bob;
- informazione `keep` per il sifting;
- eventuale intercettazione di Eve;
- base scelta da Eve;
- bit misurato da Eve.

### Stile del codice

Durante l’Unità 2 è stata confermata la scelta di mantenere il codice in uno stile didattico, più vicino a quello di un progetto universitario che a una libreria professionale.

Le scelte principali sono state:

- codice semplice e leggibile;
- cicli `for` espliciti;
- poche astrazioni;
- validazioni minime;
- niente DataFrame nella logica del protocollo;
- niente plotting nei file sorgente;
- separazione tra simulazione e rappresentazione dei risultati;
- commenti e Markdown in italiano;
- nomi funzione in inglese per coerenza con Python e Qiskit.

Questa scelta rende il codice più facilmente spiegabile durante l’esame orale.

### Strumenti Qiskit utilizzati

Anche in questa unità sono stati usati strumenti essenziali di Qiskit:

- `QuantumCircuit(1, 1)`;
- gate `X`;
- gate `H`;
- `measure`;
- `AerSimulator`.

Nel caso con Eve, il circuito viene utilizzato in due momenti concettualmente distinti:

1. Eve misura il qubit preparato da Alice;
2. Bob misura un nuovo qubit preparato da Eve sulla base del risultato della sua misura.

### Interpretazione fisica dell’attacco intercept-resend

L’attacco intercept-resend funziona nel seguente modo:

1. Alice prepara un qubit in una delle due basi BB84, `Z` oppure `X`;
2. Eve intercetta il qubit;
3. Eve sceglie casualmente una base di misura;
4. Eve misura il qubit;
5. Eve prepara un nuovo qubit coerente con il bit e la base ottenuti;
6. Bob misura il qubit ricevuto da Eve.

Il punto essenziale è che Eve non conosce la base scelta da Alice. Se Eve misura nella base corretta, può ottenere il bit senza introdurre errore. Se invece misura nella base sbagliata, la misura quantistica altera lo stato e introduce casualità.

Questo disturbo può emergere dopo il sifting come differenza tra la chiave di Alice e quella di Bob.

### Sifting e QBER con Eve

Anche in presenza di Eve, Alice e Bob applicano il sifting, cioè mantengono solo i round in cui hanno scelto la stessa base.

Dopo il sifting si confrontano le chiavi ottenute da Alice e Bob e si calcola il QBER.

Il QBER è definito operativamente come la frazione di bit diversi tra la chiave di Alice e quella di Bob dopo il sifting.

Nel caso ideale:

`QBER = 0.0`

Nel caso con Eve, invece, il QBER può diventare maggiore di zero.

### Analisi al variare della probabilità di intercettazione

Nel notebook è stata introdotta una simulazione in cui la probabilità di intercettazione di Eve assume diversi valori:

- `0.0`;
- `0.25`;
- `0.5`;
- `0.75`;
- `1.0`.

Per ogni valore della probabilità di intercettazione sono stati simulati più round BB84, è stato applicato il sifting ed è stato calcolato il QBER.

I risultati sono stati raccolti in una tabella e successivamente rappresentati graficamente.

Questa analisi permette di osservare che il QBER tende ad aumentare al crescere della probabilità di intercettazione di Eve.

### Risultato teorico atteso

Nel caso in cui Eve intercetti sempre, cioè per `intercept_probability = 1.0`, il QBER atteso teoricamente nell’attacco intercept-resend è circa `0.25`.

L’argomento intuitivo è il seguente:

- Eve sceglie la base sbagliata circa metà delle volte;
- quando Eve sceglie la base sbagliata, Bob può ottenere un bit errato circa metà delle volte;
- quindi l’errore atteso è circa `1/2 × 1/2 = 1/4`.

Pertanto, con Eve sempre attiva, ci si aspetta un QBER vicino al 25%.

Il valore simulato può non essere esattamente pari a `0.25`, perché la simulazione è statistica e viene eseguita su un numero finito di round.

### Output prodotti

L’Unità 2 produce due output principali:

- tabella CSV dei risultati:
  `results/tables/bb84_eve_qber_vs_interception.csv`

- grafico del QBER al variare della probabilità di intercettazione:
  `results/figures/bb84_eve_qber_vs_interception.png`

La tabella contiene, per ogni probabilità di intercettazione:

- probabilità di intercettazione;
- numero di round simulati;
- lunghezza della chiave dopo il sifting;
- QBER ottenuto.

Il grafico mostra sull’asse orizzontale la probabilità di intercettazione di Eve e sull’asse verticale il QBER.

### Collegamento con il materiale del corso

Questa unità utilizza direttamente concetti fondamentali del corso:

- qubit;
- basi di misura;
- base computazionale `Z`;
- base Hadamard `X`;
- gate `X`;
- gate `H`;
- misura quantistica;
- collasso dello stato;
- probabilità di misura;
- incompatibilità tra basi di misura.

La parte specifica relativa a BB84, Eve, intercept-resend e QBER rappresenta invece un’integrazione applicativa collegata al tema del progetto finale sulla Quantum Key Distribution.

### Importanza per la discussione orale

Questa unità è importante per l’esame orale perché permette di spiegare non solo come funziona BB84, ma anche perché il protocollo consente di rilevare un’intercettazione.

Il punto centrale da sottolineare è che Eve, non conoscendo la base scelta da Alice, non può misurare il qubit senza rischiare di alterarlo. Questo effetto è una conseguenza diretta della misura quantistica e dell’uso di basi incompatibili.

Il QBER diventa quindi un indicatore operativo della possibile presenza di un attacco o di rumore nel canale.

### Limiti dell’Unità 2

L’Unità 2 considera solo l’attacco intercept-resend in forma semplificata.

Non sono ancora presenti:

- rumore fisico del canale;
- decoerenza;
- amplitude damping;
- attenuazione in fibra ottica;
- protocollo E91;
- entanglement;
- test CHSH;
- confronto sistematico tra BB84 ed E91.

Inoltre, la casualità utilizzata nella simulazione è pseudocasuale ed è scelta per rendere gli esperimenti riproducibili. In un sistema crittografico reale sarebbero necessarie sorgenti di casualità crittograficamente sicure o sorgenti quantistiche di numeri casuali.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- introdurre il modello di attacco intercept-resend;
- spiegare il ruolo di Eve nel protocollo BB84;
- mostrare come la misura di Eve possa disturbare lo stato quantistico;
- collegare il disturbo quantistico all’aumento del QBER;
- mostrare il confronto tra caso ideale e caso intercettato;
- presentare una prima analisi quantitativa del QBER;
- introdurre il valore teorico atteso del 25% con Eve sempre attiva;
- preparare il confronto futuro con rumore/decoerenza ed E91.

### Possibili domande orali

1. Che cos’è un attacco intercept-resend?
2. Perché Eve deve scegliere una base di misura?
3. Cosa succede se Eve misura nella base sbagliata?
4. Perché l’attacco di Eve può aumentare il QBER?
5. Perché con Eve sempre attiva il QBER atteso è circa 25%?
6. Che ruolo ha il sifting nel rilevare la presenza di Eve?
7. Qual è la differenza tra errore dovuto a Eve ed errore dovuto a rumore fisico?
8. Perché la misura quantistica rende rilevabile un’intercettazione?
9. Perché la simulazione non restituisce sempre esattamente QBER = 0.25?
10. In che modo questa unità prepara il confronto con E91?