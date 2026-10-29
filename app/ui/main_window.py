"""
Main Window for QUANTIX Desktop Terminal
Features:
- Tabbed left & right side panels for clean settings distribution
- Quick sidebar toggle buttons in header bar to maximize chart screen space
- Responsive splitters and native desktop menu bar
"""

from PySide6 import QtWidgets, QtCore, QtGui
from app.styles import DARK_THEME_QSS
from app.core.mock_data import generate_backtest_results
from app.ui.components.chart_widget import StockChartWidget
from app.ui.components.equity_chart import EquityChartWidget
from app.ui.components.metrics_cards import MetricsDashboard
from app.ui.components.trades_table import TradeLogTable
from app.ui.components.ai_panel import AIAssistantPanel
from app.ui.components.strategy_panel import StrategyConfigPanel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QUANTIX // AI Stocks Backtesting & Quantitative Research Terminal")
        self.resize(1520, 930)
        self.setMinimumSize(1150, 750)
        
        self.setStyleSheet(DARK_THEME_QSS)

        self.create_desktop_menu()
        self.init_ui()
        self.run_initial_backtest()

    def create_desktop_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #131722;
                color: #d1d4dc;
                border-bottom: 1px solid #2a2e39;
                padding: 2px 6px;
                font-size: 12px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 4px 10px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #1e222d;
                color: #ffffff;
            }
            QMenu {
                background-color: #1e222d;
                color: #ffffff;
                border: 1px solid #363a45;
                padding: 4px;
                font-size: 12px;
            }
            QMenu::item {
                padding: 6px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2962ff;
                color: #ffffff;
            }
        """)

        # File Menu
        file_menu = menubar.addMenu("&File")
        new_act = file_menu.addAction("New Strategy Workspace")
        new_act.setShortcut("Ctrl+N")
        open_act = file_menu.addAction("Open Historical Dataset...")
        open_act.setShortcut("Ctrl+O")
        file_menu.addSeparator()
        export_act = file_menu.addAction("Export Results as CSV...")
        export_act.triggered.connect(self.on_export)
        file_menu.addSeparator()
        exit_act = file_menu.addAction("Exit")
        exit_act.triggered.connect(self.close)

        # Strategy Menu
        strat_menu = menubar.addMenu("&Strategies")
        run_act = strat_menu.addAction("Run Active Backtest")
        run_act.setShortcut("F5")
        run_act.triggered.connect(lambda: self.strategy_panel.trigger_run())
        strat_menu.addAction("Monte Carlo Robustness Test")

        # View Menu
        view_menu = menubar.addMenu("&View")
        toggle_left = view_menu.addAction("Toggle Strategy Panel")
        toggle_left.setShortcut("Ctrl+B")
        toggle_left.triggered.connect(self.toggle_left_panel)
        toggle_right = view_menu.addAction("Toggle AI Copilot")
        toggle_right.setShortcut("Ctrl+J")
        toggle_right.triggered.connect(self.toggle_right_panel)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        about_act = help_menu.addAction("About QUANTIX")
        about_act.triggered.connect(lambda: QtWidgets.QMessageBox.about(
            self, "About QUANTIX",
            "QUANTIX Desktop Terminal v2.5\nAI Stocks Backtesting & Quantitative Research Station\nBuilt with PySide6 & pyqtgraph"
        ))

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        master_layout = QtWidgets.QVBoxLayout(central_widget)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)

        # 1. Desktop Header Bar
        header = self.create_header_bar()
        master_layout.addWidget(header)

        # 2. Performance Metrics KPI Row
        metrics_container = QtWidgets.QWidget()
        metrics_container.setObjectName("metricsContainer")
        metrics_layout = QtWidgets.QVBoxLayout(metrics_container)
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        self.metrics_dashboard = MetricsDashboard()
        metrics_layout.addWidget(self.metrics_dashboard)
        master_layout.addWidget(metrics_container)

        # 3. Workstation Body Splitter
        self.body_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.body_splitter.setHandleWidth(3)

        # Left: Strategy Configuration Panel (with internal tabs)
        self.strategy_panel = StrategyConfigPanel()
        self.strategy_panel.setMinimumWidth(260)
        self.strategy_panel.setMaximumWidth(340)
        self.strategy_panel.run_backtest_signal.connect(self.on_run_backtest)
        self.body_splitter.addWidget(self.strategy_panel)

        # Center: Central Tabbed Workspace
        center_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(center_widget)
        center_layout.setContentsMargins(6, 6, 6, 6)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setProperty("mainTabs", "true")
        
        # Tab 1: Price Action & Signals
        self.chart_widget = StockChartWidget()
        self.tabs.addTab(self.chart_widget, "📈 Price Action & Candlesticks")

        # Tab 2: Equity Curve & Drawdown
        self.equity_widget = EquityChartWidget()
        self.tabs.addTab(self.equity_widget, "📊 Portfolio Equity & Drawdown")

        # Tab 3: Trade Execution Log
        self.trades_table = TradeLogTable()
        self.tabs.addTab(self.trades_table, "📜 Executed Trades Ledger")

        center_layout.addWidget(self.tabs)
        self.body_splitter.addWidget(center_widget)

        # Right: AI Research Assistant Panel (with internal tabs)
        self.ai_panel = AIAssistantPanel()
        self.ai_panel.setMinimumWidth(280)
        self.ai_panel.setMaximumWidth(360)
        self.body_splitter.addWidget(self.ai_panel)

        # Splitter Proportions (20% Left, 58% Center, 22% Right)
        self.body_splitter.setSizes([300, 880, 340])
        master_layout.addWidget(self.body_splitter, 1)

        # 4. Status Bar
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("● Ready · Tabbed Layout Active · Engine Latency: 0.12ms · Memory: 45 MB")

    def create_header_bar(self):
        header = QtWidgets.QFrame()
        header.setObjectName("headerBar")
        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(12)

        # Sidebar Toggle Left
        self.toggle_left_btn = QtWidgets.QPushButton("◧ Settings")
        self.toggle_left_btn.setProperty("toggleBtn", "true")
        self.toggle_left_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.toggle_left_btn.clicked.connect(self.toggle_left_panel)
        layout.addWidget(self.toggle_left_btn)

        # App Brand
        brand_layout = QtWidgets.QHBoxLayout()
        brand_layout.setSpacing(8)
        logo = QtWidgets.QLabel("QUANTIX")
        logo.setObjectName("appLogo")
        badge = QtWidgets.QLabel("TERMINAL")
        badge.setObjectName("appBadge")
        brand_layout.addWidget(logo)
        brand_layout.addWidget(badge)
        layout.addLayout(brand_layout)

        layout.addSpacing(10)

        # Live Active Ticker Badge
        self.symbol_badge = QtWidgets.QLabel("NVDA  $128.45  ▲ +2.85%")
        self.symbol_badge.setObjectName("tickerBadge")
        layout.addWidget(self.symbol_badge)

        layout.addStretch()

        # Desktop Action Buttons
        export_btn = QtWidgets.QPushButton("📥 Export CSV")
        export_btn.setProperty("headerBtn", "true")
        export_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self.on_export)
        
        save_btn = QtWidgets.QPushButton("💾 Save Preset")
        save_btn.setProperty("headerBtn", "true")
        save_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(lambda: QtWidgets.QMessageBox.information(self, "Preset Saved", "Current parameters saved to active workspace preset."))

        layout.addWidget(export_btn)
        layout.addWidget(save_btn)

        # Sidebar Toggle Right
        self.toggle_right_btn = QtWidgets.QPushButton("AI Copilot ◨")
        self.toggle_right_btn.setProperty("toggleBtn", "true")
        self.toggle_right_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.toggle_right_btn.clicked.connect(self.toggle_right_panel)
        layout.addWidget(self.toggle_right_btn)

        return header

    def toggle_left_panel(self):
        visible = not self.strategy_panel.isVisible()
        self.strategy_panel.setVisible(visible)
        self.toggle_left_btn.setText("◧ Settings" if visible else "◻ Settings")

    def toggle_right_panel(self):
        visible = not self.ai_panel.isVisible()
        self.ai_panel.setVisible(visible)
        self.toggle_right_btn.setText("AI Copilot ◨" if visible else "AI Copilot ◻")

    def on_export(self):
        QtWidgets.QMessageBox.information(self, "Export Complete", "Historical trades ledger and portfolio equity curve exported to CSV.")

    def run_initial_backtest(self):
        self.execute_backtest("NVDA", "AI Trend + Volatility Filter")

    def on_run_backtest(self, config):
        sym = config.get("symbol", "NVDA")
        strat = config.get("strategy", "AI Trend + Volatility Filter")
        self.execute_backtest(sym, strat)

    def execute_backtest(self, symbol, strategy):
        data = generate_backtest_results(symbol=symbol, strategy=strategy)
        
        # 1. Update Charts
        self.chart_widget.load_data(data["df"], data["trades"])
        self.equity_widget.load_data(data["equity_curve"], data["drawdown_pct"])

        # 2. Update Trades Log
        self.trades_table.load_trades(data["trades"])

        # 3. Update KPI Metrics Cards
        self.metrics_dashboard.update_metrics(data["metrics"])

        # 4. Update Header Ticker Badge
        last_price = data["df"].iloc[-1]["close"]
        prev_price = data["df"].iloc[-2]["close"]
        chg_pct = ((last_price - prev_price) / prev_price) * 100
        color = "#089981" if chg_pct >= 0 else "#f23645"
        bg = "#13241b" if chg_pct >= 0 else "#251717"
        border = "#089981" if chg_pct >= 0 else "#f23645"
        arrow = "▲" if chg_pct >= 0 else "▼"
        self.symbol_badge.setText(f"{symbol}  ${last_price:.2f}  {arrow} {chg_pct:+.2f}%")
        self.symbol_badge.setStyleSheet(f"""
            background-color: {bg};
            color: {color};
            border: 1px solid {border};
            border-radius: 5px;
            padding: 5px 12px;
            font-weight: 700;
            font-size: 12px;
            font-family: 'Consolas', 'Cascadia Code', monospace;
        """)

        # 5. Status Bar update
        self.status_bar.showMessage(f"● Symbol: {symbol} · Strategy: {strategy} · 180 Daily Bars · {len(data['trades'])} Trades · Simulation Latency: 15ms")
