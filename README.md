# Simulazione investimento fondo pensioni

## Manuale d'uso

### Disattivare Modalita' di debug

Prima di poter disattivare la modalita' di debug, e' necessario copiare i file
statici (css e js) utilizzati da otree. Per farlo e' sufficiente seguire la
seguente procedura:

### Copiare file statici

Da linea di comando scrivere il comando

`otree collectstatic`

E' sufficiente fare questa operazione UNA sola volta, non ogni volta che viene
avviato il server.

### Avviare il server

Per avviare il server e' sufficiente dare il seguente comando (da terminale):

`otree devserver <PORT>`

sostituendo il numero di porta con quello desiderato (tipicamente 8000).

Quindi ad esempio in quel caso il comando sara'

`otree devserver 8000`

Una volta avviato il server sara' raggiungibile digitando nell'url del browser
(Chrome o Firefox o qualunque altro) l'indirizzo

`http://localhost:8000`

o anche 

`http://127.0.0.1:8000`

## Modificare parametri

Se si vogliono modificare dei parametri di utilizzo, questi vanno probabilmente
cercati nei file `fondo_pensioni/pages.py` o `settings.py`.
