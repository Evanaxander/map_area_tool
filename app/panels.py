"""
panels.py - Sidebar panels: scale calibration, results display, tool controls.
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDoubleSpinBox, QComboBox, QFrame, QGroupBox,
)


def _section(title: str) -> QGroupBox:
    g = QGroupBox(title)
    g.setStyleSheet("""
        QGroupBox {
            font-size: 11px; font-weight: bold; color: #888;
            border: 1px solid #2a2a2a; border-radius: 4px;
            margin-top: 8px; padding-top: 8px;
        }
        QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
    """)
    return g


class ScalePanel(QWidget):
    """
    Explicit two-step calibration with a clear Apply button.
    No implicit/auto emissions on startup or spin changes.
    """
    scale_changed = pyqtSignal(float)  # only emits when user clicks Apply

    def __init__(self, parent=None):
        super().__init__(parent)
        self._measured_px: float = 0.0
        self._current_ppm: float = 0.0
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)

        grp = _section("Scale Calibration")
        inner = QVBoxLayout(grp)
        inner.setSpacing(8)

        # Status banner
        self._lbl_status = QLabel("NOT CALIBRATED")
        self._lbl_status.setStyleSheet(
            "color:#c04040; font-size:11px; font-weight:bold; padding:4px;"
            "background:#1a0a0a; border:1px solid #3a1a1a; border-radius:2px;"
        )
        self._lbl_status.setAlignment(Qt.AlignCenter)
        self._lbl_status.setWordWrap(True)
        inner.addWidget(self._lbl_status)

        inner.addWidget(_sep())

        # -- Method A: Ruler ---------------------------------
        inner.addWidget(_hint("STEP 1  Press R, click both ends of the scale bar on the map"))

        row1 = QHBoxLayout()
        row1.addWidget(_lbl("Measured:", 78))
        self._lbl_px = QLabel("-- px")
        self._lbl_px.setStyleSheet("color:#f0c040; font-weight:bold;")
        row1.addWidget(self._lbl_px)
        row1.addStretch()
        inner.addLayout(row1)

        inner.addWidget(_hint("STEP 2  Enter the real distance labeled on that scale bar:"))

        row2 = QHBoxLayout()
        row2.addWidget(_lbl("Real dist:", 78))
        self._spin_dist = QDoubleSpinBox()
        self._spin_dist.setRange(0.1, 1_000_000)
        self._spin_dist.setValue(10.0)   # 10 m is the most common Maps scale bar
        self._spin_dist.setSuffix(" m")
        self._spin_dist.setDecimals(1)
        self._spin_dist.setFixedWidth(95)
        row2.addWidget(self._spin_dist)
        row2.addStretch()
        inner.addLayout(row2)

        btn_a = _btn("✓  Apply (ruler method)", "#1a2a1a", "#4dc87a")
        btn_a.clicked.connect(self._apply_ruler)
        inner.addWidget(btn_a)

        inner.addWidget(_sep())

        # -- Method B: Direct --------------------------------
        inner.addWidget(_hint("OR type px/m directly if you know the scale:"))

        row3 = QHBoxLayout()
        row3.addWidget(_lbl("px / m:", 78))
        self._spin_ppm = QDoubleSpinBox()
        self._spin_ppm.setRange(0.001, 100_000)
        self._spin_ppm.setValue(1.0)
        self._spin_ppm.setDecimals(4)
        self._spin_ppm.setFixedWidth(95)
        row3.addWidget(self._spin_ppm)
        row3.addStretch()
        inner.addLayout(row3)

        btn_b = _btn("✓  Apply (manual entry)", "#1a2a1a", "#4dc87a")
        btn_b.clicked.connect(self._apply_manual)
        inner.addWidget(btn_b)

        layout.addWidget(grp)

    # ── Public API ────────────────────────────────────────────

    def set_measured_pixels(self, px: float):
        """Called by window when ruler tool completes a measurement."""
        self._measured_px = px
        self._lbl_px.setText(f"{px:.1f} px")
        dist = self._spin_dist.value()
        preview = px / dist if dist > 0 else 0
        self._lbl_status.setText(
            f"Ruler done: {px:.1f} px measured\n"
            f"Preview: {preview:.3f} px/m  →  click Apply"
        )
        self._lbl_status.setStyleSheet(
            "color:#f0c040; font-size:10px; font-weight:bold; padding:4px;"
            "background:#1a1800; border:1px solid #3a3000; border-radius:2px;"
        )

    def get_scale(self) -> float:
        return self._current_ppm

    # ── Private ───────────────────────────────────────────────

    def _apply_ruler(self):
        if self._measured_px <= 0:
            self._lbl_status.setText("No ruler measurement yet!\nPress R and draw over the scale bar first.")
            self._lbl_status.setStyleSheet(
                "color:#c04040; font-size:10px; font-weight:bold; padding:4px;"
                "background:#1a0a0a; border:1px solid #3a1a1a; border-radius:2px;"
            )
            return
        ppm = self._measured_px / self._spin_dist.value()
        self._commit(ppm)

    def _apply_manual(self):
        ppm = self._spin_ppm.value()
        self._commit(ppm)

    def _commit(self, ppm: float):
        self._current_ppm = ppm
        self._lbl_status.setText(f"CALIBRATED  ✓\n{ppm:.4f} px / m")
        self._lbl_status.setStyleSheet(
            "color:#4dc87a; font-size:11px; font-weight:bold; padding:4px;"
            "background:#0a1a0a; border:1px solid #1a3a1a; border-radius:2px;"
        )
        self.scale_changed.emit(ppm)


# ── Results panel ─────────────────────────────────────────────

class ResultsPanel(QWidget):
    unit_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)

        grp = _section("Measurements")
        inner = QVBoxLayout(grp)
        inner.setSpacing(5)

        row = QHBoxLayout()
        row.addWidget(QLabel("Unit:"))
        self._combo = QComboBox()
        self._combo.addItems(["m²", "ft²", "yd²", "km²", "acre"])
        self._combo.currentTextChanged.connect(self.unit_changed)
        row.addWidget(self._combo)
        row.addStretch()
        inner.addLayout(row)

        inner.addWidget(_sep())

        self._rows = {}
        for key, label, big in [
            ("area",      "Area",      True),
            ("width",     "Bound. W",  False),
            ("height",    "Bound. H",  False),
            ("perimeter", "Perim.",    False),
            ("points",    "Points",    False),
            ("scale",     "Scale",     False),
        ]:
            row_w = QHBoxLayout()
            l = QLabel(label)
            l.setFixedWidth(68)
            l.setStyleSheet("color:#666; font-size:11px;")
            v = QLabel("--")
            v.setWordWrap(True)
            v.setStyleSheet(
                "color:#4dc87a; font-size:14px; font-weight:bold;" if big
                else "color:#ccc; font-size:11px;"
            )
            row_w.addWidget(l)
            row_w.addWidget(v, 1)
            inner.addLayout(row_w)
            self._rows[key] = v

        layout.addWidget(grp)

    def update_results(self, data: dict):
        for k, v in self._rows.items():
            if k in data:
                v.setText(str(data[k]))

    @property
    def unit(self) -> str:
        return self._combo.currentText()


# ── Tool panel ────────────────────────────────────────────────

class ToolPanel(QWidget):
    sig_open    = pyqtSignal()
    sig_polygon = pyqtSignal()
    sig_ruler   = pyqtSignal()
    sig_close   = pyqtSignal()
    sig_undo    = pyqtSignal()
    sig_clear   = pyqtSignal()
    sig_export  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        grp = _section("Tools")
        inner = QVBoxLayout(grp)
        inner.setSpacing(4)

        self._btn_polygon = _btn("⬡  Draw Polygon  [P]",          "#1e3a2a", "#4dc87a")
        self._btn_ruler   = _btn("↔  Measure Scale Bar  [R]",     "#2a2a2a", "#ccc")
        b_open  = _btn("📂  Open Image  [Ctrl+O]",                "#2a2a2a", "#ccc")
        b_close = _btn("✓  Close & Calculate  [Enter]",           "#2a2a2a", "#ccc")
        b_undo  = _btn("↩  Undo Last Point  [Ctrl+Z]",            "#2a2a2a", "#ccc")
        b_clear = _btn("✕  Clear All  [Esc]",                     "#2a2a2a", "#c07070")
        b_exp   = _btn("↗  Export Results  [Ctrl+E]",             "#2a2a2a", "#ccc")

        b_open.clicked.connect(self.sig_open)
        self._btn_polygon.clicked.connect(self.sig_polygon)
        self._btn_ruler.clicked.connect(self.sig_ruler)
        b_close.clicked.connect(self.sig_close)
        b_undo.clicked.connect(self.sig_undo)
        b_clear.clicked.connect(self.sig_clear)
        b_exp.clicked.connect(self.sig_export)

        for w in [b_open, self._btn_polygon, self._btn_ruler,
                  b_close, b_undo, _sep(), b_clear, b_exp]:
            inner.addWidget(w)

        layout.addWidget(grp)

    def set_active(self, mode: str):
        for btn in [self._btn_polygon, self._btn_ruler]:
            btn.setStyleSheet(_bstyle("#1e2a2a", "#ccc"))
        if mode == "polygon":
            self._btn_polygon.setStyleSheet(_bstyle("#1e3a2a", "#4dc87a"))
        elif mode == "ruler":
            self._btn_ruler.setStyleSheet(_bstyle("#1e3a2a", "#4dc87a"))


# ── Widget helpers ────────────────────────────────────────────

def _bstyle(bg: str, fg: str) -> str:
    return (f"QPushButton{{background:{bg};color:{fg};border:1px solid #2a2a2a;"
            f"border-radius:3px;padding:6px 8px;text-align:left;"
            f"font-family:'Courier New';font-size:11px;}}"
            f"QPushButton:hover{{background:#282828;border-color:#444;}}"
            f"QPushButton:pressed{{background:#333;}}")


def _btn(label: str, bg: str, fg: str) -> QPushButton:
    b = QPushButton(label)
    b.setStyleSheet(_bstyle(bg, fg))
    return b


def _lbl(text: str, width: int) -> QLabel:
    l = QLabel(text)
    l.setFixedWidth(width)
    l.setStyleSheet("font-size:11px;")
    return l


def _hint(text: str) -> QLabel:
    l = QLabel(text)
    l.setWordWrap(True)
    l.setStyleSheet("color:#555; font-size:10px;")
    return l


def _sep() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("color:#222; margin:2px 0;")
    return f
