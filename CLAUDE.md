# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CatastoIT_GML_Merger_Pro** is a QGIS plugin for downloading, extracting, and merging Italian cadastral GML files. The plugin handles both map files (MAP) and parcel files (PLE), converting them to GPKG format with automatic field extraction (sheet and parcel numbers).

## Architecture

This is a QGIS plugin built using the PyQt framework following the standard QGIS plugin structure:

### Core Components

- **CatastoIT_GML_Merger_Pro.py**: Main plugin class that handles QGIS integration, toolbar/menu setup, and orchestrates the data processing workflow
- **CatastoIT_GML_Merger_Pro_dialog.py**: UI dialog class that manages the user interface built from the .ui file
- **CatastoIT_GML_Merger_Pro_dialog_base.ui**: Qt Designer UI file defining the plugin's graphical interface
- **regions.py**: Data module containing Italian regions and provinces mapping (REGIONS list and PROVINCES_BY_REGION dictionary)
- **resources.py**: Qt resource file generated from .qrc files containing embedded resources
- **__init__.py**: Plugin initialization and metadata

### Key Data Processing Flow

1. **Download**: Fetches regional ZIP files from geodati.gov.it URLs
2. **Extraction**: Decompresses province and municipality ZIP files with memory optimization
3. **Merging**: Combines GML files into unified datasets
4. **Conversion**: Transforms to GPKG format with automatic field calculation
5. **Loading**: Optionally loads results into QGIS with predefined styling

### Data Processing Features

- Downloads from RNDT (Repertorio Nazionale Dati Territoriali) at geodati.gov.it
- Handles both MAP (cadastral maps) and PLE (parcels) file types
- Extracts and adds calculated fields: Foglio (sheet), Particella (parcel), sez_censuaria (census section)
- Supports CRS reprojection from native RDN2008/ETRF2000 (EPSG:7794)
- Background processing with progress logging
- Temporary directory management with automatic cleanup

## Development Commands

This is a QGIS plugin project with no build system or testing framework. Development involves:

### Plugin Installation
- Copy plugin directory to QGIS plugins folder: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- Enable plugin in QGIS Plugin Manager
- Restart QGIS to load changes

### Testing
- Manual testing within QGIS environment
- Test with different Italian regions and province combinations
- Verify GPKG output and field calculations

### Resource Compilation
If modifying UI or resources, use QGIS development tools:
- `pyrcc5 -o resources.py resources.qrc` (if resources.qrc exists)
- Qt Designer for editing .ui files

## Key Dependencies

- QGIS 3.22+ with PyQt5/6
- Python 3.7+ with standard libraries (urllib, zipfile, tempfile, etc.)
- QGIS processing framework
- GDAL/OGR for spatial data handling

## Configuration Notes

- Plugin metadata in metadata.txt defines QGIS compatibility and plugin information
- Regional data URLs are hardcoded in processing logic
- No external configuration files or environment setup required
- Plugin creates temporary directories during processing with automatic cleanup on dialog close