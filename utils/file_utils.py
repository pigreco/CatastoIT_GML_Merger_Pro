import os
import shutil
import gc
import time
from qgis.core import QgsProject

def ensure_directory_exists(directory_path, log_function=None):
    """Assicura che una directory esista, creandola se necessario"""
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path, exist_ok=True)
            if log_function:
                log_function(f"Directory creata: {directory_path}")
            return True
        except Exception as e:
            if log_function:
                log_function(f"Errore creazione directory {directory_path}: {str(e)}")
            return False
    return True

def cleanup_temp_files(directory_path, temp_files=None, log_function=None):
    """Rimuove file temporanei e directory"""
    if not os.path.exists(directory_path):
        return True
        
    try:
        # Rilascia riferimenti ai file
        for layer_id, layer in list(QgsProject.instance().mapLayers().items()):
            if directory_path in layer.source():
                QgsProject.instance().removeMapLayer(layer_id)
        
        # Forza garbage collection
        gc.collect()
        time.sleep(1)
        
        # Rimuovi file specifici se forniti
        if temp_files:
            for file in temp_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                        if log_function:
                            log_function(f"File rimosso: {os.path.basename(file)}")
                    except Exception as e:
                        if log_function:
                            log_function(f"Errore rimozione {file}: {str(e)}")
        
        # Tenta di rimuovere la directory
        if os.path.exists(directory_path) and not os.listdir(directory_path):
            os.rmdir(directory_path)
            if log_function:
                log_function(f"Directory rimossa: {directory_path}")
        
        return True
    except Exception as e:
        if log_function:
            log_function(f"Errore pulizia: {str(e)}")
        return False