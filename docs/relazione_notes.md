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

## Unità 3 — E91 ideale, entanglement e verifica CHSH

### Obiettivo dell’unità

L’obiettivo dell’Unità 3 è introdurre il protocollo E91 in condizioni ideali e mostrarne la differenza concettuale rispetto a BB84.

Mentre BB84 è un protocollo di tipo prepare-and-measure, in cui Alice prepara direttamente uno stato quantistico e Bob lo misura, E91 è basato sull’entanglement. Alice e Bob ricevono ciascuno un qubit appartenente a una coppia entangled e costruiscono la chiave a partire dalle correlazioni tra i risultati delle loro misure.

L’unità ha quindi due obiettivi principali:

- simulare una versione didattica di E91 ideale;
- verificare, tramite il test CHSH, che le correlazioni prodotte dallo stato entangled non sono spiegabili classicamente.

### File coinvolti

I file principali coinvolti nell’Unità 3 sono:

- `src/e91.py`
- `notebooks/03_e91_basic.ipynb`
- `results/tables/e91_ideal_results.csv`
- `results/figures/e91_ideal_keep_discard.png`

Il file `e91.py` contiene la logica del protocollo E91 ideale e le funzioni per la verifica CHSH.

Il notebook `03_e91_basic.ipynb` mostra in modo narrativo il funzionamento del protocollo E91, la preparazione dello stato entangled, il sifting, il calcolo del QBER e l’estensione CHSH.

### Differenza concettuale tra BB84 ed E91

Nel protocollo BB84 Alice prepara singoli qubit in basi diverse e Bob li misura. La sicurezza è collegata al fatto che una misura effettuata da Eve in una base sbagliata può disturbare lo stato e aumentare il QBER.

Nel protocollo E91, invece, la chiave nasce da coppie entangled condivise tra Alice e Bob. Alice misura un qubit della coppia e Bob misura l’altro. Quando scelgono basi compatibili, nel caso ideale ottengono risultati correlati.

Quindi:

- BB84: Alice prepara e Bob misura;
- E91: Alice e Bob misurano qubit entangled;
- BB84 rileva l’intercettazione tramite aumento del QBER;
- E91 collega la generazione della chiave alle correlazioni quantistiche prodotte dall’entanglement.

### Stato entangled utilizzato

Nella simulazione è stato usato lo stato di Bell:

`|Φ+⟩ = (|00⟩ + |11⟩) / √2`

Questo stato non descrive due qubit indipendenti, ma un sistema bipartito entangled. La misura di un qubit è correlata alla misura dell’altro.

Nel circuito Qiskit, lo stato `|Φ+⟩` viene preparato partendo da `|00⟩` e applicando:

- un gate `H` sul primo qubit;
- un gate `CX` con controllo sul primo qubit e target sul secondo.

La sequenza concettuale è:

`|00⟩ → H sul qubit 0 → sovrapposizione → CX → (|00⟩ + |11⟩) / √2`

### Strumenti Qiskit utilizzati

In questa unità sono stati usati strumenti essenziali di Qiskit:

- `QuantumCircuit(2, 2)`;
- gate `H`;
- gate `CX`;
- gate `RY`;
- `measure`;
- `AerSimulator`.

Il gate `H` e il gate `CX` sono usati per preparare lo stato entangled.

Il gate `RY` viene invece usato nella parte CHSH per simulare misure lungo direzioni ruotate.

### Funzioni principali implementate in `e91.py`

Le funzioni principali per la simulazione E91 ideale sono:

- `check_basis(basis)`;
- `random_bases(n, seed=None)`;
- `prepare_bell_phi_plus(circuit)`;
- `measure_e91_qubit(circuit, basis, qubit, cbit)`;
- `run_e91_round(alice_basis, bob_basis)`;
- `run_e91_protocol(n_rounds, seed=None)`;
- `sift_keys(results)`;
- `compute_qber(alice_key, bob_key)`.

Le funzioni seguono lo stesso stile didattico adottato per BB84:

- codice semplice;
- cicli espliciti;
- nessun DataFrame nei file sorgente;
- nessun grafico nei file sorgente;
- risultati restituiti come lista di dizionari;
- rappresentazione tabellare gestita nel notebook.

### Simulazione E91 ideale

Nel protocollo E91 ideale simulato:

1. viene preparata una coppia entangled nello stato `|Φ+⟩`;
2. Alice sceglie casualmente una base di misura;
3. Bob sceglie casualmente una base di misura;
4. Alice misura il qubit 0;
5. Bob misura il qubit 1;
6. si mantiene il round solo se Alice e Bob hanno scelto la stessa base;
7. sui round mantenuti si costruiscono le chiavi sifted;
8. si calcola il QBER.

Nel caso ideale, quando Alice e Bob misurano nella stessa base, i risultati sono correlati. Per questo motivo il QBER ottenuto è nullo.

### Sifting e QBER

Anche in E91 si applica una procedura di sifting: Alice e Bob confrontano pubblicamente le basi usate e mantengono solo i round in cui le basi coincidono.

Dopo il sifting, si confrontano le due chiavi:

- chiave di Alice;
- chiave di Bob.

Il QBER misura la frazione di bit diversi tra le due chiavi sifted.

Nel caso E91 ideale simulato si ottiene:

`QBER = 0.0`

Questo conferma che, in assenza di rumore e attacchi, le misure compatibili su coppie entangled producono risultati coerenti per la generazione della chiave.

### Output prodotti

L’Unità 3 produce due output principali:

- tabella CSV dei round E91 ideali:
  `results/tables/e91_ideal_results.csv`

- grafico dei round mantenuti e scartati:
  `results/figures/e91_ideal_keep_discard.png`

La tabella contiene, per ogni round:

- numero del round;
- base scelta da Alice;
- base scelta da Bob;
- bit misurato da Alice;
- bit misurato da Bob;
- informazione `keep`.

Il grafico mostra il numero di round mantenuti e scartati dopo il confronto delle basi.

### Estensione CHSH

Dopo la simulazione E91 ideale è stata aggiunta una verifica CHSH per mostrare che le correlazioni generate dallo stato entangled non sono spiegabili tramite un modello classico locale.

Il test CHSH considera due possibili impostazioni di misura per Alice:

- `a`;
- `a'`.

e due possibili impostazioni di misura per Bob:

- `b`;
- `b'`.

Per ogni coppia di impostazioni si calcola una correlazione:

- `E(a,b)`;
- `E(a,b')`;
- `E(a',b)`;
- `E(a',b')`.

Queste correlazioni vengono combinate nel parametro:

`S = E(a,b) + E(a,b') + E(a',b) - E(a',b')`

Per una teoria classica locale vale:

`|S| ≤ 2`

La meccanica quantistica, usando uno stato entangled ideale, può invece raggiungere:

`|S| = 2√2 ≈ 2.828`

Nel notebook è stato verificato che il valore ottenuto supera il limite classico `2`, mostrando quindi una violazione della disuguaglianza CHSH.

### Funzioni CHSH implementate

Nel file `e91.py` sono state aggiunte le seguenti funzioni:

- `measure_in_angle(circuit, angle, qubit, cbit)`;
- `run_chsh_counts(angle_a, angle_b, shots=1000, seed=None)`;
- `compute_correlation_from_counts(counts)`;
- `run_chsh_experiment(shots=1000, seed=None)`.

