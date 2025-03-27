from qgis.core import QgsField, QgsVectorLayer, QgsFeature, QgsFeatureRequest
from PyQt5.QtCore import QVariant
import os

# Funzioni Lambda di utilità per l'elaborazione GML
extract_foglio = lambda gml_id: gml_id[32:36] if len(gml_id) > 36 else ""
extract_particella = lambda gml_id: gml_id[39:] if len(gml_id) > 39 else ""
extract_sez_censuaria = lambda gml_id: gml_id[31:32] if len(gml_id) > 32 else ""

def process_gml_features(layer, add_sezione_censuaria=False):
    """Processa le feature di un layer GML e calcola i campi foglio, particella, etc.
    
    Args:
        layer: Il layer GML da processare
        add_sezione_censuaria: Se True, aggiunge il campo sezione censuaria
        
    Returns:
        int: Numero di feature elaborate
    """
    # Verifica se il layer è valido
    if layer is None:
        return 0
    
    # Conteggio delle feature elaborate
    feature_count = 0
    
    # Creazione dei nuovi campi se non esistono già
    provider = layer.dataProvider()
    fields = provider.fields()
    
    # Aggiungi i campi necessari se non esistono già
    fields_to_add = []
    if "foglio" not in fields.names():
        fields_to_add.append(QgsField("foglio", QVariant.String, len=10))
    
    if "particella" not in fields.names():
        fields_to_add.append(QgsField("particella", QVariant.String, len=15))
    
    if add_sezione_censuaria and "sez_censuaria" not in fields.names():
        fields_to_add.append(QgsField("sez_censuaria", QVariant.String, len=5))
    
    if fields_to_add:
        provider.addAttributes(fields_to_add)
        layer.updateFields()
    
    # Indici dei campi per l'aggiornamento
    foglio_idx = layer.fields().indexFromName("foglio")
    particella_idx = layer.fields().indexFromName("particella")
    sez_censuaria_idx = layer.fields().indexFromName("sez_censuaria") if add_sezione_censuaria else -1
    
    # Processa ogni feature
    layer.startEditing()
    
    for feature in layer.getFeatures():
        gml_id = feature["gml_id"] if "gml_id" in feature.fields().names() else ""
        
        # Estrai i valori usando le funzioni lambda
        if gml_id:
            foglio = extract_foglio(gml_id)
            particella = extract_particella(gml_id)
            
            # Aggiorna i campi
            feature.setAttribute(foglio_idx, foglio)
            feature.setAttribute(particella_idx, particella)
            
            if add_sezione_censuaria and sez_censuaria_idx >= 0:
                sez_censuaria = extract_sez_censuaria(gml_id)
                feature.setAttribute(sez_censuaria_idx, sez_censuaria)
            
            layer.updateFeature(feature)
            feature_count += 1
    
    # Salva le modifiche
    layer.commitChanges()
    
    # Crea indici per migliorare le performance di query
    try:
        provider.createAttributeIndex(foglio_idx)
        provider.createAttributeIndex(particella_idx)
        if add_sezione_censuaria and sez_censuaria_idx >= 0:
            provider.createAttributeIndex(sez_censuaria_idx)
    except:
        # Alcuni provider potrebbero non supportare la creazione di indici
        pass
    
    return feature_count

def load_gml_file(gml_path, layer_name=None):
    """Carica un file GML come layer QGIS.
    
    Args:
        gml_path (str): Percorso al file GML da caricare
        layer_name (str, optional): Nome da assegnare al layer. Se None, usa il nome del file
        
    Returns:
        QgsVectorLayer: Layer caricato o None in caso di errore
    """
    if not os.path.exists(gml_path):
        return None
    
    if layer_name is None:
        layer_name = os.path.basename(gml_path).split('.')[0]
    
    # Carica il layer
    layer = QgsVectorLayer(gml_path, layer_name, "ogr")
    
    if not layer.isValid():
        return None
    
    return layer

def filter_gml_by_foglio(layer, foglio):
    """Filtra un layer GML mantenendo solo le feature di un determinato foglio.
    
    Args:
        layer (QgsVectorLayer): Il layer da filtrare
        foglio (str): Numero di foglio da mantenere
        
    Returns:
        QgsVectorLayer: Nuovo layer filtrato o None in caso di errore
    """
    if not layer or not layer.isValid():
        return None
    
    # Verifica se esiste il campo foglio
    if "foglio" not in layer.fields().names():
        # Processa il layer per aggiungere il campo foglio
        process_gml_features(layer)
    
    # Crea l'espressione di filtro
    request = QgsFeatureRequest()
    request.setFilterExpression(f"foglio = '{foglio}'")
    
    # Crea un nuovo layer con le feature filtrate
    memory_layer = QgsVectorLayer(f"{'Polygon' if layer.geometryType() == 2 else 'LineString'}", 
                                  f"{layer.name()}_foglio_{foglio}", 
                                  "memory")
    
    # Copia il CRS e i campi dal layer originale
    memory_layer.setCrs(layer.crs())
    provider = memory_layer.dataProvider()
    provider.addAttributes(layer.fields().toList())
    memory_layer.updateFields()
    
    # Aggiunge le feature che corrispondono al filtro
    features = list(layer.getFeatures(request))
    provider.addFeatures(features)
    
    return memory_layer

def get_unique_fogli(layer):
    """Restituisce una lista di tutti i fogli presenti nel layer.
    
    Args:
        layer (QgsVectorLayer): Il layer da analizzare
        
    Returns:
        list: Lista di stringhe contenenti i numeri di foglio unici
    """
    if not layer or not layer.isValid():
        return []
    
    # Verifica se esiste il campo foglio
    if "foglio" not in layer.fields().names():
        # Processa il layer per aggiungere il campo foglio
        process_gml_features(layer)
    
    # Ottieni i valori unici dal campo foglio
    fogli = set()
    for feature in layer.getFeatures():
        foglio = feature["foglio"]
        if foglio:
            fogli.add(foglio)
    
    return sorted(list(fogli))