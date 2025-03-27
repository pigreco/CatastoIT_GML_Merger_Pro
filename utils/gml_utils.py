# Funzioni Lambda di utilità per l'elaborazione GML
extract_foglio = lambda gml_id: gml_id[32:36] if len(gml_id) > 36 else ""
extract_particella = lambda gml_id: gml_id[39:] if len(gml_id) > 39 else ""
extract_sez_censuaria = lambda gml_id: gml_id[31:32] if len(gml_id) > 32 else ""

def process_gml_features(layer, add_sezione_censuaria=False):
    """Processa le feature di un layer GML e calcola i campi foglio, particella, etc."""
    # Implementazione del processamento delle feature
    pass