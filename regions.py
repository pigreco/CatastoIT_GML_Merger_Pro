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
    
    "SARDEGNA": ["CA", "NU", "OR", "SS" , "SU"],
    
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