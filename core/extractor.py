import os
import io
import shutil
from zipfile import ZipFile
import gc
from datetime import datetime

class CatastoExtractor:
    """Gestisce l'estrazione dei file dai ZIP annidati"""
    
    def __init__(self, task):
        self.task = task
        self.extracted_files = set()
    
    def process_main_zip(self, main_zip_path, province_codes, map_folder, ple_folder, file_type):
        """Elabora il file ZIP principale ed estrae i file GML filtrati per provincia"""
        map_count = ple_count = 0
        self.task.log_message.emit("Elaborazione file...")
        
        self.task.setProgress(20)  # 20% prima dell'estrazione
        
        # Implementazione dell'estrazione con filtri per provincia e tipo di file
        is_matching_province = lambda prov_name, codes: any(code in prov_name.upper() for code in codes)
        is_required_file = lambda filename, filetype: \
            (("_ple" in filename.lower() and filetype in ["Particelle (PLE)", "Entrambi"]) or \
             ("_map" in filename.lower() and filetype in ["Mappe (MAP)", "Entrambi"]))
        
        try:
            with ZipFile(main_zip_path) as main_zip:
                # Estrazione dei file delle province
                province_zips = []
                for file_info in main_zip.infolist():
                    if file_info.filename.endswith('.zip'):
                        province_zips.append(file_info)
                
                # Calcola le province filtrate in base ai codici forniti
                filtered_province_zips = []
                for prov_zip_info in province_zips:
                    prov_name = os.path.basename(prov_zip_info.filename)
                    if not province_codes or is_matching_province(prov_name, province_codes):
                        filtered_province_zips.append(prov_zip_info)
                        self.task.log_message.emit(f"Provincia trovata: {prov_name}")
                
                # Imposta avanzamento in base al numero di province
                total_provinces = len(filtered_province_zips)
                if total_provinces == 0:
                    self.task.log_message.emit("Nessuna provincia corrispondente trovata!")
                    return 0, 0
                
                province_progress_step = 60 / total_provinces  # 60% del totale per estrazione (da 20% a 80%)
                current_progress = 20
                
                # Processa ogni provincia
                for i, prov_zip_info in enumerate(filtered_province_zips):
                    prov_name = os.path.basename(prov_zip_info.filename)
                    self.task.log_message.emit(f"\nEstrazione provincia {i+1}/{total_provinces}: {prov_name}")
                    
                    if self.task.isCanceled():
                        self.task.log_message.emit("Elaborazione interrotta dall'utente")
                        return map_count, ple_count
                    
                    # Estrai ZIP provincia in memoria
                    with io.BytesIO(main_zip.read(prov_zip_info)) as prov_buffer:
                        # Gestisci i comuni nel file ZIP della provincia
                        map_count_prov, ple_count_prov = self.process_province_zip(
                            prov_buffer, prov_name, map_folder, ple_folder, file_type)
                        
                        map_count += map_count_prov
                        ple_count += ple_count_prov
                    
                    # Aggiorna progresso
                    current_progress += province_progress_step
                    self.task.setProgress(int(current_progress))
                    
                    # Forza garbage collection periodicamente
                    if i % 5 == 0:
                        gc.collect()
            
            self.task.setProgress(80)  # 80% dopo estrazione completa
            self.task.log_message.emit(f"\nEstrazione completata: {map_count} file MAP e {ple_count} file PLE trovati.")
            return map_count, ple_count
            
        except Exception as e:
            self.task.log_message.emit(f"Errore durante l'elaborazione del file ZIP principale: {str(e)}")
            import traceback
            self.task.log_message.emit(f"Dettagli: {traceback.format_exc()}")
            return map_count, ple_count
    
    def process_province_zip(self, province_buffer, province_name, map_folder, ple_folder, file_type):
        """Elabora il file ZIP di una provincia ed estrae i file GML dei comuni"""
        map_count = ple_count = 0
        
        try:
            with ZipFile(province_buffer) as province_zip:
                # Estrai i file dei comuni
                comuni_zips = []
                for file_info in province_zip.infolist():
                    if file_info.filename.endswith('.zip'):
                        comuni_zips.append(file_info)
                
                total_comuni = len(comuni_zips)
                if total_comuni == 0:
                    self.task.log_message.emit(f"Nessun comune trovato nella provincia {province_name}")
                    return 0, 0
                
                # Processa ogni comune
                for comune_zip_info in comuni_zips:
                    comune_name = os.path.basename(comune_zip_info.filename)
                    
                    if self.task.isCanceled():
                        self.task.log_message.emit("Elaborazione interrotta dall'utente")
                        return map_count, ple_count
                    
                    # Estrai ZIP comune in memoria
                    with io.BytesIO(province_zip.read(comune_zip_info)) as comune_buffer:
                        map_count_comune, ple_count_comune = self.extract_gml_files(
                            comune_buffer, comune_name, map_folder, ple_folder, file_type)
                        
                        map_count += map_count_comune
                        ple_count += ple_count_comune
                
                return map_count, ple_count
                
        except Exception as e:
            self.task.log_message.emit(f"Errore durante l'elaborazione della provincia {province_name}: {str(e)}")
            return map_count, ple_count
    
    def extract_gml_files(self, comune_buffer, comune_name, map_folder, ple_folder, file_type):
        """Estrae i file GML da uno ZIP comunale"""
        map_count = ple_count = 0
        
        try:
            with ZipFile(comune_buffer) as comune_zip:
                # Filtra i file GML
                gml_files = [f for f in comune_zip.infolist() if f.filename.lower().endswith('.gml')]
                
                # Funzione per determinare il tipo di file
                is_map_file = lambda filename: "_map" in filename.lower()
                is_ple_file = lambda filename: "_ple" in filename.lower()
                
                # Estrai i file GML nelle cartelle appropriate
                for gml_info in gml_files:
                    file_name = os.path.basename(gml_info.filename)
                    
                    if is_map_file(file_name) and file_type in ["Mappe (MAP)", "Entrambi"]:
                        target_path = os.path.join(map_folder, file_name)
                        if not os.path.exists(target_path):
                            with open(target_path, 'wb') as f:
                                f.write(comune_zip.read(gml_info))
                            map_count += 1
                            
                    elif is_ple_file(file_name) and file_type in ["Particelle (PLE)", "Entrambi"]:
                        target_path = os.path.join(ple_folder, file_name)
                        if not os.path.exists(target_path):
                            with open(target_path, 'wb') as f:
                                f.write(comune_zip.read(gml_info))
                            ple_count += 1
                
                return map_count, ple_count
                
        except Exception as e:
            self.task.log_message.emit(f"Errore durante l'estrazione dei file GML dal comune {comune_name}: {str(e)}")
            return map_count, ple_count