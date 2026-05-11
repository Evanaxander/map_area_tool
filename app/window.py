"""
window.py - Main application window. Wires canvas, panels, and logic together.
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QKeySequence
from PyQt5.QtWidgets import (
    QAction, QFileDialog, QHBoxLayout, QLabel,
    QMainWindow, QMessageBox, QScrollArea,
    QShortcut, QSizePolicy, QSplitter,
    QStatusBar, QVBoxLayout, QWidget,
)

from app.canvas import CanvasWidget, Mode
from app.geometry import (
    area_px_to_unit, bounding_box_pixels, length_px_to_unit,
    length_unit_label, perimeter_pixels, polygon_area_pixels,
)
from app.panels import ResultsPanel, ScalePanel, ToolPanel


DARK = "#141414"
SIDEBAR_W = 280


class MainWindow(QMainWindow):
    def __init__(self, image_path: Optional[str] = None):
        super().__init__()
        self.setWindowTitle("Map Area Tool")
        self.resize(1200, 780)
        self._scale_px_per_m: float = 0.0
        self._current_points: List[Tuple[float, float]] = []

        self._build_ui()
        self._apply_theme()
        self._connect_signals()
        self._build_shortcuts()

        if image_path:
            self._load_image(image_path)

    # ── UI construction ───────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(SIDEBAR_W)
        sidebar.setObjectName("sidebar")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 12, 12, 12)
        sb_layout.setSpacing(10)

        # Logo/title
        title = QLabel("MAP AREA TOOL")
        title.setStyleSheet("color: #4dc87a; font-size: 13px; font-weight: bold; letter-spacing: 2px;")
        sb_layout.addWidget(title)

        sub = QLabel("roof & region measurer")
        sub.setStyleSheet("color: #444; font-size: 11px;")
        sb_layout.addWidget(sub)

        self._tool_panel    = ToolPanel()
        self._scale_panel   = ScalePanel()
        self._results_panel = ResultsPanel()

        sb_layout.addWidget(self._tool_panel)
        sb_layout.addWidget(self._scale_panel)
        sb_layout.addWidget(self._results_panel)
        sb_layout.addStretch()

        # Shortcuts hint
        hint = QLabel("Shortcuts: P=polygon  R=ruler\nEnter=close  Ctrl+Z=undo  Esc=clear\nScroll=zoom  Middle drag=pan")
        hint.setStyleSheet("color: #333; font-size: 10px; line-height: 1.6;")
        sb_layout.addWidget(hint)

        # Canvas
        self._canvas = CanvasWidget()

        # Status bar
        self._status = QStatusBar()
        self._status.setStyleSheet("background: #0f0f0f; color: #444; font-size: 11px; font-family: 'Courier New';")
        self._lbl_coords = QLabel("x: --  y: --")
        self._lbl_coords.setStyleSheet("color: #555;")
        self._lbl_mode = QLabel("Mode: Draw Polygon")
        self._lbl_mode.setStyleSheet("color: #4dc87a;")
        self._status.addWidget(self._lbl_mode)
        self._status.addPermanentWidget(self._lbl_coords)
        self.setStatusBar(self._status)

        root.addWidget(sidebar)
        root.addWidget(self._canvas, 1)

    def _apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {DARK}; color: #e0e0e0; }}
            #sidebar {{ background: #111; border-right: 1px solid #222; }}
            QLabel {{ font-family: 'Courier New'; font-size: 12px; }}
            QDoubleSpinBox, QComboBox {{
                background: #1a1a1a;
                border: 1px solid #2a2a2a;
                color: #e0e0e0;
                font-family: 'Courier New';
                font-size: 12px;
                padding: 4px;
            }}
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                background: #2a2a2a;
            }}
        """)

    def _connect_signals(self):
        self._tool_panel.sig_open.connect(self._open_dialog)
        self._tool_panel.sig_polygon.connect(lambda: self._set_mode("polygon"))
        self._tool_panel.sig_ruler.connect(lambda: self._set_mode("ruler"))
        self._tool_panel.sig_close.connect(self._canvas.close_polygon)
        self._tool_panel.sig_undo.connect(self._canvas.undo_last)
        self._tool_panel.sig_clear.connect(self._canvas.clear)
        self._tool_panel.sig_export.connect(self._export_results)

        self._canvas.polygon_changed.connect(self._on_polygon_changed)
        self._canvas.ruler_measured.connect(self._on_ruler_measured)
        self._canvas.status_changed.connect(self._lbl_coords.setText)

        self._scale_panel.scale_changed.connect(self._on_scale_changed)
        self._results_panel.unit_changed.connect(self._on_unit_changed)

    def _build_shortcuts(self):
        QShortcut(QKeySequence("P"), self, lambda: self._set_mode("polygon"))
        QShortcut(QKeySequence("R"), self, lambda: self._set_mode("ruler"))
        QShortcut(QKeySequence("Return"), self, self._canvas.close_polygon)
        QShortcut(QKeySequence("Escape"), self, self._canvas.clear)
        QShortcut(QKeySequence("Ctrl+Z"), self, self._canvas.undo_last)
        QShortcut(QKeySequence("Ctrl+O"), self, self._open_dialog)
        QShortcut(QKeySequence("Ctrl+E"), self, self._export_results)

    # ── Mode switching ────────────────────────────────────────

    def _set_mode(self, mode: str):
        m = Mode.POLYGON if mode == "polygon" else Mode.RULER
        self._canvas.set_mode(m)
        self._tool_panel.set_active(mode)
        labels = {"polygon": "Draw Polygon", "ruler": "Measure Scale Bar"}
        self._lbl_mode.setText(f"Mode: {labels[mode]}")

    # ── Image loading ─────────────────────────────────────────

    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Map Screenshot", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)"
        )
        if path:
            self._load_image(path)

    def _load_image(self, path: str):
        if self._canvas.load_image(path):
            self.setWindowTitle(f"Map Area Tool  —  {Path(path).name}")
            self._status.showMessage(f"Loaded: {path}", 3000)
        else:
            QMessageBox.critical(self, "Error", f"Could not load image:\n{path}")

    # ── Signal handlers ───────────────────────────────────────

    def _on_polygon_changed(self, points: list):
        self._current_points = points
        self._refresh_results()

    def _on_ruler_measured(self, px_dist: float):
        self._scale_panel.set_measured_pixels(px_dist)
        self._status.showMessage(f"Scale bar measured: {px_dist:.1f} px — enter real distance in the sidebar.", 5000)

    def _on_scale_changed(self, px_per_m: float):
        self._scale_px_per_m = px_per_m
        self._refresh_results()

    def _on_unit_changed(self, unit: str):
        self._refresh_results()

    # ── Calculations ──────────────────────────────────────────

    def _refresh_results(self):
        pts  = self._current_points
        unit = self._results_panel.unit
        ppm  = self._scale_px_per_m   # only set via _on_scale_changed (explicit Apply click)

        data = {"points": str(len(pts))}

        if ppm > 0:
            data["scale"] = f"{ppm:.3f} px/m"
        else:
            data["scale"] = "not calibrated"

        if len(pts) >= 3:
            area_px2  = polygon_area_pixels(pts)
            perim_px  = perimeter_pixels(pts)
            _, _, bw, bh = bounding_box_pixels(pts)

            if ppm > 0:
                area_val  = area_px_to_unit(area_px2, ppm, unit)
                perim_val = length_px_to_unit(perim_px, ppm, unit)
                bw_val    = length_px_to_unit(bw, ppm, unit)
                bh_val    = length_px_to_unit(bh, ppm, unit)
                lu = length_unit_label(unit)
                data["area"]      = f"{area_val:,.2f} {unit}"
                data["perimeter"] = f"{perim_val:,.2f} {lu}"
                data["width"]     = f"{bw_val:,.2f} {lu}"
                data["height"]    = f"{bh_val:,.2f} {lu}"
            else:
                data["area"]      = f"{area_px2:,.0f} px²  (calibrate scale)"
                data["perimeter"] = f"{perim_px:,.0f} px"
                data["width"]     = f"{bw:,.0f} px"
                data["height"]    = f"{bh:,.0f} px"
        else:
            data["area"]      = "--"
            data["perimeter"] = "--"
            data["width"]     = "--"
            data["height"]    = "--"

        self._results_panel.update_results(data)

    # ── Export ────────────────────────────────────────────────

    def _export_results(self):
        pts = self._current_points
        if len(pts) < 3:
            QMessageBox.information(self, "Export", "Draw a polygon first.")
            return

        path, fmt = QFileDialog.getSaveFileName(
            self, "Export Results", f"area_result_{datetime.now():%Y%m%d_%H%M%S}",
            "JSON (*.json);;CSV (*.csv);;Text (*.txt)"
        )
        if not path:
            return

        unit = self._results_panel.unit
        ppm  = self._scale_px_per_m

        area_px2  = polygon_area_pixels(pts)
        perim_px  = perimeter_pixels(pts)
        _, _, bw, bh = bounding_box_pixels(pts)

        result = {
            "timestamp":        datetime.now().isoformat(),
            "unit":             unit,
            "scale_px_per_m":   ppm,
            "points_count":     len(pts),
            "polygon_points_px": [(round(x, 2), round(y, 2)) for x, y in pts],
        }

        if ppm > 0:
            lu = length_unit_label(unit)
            result["area"]           = f"{area_px_to_unit(area_px2, ppm, unit):.4f} {unit}"
            result["perimeter"]      = f"{length_px_to_unit(perim_px, ppm, unit):.4f} {lu}"
            result["bounding_width"] = f"{length_px_to_unit(bw, ppm, unit):.4f} {lu}"
            result["bounding_height"]= f"{length_px_to_unit(bh, ppm, unit):.4f} {lu}"
        else:
            result["area_px2"]       = round(area_px2, 2)
            result["perimeter_px"]   = round(perim_px, 2)
            result["bounding_width_px"]  = round(bw, 2)
            result["bounding_height_px"] = round(bh, 2)
            result["note"] = "Scale not calibrated — values in pixels."

        if path.endswith(".json"):
            with open(path, "w") as f:
                json.dump(result, f, indent=2)
        elif path.endswith(".csv"):
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                for k, v in result.items():
                    if k == "polygon_points_px":
                        writer.writerow([k, str(v)])
                    else:
                        writer.writerow([k, v])
        else:
            with open(path, "w") as f:
                for k, v in result.items():
                    f.write(f"{k}: {v}\n")

        self._status.showMessage(f"Exported to {path}", 4000)
