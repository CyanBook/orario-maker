# :date: Orario maker
Progetto scolastico creato per divertimento, per creare orari per spazi di lavoro con un'alteranza di giorni in ufficio e a casa, con un limite massimo dei desk disponibili.


## Funzionamento
*Questo programma è stato scritto e testato con Python 3.9.5 su Ubuntu 20.04*

**N.B** Tutti gli esempi e funzionamenti avranno questi valori come esempio:
- 5 giorni totali, di cui 3 in ufficio e 2 a casa
- 3 desk disponibili, a rotazione (nessuno ha il proprio)

### Generazione del primo utente
L'algoritmo parte generando tutte le possibili combinazioni del primo utente, pari a `2^(giorni totali)`.

Ogni numero, da 0 al numero totale di combinazioni meno 1, segue un albero binario perfetto (come in foto) il cui primo nodo è pari al numero di tutte le combinazioni possibili (P<sub>0:31</sub>).
Ogni ramo rappresenta un giorno diverso. Ad ogni nodo si confronta il numero rispetto alla media del range di valori del nodo meno 1.

Se più piccolo o uguale, il valore di quel giorno è 1 (in ufficio) e si prosegue al nodo "di sinistra", mentre si fa l'opposto in caso contrario.

![Albero binario](https://www.researchgate.net/profile/Guillermo-Durand/publication/326198373/figure/fig3/AS:644873308868608@1530761186566/Partition-and-perfect-binary-tree-structures-used-in-simulations-here-with-q-3-and-K-1.png)


**Esempi**

Combinazione del numero 6 (P<sub>0:31</sub>).
```
6 ≤ 15 -> 1 (0, 16)
6 ≤ 7  -> 1 (0, 8)
6 > 4  -> 0 (4, 8)
6 > 5  -> 0 (6, 8)
6 ≤ 6  -> 1 (6, 6)

6 -> [1,1,0,0,1]  # Lunedì, martedì e venerdì in ufficio
```


| Numero | Orario        |
| ------ | ------------- |
| 0      | `[1,1,1,1,1]` |
| 3      | `[1,1,1,0,0]` |
| 10     | `[1,0,1,0,1]` |

Tutti i casi che non rispettano i requisiti (3 giorni in ufficio e 2 a casa) sono eliminati e rimossi.

### Completamento del resto degli utenti
La generazione della disposizione per il resto degli utenti a seguire è direttamente collegata alla generazione del primo utente. Infatti, per "riempire" tutto occupa prima i giorni con meno persone, ed in caso di parità sceglie sempre il primo.

Per esempio, l'utente 2 del numero 10 andrà in ufficio lunedì, martedì e giovedì, in quanto il mercoledì e il venerdì sono già "usati" un giorno dall'utente 0 e il lunedì è il primo giorno con pari disponibilità.

## Output
Tramite l'uso di due librerie, `turtle` (integrata in Python) e `Pillow` (esterna), per ogni combinazione possibile viene creato un file .png composto da una tabella a doppia entrata.

Nonostante la computazione delle varie combinazioni sia praticamente istantanea (almeno con questi piccoli valori), il disegno e la seguente conversione dell'immagine possono richiedere dai 3 ai 5 secondi ciascuna.

Ciascuna immagine viene salvata nella cartella `timetables/`utenti-desks-ufficio-casa`.