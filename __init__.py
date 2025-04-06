# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CatastoIT_GML_Merger_Pro
                                 A QGIS plugin CatastoIT_GML_Merger_Pro
                                 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2025-02-10
        copyright            : (C) 2025 by Salvatore Fiandaca
        email                : Salvatore Fiandaca
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CatastoIT_GML_Merger_Pro class from file CatastoIT_GML_Merger_Pro.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .CatastoIT_GML_Merger_Pro import CatastoIT_GML_Merger_Pro
    return CatastoIT_GML_Merger_Pro(iface)
