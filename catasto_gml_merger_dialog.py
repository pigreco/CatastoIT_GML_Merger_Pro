# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CatastoIT_GML_Merger_ProDialog
                                 A QGIS plugin CatastoIT_GML_Merger_Pro
                                 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2025-02-10
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Salvatore Fiandaca
        email                : Salvatore Fiandaca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QProgressBar, QPushButton
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from .regions import REGIONS, get_provinces

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'catasto_gml_merger_dialog_base.ui'))


class catasto_gml_mergerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(catasto_gml_mergerDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Aggiungi il pulsante di minimizzazione
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)
        
        # Aggiungi ProgressBar e pulsante di annullamento
        if not hasattr(self, 'progressBar'):
            self.progressBar = QProgressBar(self)
            self.progressBar.setVisible(False)
            self.layout().addWidget(self.progressBar)
            
        if not hasattr(self, 'btn_cancel'):
            self.btn_cancel = QPushButton("Annulla", self)
            self.btn_cancel.setVisible(False)
            self.btn_cancel.clicked.connect(self.cancel_operation)
            self.layout().addWidget(self.btn_cancel)
            
        # Configura il pulsante per mostrare/nascondere la guida
        self.btn_toggle_help.clicked.connect(self.toggle_help_panel)
        
        # Popola il combobox delle regioni
        self.populate_regions()
        
        # Imposta i filtri per i file di output
        self.le_map_output.setFilter('*.gpkg')
        self.le_ple_output.setFilter('*.gpkg')
        
        def updateFileType():
            ext = self.cb_format.currentText().lower()
            self.le_map_output.setFilter('*.' + ext)
            self.le_ple_output.setFilter('*.' + ext)
            
            if self.le_map_output.filePath():
                base_path = self.le_map_output.filePath().split('.')[0]
                self.le_map_output.setFilePath(base_path + '.' + ext)
            
            if self.le_ple_output.filePath():
                base_path = self.le_ple_output.filePath().split('.')[0]
                self.le_ple_output.setFilePath(base_path + '.' + ext)
        
        # Connetti il segnale alla funzione
        self.cb_format.currentTextChanged.connect(updateFileType)
        
        # Connetti il cambio di regione all'aggiornamento delle province
        self.cb_region.currentTextChanged.connect(self.update_provinces)
        
    def closeEvent(self, event):
        # dir_path = directory_temporanea

        # try:
            # shutil.rmtree(dir_path)
            # log_message(f"directory {dir_path} rimossa correttamente")
        # except OSError as e:
           # log_message("\nError: %s : %s" % (dir_path, e.strerror))

        self.le_folder.setFilePath("")
        self.le_map_output.setFilePath("")
        self.le_ple_output.setFilePath("")
        self.cb_file_type.setCurrentIndex(0)
        self.cb_format.setCurrentIndex(0)
        self.cb_region.setCurrentIndex(0)
        self.le_url.clear()
        self.text_log.clear()
        
        print("close!")

    def populate_regions(self):
        """Popola il combobox delle regioni."""
        self.cb_region.clear()
        self.cb_region.addItems(REGIONS)

    def get_selected_region(self):
        """Restituisce la regione selezionata."""
        return self.cb_region.currentText()
    
    def update_provinces(self):
        """Aggiorna il combobox delle province in base alla regione selezionata."""
        region = self.cb_region.currentText()
        provinces = get_provinces(region)
        
        self.list_provinces.clear()
        self.list_provinces.addItems(provinces)

    def cancel_operation(self):
        """Gestisce l'evento di annullamento dell'operazione in corso."""
        self.btn_cancel.setVisible(False)
        self.progressBar.setVisible(False)
        # Aggiungi qui il codice per interrompere qualsiasi operazione in corso
        self.text_log.append("Operazione annullata dall'utente.")
        
    def example_usage(self):
        """Esempio di utilizzo della progress bar e del pulsante di annullamento."""
        self.progressBar.setVisible(True)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.btn_cancel.setVisible(True)

        # Durante l'elaborazione
        self.progressBar.setValue(50)  # aggiorna il valore

        # A operazione completata
        self.progressBar.setVisible(False)
        self.btn_cancel.setVisible(False)
        
    def toggle_help_panel(self):
        """Gestisce la visualizzazione/nascondimento del pannello della guida."""
        if self.help_browser.isVisible():
            self.help_browser.hide()
            self.btn_toggle_help.setIcon(QIcon(":/qt-project.org/styles/commonstyle/images/right-32.png"))
            self.btn_toggle_help.setToolTip("Mostra guida")
        else:
            self.help_browser.show()
            self.btn_toggle_help.setIcon(QIcon(":/qt-project.org/styles/commonstyle/images/left-32.png"))
            self.btn_toggle_help.setToolTip("Nascondi guida")
