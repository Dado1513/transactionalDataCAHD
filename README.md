# CAHD implementation

### Getting Started
Implementazione del codice CAHD (Correlation aware Anonymization of High-dimensional Data)
per anonimizzare dati di tipo transazionali trasformando prima i dati in accordo con l'algoritmo RCM (Reverse Cuthill-McKee)

### Prerequisiti
- Dati in formato transazionale
![image dati transazionali](Image Plot/transactional_data.PNG)
- Python 3.x
- Pandas, Numpy, Scipy

### Esecuzione
Eseguire il comando
```
python Main.py
```
Ed seguire i comandi a schermo

### Risultati Dataset DBMS2
Di seguito i risultati relativi al tempo di esecuzione di BMS2 (see KDD CUP 2000).
http://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php
Sono stati troncate alle prime 10000 transazioni nella costruzione del datasets (L'originale era di circa 60000).
Con 1000 transazioni, grado di privacy variabile, numero di items sensbili 10, alfa = 3.
![Risultati](Image Plot/ex_time_bms2.png)
