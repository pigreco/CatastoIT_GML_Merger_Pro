import os
import tempfile
import time
import gc
from datetime import datetime

from ..core.downloader import CatastoDownloader
from ..core.extractor import CatastoExtractor
from ..core.reprojector import CatastoReprojector
from ..utils.file_utils import ensure_directory_exists, cleanup_temp_files

class GmlProcessor:
    """Gestisce l'elaborazione completa dei file GML"""
    
    def __init__(self, task):
        self.task = task
        self.downloader = CatastoDownloader(task)
        self.extractor = CatastoExtractor(task)
        self.reprojector = CatastoReprojector(task)
        
    def process(self):
        """Esegue il processo completo di elaborazione"""
        temp_dir = None
        try:
            # Creazione directory temporanea
            temp_dir = tempfile.mkdtemp()
            self.task.directory_temporanea = temp_dir
            self.task.log_message.emit(f"Directory temporanea creata: {temp_dir}\n")
            
            # Creazione cartelle output
            map_folder = os.path.join(temp_dir, "map_files")
            ple_folder = os.path.join(temp_dir, "ple_files")
            
            if self.task.inputs["file_type"] in ["Mappe (MAP)", "Entrambi"]:
                os.makedirs(map_folder, exist_ok=True)
            
            if self.task.inputs["file_type"] in ["Particelle (PLE)", "Entrambi"]:
                os.makedirs(ple_folder, exist_ok=True)
            
            # Download file
            main_zip_path = self.downloader.download_main_zip(
                self.task.inputs["url"], temp_dir)
            
            if not main_zip_path or not os.path.exists(main_zip_path):
                self.task.log_message.emit("Download fallito")
                return False
            
            # Estrai e processa i file
            map_count, ple_count = self.extractor.process_main_zip(
                main_zip_path, 
                self.task.inputs.get("province_code", "").split(','),
                map_folder, ple_folder, 
                self.task.inputs["file_type"]
            )
            
            self.task.log_message.emit(f"Elaborazione completata: trovati {map_count} file MAP e {ple_count} file PLE")
            
            # Riproiezione dei file se necessario
            if self.task.inputs.get("reproject", False):
                output_crs = self.task.inputs.get("output_crs", "EPSG:3857")
                self.task.log_message.emit(f"Avvio riproiezione dei file al sistema di coordinate {output_crs}")
                
                if self.task.inputs["file_type"] in ["Mappe (MAP)", "Entrambi"] and map_count > 0:
                    self.reprojector.reproject_files(map_folder, output_crs, "MAP")
                    
                if self.task.inputs["file_type"] in ["Particelle (PLE)", "Entrambi"] and ple_count > 0:
                    self.reprojector.reproject_files(ple_folder, output_crs, "PLE")
                    
                self.task.log_message.emit("Riproiezione completata")
            
            # Creazione directory di output finale
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_output_dir = os.path.join(self.task.inputs["output_directory"], f"catasto_export_{timestamp}")
            ensure_directory_exists(final_output_dir)
            
            # Copia dei file elaborati nella directory di output finale
            if self.task.inputs["file_type"] in ["Mappe (MAP)", "Entrambi"] and map_count > 0:
                map_output = os.path.join(final_output_dir, "mappe")
                ensure_directory_exists(map_output)
                self.task.log_message.emit(f"Copia dei file MAP in {map_output}")
                for file in os.listdir(map_folder):
                    if os.path.isfile(os.path.join(map_folder, file)):
                        os.rename(os.path.join(map_folder, file), os.path.join(map_output, file))
            
            if self.task.inputs["file_type"] in ["Particelle (PLE)", "Entrambi"] and ple_count > 0:
                ple_output = os.path.join(final_output_dir, "particelle")
                ensure_directory_exists(ple_output)
                self.task.log_message.emit(f"Copia dei file PLE in {ple_output}")
                for file in os.listdir(ple_folder):
                    if os.path.isfile(os.path.join(ple_folder, file)):
                        os.rename(os.path.join(ple_folder, file), os.path.join(ple_output, file))
            
            self.task.log_message.emit(f"Elaborazione completata con successo. File disponibili in: {final_output_dir}")
            return True
            
        except Exception as e:
            self.task.log_message.emit(f"Errore durante l'elaborazione: {str(e)}")
            import traceback
            self.task.log_message.emit(f"Dettagli: {traceback.format_exc()}")
            self.task.exception = e
            return False
        finally:
            # Pulizia delle risorse temporanee
            if temp_dir and os.path.exists(temp_dir) and self.task.inputs.get("cleanup_temp", True):
                self.task.log_message.emit("Pulizia dei file temporanei...")
                cleanup_temp_files(temp_dir)
                gc.collect()  # Aiuta a liberare memoria