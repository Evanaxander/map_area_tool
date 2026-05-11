# Map Area Tool

Measure the area of rooftops and regions from Google Maps screenshots.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Open with file dialog
python main.py

# Open a specific image directly
python main.py /path/to/screenshot.png
```

## How to Use

### Step 1 — Calibrate the Scale
Google Maps always shows a scale bar at the bottom-left of the map.

1. Press **R** (or click "Measure Scale Bar")
2. Click the **left end** of the scale bar in your screenshot
3. Click the **right end** of the scale bar
4. In the sidebar, enter the **real distance** shown on that scale bar (e.g. `50` for "50 m")

### Step 2 — Draw Your Polygon
1. Press **P** (or click "Draw Polygon")
2. Click around the edges of the roof/region
3. Press **Enter** or double-click to close — or click near the first point (it snaps)

### Step 3 — Read Results
Area, bounding box dimensions, and perimeter are shown in the sidebar.
Switch units (m², ft², yd², km², acre) from the dropdown.

### Step 4 — Export (optional)
Press **Ctrl+E** or click "Export Results" to save as JSON, CSV, or TXT.

## Shortcuts

| Key | Action |
|-----|--------|
| P | Polygon mode |
| R | Ruler mode |
| Enter | Close polygon |
| Ctrl+Z | Undo last point |
| Esc | Clear all |
| Scroll | Zoom in/out |
| Middle drag | Pan |
| Ctrl+O | Open image |
| Ctrl+E | Export results |

## Accuracy

Accuracy depends on how precisely you measure the scale bar.
Zoom in on the scale bar before measuring for best results.
The tool uses the Shoelace formula for polygon area calculation.

## Project Structure

```
map_area_tool/
├── main.py           # Entry point
├── requirements.txt
└── app/
    ├── canvas.py     # Interactive image canvas (drawing, zoom, pan)
    ├── geometry.py   # Area/perimeter math + unit conversions
    ├── panels.py     # Sidebar UI panels
    └── window.py     # Main window, wires everything together
```
