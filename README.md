# Guida al plugin CatastoIT_GML_Merger_Pro per QGIS

> **v0.8** — [Guida online](https://pigreco.github.io/CatastoIT_GML_Merger_Pro/) | [Releases](https://github.com/pigreco/CatastoIT_GML_Merger_Pro/releases) | [Segnala un problema](https://github.com/pigreco/CatastoIT_GML_Merger_Pro/issues)

## Descrizione generale
**CatastoIT_GML_Merger_Pro** è un plugin avanzato per QGIS che consente di scaricare, estrarre e unire file GML del catasto italiano. Il plugin permette di lavorare con file di mappa (MAP) e particelle (PLE), convertendoli nel formato GPKG e aggiungendo i campi foglio, particella, sezione censuaria e nome del comune per un'integrazione completa nei flussi di lavoro GIS.

![](./img/gui.png)

## Funzionalità principali

1. **Download dati catastali**: Scarica automaticamente file ZIP da un URL specifico per ogni regione italiana [RNDT](https://geodati.gov.it/geoportale/visualizzazione-metadati/scheda-metadati/?uuid=age:S_0000_ITALIA)
2. **Estrazione intelligente**: Decomprime file ZIP delle province e dei comuni con gestione ottimizzata dello spazio
3. **Unione file GML**: Unisce i file GML estratti in un unico file con risoluzione automatica dei conflitti
4. **Conversione multi-formato**: Supporta l'esportazione in GPKG
5. **Caricamento in QGIS**: Opzione per caricare direttamente i layer risultanti in QGIS con stile predefinito
6. **Gestione della memoria**: Ottimizzazione per la gestione di grandi volumi di dati catastali
7. **Log dettagliato**: Registrazione completa delle operazioni per controllo e debug
8. **Filtro geografico per provincia**: Possibilità di selezionare più province con CTRL+clic
9. **Filtro per comune**: Widget di selezione interattivo (transfer widget) per filtrare uno o più comuni specifici all'interno delle province selezionate — ricerca per nome, doppio clic o pulsanti → ← per aggiungere/rimuovere
10. **Report statistico**: Generazione automatica di report sui dati elaborati
11. **Supporto sezione censuaria**: Possibilità di aggiungere automaticamente la sezione censuaria nelle Particelle
12. **Riproiezione dati**: Possibilità di riproiettare i dati catastali in altri sistemi di riferimento (CRS) oltre al nativo (EPSG:6706)
13. **Nome comune** *(nuovo in v0.5)*: Checkbox opzionale per aggiungere il campo `comune` con il nome del comune ricavato automaticamente dal codice Belfiore
14. **Guida online** *(nuovo in v0.5)*: Documentazione completa su [GitHub Pages](https://pigreco.github.io/CatastoIT_GML_Merger_Pro/)
15. **Stile predefinito PLE** *(nuovo in v0.6)*: Al caricamento in QGIS, il layer particelle viene visualizzato con renderer a regole — particelle trasparenti, strade in grigio, acque in blu
16. **Resilienza GML non validi** *(nuovo in v0.7)*: File GML corrotti o non validi vengono automaticamente saltati con avviso nel log — il processo continua con i file validi senza interrompersi
17. **Granularità output** *(nuovo in v0.8)*: Nuova combobox per scegliere come aggregare i file di output — unico file (comportamento classico), un file per provincia o un file per comune; nei modi multi-file i layer vengono caricati in QGIS all'interno di un gruppo dedicato nel pannello Layer

## Come utilizzare il plugin

1. Avvia il plugin dall'icona nella barra degli strumenti o dal menu Plugin
2. Seleziona la **regione** dal menu a discesa (l'URL si aggiorna automaticamente)
3. Seleziona una o più **province** (CTRL+clic per selezione multipla)
4. *(Opzionale)* Usa il **filtro comuni** per limitare l'elaborazione a specifici comuni: cerca per nome nel campo di ricerca, poi sposta i comuni desiderati nella lista "Selezionati" con doppio clic o pulsante →
5. Seleziona il **tipo di file** da elaborare (Mappe, Particelle o Entrambi)
6. Se lavori con Particelle, puoi attivare l'opzione **"Aggiungi Sezione Censuaria nelle Particelle"**
7. *(Opzionale)* Attiva **"Aggiungi Nome Comune"** per includere il campo `comune` nell'output *(v0.5)*
8. Scegli il **formato di output** (solo GPKG) e la **granularità** (unico file / per provincia / per comune) *(v0.8)*
9. Definisci la **cartella di destinazione** e i nomi dei file di output
10. *(Opzionale)* Seleziona una **cartella temporanea** se quella di sistema ha poco spazio
11. *(Opzionale)* Seleziona il **CRS di output** per riproiettare i dati
12. Spunta **"Carica layer in QGIS"** se vuoi visualizzare subito il risultato
13. Clicca su **"Elabora"** per avviare il processo in background
14. Monitora l'avanzamento attraverso i messaggi nel riquadro di log
15. Al termine, visualizza il report statistico generato automaticamente
16. Clicca su **"Pulisci File Temporanei e Chiudi"** per ripulire le directory temporanee
17. Per la documentazione completa clicca **"Guida online"** o visita [pigreco.github.io/CatastoIT_GML_Merger_Pro](https://pigreco.github.io/CatastoIT_GML_Merger_Pro/)

## Note tecniche
- Il plugin crea directory temporanee per l'elaborazione con pulizia automatica al momento della chiusura
- La procedura include: download, estrazione, unione, filtro degli attributi, aggiunta campi calcolati e riproiezione
- I tempi di elaborazione vengono mostrati al termine del processo
- Gestione ottimizzata della memoria per file di grandi dimensioni (streaming BytesIO per ZIP provinciali)
- CRS nativo dei dati AdE: **EPSG:6706** (RDN2008 Geographic 2D, coordinate in gradi) — scritto correttamente nelle tabelle SRS del GPKG *(fix v0.5)*
- Se si seleziona un CRS di output diverso da EPSG:6706, i dati vengono riproiettati automaticamente
- Il **filtro comuni** usa il codice catastale Belfiore (es. A662 = BARI) ricavato dalla struttura dei file ZIP originali
- Il **nome comune** viene ricavato automaticamente tramite lookup sul codice Belfiore contenuto nel campo `ADMINISTRATIVEUNIT`

## Dati di output
- Nei file di output vengono eliminati i campi inutili e mantenuti solo `gml_id` e `ADMINISTRATIVEUNIT`
- Nei file di output vengono aggiunti campi calcolati per facilitare l'identificazione catastale:
  - Campo **Foglio**: estratto automaticamente dai dati originali per rapida consultazione
  - Campo **Particella**: numero identificativo della particella catastale, elaborato dal codice originale
  - Campo **sez_censuaria**: (opzionale) identifica la sezione censuaria estratta dal codice originale
  - Campo **comune**: *(nuovo in v0.5, opzionale)* nome del comune ricavato dal codice Belfiore in `ADMINISTRATIVEUNIT`
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

L'autore del plugin non è un developer ma è riuscito a realizzare il plugin con l'ausilio della AI.

## Video Demo

[![QGIS Tutorial Video](https://img.youtube.com/vi/lFHrthP1nHs/0.jpg)](https://youtu.be/lFHrthP1nHs)
