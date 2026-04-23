# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CatastoIT_GML_Merger_Pro** is a QGIS plugin for downloading, extracting, and merging Italian cadastral GML files. The plugin handles both map files (MAP) and parcel files (PLE), converting them to GPKG format with automatic field extraction (sheet and parcel numbers).

## Architecture

This is a QGIS plugin built using the PyQt framework following the standard QGIS plugin structure:

### Core Components

- **CatastoIT_GML_Merger_Pro.py**: Contains two classes — `CatastoIT_GML_Merger_Pro` (QGIS entry point: toolbar, menu, `run()`) and `GmlProcessingTask(QgsTask)` (all background processing: download, extraction, merge, field calc, CRS fix). All GPKG manipulation inside `GmlProcessingTask` must use pure sqlite3, never `QgsVectorLayer`.
- **CatastoIT_GML_Merger_Pro_dialog.py**: UI dialog class built from the .ui file; handles region/province/comuni widgets, transfer widget logic, and user input collection.
- **CatastoIT_GML_Merger_Pro_dialog_base.ui**: Qt Designer UI file — edit with Qt Designer, do not hand-edit.
- **regions.py**: Italian regions and provinces mapping (REGIONS list and PROVINCES_BY_REGION dictionary).
- **comuni.py**: Lookup table for 7904 comuni × 107 province (codice Belfiore → nome, sigla provincia).
- **resources.py**: Qt resource binary — compiled from PyQt5's `pyrcc5`, uses `from qgis.PyQt import QtCore` for Qt6 compatibility. Contains only the toolbar icon (icon.png). Do not regenerate unless the icon changes.
- **__init__.py**: Plugin initialization and metadata.

### Key Data Processing Flow

1. **Download**: Fetches regional ZIP files from geodati.gov.it URLs
2. **Extraction**: Decompresses province and municipality ZIP files with memory optimization
3. **Merging**: Combines GML files using a 3-level fallback: (1) `native:mergevectorlayers` on all valid files at once; (2) `merge_files_alternative` — batch merge in chunks of 10, with per-batch fallback to GDAL; (3) individual files collected directly if both strategies fail.
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
- `reproject_layer()` writes a new file with CRS suffix (e.g. `output_EPSG_32632.gpkg`) — it does not reproject in-place. The caller must handle the returned path.
- `QgsVectorLayer` is used in the background thread only for validating GML source files before merge (read-only, not stored). All write/modify operations on GPKG go through sqlite3.

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
Only needed if `icon.png` changes — `resources.py` contains the compiled icon binary:
- `pyrcc5 -o resources.py resources.qrc`
- The output uses `from qgis.PyQt import QtCore` (not `from PyQt5 import QtCore`) for Qt6 compatibility — verify after regenerating.
- Qt Designer for editing `CatastoIT_GML_Merger_Pro_dialog_base.ui`

### Releasing
Load the GitHub token before any `curl`/`gh` API call:
```bash
export $(grep -v '^#' .env | xargs)
```
Bump `version=` in `metadata.txt` (single source of truth) and update `changelog=` before tagging.

## Key Dependencies

- QGIS 3.22+ with PyQt5/6
- Python 3.7+ with standard libraries (urllib, zipfile, tempfile, sqlite3, etc.)
- QGIS processing framework
- GDAL/OGR for spatial data handling

## Configuration Notes

- Plugin metadata in `metadata.txt` defines QGIS compatibility — **single source of truth for version**
- Regional data URLs are hardcoded in `GmlProcessingTask.run()` (no config file)
- `.env` file stores `GITHUB_TOKEN` (not tracked by git) — load with `export $(grep -v '^#' .env | xargs)` before any GitHub API call; never hardcode the token value
- Plugin creates temporary directories during processing with automatic cleanup on dialog close
- `ple_style.qml` is applied to PLE layers at load time; contains rule-based renderer (transparent parcels, grey roads, blue water)