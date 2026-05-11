# Map Area Tool - Project Documentation

**Version:** 1.0  
**Last Updated:** May 2026  
**Project Type:** Desktop Application (Python/PyQt5)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Purpose and Features](#purpose-and-features)
3. [System Requirements](#system-requirements)
4. [Installation Guide](#installation-guide)
5. [Usage Guide](#usage-guide)
6. [Project Architecture](#project-architecture)
7. [Technical Specifications](#technical-specifications)
8. [Keyboard Shortcuts Reference](#keyboard-shortcuts-reference)
9. [Calculation Methods](#calculation-methods)
10. [Export Functionality](#export-functionality)
11. [Troubleshooting](#troubleshooting)
12. [Development Notes](#development-notes)

---

## Project Overview

**Map Area Tool** is a desktop application designed to measure and calculate the area of regions, rooftops, and structures from Google Maps screenshots. The tool provides an interactive graphical interface for drawing polygons over map regions and precisely calibrating measurements based on map scale bars.

### Key Capabilities

- Extract precise area measurements from map images
- Support for multiple unit conversions (m², ft², yd², km², acres)
- Interactive polygon drawing with real-time validation
- Ruler-based scale calibration system
- Export results in multiple formats (JSON, CSV, TXT)
- Intuitive keyboard shortcuts for efficient workflows
- Zoom and pan functionality for detailed precision work

---

## Purpose and Features

### Primary Use Cases

1. **Real Estate Analysis**: Measure rooftop and property dimensions for solar panel installations, landscaping, or development planning
2. **Urban Planning**: Analyze land plots, green spaces, and infrastructure areas
3. **Surveying**: Quick-reference measurements from satellite imagery
4. **Construction Planning**: Preliminary measurements for project scoping

### Feature Set

| Feature | Description |
|---------|-------------|
| **Scale Calibration** | Two methods: ruler-based measurement or direct pixel-per-meter entry |
| **Polygon Drawing** | Click-based polygon creation with automatic snapping to starting point |
| **Multi-Unit Support** | Convert measurements between m², ft², yd², km², and acres |
| **Bounding Box** | Calculate and display width and height of selected regions |
| **Perimeter Calculation** | Automatic perimeter calculation for drawn polygons |
| **Pan & Zoom** | Navigate large images with scroll and middle-mouse dragging |
| **Undo Functionality** | Step-by-step point removal for error correction |
| **Data Export** | Save measurement results in JSON, CSV, or TXT formats |
| **Command-Line Input** | Open images directly from command line with file path argument |

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.7 or higher
- **RAM**: 2 GB minimum
- **Disk Space**: 50 MB for application and dependencies
- **Display**: 1024×768 resolution minimum (1200×800 recommended)

### Dependencies

The project requires two primary Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| **PyQt5** | ≥5.15.0 | GUI framework for desktop application |
| **Pillow** | ≥9.0.0 | Image processing and rendering |

---

## Installation Guide

### Prerequisites

- Python 3.7+ installed and available in system PATH
- pip package manager (included with Python)
- git (optional, for version control)

### Step-by-Step Installation

#### 1. Clone or Download the Project

```bash
# Using git
git clone <repository-url>
cd map_area_tool

# OR download and extract the ZIP file manually
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
# Test import of required packages
python -c "import PyQt5; import PIL; print('Installation successful!')"
```

### Troubleshooting Installation

**Issue**: "python: command not found"
- **Solution**: Ensure Python is installed and added to PATH. Use `python3` instead on macOS/Linux.

**Issue**: "ModuleNotFoundError: No module named 'PyQt5'"
- **Solution**: Activate virtual environment and run `pip install PyQt5>=5.15.0`

**Issue**: "Permission denied" on macOS/Linux
- **Solution**: Prepend `sudo` to pip command or use a virtual environment.

---

## Usage Guide

### Quick Start

#### Method 1: Using File Dialog

```bash
python main.py
```

A file dialog will open. Select a Google Maps screenshot image file.

#### Method 2: Direct Image Path

```bash
python main.py /path/to/screenshot.png
```

The application opens directly with the specified image loaded.

### Step-by-Step Measurement Workflow

#### Step 1: Calibrate the Scale

Before drawing any measurement polygons, you must calibrate the measurement scale using the scale bar that appears on Google Maps screenshots.

**Process:**

1. Look for the **scale bar** at the bottom-left corner of the map image (typically shows "50 m" or similar)
2. Press **R** key or click **"Measure Scale Bar"** button
3. Click the **left endpoint** of the scale bar in the image
4. Click the **right endpoint** of the scale bar
5. The measured pixel distance will display in the sidebar
6. In the **"Real dist:"** field, enter the distance shown on the scale bar (e.g., `50` for "50 m")
7. Click **"✓ Apply (ruler method)"**
8. Status should change to **"CALIBRATED ✓"** with the calculated px/m value

**Alternative Method - Manual Entry:**

If you know the scale in pixels-per-meter:

1. In the **"px / m:"** field, enter the calculated value
2. Click **"✓ Apply (manual entry)"**

**Calibration Accuracy Notes:**

- Zoom in on the scale bar for maximum precision
- Ensure exact endpoint selection
- Recalibrate if changing map zoom levels
- The accuracy of all subsequent measurements depends on calibration accuracy

#### Step 2: Draw Your Measurement Polygon

Once the scale is calibrated:

1. Press **P** key or click **"Draw Polygon"** button to enter polygon mode
2. **Click points** around the perimeter of the region to measure (rooftop, land plot, etc.)
3. The status bar updates with coordinates as you move the mouse
4. Points snap to the starting point when within the snap radius (10 pixels)

**Closing the Polygon:**

- **Double-click** on the canvas to close the polygon
- Press **Enter** key to close the polygon
- Click near the starting point to snap and close automatically

#### Step 3: Review Measurement Results

The **Results Panel** displays:

| Metric | Description |
|--------|-------------|
| **Area** | Total enclosed area in selected unit |
| **Width** | Horizontal dimension of bounding box |
| **Height** | Vertical dimension of bounding box |
| **Perimeter** | Total boundary length of polygon |

#### Step 4: Convert Units (Optional)

1. Click the **unit dropdown** (default: m²)
2. Select desired unit: ft², yd², km², or acre
3. All measurements automatically convert to the new unit

#### Step 5: Export Results (Optional)

1. Press **Ctrl+E** or click **"Export Results"**
2. Select file format:
   - **JSON**: Full structured data
   - **CSV**: Comma-separated values for spreadsheet import
   - **TXT**: Human-readable text format
3. Choose save location and filename
4. Results file is created with timestamp

### Tips for Accurate Measurements

1. **Zoom Strategy**: Start zoomed out to identify the entire region, then zoom in for precise point placement
2. **Scale Bar Selection**: Use the clearest, most legible scale bar available
3. **Point Precision**: Click slowly and deliberately at precise boundary locations
4. **Undo Usage**: Use Ctrl+Z to remove incorrectly placed points without restarting
5. **Multiple Measurements**: Complete one polygon before starting another (press Esc to clear)

---

## Project Architecture

### Directory Structure

```
map_area_tool/
├── main.py                 # Application entry point and initialization
├── requirements.txt        # Python dependency specifications
├── README.md              # Quick start guide
├── DOCUMENTATION.md       # This comprehensive documentation
├── area_result_*.json     # Generated measurement export files
└── app/
    ├── __init__.py        # Package initialization (empty)
    ├── window.py          # Main window orchestration and logic
    ├── canvas.py          # Drawing canvas and interaction handling
    ├── geometry.py        # Mathematical calculations and unit conversion
    └── panels.py          # UI sidebar panels and controls
```

### Module Responsibilities

#### `main.py` - Application Entry Point

- Initializes QApplication
- Creates main window
- Handles command-line arguments for image path
- Manages application lifecycle

```python
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Map Area Tool")
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(image_path=image_path)
    window.show()
    sys.exit(app.exec_())
```

#### `window.py` - Main Window Orchestration

**Responsibilities:**
- Constructs the complete UI layout (sidebar + canvas)
- Manages application state (scale, points, results)
- Handles keyboard shortcuts and menu actions
- Orchestrates communication between canvas and panels
- Exports measurement results
- Applies visual theme and styling

**Key Classes:**
- `MainWindow(QMainWindow)`: Root application window

**Key Attributes:**
- `_scale_px_per_m`: Current scale calibration (pixels per meter)
- `_current_points`: List of polygon vertices as (x, y) tuples
- `_canvas`: Interactive drawing widget
- `_scale_panel`: Scale calibration UI
- `_results_panel`: Results display UI
- `_tool_panel`: Tool control buttons

#### `canvas.py` - Interactive Drawing Canvas

**Responsibilities:**
- Renders loaded image to screen
- Handles mouse and keyboard input
- Manages polygon drawing state
- Implements zoom and pan functionality
- Implements ruler measurement tool
- Emits signals for external state updates

**Key Classes:**
- `CanvasWidget(QWidget)`: Custom widget for image display and drawing
- `Mode(Enum)`: Operation mode (POLYGON, RULER, PAN)

**Signals:**
- `polygon_changed`: Emits updated point list when polygon changes
- `ruler_measured`: Emits measured pixel distance from ruler tool
- `status_changed`: Emits status message for display

**Key Methods:**
- `load_image(path)`: Load and display an image file
- `set_mode(mode)`: Switch between polygon, ruler, and pan modes
- `clear()`: Reset all drawing state
- `undo_last()`: Remove the last added point

#### `geometry.py` - Mathematical Calculations

**Responsibilities:**
- Performs all geometric calculations in pixel space
- Implements unit conversions
- Provides helper functions for geometric operations
- Maintains separation of concerns (math vs. UI)

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `polygon_area_pixels(points)` | Calculate polygon area using Shoelace formula |
| `perimeter_pixels(points)` | Calculate total polygon perimeter |
| `bounding_box_pixels(points)` | Calculate bounding rectangle dimensions |
| `distance_pixels(p1, p2)` | Euclidean distance between two points |
| `area_px_to_unit(area_px2, scale, unit)` | Convert pixel area to specified unit |
| `length_px_to_unit(length_px, scale, unit)` | Convert pixel length to specified unit |

**Supported Units:**
- `m²` / `m`: Square meters / meters
- `ft²` / `ft`: Square feet / feet
- `yd²` / `yd`: Square yards / yards
- `km²` / `km`: Square kilometers / kilometers
- `acre` / `m`: Acres / meters

#### `panels.py` - Sidebar UI Components

**Responsibilities:**
- Constructs sidebar panels for user interaction
- Manages scale calibration UI
- Displays measurement results
- Provides tool control buttons
- Emits signals for user actions

**Key Classes:**
- `ScalePanel(QWidget)`: Scale calibration interface
- `ResultsPanel(QWidget)`: Results display panel
- `ToolPanel(QWidget)`: Tool selection buttons

**Key Signals:**
- `scale_changed`: Emits new calibration value
- `results_selected`: Emits unit change requests

---

## Technical Specifications

### Coordinate Systems

The application uses two coordinate systems:

1. **Image Space**: Original image pixel coordinates (0, 0) at top-left
2. **Canvas Space**: Rendered canvas coordinates accounting for zoom/pan

Conversions between systems are handled internally by `CanvasWidget`.

### Calculation Methods

#### Polygon Area (Shoelace Formula)

The application uses the Shoelace formula (also known as the Gauss area formula) for precise polygon area calculation:

$$\text{Area} = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$

This algorithm:
- Works for non-self-intersecting polygons
- Calculates area directly from vertex coordinates
- Provides O(n) time complexity where n is vertex count

#### Unit Conversion Factors

| Target Unit | Conversion Factor from m² |
|-------------|---------------------------|
| m² | 1.0 |
| ft² | 10.7639 |
| yd² | 1.19599 |
| km² | 0.000001 |
| acre | 0.000247105 |

### Image Rendering

- **Format Support**: PNG, JPEG, BMP, GIF (via Pillow)
- **Maximum Recommended Size**: 8000×8000 pixels
- **Color Depth**: 8-bit to 32-bit (automatic handling)

### Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Polygon Area | O(n) | n = number of vertices |
| Perimeter | O(n) | n = number of vertices |
| Drawing Update | O(1) | Per-frame rendering |
| Zoom/Pan | O(1) | Transform operations |

---

## Keyboard Shortcuts Reference

### Drawing and Navigation

| Shortcut | Action | Mode | Context |
|----------|--------|------|---------|
| **P** | Toggle Polygon Mode | Drawing | Any |
| **R** | Toggle Ruler Mode | Measurement | Any |
| **Enter** | Close Polygon | Drawing | Polygon Mode Active |
| **Ctrl+Z** | Undo Last Point | Drawing | Points Exist |
| **Esc** | Clear All Points | Drawing | Any |
| **Scroll** | Zoom In/Out | Navigation | Canvas Focused |
| **Middle Drag** | Pan Canvas | Navigation | Canvas Focused |

### File Operations

| Shortcut | Action | Context |
|----------|--------|---------|
| **Ctrl+O** | Open Image | Any |
| **Ctrl+E** | Export Results | Measurement Complete |

### Quick Reference

- **Drawing**: Start with P → Click points → Enter to close
- **Calibrate**: Press R → Click scale bar ends → Enter distance → Apply
- **Modify**: Use Ctrl+Z to undo, Esc to clear all
- **Export**: Press Ctrl+E when measurement is complete

---

## Export Functionality

### Supported Formats

#### JSON Format
Contains structured data with full precision for programmatic access.

**File Format:**
```json
{
  "timestamp": "2026-05-11_16:30:44",
  "polygon_points": [
    [123.45, 456.78],
    [234.56, 567.89],
    [345.67, 678.90]
  ],
  "area": {
    "square_meters": 1234.56,
    "square_feet": 13279.32,
    "square_yards": 1475.48,
    "square_kilometers": 0.001235,
    "acres": 0.305
  },
  "perimeter": {
    "meters": 142.5,
    "feet": 467.8,
    "yards": 155.9,
    "kilometers": 0.143
  },
  "bounding_box": {
    "width_pixels": 456,
    "height_pixels": 789,
    "width_meters": 45.6,
    "height_meters": 78.9
  },
  "calibration": {
    "pixels_per_meter": 10.0,
    "scale_reference": "Google Maps scale bar"
  }
}
```

#### CSV Format
Tabular format suitable for spreadsheet import.

**File Format:**
```
Measurement,Value,Unit
Area,1234.56,m²
Perimeter,142.5,m
Width,45.6,m
Height,78.9,m
Bounding Box Width,456,px
Bounding Box Height,789,px
Calibration (px/m),10.0,px/m
```

#### TXT Format
Human-readable text format for quick reference.

**File Format:**
```
MAP AREA TOOL - MEASUREMENT RESULTS
====================================
Timestamp: 2026-05-11 16:30:44

AREA MEASUREMENTS
-----------------
Area: 1234.56 m²
      13279.32 ft²
      1475.48 yd²
      0.001235 km²
      0.305 acres

DIMENSIONS
----------
Perimeter: 142.5 m
Width: 45.6 m
Height: 78.9 m

BOUNDING BOX (pixels)
---------------------
Width: 456 px
Height: 789 px

CALIBRATION
-----------
Scale: 10.0 px/m
Reference: Google Maps scale bar
```

### Export Process

1. Complete a measurement polygon (Enter or double-click to close)
2. Press **Ctrl+E** or click **"Export Results"** button
3. Choose format and location in file dialog
4. File is saved with timestamp in filename
5. Confirmation message appears in status bar

---

## Calculation Methods

### Measurement Pipeline

```
1. Scale Calibration
   └─→ Establishes px/m conversion factor

2. Polygon Drawing
   └─→ User clicks points on canvas

3. Point Conversion
   ├─→ Screen coords → Image coords (accounting for zoom/pan)
   └─→ Store as normalized image-space coordinates

4. Geometric Calculation
   ├─→ Shoelace formula → Area (px²)
   ├─→ Distance accumulation → Perimeter (px)
   └─→ Min/Max → Bounding box (px)

5. Unit Conversion
   ├─→ Multiply by scale factor (px/m)
   ├─→ Apply unit conversion factors
   └─→ Display all supported units

6. Export
   └─→ Format results according to selected format
```

### Error Handling

| Scenario | Behavior |
|----------|----------|
| Less than 3 polygon points | Area displays as 0 |
| No scale calibration | Prompts user to calibrate before drawing |
| Invalid image file | Error message displayed, file dialog reopens |
| Empty polygon result | Displays "0.00" with unit label |

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Application Won't Start

**Symptoms**: Error message on launch or application crashes immediately

**Troubleshooting Steps:**
1. Verify Python version: `python --version` (must be 3.7+)
2. Check virtual environment activation (should see `(.venv)` in terminal)
3. Reinstall dependencies: `pip install --upgrade -r requirements.txt`
4. Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`

#### Issue: "Scale Not Calibrated" Error

**Symptoms**: Cannot draw measurements; message states scale not calibrated

**Solution:**
1. Press **R** to enter ruler mode
2. Carefully click both ends of the Google Maps scale bar
3. Enter the distance shown on the scale bar in the "Real dist:" field
4. Click "Apply (ruler method)" button
5. Status should change to "CALIBRATED ✓"

#### Issue: Measurements Appear Incorrect

**Symptoms**: Calculated areas don't match expectations

**Diagnosis Steps:**
1. **Verify scale calibration**: Recalibrate using a known distance
2. **Check polygon closure**: Ensure polygon is properly closed (status bar shows)
3. **Confirm point placement**: Zoom in to verify accurate vertex positioning
4. **Test with reference**: Create a polygon of known dimensions to verify accuracy

**Common Causes:**
- Inaccurate scale calibration (most common)
- Polygon not properly closed
- Zoom level changed during measurement without recalibration
- Image distortion from non-square pixels

#### Issue: Image File Won't Load

**Symptoms**: "Failed to load image" error or blank canvas

**Solutions:**
1. Verify file format is supported (PNG, JPEG, BMP, GIF)
2. Check file path contains no special characters or spaces
3. Ensure file is not corrupted: try opening in image viewer
4. Verify read permissions on file
5. Use absolute path instead of relative path

#### Issue: Slow Performance or Lag

**Symptoms**: Delayed response to mouse input or drawing appears sluggish

**Solutions:**
1. **Reduce image size**: Large images (>8000×8000) may cause slowdown
2. **Close other applications**: Frees system RAM
3. **Disable hardware acceleration** (if applicable in PyQt5 settings)
4. **Update graphics drivers**: Ensures optimal rendering performance

#### Issue: Export Files Not Being Created

**Symptoms**: Click "Export" but no file appears

**Troubleshooting:**
1. Verify at least one complete measurement polygon exists
2. Check write permissions in target directory
3. Ensure filename doesn't contain invalid characters
4. Check free disk space (requires ~1 MB per export)
5. Look in default Documents folder if path not confirmed

---

## Development Notes

### Code Style and Conventions

- **Language**: Python 3.7+
- **Framework**: PyQt5 (version 5.15.0+)
- **Image Library**: Pillow (version 9.0.0+)
- **Naming**: PEP 8 style guide adherence
- **Docstring Format**: Module and function level docstrings included

### Extending the Application

#### Adding New Unit Types

1. Update `geometry.py`:
   - Add conversion factor to `conversions` dictionary in `area_px_to_unit()`
   - Add length unit mapping to `length_conversions` dictionary
   - Update `length_unit_label()` mapping

2. Update `panels.py`:
   - Add new unit option to unit dropdown in `ResultsPanel`

#### Adding Export Formats

1. Extend `window.py` export function:
   - Add new format case in `_export_results()` method
   - Implement formatter function following existing patterns

2. Create formatter function:
   ```python
   def _format_results_newformat(self, data):
       """Custom format implementation"""
       # Transform data dictionary to desired format
       return formatted_output
   ```

#### Modifying Drawing Behavior

1. Edit `canvas.py` `CanvasWidget` class:
   - Modify `mousePressEvent()` for point selection behavior
   - Update `paintEvent()` for visual rendering
   - Adjust `SNAP_RADIUS` constant for snapping sensitivity

### Known Limitations

1. **Maximum Polygon Vertices**: No hard limit, but >1000 points may cause UI lag
2. **Image Size**: Tested up to 8000×8000 pixels; larger images may exceed system memory
3. **Precision**: Limited to floating-point precision (~15 significant digits)
4. **Scale Consistency**: Scale must be manually recalibrated if map zoom level changes
5. **Non-Rectilinear Regions**: Works for any polygon shape but performs best with closed, non-self-intersecting shapes

### Future Enhancement Opportunities

- [ ] Batch processing multiple images
- [ ] Polygon templates for common shapes
- [ ] Real-time measurement preview
- [ ] Measurement history and undo stack
- [ ] Multi-layer support for overlapping measurements
- [ ] Integration with external map APIs
- [ ] Measurement validation against known reference objects
- [ ] Custom color themes and UI customization

### Testing Recommendations

Before deploying updates:

1. **Unit Tests**: Test geometry calculations with known values
2. **Integration Tests**: Test complete workflows with sample images
3. **Cross-Platform Testing**: Verify on Windows, macOS, and Linux
4. **Performance Testing**: Test with large images and complex polygons
5. **User Acceptance Testing**: Validate against real-world use cases

---

## Support and Maintenance

### Contact Information

For issues, feature requests, or support:
- Review this documentation first
- Check the Troubleshooting section above
- Consult the README.md for quick reference

### Documentation Updates

This documentation was last updated in **May 2026** for version **1.0**.

For the most current information, refer to:
- In-application help text (press F1 or check Help menu)
- README.md for quick start
- Source code comments and docstrings

---

## Appendix: Quick Reference Commands

### Installation
```bash
pip install -r requirements.txt
```

### Launch
```bash
python main.py
python main.py image.png
```

### Workflow
1. Open image → Calibrate scale (R) → Draw polygon (P) → Close (Enter) → Export (Ctrl+E)

### Keyboard Shortcuts
- **P**: Polygon mode
- **R**: Ruler/calibration mode
- **Enter**: Close polygon
- **Ctrl+Z**: Undo point
- **Esc**: Clear all
- **Ctrl+E**: Export

---

**End of Documentation**

*For technical inquiries or development contributions, review the source code structure and module responsibilities outlined in the Project Architecture section.*
