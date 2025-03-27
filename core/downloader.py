import os
import urllib.request
import urllib.parse
import time
from datetime import datetime
import shutil
import ssl
import certifi
import socket
import traceback

class CatastoDownloader:
    """Gestisce il download dei file dal servizio catastale"""
    
    def __init__(self, task):
        self.task = task  # riferimento al task principale
        self.context = ssl.create_default_context(cafile=certifi.where())
        self.timeout = 180  # aumento timeout a 180 secondi
        # Disabilita la verifica del certificato solo se necessario
        # self.context.check_hostname = False
        # self.context.verify_mode = ssl.CERT_NONE
    
    def download_main_zip(self, url, destination_folder):
        """Scarica il file ZIP principale"""
        self.task.log_message.emit(f"Download del file zip principale: {url}")
        self.task.log_message.emit("Verifica del collegamento internet...")
        self.task.setProgress(5)  # 5% dopo inizializzazione
        
        # Controlla se l'URL è valido
        if not url or not url.startswith('http'):
            self.task.log_message.emit("URL non valido. Verifica l'indirizzo di download.")
            return None
            
        # Controlla se la connessione internet è attiva
        if not self._check_internet_connection():
            self.task.log_message.emit("Impossibile connettersi a internet. Verifica la tua connessione.")
            return None
            
        main_zip_path = os.path.join(destination_folder, "downloaded.zip")
        start_time = datetime.now()
        
        # Prima verifica se l'URL esiste
        self.task.log_message.emit("Verifica esistenza dell'URL...")
        if not self.check_url_exists(url):
            self.task.log_message.emit(f"URL non raggiungibile: {url}")
            return None
        
        self.task.log_message.emit("Avvio download...")
        
        try:
            # Tenta il download con retry automatico
            success = self.download_with_retry(url, main_zip_path, max_retries=3, retry_delay=5)
            
            if not success:
                self.task.log_message.emit("Download fallito dopo i tentativi.")
                return None
                
            download_time = datetime.now() - start_time
            file_size = os.path.getsize(main_zip_path)
            
            self.task.log_message.emit(f"Download completato in {download_time}. Dimensione file: {self._format_size(file_size)}")
            self.task.setProgress(15)  # 15% dopo download
            
            # Verifica dimensione del file
            if file_size < 1000:  # Verifica che il file non sia troppo piccolo (probabilmente un errore)
                self.task.log_message.emit(f"Attenzione: il file scaricato è molto piccolo ({file_size} bytes). Potrebbe essere un errore.")
                # Controlla contenuto per vedere se è una pagina di errore
                with open(main_zip_path, 'r', errors='ignore') as f:
                    content_preview = f.read(500)
                    if '<html' in content_preview.lower() or '<!doctype' in content_preview.lower():
                        self.task.log_message.emit("Il file scaricato è una pagina HTML di errore, non un file ZIP.")
                        if "404" in content_preview:
                            self.task.log_message.emit("Errore 404: File non trovato sul server.")
                        elif "403" in content_preview:
                            self.task.log_message.emit("Errore 403: Accesso negato. Verifica che l'URL sia corretto e accessibile.")
                        elif "500" in content_preview:
                            self.task.log_message.emit("Errore 500: Errore interno del server.")
                        
                        # Rimuovi il file di errore
                        if os.path.exists(main_zip_path):
                            os.remove(main_zip_path)
                        return None
                
            return main_zip_path
        except Exception as e:
            self.task.log_message.emit(f"Errore durante il download: {str(e)}")
            self.task.log_message.emit(f"Dettagli: {traceback.format_exc()}")
            if os.path.exists(main_zip_path):
                os.remove(main_zip_path)  # Rimuovi file parziale in caso di errore
            return None
    
    def _check_internet_connection(self):
        """Verifica se la connessione internet è attiva."""
        try:
            # Tenta di connettersi a Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            try:
                # Prova un'alternativa se Google DNS non è raggiungibile
                socket.create_connection(("1.1.1.1", 53), timeout=5)
                return True
            except OSError:
                return False
    
    def download_with_retry(self, url, dest_path, max_retries=3, retry_delay=5):
        """Scarica un file con supporto per tentativi multipli in caso di errore."""
        self.task.log_message.emit(f"Download del file: {os.path.basename(dest_path)}")
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Utilizzo direttamente urllib senza la funzione download_with_progress per maggiore affidabilità
                self.task.log_message.emit(f"Tentativo {retry_count+1} di {max_retries}...")
                
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(req, timeout=self.timeout, context=self.context) as response:
                    total_size = int(response.headers.get('Content-Length', 0))
                    if total_size > 0:
                        self.task.log_message.emit(f"Dimensione totale del file: {self._format_size(total_size)}")
                    
                    # Rimuovi il file se esiste già
                    if os.path.exists(dest_path):
                        os.remove(dest_path)
                    
                    # Download con aggiornamento progressivo
                    downloaded = 0
                    block_size = 1024 * 1024  # 1MB per blocco
                    last_progress = -1
                    
                    with open(dest_path, 'wb') as out_file:
                        while True:
                            buffer = response.read(block_size)
                            if not buffer:
                                break
                                
                            downloaded += len(buffer)
                            out_file.write(buffer)
                            
                            # Aggiorna progresso solo quando cambia del 5%
                            if total_size > 0:
                                progress = int(downloaded * 100 / total_size)
                                if progress % 5 == 0 and progress != last_progress:
                                    self.task.log_message.emit(f"Download in corso: {progress}% completato")
                                    last_progress = progress
                
                # Verifica che il file esista e non sia vuoto
                if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                    self.task.log_message.emit("Download completato con successo.")
                    return True
                else:
                    raise Exception("File scaricato vuoto o non valido")
                    
            except Exception as e:
                retry_count += 1
                if os.path.exists(dest_path):
                    os.remove(dest_path)  # Rimuovi file parziale in caso di errore
                
                if retry_count < max_retries:
                    self.task.log_message.emit(f"Tentativo {retry_count} fallito: {str(e)}. Nuovo tentativo tra {retry_delay} secondi...")
                    time.sleep(retry_delay)
                else:
                    self.task.log_message.emit(f"Download fallito dopo {max_retries} tentativi: {str(e)}")
                    return False
    
    def check_url_exists(self, url):
        """Verifica se un URL esiste senza scaricare l'intero contenuto."""
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30, context=self.context) as response:
                return response.getcode() == 200
        except Exception as e:
            self.task.log_message.emit(f"Errore nella verifica URL: {str(e)}")
            return False
    
    def _format_size(self, size_bytes):
        """Formatta una dimensione in bytes in un formato leggibile."""
        if size_bytes < 0:
            return "Unknown"
        elif size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.1f} GB"