# Nome del progetto

## Dipendenze

- [Neo4j](https://neo4j.com/)
- [MongoDB](https://www.mongodb.com/)
- Python

## Descrizione

Breve descrizione del progetto e delle sue funzionalità.

## Requisiti

- Docker: Assicurati di avere Docker installato sul tuo sistema. Puoi scaricarlo dal sito ufficiale di Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)
- Python: Assicurati di avere Python installato sul tuo sistema. Puoi scaricarlo dal sito ufficiale di Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Istruzioni per l'avvio

( Poichè il file archivio con le geometrie e le misurazioni pesa 3 gb lascio il link di download, creare una cartella "archive" ed estrarre il rar li per utilizzarlo nel progetto https://www.kaggle.com/datasets/giobbu/belgium-obu?select=Anderlecht_streets.json )

### 1. Creazione e attivazione dell'ambiente virtuale

- Apri un terminale o una finestra del prompt dei comandi.
- Digita il seguente comando per creare un nuovo ambiente virtuale:

    ```
    python -m venv venv
    ```

  `venv` è il nome dell'ambiente virtuale. Puoi scegliere un nome differente se preferisci.

- Dopo aver creato l'ambiente virtuale, esegui il seguente comando per attivarlo:

    - Windows:
      ```
      venv\Scripts\activate
      ```

    - macOS/Linux:
      ```
      source venv/bin/activate
      ```

### 2. Installazione delle librerie

- Assicurati di trovarti nella directory del progetto, dove si trova il file `requirements.txt`.
- Esegui il seguente comando per installare le librerie necessarie:

    ```
    pip install -r requirements.txt
    ```

  Questo comando installerà tutte le librerie elencate nel file `requirements.txt`.
### BASTA FARE docker compose up LOL ###
### 3. Avvio di Neo4j

- Apri un altro terminale o una finestra del prompt dei comandi.
- Digita il seguente comando per scaricare l'immagine Docker di Neo4j:

    ```
    docker pull neo4j
    ```

- Dopo aver completato il download, esegui il seguente comando per avviare un contenitore Docker di Neo4j:

    ```
    docker run --name neo4j_instance -p 7474:7474 -p 7687:7687 -d neo4j
    ```

- A questo punto, puoi accedere all'interfaccia Web di Neo4j aprendo il tuo browser e digitando l'URL [http://localhost:7474](http://localhost:7474). Utilizza le seguenti credenziali di accesso:

    - Nome utente (Username): neo4j
    - Password: neo4j

### 4. Avvio di MongoDB

- Apri un altro terminale o una finestra del prompt dei comandi.
- Digita il seguente comando per scaricare l'immagine Docker di MongoDB:

    ```
    docker pull mongo
    ```

- Dopo aver completato il download, esegui il seguente comando per avviare un contenitore Docker di MongoDB:

    ```
    docker run --name mongodb_instance -p 27017:27017 -d mongo
    ```

- A questo punto, MongoDB è in esecuzione e pronto per essere utilizzato nel tuo progetto.

### 5. Avvio di Flask ( Web Server )

- Apri un altro terminale o una finestra del prompt dei comandi.
- Digita il seguente comando:

    ```
    flask --app main.py --debug run
    o
    flask --app main.py run 
    ```

- A questo punto, è tutto pronto.

## Configurazione

Se hai bisogno di configurazioni aggiuntive per Neo4j o MongoDB, consulta la documentazione ufficiale di Neo4j e MongoDB per ulteriori dettagli.

## Contributi

Qualora volessi contribuire a questo progetto, fai riferimento alle linee guida per i contributi e invia le tue pull request.

## Licenza

Inserisci qui la licenza del tuo progetto (es. MIT, Apache, etc.).

## Contatti

- Nome: Emanuele Giordano, Luca Pallonetto, Luca Pastore
- Email: emanuel.giordano@studenti.unina.it
