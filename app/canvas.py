"""
canvas.py - Interactive image canvas with polygon drawing and scale measurement.
"""

import math
from enum import Enum, auto
from typing import List, Optional, Tuple

from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal
from PyQt5.QtGui import (
    QColor, QCursor, QFont, QImage, QPainter, QPen,
    QPixmap, QPolygonF, QBrush, QPainterPath,
)
from PyQt5.QtWidgets import QWidget, QSizePolicy

from app.geometry import distance_pixels


class Mode(Enum):
    POLYGON = auto()
    RULER   = auto()
    PAN     = auto()


SNAP_RADIUS = 10  # px - snap to first point to close polygon


class CanvasWidget(QWidget):
    """
    Displays a map image and lets the user:
      - Draw a polygon by clicking points (closes on snap or double-click)
      - Measure a line (ruler mode) to calibrate the scale
    """

    polygon_changed = pyqtSignal(list)   # emits list of image-space points
    ruler_measured  = pyqtSignal(float)  # emits pixel distance of ruler line
    status_changed  = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 500)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

        self._pixmap: Optional[QPixmap] = None
        self._mode = Mode.POLYGON

        # Polygon state
        self._points: List[QPointF] = []   # in image coords
        self._closed = False
        self._hover: Optional[QPointF] = None  # current mouse in image coords

        # Ruler state
        self._ruler_pts: List[QPointF] = []

        # Pan/zoom
        self._offset = QPointF(0, 0)
        self._scale  = 1.0
        self._pan_start: Optional[QPoint] = None
        self._pan_offset_start = QPointF(0, 0)

        self.setFocusPolicy(Qt.StrongFocus)

    # ── Public API ────────────────────────────────────────────

    def load_image(self, path: str) -> bool:
        pix = QPixmap(path)
        if pix.isNull():
            return False
        self._pixmap = pix
        self._fit_image()
        self.clear()
        return True

    def set_mode(self, mode: Mode):
        self._mode = mode
        if mode == Mode.RULER:
            self._ruler_pts = []
        self.update()
        self._emit_status()

    @property
    def mode(self) -> Mode:
        return self._mode

    def clear(self):
        self._points = []
        self._closed = False
        self._ruler_pts = []
        self._hover = None
        self.polygon_changed.emit([])
        self.update()

    def undo_last(self):
        if self._mode == Mode.POLYGON and self._points:
            if self._closed:
                self._closed = False
            else:
                self._points.pop()
            self.polygon_changed.emit(self._img_points_as_tuples())
            self.update()
        elif self._mode == Mode.RULER and self._ruler_pts:
            self._ruler_pts.pop()
            self.update()

    def get_polygon_points(self) -> List[Tuple[float, float]]:
        return self._img_points_as_tuples()

    def close_polygon(self):
        if len(self._points) >= 3 and not self._closed:
            self._closed = True
            self.polygon_changed.emit(self._img_points_as_tuples())
            self.update()

    # ── Image fitting ─────────────────────────────────────────

    def _fit_image(self):
        if not self._pixmap:
            return
        w, h = self.width(), self.height()
        iw, ih = self._pixmap.width(), self._pixmap.height()
        if iw == 0 or ih == 0:
            return
        self._scale = min(w / iw, h / ih) * 0.95
        self._offset = QPointF(
            (w - iw * self._scale) / 2,
            (h - ih * self._scale) / 2,
        )

    def resizeEvent(self, event):
        self._fit_image()
        self.update()

    # ── Coordinate helpers ────────────────────────────────────

    def _widget_to_img(self, p: QPointF) -> QPointF:
        return QPointF(
            (p.x() - self._offset.x()) / self._scale,
            (p.y() - self._offset.y()) / self._scale,
        )

    def _img_to_widget(self, p: QPointF) -> QPointF:
        return QPointF(
            p.x() * self._scale + self._offset.x(),
            p.y() * self._scale + self._offset.y(),
        )

    def _img_points_as_tuples(self) -> List[Tuple[float, float]]:
        return [(p.x(), p.y()) for p in self._points]

    def _near_first_point(self, widget_pos: QPointF) -> bool:
        if not self._points:
            return False
        first_w = self._img_to_widget(self._points[0])
        dx = widget_pos.x() - first_w.x()
        dy = widget_pos.y() - first_w.y()
        return math.sqrt(dx*dx + dy*dy) < SNAP_RADIUS

    # ── Mouse events ──────────────────────────────────────────

    def mousePressEvent(self, event):
        pos = QPointF(event.pos())

        if event.button() == Qt.MiddleButton or (
            event.button() == Qt.LeftButton and self._mode == Mode.PAN
        ):
            self._pan_start = event.pos()
            self._pan_offset_start = QPointF(self._offset)
            self.setCursor(Qt.ClosedHandCursor)
            return

        if event.button() != Qt.LeftButton:
            return

        if self._mode == Mode.POLYGON:
            if self._closed:
                return
            img_pos = self._widget_to_img(pos)

            # Snap to first point -> close polygon
            if len(self._points) >= 3 and self._near_first_point(pos):
                self._closed = True
                self.polygon_changed.emit(self._img_points_as_tuples())
                self.update()
                return

            self._points.append(img_pos)
            self.polygon_changed.emit(self._img_points_as_tuples())
            self.update()

        elif self._mode == Mode.RULER:
            img_pos = self._widget_to_img(pos)
            self._ruler_pts.append(img_pos)
            if len(self._ruler_pts) == 2:
                dist = distance_pixels(
                    (self._ruler_pts[0].x(), self._ruler_pts[0].y()),
                    (self._ruler_pts[1].x(), self._ruler_pts[1].y()),
                )
                self.ruler_measured.emit(dist)
                self._ruler_pts = []
            self.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self._mode == Mode.POLYGON:
            if len(self._points) >= 3 and not self._closed:
                self._closed = True
                self.polygon_changed.emit(self._img_points_as_tuples())
                self.update()

    def mouseMoveEvent(self, event):
        pos = QPointF(event.pos())

        if self._pan_start is not None:
            delta = event.pos() - self._pan_start
            self._offset = QPointF(
                self._pan_offset_start.x() + delta.x(),
                self._pan_offset_start.y() + delta.y(),
            )
            self.update()
            return

        self._hover = self._widget_to_img(pos)

        # Cursor hint
        if self._mode == Mode.POLYGON and not self._closed:
            if len(self._points) >= 3 and self._near_first_point(pos):
                self.setCursor(Qt.CrossCursor)
            else:
                self.setCursor(Qt.CrossCursor)
        elif self._mode == Mode.RULER:
            self.setCursor(Qt.CrossCursor)

        self.update()
        x, y = int(self._hover.x()), int(self._hover.y())
        self.status_changed.emit(f"x: {x}  y: {y}")

    def mouseReleaseEvent(self, event):
        if self._pan_start is not None:
            self._pan_start = None
            self.setCursor(Qt.ArrowCursor)

    def wheelEvent(self, event):
        if not self._pixmap:
            return
        factor = 1.12 if event.angleDelta().y() > 0 else 1 / 1.12
        mouse_pos = QPointF(event.pos())
        self._offset = mouse_pos - factor * (mouse_pos - self._offset)
        self._scale *= factor
        self.update()

    # ── Keyboard ──────────────────────────────────────────────

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clear()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.close_polygon()
        elif event.key() == Qt.Key_Z and (event.modifiers() & Qt.ControlModifier):
            self.undo_last()

    # ── Painting ──────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#1a1a1a"))

        if not self._pixmap:
            painter.setPen(QColor("#444"))
            painter.drawText(self.rect(), Qt.AlignCenter, "No image loaded")
            return

        # Image
        painter.drawPixmap(
            int(self._offset.x()), int(self._offset.y()),
            int(self._pixmap.width() * self._scale),
            int(self._pixmap.height() * self._scale),
            self._pixmap,
        )

        self._draw_polygon(painter)
        self._draw_ruler(painter)

    def _draw_polygon(self, painter: QPainter):
        if not self._points:
            return

        widget_pts = [self._img_to_widget(p) for p in self._points]

        # Fill
        if len(widget_pts) >= 3:
            path = QPainterPath()
            path.moveTo(widget_pts[0])
            for p in widget_pts[1:]:
                path.lineTo(p)
            path.closeSubpath()
            painter.fillPath(path, QBrush(QColor(80, 200, 120, 50)))

        # Edges
        pen = QPen(QColor("#4dc87a"), 2, Qt.SolidLine)
        painter.setPen(pen)
        for i in range(len(widget_pts) - 1):
            painter.drawLine(widget_pts[i], widget_pts[i + 1])
        if self._closed and len(widget_pts) >= 3:
            painter.drawLine(widget_pts[-1], widget_pts[0])

        # Live edge to mouse
        if not self._closed and self._hover and widget_pts:
            hover_w = self._img_to_widget(self._hover)
            pen2 = QPen(QColor(77, 200, 122, 120), 1, Qt.DashLine)
            painter.setPen(pen2)
            painter.drawLine(widget_pts[-1], hover_w)

            # Show snap circle near first point
            if len(widget_pts) >= 3 and self._near_first_point(hover_w):
                painter.setPen(QPen(QColor("#fff"), 1))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(widget_pts[0], SNAP_RADIUS, SNAP_RADIUS)

        # Vertices
        for i, p in enumerate(widget_pts):
            if i == 0:
                painter.setBrush(QBrush(QColor("#ffffff")))
                painter.setPen(QPen(QColor("#000"), 1))
                painter.drawEllipse(p, 5, 5)
            else:
                painter.setBrush(QBrush(QColor("#4dc87a")))
                painter.setPen(QPen(QColor("#000"), 1))
                painter.drawEllipse(p, 4, 4)

            # Point label
            painter.setPen(QColor("#cccccc"))
            font = QFont("Courier", 9)
            painter.setFont(font)
            painter.drawText(QPointF(p.x() + 7, p.y() - 5), str(i + 1))

    def _draw_ruler(self, painter: QPainter):
        if not self._ruler_pts:
            return
        pen = QPen(QColor("#f0c040"), 2, Qt.DashLine)
        painter.setPen(pen)

        pts_w = [self._img_to_widget(p) for p in self._ruler_pts]

        if len(pts_w) == 1 and self._hover:
            hover_w = self._img_to_widget(self._hover)
            painter.drawLine(pts_w[0], hover_w)

        for p in pts_w:
            painter.setBrush(QBrush(QColor("#f0c040")))
            painter.setPen(QPen(QColor("#000"), 1))
            painter.drawEllipse(p, 5, 5)

    def _emit_status(self):
        labels = {Mode.POLYGON: "Draw Polygon", Mode.RULER: "Measure Scale Bar", Mode.PAN: "Pan"}
        self.status_changed.emit(f"Mode: {labels[self._mode]}")