La funzione `measure_in_angle` applica una rotazione `RY(-angle)` prima della misura standard. In questo modo una misura lungo una direzione ruotata viene ricondotta a una misura nella base computazionale.

La funzione `run_chsh_counts` prepara lo stato entangled, misura Alice e Bob secondo due angoli scelti e restituisce i conteggi.

La funzione `compute_correlation_from_counts` associa ai bit i valori:

- `0 → +1`;
- `1 → -1`.

Poi calcola la media dei prodotti tra il risultato di Alice e quello di Bob.

La funzione `run_chsh_experiment` calcola le quattro correlazioni CHSH e restituisce il parametro `S`.

### Interpretazione teorica di CHSH

La verifica CHSH serve a distinguere correlazioni classiche e correlazioni quantistiche.

In una descrizione classica locale si assume che i risultati delle misure siano già predeterminati, anche se non conosciuti. In questo caso si può dimostrare che il parametro CHSH non può superare `2` in valore assoluto.

La meccanica quantistica non richiede invece che osservabili incompatibili abbiano valori simultaneamente definiti prima della misura. Per uno stato entangled, le correlazioni tra le misure di Alice e Bob possono quindi superare il limite classico.

Il risultato `|S| > 2` indica che le correlazioni osservate non sono compatibili con un modello classico locale.

### Collegamento tra E91 e CHSH

Nel progetto, CHSH non viene usato direttamente per calcolare la chiave, ma serve a rafforzare l’interpretazione fisica di E91.

La simulazione E91 ideale mostra che Alice e Bob possono ottenere una chiave condivisa dai risultati correlati delle misure su coppie entangled.

La verifica CHSH mostra invece che tali correlazioni non sono semplicemente classiche, ma derivano dalla natura entangled dello stato quantistico.

Questa distinzione è importante perché E91 è un protocollo entanglement-based: la presenza di correlazioni quantistiche è parte centrale della sua interpretazione.

### Collegamento con il materiale del corso

Questa unità utilizza direttamente concetti fondamentali del corso:

- qubit;
- stati di base `|0⟩` e `|1⟩`;
- sovrapposizione;
- prodotto tensoriale;
- sistemi bipartiti;
- gate unitari;
- gate `H`;
- gate `CX`;
- entanglement;
- stati di Bell;
- misura quantistica;
- basi di misura;
- probabilità di misura;
- correlazioni quantistiche.

La parte specifica su E91, QKD entanglement-based e test CHSH rappresenta un’integrazione applicativa collegata al progetto finale.

### Importanza per la discussione orale

Questa unità è importante per l’esame orale perché permette di distinguere chiaramente BB84 ed E91.

Un punto efficace da sottolineare è:

Nel BB84 la sicurezza è legata al disturbo introdotto da una misura non autorizzata su stati non ortogonali. Nell’E91, invece, il protocollo si basa sulle correlazioni quantistiche di coppie entangled. La verifica CHSH mostra che tali correlazioni superano il limite delle teorie classiche locali.

Quindi E91 consente di collegare la Quantum Key Distribution non solo alla misura quantistica, ma anche all’entanglement e alla non località quantistica.

### Limiti dell’Unità 3

L’Unità 3 considera E91 in condizioni ideali.

Non sono ancora presenti:

- Eve applicata a E91;
- rumore del canale;
- decoerenza;
- amplitude damping;
- attenuazione in fibra;
- confronto quantitativo completo BB84/E91;
- analisi della chiave in presenza di imperfezioni sperimentali.

Inoltre, la verifica CHSH è simulata in un contesto ideale e didattico. In un esperimento reale, la stima delle correlazioni richiederebbe attenzione a perdite, rumore, inefficienze dei rivelatori e scelta casuale delle basi.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- introdurre E91 come protocollo entanglement-based;
- spiegare la differenza rispetto a BB84;
- mostrare la preparazione dello stato di Bell `|Φ+⟩`;
- spiegare il ruolo del gate `H` e del gate `CX`;
- descrivere il sifting in E91;
- mostrare che nel caso ideale il QBER è nullo;
- introdurre le correlazioni quantistiche;
- presentare il test CHSH;
- spiegare il limite classico `|S| ≤ 2`;
- mostrare la violazione CHSH come firma delle correlazioni quantistiche;
- preparare il confronto tra BB84 ed E91.

### Possibili domande orali

1. Qual è la differenza principale tra BB84 ed E91?
2. Che cos’è uno stato entangled?
3. Come si prepara lo stato di Bell `|Φ+⟩` con Qiskit?
4. Qual è il ruolo del gate `H` nella preparazione dello stato di Bell?
5. Qual è il ruolo del gate `CX`?
6. Perché in E91 Alice e Bob possono ottenere bit correlati?
7. Come funziona il sifting in E91?
8. Perché nel caso ideale il QBER è nullo?
9. Che cosa misura il parametro CHSH?
10. Cosa significa violare il limite classico `|S| ≤ 2`?
11. Perché il valore massimo quantistico è `2√2`?
12. Perché CHSH rafforza l’interpretazione fisica di E91?
13. In che senso le correlazioni entangled non sono spiegabili classicamente?
14. Qual è il collegamento tra entanglement, E91 e sicurezza della QKD?

## Unità 4 — Confronto BB84 vs E91

### Obiettivo dell’unità

L’obiettivo dell’Unità 4 è confrontare i protocolli BB84 ed E91 usando metriche comuni e risultati già prodotti nelle unità precedenti.

Dopo avere simulato separatamente BB84 ideale, BB84 con Eve intercept-resend ed E91 ideale con verifica CHSH, questa unità raccoglie i risultati in un notebook unico di confronto.

Il confronto considera sia aspetti quantitativi, come QBER e sifted key rate, sia aspetti qualitativi, come robustezza, sicurezza, costo sperimentale e scalabilità.

### File coinvolti

I file principali coinvolti nell’Unità 4 sono:

- `src/metrics.py`
- `notebooks/04_comparison_and_results.ipynb`
- `results/tables/comparison_summary.csv`
- `results/tables/repeated_experiments.csv`
- `results/tables/repeated_experiments_summary.csv`
- `results/figures/comparison_qber.png`
- `results/figures/comparison_sifted_key_rate.png`
- `results/figures/repeated_qber_mean.png`
- `results/figures/repeated_key_rate_mean.png`

Il file `metrics.py` contiene funzioni comuni per calcolare metriche confrontabili tra protocolli QKD.

Il notebook `04_comparison_and_results.ipynb` raccoglie le simulazioni già sviluppate, calcola le metriche comuni e produce tabelle e grafici di confronto.

### Metriche comuni introdotte

Per confrontare BB84 ed E91 è stato creato il modulo `metrics.py`.

Le metriche principali sono:

- numero totale di round;
- numero di round mantenuti dopo il sifting;
- numero di round scartati;
- lunghezza della chiave sifted;
- sifted key rate;
- QBER;
- soglia QBER;
- accettazione o rifiuto della chiave.

Il sifted key rate è definito come:

`sifted_key_rate = lunghezza chiave sifted / numero round totali`

La decisione di accettazione della chiave è modellata tramite una soglia QBER semplificata:

`qber_threshold = 0.11`

Se il QBER è minore o uguale alla soglia, la chiave viene considerata accettata. Se il QBER supera la soglia, la chiave viene rifiutata.

Questa soglia non sostituisce una procedura completa di information reconciliation e privacy amplification, ma serve come criterio operativo semplificato per confrontare gli scenari simulati.

