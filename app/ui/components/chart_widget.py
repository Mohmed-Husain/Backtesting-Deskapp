"""
Interactive Stock Candlestick, Indicators, and Volume Chart
Refactored for true desktop terminal experience:
- Seamless background matching the desktop palette (#131722)
- High-contrast HUD bar with clear labels and crisp colored values
- Responsive crosshairs and smooth panning/zooming
"""

import pyqtgraph as pg
from PySide6 import QtCore, QtGui, QtWidgets


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.picture = QtGui.QPicture()
        self.generatePicture()

    def generatePicture(self):
        p = QtGui.QPainter(self.picture)
        w = 0.35
        green_pen = pg.mkPen('#089981', width=1.2)
        green_brush = pg.mkBrush('#089981')
        red_pen = pg.mkPen('#f23645', width=1.2)
        red_brush = pg.mkBrush('#f23645')

        for (t, op, cl, lo, hi) in self.data:
            if cl >= op:
                p.setPen(green_pen)
                p.setBrush(green_brush)
            else:
                p.setPen(red_pen)
                p.setBrush(red_brush)
            p.drawLine(QtCore.QPointF(t, lo), QtCore.QPointF(t, hi))
            p.drawRect(QtCore.QRectF(t - w, op, w * 2, cl - op))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class StockChartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top Chart HUD Info Bar
        self.hud_label = QtWidgets.QLabel("Hover cursor over candlesticks to inspect OHLCV data")
        self.hud_label.setStyleSheet("""
            color: #9598a1;
            font-size: 12px;
            font-family: 'Consolas', 'Cascadia Code', monospace;
            padding: 8px 14px;
            background-color: #1e222d;
            border-bottom: 1px solid #2a2e39;
        """)
        layout.addWidget(self.hud_label)

        # pyqtgraph Canvas
        pg.setConfigOptions(antialias=True, background='#131722', foreground='#787b86')
        self.gw = pg.GraphicsLayoutWidget()
        layout.addWidget(self.gw)

        # Price Plot (Top, Row 0)
        self.price_plot = self.gw.addPlot(row=0, col=0)
        self.price_plot.showGrid(x=True, y=True, alpha=0.15)
        self.price_plot.setLabel('left', 'Price ($)', color='#787b86')
        self.price_plot.hideAxis('bottom')

        # Volume Plot (Bottom, Row 1)
        self.vol_plot = self.gw.addPlot(row=1, col=0)
        self.vol_plot.setMaximumHeight(110)
        self.vol_plot.showGrid(x=True, y=True, alpha=0.15)
        self.vol_plot.setLabel('left', 'Volume', color='#787b86')
        self.vol_plot.setXLink(self.price_plot)

        # Crosshairs
        self.v_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#2962ff', style=QtCore.Qt.PenStyle.DashLine, width=1))
        self.h_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#2962ff', style=QtCore.Qt.PenStyle.DashLine, width=1))
        self.price_plot.addItem(self.v_line, ignoreBounds=True)
        self.price_plot.addItem(self.h_line, ignoreBounds=True)

        self.gw.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def load_data(self, df, trades=None):
        self.df = df
        self.price_plot.clear()
        self.vol_plot.clear()

        # Re-attach crosshairs
        self.price_plot.addItem(self.v_line, ignoreBounds=True)
        self.price_plot.addItem(self.h_line, ignoreBounds=True)

        # Candlesticks
        candle_data = [
            (row['index'], row['open'], row['close'], row['low'], row['high'])
            for _, row in df.iterrows()
        ]
        self.candle_item = CandlestickItem(candle_data)
        self.price_plot.addItem(self.candle_item)

        # Overlaid Moving Averages
        x = df['index'].values
        self.price_plot.plot(x, df['sma_fast'].values, pen=pg.mkPen('#f59e0b', width=1.6), name='SMA 10')
        self.price_plot.plot(x, df['sma_slow'].values, pen=pg.mkPen('#2962ff', width=1.6), name='SMA 30')

        # Volume Bars
        for _, row in df.iterrows():
            color = '#089981' if row['close'] >= row['open'] else '#f23645'
            bar = pg.BarGraphItem(x=[row['index']], height=[row['volume']], width=0.55, brush=pg.mkBrush(color))
            self.vol_plot.addItem(bar)

        # Trade markers
        if trades:
            buy_x, buy_y = [], []
            sell_x, sell_y = [], []
            for t in trades:
                buy_x.append(t["entry_idx"])
                buy_y.append(t["entry_price"] * 0.985)
                sell_x.append(t["exit_idx"])
                sell_y.append(t["exit_price"] * 1.015)

            buy_scatter = pg.ScatterPlotItem(
                x=buy_x, y=buy_y, size=12, symbol='t1', 
                brush=pg.mkBrush('#089981'), pen=pg.mkPen('#ffffff', width=1)
            )
            self.price_plot.addItem(buy_scatter)

            sell_scatter = pg.ScatterPlotItem(
                x=sell_x, y=sell_y, size=12, symbol='t', 
                brush=pg.mkBrush('#f23645'), pen=pg.mkPen('#ffffff', width=1)
            )
            self.price_plot.addItem(sell_scatter)

        self.price_plot.autoRange()
        self.vol_plot.autoRange()

    def on_mouse_moved(self, pos):
        if self.df is None or self.df.empty:
            return

        if self.price_plot.sceneBoundingRect().contains(pos):
            mouse_point = self.price_plot.vb.mapSceneToView(pos)
            idx = int(round(mouse_point.x()))
            
            if 0 <= idx < len(self.df):
                row = self.df.iloc[idx]
                self.v_line.setPos(mouse_point.x())
                self.h_line.setPos(mouse_point.y())

                c_color = "#089981" if row['close'] >= row['open'] else "#f23645"
                self.hud_label.setText(
                    f"Date: <b style='color:#ffffff;'>{row['date']}</b> &nbsp;|&nbsp; "
                    f"O: <b style='color:#ffffff;'>${row['open']:.2f}</b> &nbsp; "
                    f"H: <b style='color:#ffffff;'>${row['high']:.2f}</b> &nbsp; "
                    f"L: <b style='color:#ffffff;'>${row['low']:.2f}</b> &nbsp; "
                    f"C: <b style='color:{c_color};'>${row['close']:.2f}</b> &nbsp;|&nbsp; "
                    f"Vol: <b style='color:#ffffff;'>{row['volume']:,}</b> &nbsp;|&nbsp; "
                    f"<span style='color:#f59e0b;'>SMA10:</span> ${row['sma_fast']:.2f} &nbsp; "
                    f"<span style='color:#2962ff;'>SMA30:</span> ${row['sma_slow']:.2f}"
                )
