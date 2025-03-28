import os
import pandas as pd
import geopandas as gpd
from qgis.core import QgsVectorLayer, QgsProject

class JoinANPR:
    def __init__(self, plugin_dir):
        """Inizializza il modulo di join."""
        self.plugin_dir = plugin_dir
        self.csv_path = os.path.join(plugin_dir, "comuniANPR_ISTAT.csv")
        
    def perform_join(self, output_gpkg):
        """Esegue la join tra il file GPKG e il CSV ANPR-ISTAT."""
        if not os.path.exists(self.csv_path):
            return False, f"File CSV non trovato: {self.csv_path}"
            
        if not os.path.exists(output_gpkg):
            return False, f"File GPKG non trovato: {output_gpkg}"
            
        try:
            # Carica il file CSV
            df_anpr = pd.read_csv(self.csv_path)
            
            # Carica il file GPKG
            gdf = gpd.read_file(output_gpkg)
            
            # Lista delle colonne per diagnostica
            columns_info = f"Colonne nel GPKG: {', '.join(gdf.columns)}"
            
            # Verifica se esistono i campi necessari
            if "ADMINISTRATIVEUNIT" not in gdf.columns:
                return False, f"Campo 'ADMINISTRATIVEUNIT' non presente nel file GPKG. {columns_info}"
                
            if "CODCATASTALE" not in df_anpr.columns:
                return False, "Campo 'CODCATASTALE' non presente nel file CSV"
                
            if "DENOMINAZIONE_IT" not in df_anpr.columns or "SIGLAPROVINCIA" not in df_anpr.columns:
                return False, "Campi richiesti non presenti nel file CSV"
                
            # Esegue la join
            gdf = gdf.merge(
                df_anpr[["CODCATASTALE", "DENOMINAZIONE_IT", "SIGLAPROVINCIA"]], 
                left_on="ADMINISTRATIVEUNIT", 
                right_on="CODCATASTALE", 
                how="left"
            )
            
            # Salva il risultato sovrascrivendo il file originale
            gdf.to_file(output_gpkg, driver="GPKG")
            
            return True, f"Join completata con successo: {output_gpkg}"
            
        except Exception as e:
            return False, f"Errore durante l'esecuzione della join: {str(e)}"
            
    def check_anpr_file(self):
        """Verifica l'esistenza e la struttura del file CSV ANPR-ISTAT."""
        if not os.path.exists(self.csv_path):
            return False, f"File CSV non trovato: {self.csv_path}"
            
        try:
            # Verifica struttura del CSV
            df_sample = pd.read_csv(self.csv_path, nrows=5)
            required_fields = ["CODCATASTALE", "DENOMINAZIONE_IT", "SIGLAPROVINCIA"]
            missing_fields = [field for field in required_fields if field not in df_sample.columns]
            
            if missing_fields:
                return False, f"Campi mancanti nel CSV: {', '.join(missing_fields)}"
            
            return True, "File ANPR-ISTAT verificato correttamente"
        except Exception as e:
            return False, f"Errore durante la verifica del file ANPR: {str(e)}"