### Funzioni implementate in `metrics.py`

Il file `metrics.py` contiene le seguenti funzioni:

- `count_kept_rounds(results)`;
- `count_discarded_rounds(results)`;
- `compute_sifted_key_length(alice_key)`;
- `compute_sifted_key_rate(alice_key, n_rounds)`;
- `decide_key_acceptance(qber, qber_threshold=0.11)`;
- `summarize_qkd_results(protocol_name, results, alice_key, bob_key, qber, qber_threshold=0.11)`.

Queste funzioni non usano Qiskit, pandas o matplotlib. Servono solo a calcolare metriche comuni a partire dai risultati delle simulazioni.

### Scenari confrontati

Nel notebook di confronto sono stati considerati tre scenari principali:

1. BB84 ideale;
2. BB84 con Eve intercept-resend sempre attiva;
3. E91 ideale.

Per E91 è stato richiamato anche il risultato del test CHSH, come indicatore della presenza di correlazioni quantistiche non classiche.

### BB84 ideale

Nel caso BB84 ideale, Alice prepara singoli qubit in basi casuali e Bob li misura in basi casuali.

Dopo il sifting vengono mantenuti solo i round in cui Alice e Bob hanno scelto la stessa base.

In assenza di Eve e rumore, i bit mantenuti coincidono e il QBER è nullo.

Questo scenario rappresenta il riferimento ideale del protocollo prepare-and-measure.

### BB84 con Eve intercept-resend

Nel caso BB84 con Eve, l’attaccante intercetta i qubit inviati da Alice, li misura in una base scelta casualmente e reinvia a Bob nuovi qubit coerenti con il risultato ottenuto.

Quando Eve sceglie una base diversa da quella di Alice, la sua misura può disturbare lo stato quantistico. Questo disturbo può produrre errori nella chiave sifted e quindi aumentare il QBER.

Nel confronto, BB84 con Eve mostra un QBER significativamente maggiore rispetto al caso ideale e può superare la soglia di accettazione scelta.

Questo scenario mostra il ruolo del QBER come indicatore operativo della presenza di un attacco o di disturbo nel canale.

### E91 ideale

Nel caso E91 ideale, Alice e Bob misurano qubit appartenenti a coppie entangled nello stato di Bell `|Φ+⟩`.

Quando scelgono basi compatibili, i risultati sono correlati e possono essere usati per costruire una chiave condivisa.

In assenza di rumore e attacchi, il QBER è nullo.

E91 si distingue da BB84 perché la chiave nasce dalle correlazioni di uno stato entangled, non dalla preparazione diretta di singoli qubit da parte di Alice.

### Ruolo di CHSH nel confronto

Il test CHSH non è una metrica di lunghezza della chiave, ma una verifica della natura quantistica delle correlazioni usate in E91.

Nel notebook viene richiamato il parametro `S` di CHSH.

Per una teoria classica locale vale:

`|S| ≤ 2`

Per uno stato entangled ideale la meccanica quantistica può produrre valori vicini a:

`2√2 ≈ 2.828`

Nel confronto, il valore ottenuto risulta maggiore di `2`, mostrando una violazione del limite classico.

Questa violazione rafforza l’interpretazione di E91 come protocollo basato su correlazioni quantistiche non classiche.

### Esperimenti ripetuti su più seed

Per rendere il confronto più robusto, gli scenari principali sono stati ripetuti più volte con seed diversi.

Questo permette di osservare non solo una singola simulazione, ma il comportamento medio delle metriche.

Per ogni esperimento sono stati calcolati:

- QBER;
- sifted key rate;
- lunghezza della chiave sifted;
- accettazione o rifiuto della chiave.

Successivamente sono state calcolate media e deviazione standard per ciascun protocollo.

Questa analisi permette di valutare la stabilità statistica dei risultati.

### Risultati qualitativi del confronto

Dal confronto emergono alcuni punti principali:

- BB84 ideale ed E91 ideale hanno QBER nullo in assenza di rumore e attacchi;
- BB84 con Eve presenta un aumento del QBER;
- il sifted key rate è mediamente vicino a 0.5 quando Alice e Bob scelgono casualmente tra due basi;
- la presenza di Eve può portare al rifiuto della chiave se il QBER supera la soglia scelta;
- E91 richiede una sorgente entangled, quindi è più esigente dal punto di vista sperimentale;
- E91 permette però di collegare la QKD alla verifica di correlazioni quantistiche tramite CHSH.

### Robustezza

Nel confronto attuale, la robustezza è valutata principalmente tramite il QBER.

BB84 è sensibile all’attacco intercept-resend: la misura di Eve può introdurre errori rilevabili.

E91, nel caso ideale, presenta QBER nullo e consente anche di verificare la natura quantistica delle correlazioni tramite CHSH.

Una valutazione più completa della robustezza richiederà l’introduzione di rumore, decoerenza e modelli di canale.

### Sicurezza

Nel caso BB84, la sicurezza operativa è collegata al fatto che un attaccante che misura in una base sbagliata altera lo stato e aumenta il QBER.

Nel caso E91, la sicurezza è collegata alle correlazioni entangled. La violazione CHSH mostra che tali correlazioni non possono essere spiegate da un modello classico locale.

Nel progetto, questa differenza viene usata per distinguere il ruolo del QBER in BB84 e il ruolo delle correlazioni quantistiche in E91.

### Costo computazionale e sperimentale

Dal punto di vista della simulazione, BB84 usa circuiti a un qubit, mentre E91 usa circuiti a due qubit.

Dal punto di vista sperimentale, BB84 è più semplice perché richiede la preparazione e misura di singoli qubit.

E91 è più complesso perché richiede:

- sorgenti entangled;
- distribuzione di coppie entangled;
- misure correlate tra Alice e Bob;
- eventuale verifica CHSH.

Quindi, anche se nella simulazione la differenza computazionale può essere contenuta, dal punto di vista sperimentale E91 è più oneroso.

### Scalabilità

In questa unità la scalabilità è discussa solo in modo preliminare.

Le metriche utili per studiarla sono:

- numero di round;
- lunghezza della chiave sifted;
- sifted key rate;
- QBER medio;
- stabilità delle metriche su più seed;
- tempo di simulazione, eventualmente da aggiungere in una fase successiva.

Una valutazione più significativa della scalabilità richiederà l’introduzione di rumore, perdita o distanza, che saranno oggetto dell’unità successiva.

### Output prodotti

L’Unità 4 produce le seguenti tabelle:

- `results/tables/comparison_summary.csv`;
- `results/tables/repeated_experiments.csv`;
- `results/tables/repeated_experiments_summary.csv`.

Produce inoltre i seguenti grafici:

- `results/figures/comparison_qber.png`;
- `results/figures/comparison_sifted_key_rate.png`;
- `results/figures/repeated_qber_mean.png`;
- `results/figures/repeated_key_rate_mean.png`.

Questi output saranno utili nella relazione finale per mostrare il confronto tra protocolli in forma sintetica.

### Limiti dell’Unità 4

Il confronto resta ancora ideale o semi-ideale.

In particolare, non sono ancora inclusi:

- rumore fisico del canale;
- decoerenza;
- amplitude damping;
- attenuazione in fibra;
- distanza;
- inefficienza dei rivelatori;
- privacy amplification;
- information reconciliation;
- autenticazione del canale classico.

