from qgis.core import QgsTask
from PyQt5.QtCore import pyqtSignal

class GmlProcessingTask(QgsTask):
    """Task base per l'elaborazione dei file GML in background"""
    
    # Definizione dei segnali per comunicare con l'interfaccia
    progress_changed = pyqtSignal(int)
    log_message = pyqtSignal(str)
    task_completed = pyqtSignal(bool, dict)
    
    def __init__(self, description, inputs, expiration=0):
        """
        Costruttore del task di elaborazione GML
        
        :param description: Descrizione del task
        :param inputs: Dizionario con i parametri di input
        :param expiration: Tempo di scadenza del task in millisecondi (0 = nessuna scadenza)
        """
        super().__init__(description, QgsTask.CanCancel, expiration)
        self.inputs = inputs
        self.directory_temporanea = None
        self.exception = None
        self.result = {
            'map_count': 0,
            'ple_count': 0,
            'processing_times': {}
        }
    
    def run(self):
        """Implementazione in core/processor.py"""
        pass
    
    def finished(self, result):
        """Viene chiamato quando il task è completato"""
        self.task_completed.emit(result, self.result)