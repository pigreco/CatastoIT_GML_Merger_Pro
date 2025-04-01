REGIONS = [
    "ABRUZZO", "BASILICATA", "CALABRIA", "CAMPANIA", "EMILIA-ROMAGNA",
    "FRIULI-VENEZIA-GIULIA", "LAZIO", "LIGURIA", "LOMBARDIA", "MARCHE",
    "MOLISE", "PIEMONTE", "PUGLIA", "SARDEGNA", "SICILIA", "TOSCANA", 
    "UMBRIA", "VALLE-AOSTA", "VENETO"
]

# Dizionario delle province italiane organizzate per regione (con sigle in maiuscolo)
PROVINCES_BY_REGION = {
    "ABRUZZO": ["AQ", "CH", "PE", "TE"],
    
    "BASILICATA": ["MT", "PZ"],
    
    "CALABRIA": ["CZ", "CS", "KR", "RC", "VV"],
    
    "CAMPANIA": ["AV", "BN", "CE", "NA", "SA"],
    
    "EMILIA-ROMAGNA": ["BO", "FE", "FO", "MO", "PR", "PC", "RA", "RE", "RN"],
    
    "FRIULI-VENEZIA-GIULIA": ["GO", "PN", "TS", "UD"],
    
    "LAZIO": ["FR", "LT", "RI", "RM", "VT"],
    
    "LIGURIA": ["GE", "IM", "SP", "SV"],
    
    "LOMBARDIA": ["BG", "BS", "CO", "CR", "LC", "LO", "MN", "MI", "MB", "PV", "SO", "VA"],
    
    "MARCHE": ["AN", "AP", "FM", "MC", "PU"],
    
    "MOLISE": ["CB", "IS"],
    
    "PIEMONTE": ["AL", "AT", "BI", "CN", "NO", "TO", "VB", "VC"],
    
    "PUGLIA": ["BA", "BT", "BR", "FG", "LE", "TA"],
    
    "SARDEGNA": ["CA", "NU", "OR", "SS"],
    
    "SICILIA": ["AG", "CL", "CT", "EN", "ME", "PA", "RG", "SR", "TP"],
    
    "TOSCANA": ["AR", "FI", "GR", "LI", "LU", "MS", "PI", "PT", "PO", "SI"],
    
    "UMBRIA": ["PG", "TR"],
    
    "VALLE-AOSTA": ["AO"],
    
    "VENETO": ["BL", "PD", "RO", "TV", "VE", "VR", "VI"]
}