Inoltre, il confronto con Eve è stato applicato esplicitamente solo a BB84. Per E91 è stato invece usato il test CHSH come verifica delle correlazioni quantistiche.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- presentare una tabella comparativa tra BB84 ed E91;
- confrontare QBER e sifted key rate;
- discutere l’effetto dell’attacco intercept-resend su BB84;
- discutere il ruolo di CHSH in E91;
- introdurre una soglia QBER come criterio semplificato di accettazione;
- analizzare la stabilità statistica tramite esperimenti ripetuti;
- discutere costo sperimentale e scalabilità;
- preparare l’introduzione del rumore e della decoerenza.

### Possibili domande orali

1. Quali metriche sono state usate per confrontare BB84 ed E91?
2. Che cos’è il sifted key rate?
3. Perché BB84 ideale ha QBER nullo?
4. Perché BB84 con Eve ha QBER più alto?
5. Cosa rappresenta la soglia QBER?
6. Perché la chiave può essere accettata o rifiutata?
7. Qual è la differenza tra QBER e sifted key rate?
8. Perché E91 è più complesso sperimentalmente di BB84?
9. Che ruolo ha CHSH nel confronto?
10. Perché il confronto attuale non è ancora sufficiente per parlare di scalabilità reale?
11. Perché è utile ripetere gli esperimenti su più seed?
12. Quali aspetti richiedono l’introduzione del rumore?

## Unità 5 — Rumore, decoerenza e scalabilità

### Obiettivo dell’unità

L’obiettivo dell’Unità 5 è introdurre modelli di rumore e dissipazione nel protocollo BB84, passando progressivamente da modelli didattici semplici a una versione più vicina all’articolo fornito dal docente.

Nelle unità precedenti il progetto ha considerato:

- BB84 ideale;
- BB84 con attacco intercept-resend;
- E91 ideale;
- verifica CHSH;
- confronto BB84/E91 tramite metriche comuni.

In questa unità il canale quantistico non viene più trattato come ideale, ma come soggetto a rumore, decoerenza e dissipazione. L’obiettivo è studiare come tali effetti aumentino il QBER e possano portare al rifiuto della chiave.

La struttura dell’unità è progressiva:

1. rumore bit-flip;
2. amplitude damping tramite Qiskit Aer NoiseModel;
3. confronto bit-flip/amplitude damping;
4. modello Jaynes-Cummings semplificato ispirato all’articolo;
5. QBER in funzione della distanza;
6. analisi dell’effetto del parametro R.

### File coinvolti

I file principali coinvolti sono:

- `src/noise.py`;
- `notebooks/05_noise_decoherence_optional.ipynb`;
- `results/tables/bb84_bit_flip_noise_sweep.csv`;
- `results/tables/bb84_amplitude_damping_sweep.csv`;
- `results/tables/bb84_noise_model_comparison.csv`;
- `results/tables/bb84_jc_damping_probability_vs_distance.csv`;
- `results/tables/bb84_jc_qber_vs_distance_R_0_1.csv`;
- `results/tables/bb84_jc_qber_vs_distance_multi_R.csv`;
- `results/tables/bb84_jc_acceptance_table.csv`;
- `results/figures/` con i grafici associati a QBER, key rate, damping probability e confronto multi-R.

Il modulo `noise.py` contiene le funzioni per simulare rumore bit-flip, amplitude damping standard e amplitude damping ispirato al modello Jaynes-Cummings.

Il notebook `05_noise_decoherence_optional.ipynb` raccoglie gli esperimenti, costruisce tabelle e grafici e salva i risultati finali.

### Rumore bit-flip

Il primo modello introdotto è il rumore bit-flip.

Nel modello bit-flip, il canale applica un gate `X` al qubit trasmesso con probabilità `noise_probability`.

Il gate `X` agisce come inversione nella base computazionale:

- `|0⟩` diventa `|1⟩`;
- `|1⟩` diventa `|0⟩`.

Nel protocollo BB84, però, Alice può preparare anche stati nella base diagonale `X`, cioè `|+⟩` e `|-⟩`. In quella base l’effetto del gate `X` non produce lo stesso tipo di errore osservabile:

- `X|+⟩ = |+⟩`;
- `X|-⟩ = -|-⟩`.

Il segno globale non modifica le probabilità di misura. Per questo il QBER osservato può essere inferiore alla probabilità nominale di rumore.

Questa osservazione è importante perché mostra che la probabilità con cui un errore viene applicato al canale non coincide necessariamente con il QBER finale.

### Funzioni bit-flip implementate

In `src/noise.py` sono state implementate le seguenti funzioni:

- `check_probability(probability)`;
- `apply_bit_flip_noise(circuit, qubit, noise_probability, seed=None)`;
- `run_bb84_round_with_bit_flip_noise(alice_bit, alice_basis, bob_basis, noise_probability=0.0, seed=None)`;
- `run_bb84_protocol_with_bit_flip_noise(n_rounds, noise_probability=0.0, seed=None)`.

La funzione `apply_bit_flip_noise` applica il gate `X` con probabilità `noise_probability` e restituisce anche una variabile booleana `noise_applied`, che indica se il bit-flip è stato effettivamente applicato in quello specifico round.

### Risultati bit-flip

Nel notebook 05 è stato studiato il QBER al variare di `noise_probability`.

I risultati mostrano che:

- aumentando la probabilità di rumore, il QBER tende ad aumentare;
- il QBER non coincide esattamente con la probabilità di rumore;
- il sifted key rate resta legato soprattutto alla probabilità che Alice e Bob scelgano la stessa base;
- la soglia QBER permette di decidere se la chiave deve essere accettata o rifiutata.

Il bit-flip è stato usato come primo modello didattico, utile per evidenziare il legame tra rumore del canale e aumento degli errori nella chiave sifted.

### Amplitude damping standard

Il secondo modello introdotto è l’amplitude damping.

L’amplitude damping è un canale quantistico dissipativo che descrive il decadimento dallo stato eccitato allo stato fondamentale:

`|1⟩ → |0⟩`

con una certa probabilità.

A differenza del bit-flip, l’amplitude damping è un rumore asimmetrico:

- `|0⟩` è stabile;
- `|1⟩` può decadere verso `|0⟩`.

Nel progetto questo modello è stato implementato usando `NoiseModel` e `amplitude_damping_error` di Qiskit Aer.

La scelta è coerente con l’idea fisica dell’articolo fornito dal docente, nel quale l’amplitude damping viene usato per descrivere dissipazione, scattering e attenuazione durante la trasmissione.

### Funzioni amplitude damping implementate

In `src/noise.py` sono state aggiunte le seguenti funzioni:

- `build_amplitude_damping_noise_model(damping_probability)`;
- `run_bb84_round_with_amplitude_damping(alice_bit, alice_basis, bob_basis, damping_probability=0.0, seed=None)`;
- `run_bb84_protocol_with_amplitude_damping(n_rounds, damping_probability=0.0, seed=None)`.

Nel circuito il canale rumoroso è rappresentato tramite un’istruzione `id`, alla quale il noise model associa l’errore di amplitude damping.

Il flusso del singolo round diventa:

Alice prepara il qubit → passaggio nel canale `id` rumoroso → Bob misura.

### Confronto bit-flip e amplitude damping

Nel notebook 05 è stato confrontato il comportamento dei due modelli di rumore:

- bit-flip;
- amplitude damping.

Il bit-flip applica una inversione discreta tramite il gate `X`.

