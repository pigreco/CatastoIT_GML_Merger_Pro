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
- **comuni.py**: Lookup table for 7904 comuni × 107 province (codice Belfiore → nome, sigla provincia)
- **resources.py**: Qt resource file generated from .qrc files containing embedded resources
- **__init__.py**: Plugin initialization and metadata

### Key Data Processing Flow

1. **Download**: Fetches regional ZIP files from geodati.gov.it URLs
2. **Extraction**: Decompresses province and municipality ZIP files with memory optimization
3. **Merging**: Combines GML files into unified datasets using 3-level fallback strategy
4. **Field calculation**: Adds foglio, particella, sez_censuaria, comune via pure sqlite3 (thread-safe)
5. **CRS fix**: Labels GPKG as EPSG:4326 to fix axis order issue with GDAL 3.12+/PROJ 9.7+
6. **Loading**: Optionally loads results into QGIS with predefined styling

### Data Processing Features

- Downloads from RNDT (Repertorio Nazionale Dati Territoriali) at geodati.gov.it
- Handles both MAP (cadastral maps) and PLE (parcels) file types
- Extracts and adds calculated fields: Foglio (sheet), Particella (parcel), sez_censuaria (census section), comune
- Optional filtering by comune (codice Belfiore)
- Output granularity: unico file / un file per provincia / un file per comune
- CRS: native data is EPSG:6706 (RDN2008); GPKG labeled as EPSG:4326 (same coordinates, <1m diff for Italy)
- Background processing (QgsTask) with progress logging — no Qt objects in background thread
- Temporary directory management with automatic cleanup

### Output Granularity

- **Unico**: single output file per type; name includes province suffix + optional comuni codes
- **Per provincia**: one file per province; `{base}_{PROV}.gpkg`; no province/comuni suffix on base
- **Per comune**: one file per comune; `{base}_{PROV}_{BELFIORE}.gpkg`; no province/comuni suffix on base

### Known Technical Notes

- GPKG R-tree triggers use `ST_IsEmpty()` (SpatiaLite), unavailable in plain sqlite3.
  Fix: drop all triggers on the table before `executemany UPDATE`, recreate not needed (geometry unchanged).
- EPSG:6706 with GDAL 3.12+ produces `Data axis to CRS axis mapping: 2,1` → layer invisible with OSM background.
  Fix: label GPKG as EPSG:4326 via sqlite3 after merge.
- Destroying `QgsVectorLayer` in a `QgsTask` background thread causes access violation on Windows.
  Fix: use pure sqlite3 for all GPKG manipulation in background tasks.
- Signal connections in `run()` must be disconnected before reconnecting to prevent duplicate task spawning.

## Development Commands

This is a QGIS plugin project with no build system or testing framework. Development involves:

### Plugin Installation
- Copy plugin directory to QGIS plugins folder: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\` (Windows)
- Enable plugin in QGIS Plugin Manager
- Restart QGIS to load changes

### Testing
- Manual testing within QGIS environment
- Test all three output granularities (unico, per provincia, per comune) with and without comuni filter
- Verify GPKG output, field calculations, and layer visibility with OSM background

### Resource Compilation
If modifying UI or resources, use QGIS development tools:
- `pyrcc5 -o resources.py resources.qrc` (if resources.qrc exists)
- Qt Designer for editing .ui files

## Key Dependencies

- QGIS 3.22+ with PyQt5/6
- Python 3.7+ with standard libraries (urllib, zipfile, tempfile, sqlite3, etc.)
- QGIS processing framework
- GDAL/OGR for spatial data handling

## Configuration Notes

- Plugin metadata in `metadata.txt` defines QGIS compatibility — **single source of truth for version**
- Regional data URLs are hardcoded in processing logic
- `.env` file stores `GITHUB_TOKEN` (not tracked by git)
- Plugin creates temporary directories during processing with automatic cleanup on dialog close