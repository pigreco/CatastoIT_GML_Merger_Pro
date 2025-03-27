from qgis.core import QgsTask
from PyQt5.QtCore import pyqtSignal

class GmlProcessingTask(QgsTask):
    """Task base per l'elaborazione dei file GML in background"""
    
    # Definizione dei segnali per comunicare con l'interfaccia
    progress_changed = pyqtSignal(int)
    log_message = pyqtSignal(str)
    task_completed = pyqtSignal(bool, object)
    
    def __init__(self, description, inputs):
        super().__init__(description, QgsTask.CanCancel)
        self.inputs = inputs
        self.directory_temporanea = None
        self.exception = None
        self.processing_times = {}
        self.result = {}
    
    def run(self):
        """Implementazione in core/processor.py"""
        pass
    
    def finished(self, result):
        """Viene chiamato quando il task è completato"""
        self.task_completed.emit(result, self.result)