L’amplitude damping rappresenta invece una perdita di eccitazione da `|1⟩` verso `|0⟩`.

Entrambi possono aumentare il QBER, ma con meccanismi differenti.

Il confronto mostra che modelli di rumore diversi possono produrre curve QBER differenti, anche a parità di probabilità nominale. Questo è importante perché il rumore quantistico non può essere ridotto a un unico parametro astratto senza considerare il tipo di canale fisico modellato.

### Collegamento con l’articolo del docente

L’articolo di riferimento è *Dissipative dynamics in quantum key distribution*.

L’articolo studia la dinamica dissipativa nel protocollo BB84, simulando l’attenuazione in fibra ottica tramite il modello Jaynes-Cummings e calcolando il QBER in funzione della distanza. L’obiettivo è mostrare come l’interazione sistema-ambiente influenzi la trasmissione dell’informazione quantistica.

Nel paper, il sistema aperto è costituito dal qubit trasmesso, mentre l’ambiente rappresenta i modi esterni con cui il qubit interagisce durante la propagazione. L’articolo collega il canale di amplitude damping al modello Jaynes-Cummings, mostrando che la dissipazione può essere descritta tramite la sopravvivenza della componente eccitata.

Nel nostro progetto l’articolo è stato usato come base teorica per costruire un modello semplificato:

distanza → tempo di propagazione → ampiezza `C1(t)` → damping probability → simulazione BB84 → QBER.

### Sistemi quantistici aperti

Un sistema quantistico aperto è un sistema che interagisce con un ambiente esterno.

Nel nostro caso:

- il sistema è il qubit/fotone trasmesso da Alice a Bob;
- l’ambiente rappresenta il canale fisico, la fibra, scattering, dissipazione e modi esterni.

Nei sistemi chiusi l’evoluzione è unitaria. Nei sistemi aperti, invece, osservando solo il sistema principale, l’evoluzione può diventare non unitaria perché parte dell’informazione o dell’energia viene trasferita all’ambiente.

Questa distinzione è centrale per comprendere perché il rumore del canale possa alterare la chiave BB84.

### Modello Jaynes-Cummings semplificato

Il modello Jaynes-Cummings descrive un sistema a due livelli accoppiato a un ambiente bosonico. Nell’articolo viene usato per modellare la trasmissione quantistica in fibra ottica.

Nel nostro progetto non è stata implementata la master equation completa, ma una versione semplificata basata sull’ampiezza `C1(t)`.

`C1(t)` rappresenta l’ampiezza di probabilità che il sistema resti nello stato eccitato `|1⟩` dopo un tempo `t`.

Da `C1(t)` si ricava la probabilità effettiva di damping:

`damping_probability = 1 - |C1(t)|²`

Il significato fisico è:

- se `|C1(t)|²` è vicino a 1, lo stato eccitato sopravvive;
- se `|C1(t)|²` diminuisce, aumenta la probabilità di decadimento;
- maggiore damping può produrre maggiore QBER.

### Catena distanza → damping → QBER

Per collegare il modello alla distanza, è stata usata la catena:

1. scelta della distanza `d` in km;
2. conversione in tempo di propagazione `t = d / v`;
3. calcolo del parametro `lambda` dalla attenuazione della fibra;
4. calcolo dell’ampiezza `C1(t)`;
5. calcolo della damping probability;
6. esecuzione di BB84 con amplitude damping;
7. calcolo del QBER.

I parametri principali sono:

- `distance_km`: distanza Alice-Bob;
- `fiber_speed_km_s`: velocità della luce nella fibra;
- `attenuation_db_per_km`: attenuazione della fibra;
- `coupling_ratio`: parametro `R = Γ0 / λ`.

Nel notebook sono stati usati valori coerenti con il modello semplificato e con l’articolo, tra cui:

- `fiber_speed_km_s = 203390`;
- `attenuation_db_per_km = 0.21`;
- valori di `R` come `0.1`, `0.3`, `0.49`.

### Funzioni Jaynes-Cummings implementate

In `src/noise.py` sono state aggiunte le seguenti funzioni:

- `compute_lambda_from_attenuation(attenuation_db_per_km, fiber_speed_km_s=203390)`;
- `compute_time_from_distance(distance_km, fiber_speed_km_s=203390)`;
- `compute_c1_amplitude(time_s, lambda_parameter, coupling_ratio)`;
- `compute_jc_damping_probability(time_s, lambda_parameter, coupling_ratio)`;
- `compute_jc_damping_probability_from_distance(distance_km, attenuation_db_per_km=0.21, coupling_ratio=0.1, fiber_speed_km_s=203390)`;
- `run_bb84_protocol_with_jc_amplitude_damping(n_rounds, distance_km, attenuation_db_per_km=0.21, coupling_ratio=0.1, fiber_speed_km_s=203390, seed=None)`.

Queste funzioni non sostituiscono il modello standard Qiskit Aer, ma aggiungono un livello più vicino all’articolo del docente.

### QBER in funzione della distanza

Nel notebook è stato calcolato il QBER di BB84 in funzione della distanza usando il modello Jaynes-Cummings semplificato.

Per ogni distanza:

- si calcola la damping probability;
- si esegue il protocollo BB84;
- si effettua il sifting;
- si calcola il QBER;
- si confronta il QBER con la soglia di accettazione.

Il risultato atteso è che, all’aumentare della distanza, la qualità del canale peggiora e il QBER tende ad aumentare, pur con fluttuazioni statistiche dovute al numero finito di round.

Il sifted key rate resta invece legato soprattutto alla scelta casuale delle basi e quindi non rappresenta, da solo, la qualità fisica del canale.

### Effetto del parametro R

Il parametro `R` controlla la forza relativa dell’accoppiamento sistema-ambiente.

Nel notebook sono stati confrontati diversi valori:

- `R = 0.1`;
- `R = 0.3`;
- `R = 0.49`.

Valori piccoli di `R` producono una crescita più moderata della dissipazione e del QBER.

Valori più grandi producono una dinamica più intensa e possono avvicinare il modello al regime non markoviano.

Nel paper, aumentando `R`, il QBER evolve verso un comportamento non markoviano, con oscillazioni a brevi distanze; a distanze grandi, invece, il QBER tende a saturare verso un valore comune. Nel nostro progetto questa parte è trattata in modo semplificato e didattico.

### Markoviano e non markoviano

Nel regime markoviano, l’ambiente non restituisce informazione al sistema. La perdita è sostanzialmente irreversibile e il QBER tende a crescere in modo regolare con la distanza.

Nel regime non markoviano, l’ambiente conserva memoria e può esserci uno scambio di informazione o energia tra sistema e ambiente. Questo può produrre oscillazioni del QBER, soprattutto a brevi distanze.

L’articolo mostra che i dati sperimentali considerati sono compatibili con una dinamica markoviana, ma studia anche il passaggio verso il regime non markoviano variando il parametro `R`.

Nel nostro progetto il regime non markoviano non viene riprodotto integralmente, ma viene discusso come estensione del modello e come interpretazione del ruolo del parametro `R`.

### Output prodotti

L’Unità 5 produce tabelle come:

- `results/tables/bb84_bit_flip_noise_sweep.csv`;
- `results/tables/bb84_amplitude_damping_sweep.csv`;
- `results/tables/bb84_noise_model_comparison.csv`;
- `results/tables/bb84_jc_damping_probability_vs_distance.csv`;
- `results/tables/bb84_jc_qber_vs_distance_R_0_1.csv`;
- `results/tables/bb84_jc_qber_vs_distance_multi_R.csv`;
- `results/tables/bb84_jc_acceptance_table.csv`.

