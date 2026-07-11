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