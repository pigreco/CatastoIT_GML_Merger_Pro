import os
import time
import processing
from qgis.core import QgsCoordinateReferenceSystem

class CatastoReprojector:
    """Gestisce la riproiezione dei layer"""
    
    def __init__(self, task):
        self.task = task
    
    def reproject_layer(self, input_file, target_crs, file_type):
        """Riproietta un layer vettoriale nel CRS specificato"""
        try:
            self.task.log_message.emit(f"Riproiezione del layer {file_type} nel sistema {target_crs}...")
            
            # Crea il nome file di output
            create_output_name = lambda base, ext, crs: f"{base}_{crs.replace(':', '_')}{ext}"
            
            basename = os.path.splitext(input_file)[0]
            extension = os.path.splitext(input_file)[1]
            output_file = create_output_name(basename, extension, target_crs)
            
            # Gestione file esistenti
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                    self.task.log_message.emit(f"File riproiettato esistente rimosso: {os.path.basename(output_file)}")
                except Exception as e:
                    self.task.log_message.emit(f"ATTENZIONE: Impossibile rimuovere il file riproiettato esistente: {str(e)}")
                    # Usa timestamp per evitare conflitti
                    output_file = f"{basename}_{target_crs.replace(':', '_')}_{int(time.time())}{extension}"
            
            # Parametri riproiezione
            create_reproject_params = lambda input_file, target_crs, output_file: {
                'INPUT': input_file,
                'TARGET_CRS': target_crs,
                'OUTPUT': output_file
            }
            
            params = create_reproject_params(input_file, target_crs, output_file)
            
            # Esegui la riproiezione
            result = processing.run("native:reprojectlayer", params)
            output_file = result['OUTPUT']
            
            self.task.log_message.emit(f"Riproiezione completata: {os.path.basename(output_file)}")
            return output_file
        except Exception as e:
            self.task.log_message.emit(f"ERRORE durante la riproiezione del layer {file_type}: {str(e)}")
            import traceback
            self.task.log_message.emit(f"Dettagli: {traceback.format_exc()}")
            return None