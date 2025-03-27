import os
import urllib.request
from datetime import datetime

class CatastoDownloader:
    """Gestisce il download dei file dal servizio catastale"""
    
    def __init__(self, task):
        self.task = task  # riferimento al task principale
    
    def download_main_zip(self, url, destination_folder):
        """Scarica il file ZIP principale"""
        self.task.log_message.emit("Download del file zip principale...")
        self.task.setProgress(5)  # 5% dopo inizializzazione
        
        main_zip_path = os.path.join(destination_folder, "downloaded.zip")
        start_time = datetime.now()
        
        try:
            urllib.request.urlretrieve(url, main_zip_path)
            download_time = datetime.now() - start_time
            self.task.log_message.emit(f"Download completato in {download_time}")
            self.task.setProgress(15)  # 15% dopo download
            return main_zip_path
        except Exception as e:
            self.task.log_message.emit(f"Errore durante il download: {str(e)}")
            return None