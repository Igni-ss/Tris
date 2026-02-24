# Tris

Una semplice implementazione del gioco tris (tic-tac-toe) contro il computer, che utilizza l'algoritmo Minimax.

## Installazione

1. Clona il repository:

   ```bash
   git clone https://github.com/Igni-ss/Tris.git
   cd Tris
   ```

2. (Opzionale) Crea e attiva un ambiente virtuale:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Installa le dipendenze per lo sviluppo e i test (opzionale, solo se vuoi contribuire o eseguire i test):

   ```bash
   pip install -r requirements_dev.txt
   ```

## Avvio del gioco

Per avviare il gioco con interfaccia grafica:

```bash
python3 -m src.main
```

## Esecuzione dei test

Per eseguire i test, dopo aver installato `requrements_dev.txt`, si può lanciare:

```bash
pytest --cov src tests/
```