# Dizionario per mappare le sigle alle province complete (per riferimento)
PROVINCE_CODES_TO_NAMES = {
    "AQ": "L'Aquila", "CH": "Chieti", "PE": "Pescara", "TE": "Teramo",
    "MT": "Matera", "PZ": "Potenza",
    "CZ": "Catanzaro", "CS": "Cosenza", "KR": "Crotone", "RC": "Reggio Calabria", "VV": "Vibo Valentia",
    "AV": "Avellino", "BN": "Benevento", "CE": "Caserta", "NA": "Napoli", "SA": "Salerno",
    "BO": "Bologna", "FE": "Ferrara", "FO": "Forlì-Cesena", "MO": "Modena", "PR": "Parma", 
    "PC": "Piacenza", "RA": "Ravenna", "RE": "Reggio Emilia", "RN": "Rimini",
    "GO": "Gorizia", "PN": "Pordenone", "TS": "Trieste", "UD": "Udine",
    "FR": "Frosinone", "LT": "Latina", "RI": "Rieti", "RM": "Roma", "VT": "Viterbo",
    "GE": "Genova", "IM": "Imperia", "SP": "La Spezia", "SV": "Savona",
    "BG": "Bergamo", "BS": "Brescia", "CO": "Como", "CR": "Cremona", "LC": "Lecco", "LO": "Lodi", 
    "MN": "Mantova", "MI": "Milano", "MB": "Monza e della Brianza", "PV": "Pavia", "SO": "Sondrio", "VA": "Varese",
    "AN": "Ancona", "AP": "Ascoli Piceno", "FM": "Fermo", "MC": "Macerata", "PU": "Pesaro e Urbino",
    "CB": "Campobasso", "IS": "Isernia",
    "AL": "Alessandria", "AT": "Asti", "BI": "Biella", "CN": "Cuneo", "NO": "Novara", 
    "TO": "Torino", "VB": "Verbano-Cusio-Ossola", "VC": "Vercelli",
    "BA": "Bari", "BT": "Barletta-Andria-Trani", "BR": "Brindisi", "FG": "Foggia", "LE": "Lecce", "TA": "Taranto",
    "CA": "Cagliari", "NU": "Nuoro", "OR": "Oristano", "SS": "Sassari", "SU": "Sud Sardegna",
    "AG": "Agrigento", "CL": "Caltanissetta", "CT": "Catania", "EN": "Enna", "ME": "Messina", 
    "PA": "Palermo", "RG": "Ragusa", "SR": "Siracusa", "TP": "Trapani",
    "AR": "Arezzo", "FI": "Firenze", "GR": "Grosseto", "LI": "Livorno", "LU": "Lucca", 
    "MS": "Massa-Carrara", "PI": "Pisa", "PT": "Pistoia", "PO": "Prato", "SI": "Siena",
    "PG": "Perugia", "TR": "Terni",
    "AO": "Aosta",
    "BL": "Belluno", "PD": "Padova", "RO": "Rovigo", "TV": "Treviso", "VE": "Venezia", "VR": "Verona", "VI": "Vicenza"
}

# Funzione per ottenere tutte le province di una regione
def get_provinces(region):
    """
    Restituisce l'elenco delle province (sigle) per una data regione
    """
    return PROVINCES_BY_REGION.get(region.upper(), [])

# Funzione per ottenere tutte le province italiane
def get_all_provinces():
    """
    Restituisce una lista di tutte le sigle delle province italiane
    """
    all_provinces = []
    for provinces in PROVINCES_BY_REGION.values():
        all_provinces.extend(provinces)
    return sorted(all_provinces)

# Funzione per trovare la regione di una provincia
def get_region_by_province(province_code):
    """
    Restituisce la regione di appartenenza di una provincia (sigla)
    """
    for region, provinces in PROVINCES_BY_REGION.items():
        if province_code in provinces:
            return region
    return None

# Funzione per ottenere il nome completo di una provincia dalla sua sigla
def get_province_name(province_code):
    """
    Restituisce il nome completo di una provincia dalla sua sigla
    """
    return PROVINCE_CODES_TO_NAMES.get(province_code.upper(), None)

# Funzione per ottenere la sigla di una provincia dal suo nome completo
def get_province_code(province_name):
    """
    Restituisce la sigla di una provincia dal suo nome completo
    """
    for code, name in PROVINCE_CODES_TO_NAMES.items():
        if name.lower() == province_name.lower():
            return code
    return None

import duckdb
import os