Produce inoltre grafici relativi a:

- QBER vs probabilità di bit-flip;
- sifted key rate vs probabilità di bit-flip;
- QBER vs amplitude damping;
- confronto QBER bit-flip/amplitude damping;
- damping probability vs distanza;
- QBER vs distanza;
- sifted key rate vs distanza;
- QBER vs distanza per diversi valori di `R`.

Questi output possono essere usati nella relazione finale per mostrare l’effetto progressivo del rumore sulla qualità della chiave.

### Limiti del modello

Il modello implementato resta semplificato.

Non sono stati inclusi:

- perdita esplicita di fotoni;
- dark counts;
- efficienza dei detector;
- apparato sperimentale completo;
- riconciliazione dell’informazione;
- privacy amplification;
- autenticazione del canale classico;
- best fit su dati sperimentali;
- master equation completa;
- riproduzione esatta delle figure dell’articolo.

Il progetto non pretende quindi di riprodurre integralmente l’articolo. L’obiettivo è usare l’articolo come riferimento teorico per costruire una simulazione didattica coerente, che colleghi dissipazione, distanza e QBER.

### Risultato concettuale dell’unità

L’Unità 5 mostra che il QBER può aumentare per cause diverse:

1. intercettazione da parte di Eve;
2. rumore bit-flip;
3. amplitude damping;
4. dissipazione dipendente dalla distanza secondo un modello Jaynes-Cummings semplificato.

Questa distinzione è centrale per il progetto, perché permette di separare gli errori causati da un attaccante dagli errori causati dal canale fisico.

Nel caso reale, un QBER elevato non prova automaticamente la presenza di Eve: può anche derivare da rumore, decoerenza o imperfezioni sperimentali. Per questo il protocollo deve stimare il QBER e decidere se accettare o rifiutare la chiave.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- introdurre la differenza tra protocollo ideale e canale fisico rumoroso;
- spiegare il ruolo del QBER come metrica di qualità della chiave;
- confrontare rumore bit-flip e amplitude damping;
- collegare amplitude damping a dissipazione e decoerenza;
- mostrare un collegamento con l’articolo del docente;
- discutere il modello Jaynes-Cummings in forma semplificata;
- analizzare QBER in funzione della distanza;
- discutere il ruolo del parametro `R`;
- evidenziare i limiti della simulazione;
- preparare una sezione sulle prospettive future.

### Possibili domande orali

1. Perché hai introdotto il rumore dopo BB84 ideale e BB84 con Eve?
2. Che differenza c’è tra bit-flip e amplitude damping?
3. Perché il QBER non coincide necessariamente con la probabilità di rumore?
4. Che cosa rappresenta l’amplitude damping?
5. Perché l’amplitude damping è un modello asimmetrico?
6. Come hai implementato l’amplitude damping in Qiskit?
7. Perché hai usato l’istruzione `id` nel circuito?
8. Che ruolo ha l’articolo del docente nel progetto?
9. Che cos’è un sistema quantistico aperto?
10. Che cosa rappresenta il modello Jaynes-Cummings?
11. Che cosa rappresenta `C1(t)`?
12. Come ricavi la damping probability da `C1(t)`?
13. Come colleghi la distanza al QBER?
14. Che cosa rappresenta il parametro `R`?
15. Qual è la differenza tra regime markoviano e non markoviano?
16. Perché il modello implementato è una semplificazione dell’articolo?
17. Quali elementi fisici non hai incluso nella simulazione?
18. Perché un QBER alto non implica necessariamente la presenza di Eve?
19. Quale metrica useresti per decidere se accettare o rifiutare una chiave?
20. Come estenderesti il progetto in futuro?

## Unità 6 — E91 con attacco intercept-resend e controllo CHSH

### Obiettivo dell’unità

L’obiettivo dell’Unità 6 è estendere lo studio dell’intercettazione anche al protocollo E91.

Nelle unità precedenti l’attacco intercept-resend era stato implementato sul protocollo BB84. In quel caso Eve intercetta il qubit preparato da Alice, lo misura in una base scelta casualmente e reinvia a Bob un nuovo qubit coerente con il risultato ottenuto.

Nel protocollo E91 la situazione è diversa: Alice e Bob non usano qubit preparati direttamente da Alice, ma condividono coppie entangled. Eve, quindi, intercetta il qubit entangled destinato a Bob. Misurando quel qubit, Eve rompe l’entanglement originario tra Alice e Bob e reinvia a Bob un nuovo qubit preparato in base al risultato della propria misura.

Questa unità permette quindi di osservare l’effetto dell’intercettazione su E91 tramite due metriche:

- QBER;
- parametro CHSH `S`.

Questa è una differenza importante rispetto a BB84: in BB84 il disturbo viene rilevato principalmente tramite QBER, mentre in E91 è possibile osservare anche la degradazione delle correlazioni quantistiche tramite CHSH.

### File coinvolti

I file principali coinvolti sono:

- `src/e91.py`;
- `notebooks/06_e91_intercept_resend_qber.ipynb`;
- `notebooks/04_comparison_and_results.ipynb`;
- `results/tables/e91_eve_qber_vs_interception.csv`;
- `results/tables/e91_eve_chsh_vs_interception.csv`;
- `results/tables/e91_eve_qber_chsh_comparison.csv`;
- `results/figures/e91_eve_qber_vs_interception.png`;
- `results/figures/e91_eve_chsh_vs_interception.png`;
- `results/figures/e91_eve_qber_for_chsh_comparison.png`.

Il file `src/e91.py` contiene le funzioni per E91 ideale, E91 con Eve, CHSH ideale e CHSH con Eve.

Il notebook `06_e91_intercept_resend_qber.ipynb` raccoglie la simulazione specifica dell’attacco su E91.

Il notebook `04_comparison_and_results.ipynb` è stato aggiornato per includere nel confronto finale anche E91 con Eve e CHSH con Eve.

### Differenza tra intercept-resend in BB84 e in E91

Nel protocollo BB84, Alice prepara direttamente un qubit in una certa base e lo invia a Bob. Eve intercetta questo qubit, lo misura in una base casuale e poi reinvia a Bob un qubit preparato da lei.

Nel protocollo E91, invece, Alice e Bob ricevono due qubit appartenenti a una coppia entangled. Eve intercetta il qubit destinato a Bob. Misurando quel qubit, Eve non si limita a leggere uno stato già preparato da Alice, ma altera la coppia entangled nel suo complesso.

La differenza concettuale è quindi:

- in BB84 Eve disturba uno stato preparato da Alice;
- in E91 Eve rompe le correlazioni entangled tra Alice e Bob.

Questa distinzione è centrale nella relazione, perché mostra che E91 offre una diagnostica più ricca: non solo il QBER può aumentare, ma anche la violazione CHSH può degradarsi o sparire.

### Funzioni E91 con Eve implementate

In `src/e91.py` sono state aggiunte funzioni per simulare l’attacco intercept-resend su E91:

- `choose_eve_basis(seed=None)`;
- `prepare_single_qubit_from_bit_basis(circuit, bit, basis, qubit=0)`;
- `run_e91_round_with_eve(alice_basis, bob_basis, intercept_probability=1.0, seed=None)`;
- `run_e91_protocol_with_eve(n_rounds, intercept_probability=1.0, seed=None)`.

