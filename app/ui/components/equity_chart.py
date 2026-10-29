"""
Equity Curve and Drawdown Chart Component
Refactored using jakubkrehel/skills principles:
- Clear semantic colors: Emerald growth (#2ea043) and crimson drawdown (#f85149)
- High-water mark dashed guideline for peak portfolio valuation
"""

import pyqtgraph as pg
from PySide6 import QtWidgets, QtCore
import numpy as np


class EquityChartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.gw = pg.GraphicsLayoutWidget()
        layout.addWidget(self.gw)

        # Equity Plot (Top)
        self.equity_plot = self.gw.addPlot(row=0, col=0)
        self.equity_plot.showGrid(x=True, y=True, alpha=0.12)
        self.equity_plot.setLabel('left', 'Portfolio ($)', color='#8b949e')
        self.equity_plot.setTitle('<span style="color: #f0f6fc; font-weight: 600; font-size: 11px;">Cumulative Portfolio Equity</span>')
        self.equity_plot.hideAxis('bottom')

        # Drawdown Plot (Bottom)
        self.dd_plot = self.gw.addPlot(row=1, col=0)
        self.dd_plot.setMaximumHeight(130)
        self.dd_plot.showGrid(x=True, y=True, alpha=0.12)
        self.dd_plot.setLabel('left', 'Drawdown (%)', color='#f85149')
        self.dd_plot.setXLink(self.equity_plot)

    def load_data(self, equity_curve, drawdown_pct):
        self.equity_plot.clear()
        self.dd_plot.clear()

        x = np.arange(len(equity_curve))
        y = np.array(equity_curve)

        # Equity curve plot
        pen = pg.mkPen('#2ea043', width=2.0)
        curve = self.equity_plot.plot(x, y, pen=pen)

        # Subtle area fill
        fill_brush = pg.mkBrush(46, 160, 67, 30)
        fill_curve = pg.PlotCurveItem(x, np.full_like(y, y[0]), pen=pg.mkPen(None))
        self.equity_plot.addItem(fill_curve)
        fill = pg.FillBetweenItem(curve, fill_curve, brush=fill_brush)
        self.equity_plot.addItem(fill)

        # High-Water Mark line
        peak = np.maximum.accumulate(y)
        self.equity_plot.plot(x, peak, pen=pg.mkPen('#8b949e', width=1, style=QtCore.Qt.PenStyle.DashLine))

        # Underwater Drawdown Plot
        dd_arr = np.array(drawdown_pct)
        dd_curve = self.dd_plot.plot(x, dd_arr, pen=pg.mkPen('#f85149', width=1.5))
        zero_curve = pg.PlotCurveItem(x, np.zeros_like(dd_arr), pen=pg.mkPen(None))
        self.dd_plot.addItem(zero_curve)
        dd_fill = pg.FillBetweenItem(dd_curve, zero_curve, brush=pg.mkBrush(248, 81, 73, 40))
        self.dd_plot.addItem(dd_fill)

        self.equity_plot.autoRange()
        self.dd_plot.autoRange()