def get_municipalities_by_province(province_code):
    """
    Restituisce tutti i comuni appartenenti a una provincia
    utilizzando il file index.parquet.
    
    Args:
        province_code (str): Sigla della provincia (es. "TO", "MI")
        
    Returns:
        list: Lista di dizionari con le informazioni dei comuni 
              [{"comune": "A016 (ACCEGLIO)", "CODISTAT": "004001", "DENOMINAZIONE_IT": "ACCEGLIO"}, ...]
    """
    # Normalizza il codice provincia
    province_code = province_code.upper()
    
    # Mappa delle sigle provincia ai codici ISTAT provincia (primi 3 caratteri del CODISTAT)
    province_code_map = {
        # Piemonte
        "TO": "001", "VC": "002", "NO": "003", "CN": "004", "AT": "005", 
        "AL": "006", "BI": "096", "VB": "103",
        # Valle d'Aosta
        "AO": "007",
        # Lombardia
        "VA": "012", "CO": "013", "SO": "014", "MI": "015", "BG": "016", 
        "BS": "017", "PV": "018", "CR": "019", "MN": "020", "LC": "097", 
        "LO": "098", "MB": "108",
        # Trentino-Alto Adige
        "BZ": "021", "TN": "022",
        # Veneto
        "VR": "023", "VI": "024", "BL": "025", "TV": "026", "VE": "027", 
        "PD": "028", "RO": "029",
        # Friuli-Venezia Giulia
        "UD": "030", "GO": "031", "TS": "032", "PN": "093",
        # Liguria
        "IM": "008", "SV": "009", "GE": "010", "SP": "011",
        # Emilia-Romagna
        "PC": "033", "PR": "034", "RE": "035", "MO": "036", "BO": "037", 
        "FE": "038", "RA": "039", "FC": "040", "RN": "099",
        # Toscana
        "MS": "045", "LU": "046", "PT": "047", "FI": "048", "LI": "049", 
        "PI": "050", "AR": "051", "SI": "052", "GR": "053", "PO": "100",
        # Umbria
        "PG": "054", "TR": "055",
        # Marche
        "PU": "041", "AN": "042", "MC": "043", "AP": "044", "FM": "109",
        # Lazio
        "VT": "056", "RI": "057", "RM": "058", "LT": "059", "FR": "060",
        # Abruzzo
        "AQ": "066", "TE": "067", "PE": "068", "CH": "069",
        # Molise
        "IS": "094", "CB": "070",
        # Campania
        "CE": "061", "BN": "062", "NA": "063", "AV": "064", "SA": "065",
        # Puglia
        "FG": "071", "BA": "072", "TA": "073", "BR": "074", "LE": "075", 
        "BT": "110",
        # Basilicata
        "PZ": "076", "MT": "077",
        # Calabria
        "CS": "078", "CZ": "079", "RC": "080", "KR": "101", "VV": "102",
        # Sicilia
        "TP": "081", "PA": "082", "ME": "083", "AG": "084", "CL": "085", 
        "EN": "086", "CT": "087", "RG": "088", "SR": "089",
        # Sardegna
        "SS": "090", "NU": "091", "CA": "092", "OR": "095", "SU": "111"
    }
    
    # Ottieni il codice ISTAT della provincia
    istat_code = province_code_map.get(province_code)
    if not istat_code:
        return []
    
    # Percorso al file index.parquet
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(base_dir, "index.parquet")
    
    # Verifica che il file esista
    if not os.path.exists(parquet_path):
        return []
    
    try:
        # Crea una connessione DuckDB in memoria
        con = duckdb.connect(database=':memory:')
        
        # Leggi il file parquet direttamente nella query per evitare problemi di registrazione
        query = f"""
        SELECT *
        FROM read_parquet('{parquet_path}')
        WHERE CODISTAT LIKE '{istat_code}%'
        ORDER BY DENOMINAZIONE_IT
        """
        
        # Esegui la query
        result = con.execute(query).fetchall()
        
        # Converti il risultato in lista di dizionari
        municipalities = []
        for row in result:
            # Usando gli indici corretti in base al feedback
            # comune: indice 0, CODISTAT: indice 2, DENOMINAZIONE_IT: indice 3
            municipalities.append({
                "comune": f"{row[0]}_{row[3]}",  # Manteniamo questo formato per la visualizzazione
                "codice_catasto": row[0],         # Aggiungiamo il solo codice catasto per la ricerca file
                "CODISTAT": row[2],
                "DENOMINAZIONE_IT": row[3]
            })
        
        return municipalities
        
    except Exception as e:
        # In caso di errore, ritorna una lista vuota
        return []
    
    finally:
        if 'con' in locals():
            con.close()