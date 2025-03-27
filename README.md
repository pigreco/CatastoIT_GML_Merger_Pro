# Guida al plugin CatastoIT_GML_Merger_Pro per QGIS

## Descrizione generale
**CatastoIT_GML_Merger_Pro** è un plugin avanzato per QGIS che consente di scaricare, estrarre e unire file GML del catasto italiano. Il plugin permette di lavorare con file di mappa (MAP) e particelle (PLE), convertendoli nel formato GPKG e aggiungendo i campi foglio e particella per un'integrazione completa nei flussi di lavoro GIS.

![](./img/gui.png)

## Funzionalità principali

1. **Download dati catastali**: Scarica automaticamente file ZIP da un URL specifico per ogni regione italiana [RNDT](https://geodati.gov.it/geoportale/visualizzazione-metadati/scheda-metadati/?uuid=age:S_0000_ITALIA)
2. **Estrazione intelligente**: Decomprime file ZIP delle province e dei comuni con gestione ottimizzata dello spazio
3. **Unione file GML**: Unisce i file GML estratti in un unico file con risoluzione automatica dei conflitti
4. **Conversione multi-formato**: Supporta l'esportazione in GPKG
5. **Caricamento in QGIS**: Opzione per caricare direttamente i layer risultanti in QGIS con stile predefinito
6. **Gestione della memoria**: Ottimizzazione per la gestione di grandi volumi di dati catastali
7. **Log dettagliato**: Registrazione completa delle operazioni per controllo e debug
8. **Filtro geografico**: Possibilità di selezionare più province
9. **Report statistico**: Generazione automatica di report sui dati elaborati
10. **Supporto sezione censuaria**: Possibilità di aggiungere automaticamente la sezione censuaria nelle Particelle
11. **Riproiezione dati**: Possibilità di riproiettare i dati catastali in altri sistemi di riferimento (CRS) oltre al nativo RDN2008/ETRF2000 (EPSG:7794)

## Come utilizzare il plugin

1. Avvia il plugin dall'icona nella barra degli strumenti o dal menu Plugin
2. Seleziona la regione dal menu a discesa (l'URL si aggiorna automaticamente)
3. Seleziona il tipo di file da elaborare (Mappe, Particelle o entrambi)
4. Applica eventuali filtri geografici per province specifiche
5. Se lavori con Particelle, puoi attivare l'opzione "Aggiungi Sezione Censuaria nelle Particelle"
6. Scegli il formato di output desiderato (solo GPKG)
7. Definisci i percorsi dei file di output
8. Seleziona il sistema di riferimento (CRS) desiderato per i dati di output (opzionale)
9. Seleziona se caricare i layer risultanti in QGIS
10. Clicca su "Elabora" per avviare il processo
11. Monitora l'avanzamento attraverso i messaggi nel riquadro di log
12. Al termine, visualizza il report statistico generato automaticamente
13. Clicca su "Chiudi" per pulire le directory temporanee

## Note tecniche
- Il plugin crea directory temporanee per l'elaborazione con pulizia automatica
- La procedura include: download, estrazione, unione, filtro degli attributi e riproiezione
- I tempi di elaborazione vengono mostrati al termine del processo
- Gestione ottimizzata della memoria per file di grandi dimensioni
- I dati vengono riproiettati dal sistema nativo RDN2008/ETRF2000 (EPSG:7794) al CRS selezionato dall'utente

## Dati di output
- Nei file di output vengono eliminati i campi inutili e mantenuti solo `gml_id` e `ADMINISTRATIVEUNIT`
- Nei file di output vengono aggiunti campi calcolati per facilitare l'identificazione catastale:
  - Campo **Foglio**: estratto automaticamente dai dati originali per rapida consultazione
  - Campo **Particella**: numero identificativo della particella catastale, elaborato dal codice originale
  - Campo **sez_censuaria**: (opzionale) identifica la sezione censuaria estratta dal codice originale
- La combinazione di questi campi consente ricerche e filtraggio immediato dei dati catastali
- Gli attributi originali vengono mantenuti per compatibilità con altri sistemi
- I dati vengono forniti nel sistema di coordinate (CRS) scelto dall'utente durante l'elaborazione

## Requisiti di sistema
- QGIS 3.22 o superiore
- Connessione internet per il download dei dati
- Almeno 4GB di RAM (8GB consigliati per province estese)
- Spazio su disco sufficiente per i dati temporanei e di output
- Python 3.7 o superiore con librerie GDAL/OGR

## Disclaimer

L'autore del plugin non è un developer professionista ma è riuscito a realizzare il plugin con l'ausilio dell'intelligenza artificiale.

## Licenza
Questo plugin è rilasciato sotto licenza GPL v3. I dati catastali sono di proprietà dell'Agenzia delle Entrate e soggetti alle loro condizioni d'uso.

## Supporto e contributi
- Per segnalazioni di bug o richieste di funzionalità, utilizzare la sezione Issues su GitHub
- I contributi sono benvenuti tramite pull request
- Per domande o supporto, contattare l'autore tramite la pagina del plugin

## Ringraziamenti
- All'Agenzia delle Entrate per aver reso disponibili i dati catastali in formato aperto
- Alla comunità QGIS per il supporto e gli strumenti di sviluppo
- A tutti i beta tester che hanno contribuito a migliorare la stabilità del plugin

## Struttura del plugin

Il plugin è organizzato seguendo una struttura modulare multi-file che ne facilita la manutenzione e l'estensibilità:

```
CatastoIT_GML_Merger_Pro/
├── __init__.py              # Punto di ingresso del plugin
├── metadata.txt            # Metadati del plugin per QGIS
├── README.md               # Questo file di documentazione
├── LICENSE                 # Licenza GPL v3
├── core/                   # Funzionalità core del plugin
│   ├── __init__.py
│   ├── processor.py        # Classe principale di elaborazione
│   ├── downloader.py       # Gestione del download dei dati
│   ├── extractor.py        # Estrazione e decompressione
│   ├── reprojector.py      # Riproiezione dei dati
│   └── merger.py           # Unione dei file GML
├── gui/                    # Interfaccia utente
│   ├── __init__.py
│   ├── main_dialog.py      # Finestra principale
│   ├── progress_dialog.py  # Finestra di progresso
│   └── region_selector.py  # Widget per selezione regioni
├── utils/                  # Utilità varie
│   ├── __init__.py
│   ├── file_utils.py       # Utilità per file e cartelle
│   ├── log_utils.py        # Sistema di logging
│   ├── gis_utils.py        # Funzioni GIS
│   └── config.py           # Configurazioni
├── resources/              # Risorse del plugin
│   ├── icons/              # Icone
│   ├── styles/             # Stili QGIS
│   └── ui/                 # File UI
└── img/                    # Immagini per documentazione
```

### Componenti principali

1. **Core**: Contiene le classi principali che gestiscono la logica di business del plugin:
   - `processor.py`: Orchestratore del flusso di elaborazione completo
   - `downloader.py`: Gestisce il download dei dati catastali
   - `extractor.py`: Si occupa dell'estrazione dei file ZIP
   - `reprojector.py`: Gestisce la riproiezione dei dati
   - `merger.py`: Unisce i file GML in un unico file

2. **GUI**: Include i componenti dell'interfaccia utente:
   - `main_dialog.py`: Finestra principale del plugin
   - `progress_dialog.py`: Mostra l'avanzamento dell'elaborazione
   - `region_selector.py`: Widget per la selezione della regione

3. **Utils**: Contiene funzioni di utilità generica:
   - `file_utils.py`: Funzioni per la gestione di file e cartelle
   - `log_utils.py`: Sistema di logging
   - `gis_utils.py`: Funzioni specifiche per le operazioni GIS
   - `config.py`: Configurazioni generali e costanti

4. **Resources**: Contiene le risorse statiche del plugin come icone, stili QGIS e file UI

Questa architettura modulare facilita:
- Manutenzione: ogni componente ha responsabilità ben definite
- Testing: è possibile testare singolarmente ciascun modulo
- Estensibilità: nuove funzionalità possono essere aggiunte facilmente
- Collaborazione: più sviluppatori possono lavorare su componenti diversi