import csv
import os

def crea_dizionario_comuni():
    """
    Crea un dizionario che associa il codice catastale di un comune 
    al suo codice ISTAT, denominazione e sigla provincia.
    """
    # Percorso del file CSV
    file_path = os.path.join(os.path.dirname(__file__), 'comuniANPR_ISTAT.csv')
    
    # Dizionario per memorizzare le associazioni
    comuni_dict = {}
    
    # Leggi il file CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Elabora ciascuna riga
        for row in csv_reader:
            codice_catastale = row['CODCATASTALE']
            codice_istat = row['CODISTAT']
            denominazione = row['DENOMINAZIONE_IT']
            sigla_provincia = row['SIGLAPROVINCIA']
            
            # Aggiungi al dizionario
            comuni_dict[codice_catastale] = {
                'codistat': codice_istat,
                'denominazione': denominazione,
                'sigla_provincia': sigla_provincia
            }
    
    return comuni_dict

def cerca_comune_per_codice_catastale(codice_catastale):
    """
    Cerca un comune dato il suo codice catastale e restituisce le informazioni associate.
    
    Args:
        codice_catastale: Il codice catastale del comune da cercare
        
    Returns:
        Un dizionario con le informazioni del comune o None se non trovato
    """
    comuni = crea_dizionario_comuni()
    return comuni.get(codice_catastale)

if __name__ == "__main__":
    # Esempio di utilizzo
    comuni = crea_dizionario_comuni()
    
    # Stampa il numero totale di comuni nel dizionario
    print(f"Numero totale di comuni nel dizionario: {len(comuni)}")
    
    # Esempio: cerca un comune specifico
    codice_esempio = "A074"  # Codice catastale di Agliè
    comune = cerca_comune_per_codice_catastale(codice_esempio)
    
    if comune:
        print(f"\nInformazioni per il comune con codice catastale {codice_esempio}:")
        print(f"Codice ISTAT: {comune['codistat']}")
        print(f"Denominazione: {comune['denominazione']}")
        print(f"Sigla Provincia: {comune['sigla_provincia']}")
    else:
        print(f"\nNessun comune trovato con codice catastale {codice_esempio}")
    
    # Puoi aggiungere qui ulteriori test o esempi di utilizzo