# Inserisci questo nel metodo run() della classe GmlProcessingTask

def run(self):
    """Esegue l'elaborazione in background"""
    try:
        # Imposta il flag di cancellazione
        self.killswitch = False
        
        self.log_message.emit("Inizializzazione processore GML...")
        processor = GmlProcessor(self)
        
        # Log dell'avvio con timestamp
        start_time = datetime.now()
        self.log_message.emit(f"Avvio elaborazione: {start_time.strftime('%H:%M:%S')}")
        
        # Elabora i dati
        success = processor.process()
        
        # Log della conclusione con tempo impiegato
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        
        if success:
            self.log_message.emit(f"<span style='color:green;font-weight:bold;'>Elaborazione completata con successo in {elapsed_time}</span>")
        else:
            self.log_message.emit(f"<span style='color:red;font-weight:bold;'>Elaborazione completata con errori in {elapsed_time}</span>")
        
        # Notifica completamento
        self.task_completed.emit(success)
        return success
        
    except Exception as e:
        import traceback
        self.exception = e
        self.log_message.emit(f"<span style='color:red;font-weight:bold;'>Errore durante l'elaborazione: {str(e)}</span>")
        self.log_message.emit(f"<span style='color:red;'>Dettagli: {traceback.format_exc()}</span>")
        self.task_completed.emit(False)
        return False