La funzione `choose_eve_basis` sceglie casualmente la base di Eve tra `Z` e `X`.

La funzione `prepare_single_qubit_from_bit_basis` permette a Eve di ricostruire un qubit coerente con il bit e la base ottenuti dalla propria misura.

La funzione `run_e91_round_with_eve` simula un singolo round E91 con eventuale intercettazione.

La funzione `run_e91_protocol_with_eve` ripete il round per più iterazioni, salvando per ogni round:

- round;
- base di Alice;
- base di Bob;
- bit di Alice;
- bit di Bob;
- informazione sul fatto che Eve abbia intercettato;
- base scelta da Eve;
- bit ottenuto da Eve;
- indicatore `keep`, cioè se Alice e Bob hanno scelto la stessa base.

La struttura dei dizionari è stata mantenuta coerente con quella già usata nel protocollo BB84 con Eve.

### E91 senza Eve

Nel caso ideale senza Eve, la sorgente prepara coppie entangled nello stato di Bell `|Φ+⟩`.

Quando Alice e Bob scelgono la stessa base, i risultati sono correlati e possono essere usati per costruire una chiave condivisa.

In assenza di rumore e attacchi, il QBER atteso è nullo.

Questo scenario rappresenta il riferimento ideale per valutare l’effetto dell’intercettazione.

### E91 con Eve intercept-resend

Nel caso con Eve, l’attaccante intercetta il qubit destinato a Bob.

La sequenza concettuale è:

1. la sorgente prepara una coppia entangled;
2. Alice riceve il proprio qubit;
3. Eve intercetta il qubit destinato a Bob;
4. Eve misura il qubit in base `Z` o `X`;
5. la misura di Eve rompe l’entanglement originario;
6. Eve prepara un nuovo qubit coerente con il risultato ottenuto;
7. Bob misura il qubit ricevuto da Eve;
8. Alice e Bob eseguono il sifting;
9. viene calcolato il QBER.

L’effetto atteso è un aumento del QBER rispetto al caso ideale, perché Bob non misura più il qubit originariamente entangled con quello di Alice.

### QBER al variare della probabilità di intercettazione

Nel notebook `06_e91_intercept_resend_qber.ipynb` è stata studiata la variazione del QBER in funzione della probabilità di intercettazione di Eve.

Sono stati considerati valori del tipo:

- `intercept_probability = 0.0`;
- `intercept_probability = 0.25`;
- `intercept_probability = 0.5`;
- `intercept_probability = 0.75`;
- `intercept_probability = 1.0`.

Il risultato qualitativo atteso è:

- per `intercept_probability = 0.0`, il QBER è nullo o molto vicino a zero;
- aumentando la probabilità di intercettazione, il QBER tende ad aumentare;
- per Eve sempre attiva, il QBER risulta sensibilmente maggiore rispetto al caso ideale.

Questa analisi è analoga a quella già fatta per BB84, ma nel caso E91 il significato fisico è diverso: l’aumento del QBER deriva dalla rottura delle correlazioni entangled.

### Controllo CHSH in presenza di Eve

Poiché E91 si basa sull’entanglement, il QBER non è l’unica metrica significativa. Alice e Bob possono anche controllare se le loro correlazioni violano la disuguaglianza CHSH.

Nel caso ideale, il parametro CHSH soddisfa:

`|S| > 2`

e si avvicina al valore quantistico ideale:

`2√2 ≈ 2.828`

Nel caso con Eve, l’attacco intercept-resend tende a ridurre `|S|`, perché Eve misura il qubit destinato a Bob e rompe l’entanglement.

Quindi l’effetto atteso è:

- E91 ideale: `QBER ≈ 0` e `|S| > 2`;
- E91 con Eve: `QBER` aumenta e `|S|` diminuisce.

Questa doppia osservazione rende E91 più ricco dal punto di vista diagnostico rispetto a BB84.

### Funzioni CHSH con Eve implementate

In `src/e91.py` sono state aggiunte funzioni per stimare CHSH in presenza di Eve:

- `run_chsh_counts_with_eve(angle_a, angle_b, intercept_probability=1.0, shots=1000, seed=None)`;
- `run_chsh_experiment_with_eve(intercept_probability=1.0, shots=1000, seed=None)`.

La funzione `run_chsh_counts_with_eve` esegue misure CHSH in presenza di Eve per una coppia di angoli.

La funzione `run_chsh_experiment_with_eve` ripete il calcolo per le quattro coppie di angoli usate nella disuguaglianza CHSH e restituisce:

- correlazioni `E_ab`, `E_ab_prime`, `E_a_prime_b`, `E_a_prime_b_prime`;
- parametro `S`;
- valore assoluto `abs_S`;
- limite classico;
- limite quantistico;
- booleano `violates_chsh`;
- probabilità di intercettazione;
- numero di shots.

La logica è coerente con la funzione CHSH ideale già implementata.

### Risultati CHSH con Eve

Nel test eseguito, al variare di `intercept_probability`, il parametro `|S|` ha mostrato un andamento decrescente.

Un esempio di risultati ottenuti è:

- `intercept_probability = 0.0`, `|S| ≈ 2.916`, violazione CHSH presente;
- `intercept_probability = 0.25`, `|S| ≈ 2.552`, violazione CHSH presente;
- `intercept_probability = 0.5`, `|S| ≈ 2.104`, violazione CHSH ancora formalmente presente ma debole;
- `intercept_probability = 0.75`, `|S| ≈ 1.814`, violazione CHSH assente;
- `intercept_probability = 1.0`, `|S| ≈ 1.412`, violazione CHSH assente.

Questi risultati mostrano che l’intercettazione degrada progressivamente le correlazioni quantistiche.

Il valore a `intercept_probability = 0.0` può risultare leggermente superiore a `2√2` a causa delle fluttuazioni statistiche dovute al numero finito di shots. Questo non rappresenta una violazione fisica del limite quantistico, ma una stima campionaria.

### Soglie QBER e interpretazione CHSH

Nel progetto viene usata la soglia didattica:

`qber_threshold = 0.11`

Questa soglia viene applicata in modo uniforme agli scenari BB84 ed E91 come criterio semplificato di accettazione o rifiuto della chiave. Il valore è collegato alla stima asintotica didattica:

`r ≈ 1 - 2 h₂(Q)`

dove `h₂(Q)` è l'entropia binaria e `Q` è il QBER. Non si tratta di una soglia universale valida per ogni implementazione reale, ma di un riferimento utile per confrontare gli scenari simulati.

Per CHSH, invece, i riferimenti teorici usati nel progetto sono:

- limite classico: `|S| ≤ 2`;
- limite quantistico ideale di Tsirelson: `2√2`.

Non viene adottata una soglia CHSH universale aggiuntiva. Il progetto usa invece due metriche quantitative:

- `chsh_gap = |S| - 2`;
- `chsh_strength`, cioè la posizione normalizzata di `|S|` tra il limite classico `2` e il limite quantistico ideale `2√2`.

Una violazione CHSH debole non dimostra automaticamente l'assenza di Eve. Indica solo che le correlazioni restano formalmente non classiche, ma devono essere interpretate insieme al QBER e al contesto della simulazione.

Da citare in relazione: Shor-Preskill per BB84; CHSH/Tsirelson per i limiti CHSH.

### Violazione CHSH formale

Nel codice, il booleano `violates_chsh` indica se:

`|S| > 2`

Questa condizione significa che le correlazioni osservate violano il limite classico locale.

Tuttavia, una violazione appena sopra 2 non deve essere interpretata automaticamente come garanzia di sicurezza operativa.

Ad esempio, un valore `|S| = 2.104` viola formalmente la disuguaglianza CHSH, ma è molto vicino al limite classico. Nel progetto questo caso viene interpretato guardando anche `chsh_gap` e `chsh_strength`.

Questa distinzione è importante per la relazione:

- `violates_chsh = True` non significa necessariamente “Eve è assente”;
- significa solo che le correlazioni sono ancora non classiche;
- per decidere se accettare la chiave bisogna considerare anche QBER e valore quantitativo di `|S|`.

### Decisione operativa semplificata

Nel notebook è stata introdotta una decisione finale semplificata.

Per BB84, la decisione è basata principalmente sul QBER:

`accepted_final = QBER <= qber_threshold`

Per E91, invece, la decisione usa sia QBER sia CHSH:

`accepted_final = accepted_by_qber and violates_chsh`

dove:

- `accepted_by_qber` è vero se `QBER <= qber_threshold`;
- `violates_chsh` è vero se `|S| > 2`.

Questa decisione non sostituisce una procedura completa di sicurezza, ma serve come criterio operativo didattico per confrontare i protocolli.

### Confronto aggiornato nel notebook 04

Il notebook `04_comparison_and_results.ipynb` è stato aggiornato per includere:

- BB84 ideale;
- BB84 con Eve;
- E91 ideale;
- E91 con Eve;
- CHSH ideale;
- CHSH con Eve.

La tabella comparativa finale include metriche come:

- protocollo;
- scenario;
- numero di round;
- lunghezza della chiave sifted;
- sifted key rate;
- QBER;
- soglia QBER;
- accettazione tramite QBER;
- `abs_S`;
- violazione CHSH;
- `chsh_gap`;
- `chsh_strength`;
- limiti teorici CHSH;
- decisione finale.

Per BB84 le colonne relative a CHSH non si applicano.

Per E91, invece, CHSH è parte essenziale della valutazione.

### Differenza finale tra BB84 ed E91 in presenza di Eve

Il confronto aggiornato mette in evidenza una distinzione importante:

- BB84 rileva l’intercettazione principalmente tramite l’aumento del QBER;
- E91 rileva l’intercettazione sia tramite l’aumento del QBER sia tramite la riduzione del parametro CHSH.

In BB84, Eve introduce errori perché può misurare nella base sbagliata e disturbare lo stato preparato da Alice.

In E91, Eve introduce disturbo perché misura il qubit destinato a Bob e rompe l’entanglement con il qubit di Alice.

Quindi E91 è più complesso da realizzare sperimentalmente, ma offre un controllo più ricco sulle correlazioni quantistiche.

### Robustezza

Dal punto di vista della robustezza, E91 offre una doppia diagnostica:

- QBER;
- CHSH.

Un attacco parziale può lasciare ancora una violazione CHSH formale, ma ridotta. Per questo non basta controllare se `|S| > 2`; è utile considerare anche quanto `|S|` sia distante dal limite classico.

Il progetto introduce quindi un criterio operativo più prudente basato su una soglia CHSH maggiore di 2.

### Complessità e costo

L’estensione conferma anche una differenza di costo tra BB84 ed E91.

BB84 usa circuiti a un qubit per round, con preparazione diretta dello stato da parte di Alice e misura da parte di Bob.

E91 usa circuiti a due qubit entangled e richiede:

- sorgente entangled;
- distribuzione di coppie entangled;
- misure correlate;
- controllo CHSH;
- maggiore complessità sperimentale.

Dal punto di vista computazionale, E91 richiede più circuiti e più misure, soprattutto quando viene aggiunto il controllo CHSH.

Dal punto di vista sperimentale, E91 è più oneroso, ma consente una verifica più profonda della natura quantistica delle correlazioni.

### Output prodotti

L’Unità 6 produce tabelle come:

- `results/tables/e91_eve_qber_vs_interception.csv`;
- `results/tables/e91_eve_chsh_vs_interception.csv`;
- `results/tables/e91_eve_qber_chsh_comparison.csv`.

Produce inoltre grafici come:

- `results/figures/e91_eve_qber_vs_interception.png`;
- `results/figures/e91_eve_chsh_vs_interception.png`;
- `results/figures/e91_eve_qber_for_chsh_comparison.png`.

Il notebook di confronto finale aggiorna anche:

- `results/tables/comparison_summary.csv`;
- `results/figures/comparison_qber.png`;
- `results/figures/comparison_chsh_e91.png`.

### Limiti dell’unità

L’unità resta comunque semplificata.

Non sono stati inclusi:

- rumore fisico su E91;
- amplitude damping su E91;
- perdita di fotoni;
- dark counts;
- efficienza dei detector;
- riconciliazione dell’informazione;
- privacy amplification;
- autenticazione del canale classico;
- analisi statistica rigorosa della significatività della violazione CHSH;
- stima quantitativa dell’informazione posseduta da Eve.

Inoltre, il progetto non adotta una soglia CHSH universale aggiuntiva. La violazione viene interpretata tramite `violates_chsh`, `chsh_gap` e `chsh_strength`.

### Risultato concettuale dell’unità

L’Unità 6 completa il confronto tra BB84 ed E91 in presenza di Eve.

Il risultato concettuale principale è:

- BB84 consente di rilevare l’intercettazione tramite QBER;
- E91 consente di rilevare l’intercettazione tramite QBER e tramite degradazione della violazione CHSH.

Questa unità rende il progetto più coerente con l’obiettivo iniziale di confrontare BB84 ed E91 dal punto di vista della sicurezza, della robustezza, della scalabilità e del costo sperimentale.

### Elementi da usare nella relazione finale

Questa unità può essere usata nella relazione per:

- spiegare come cambia intercept-resend passando da BB84 a E91;
- mostrare che Eve rompe l’entanglement in E91;
- analizzare il QBER al variare della probabilità di intercettazione;
- mostrare la degradazione del parametro CHSH;
- distinguere violazione CHSH formale e accettazione operativa;
- confrontare BB84 ed E91 in presenza di Eve;
- discutere robustezza, costo e complessità dei due protocolli;
- preparare la conclusione del progetto.

### Possibili domande orali

1. Come cambia l’attacco intercept-resend tra BB84 ed E91?
2. Perché in E91 Eve rompe l’entanglement?
3. Perché il QBER aumenta in E91 con Eve?
4. Perché E91 permette un controllo tramite CHSH?
5. Che cosa rappresenta il parametro `S`?
6. Perché `|S| > 2` indica violazione del limite classico?
7. Perché `violates_chsh = True` non significa automaticamente che Eve sia assente?
8. Che differenza c’è tra violazione CHSH formale e forza quantitativa della violazione?
9. Che cosa rappresentano `chsh_gap` e `chsh_strength`?
10. Come si comporta `|S|` al crescere della probabilità di intercettazione?
11. Perché E91 è più costoso sperimentalmente di BB84?
12. In che senso E91 offre una diagnostica più ricca?
13. Quali limiti ha la simulazione di Eve su E91?
14. Come estenderesti il modello a rumore fisico su E91?
15. Perché QBER e CHSH devono essere valutati insieme?
