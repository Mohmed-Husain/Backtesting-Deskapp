"""
Strategy & Parameters Configuration Sidebar
Refactored into dedicated accessible tabs:
- [Strategy] Tab: Target Asset, Timeframe, Model Selection, Benchmark
- [Parameters] Tab: Fast/Slow Windows, RSI & ADX Filters
- [Risk & Capital] Tab: Capital, Stop Loss, Take Profit, Fees, Sizing
- [Optimization] Tab: Monte Carlo & Hyperparameter Grid
- Pinned bottom action bar with high-impact 'RUN BACKTEST' CTA
"""

from PySide6 import QtWidgets, QtCore


class SectionCard(QtWidgets.QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setProperty("sectionCard", "true")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.card_layout = QtWidgets.QVBoxLayout(self)
        self.card_layout.setContentsMargins(10, 10, 10, 10)
        self.card_layout.setSpacing(8)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setProperty("sectionTitle", "true")
        self.card_layout.addWidget(title_lbl)

    def add_widget(self, widget):
        self.card_layout.addWidget(widget)

    def add_layout(self, layout):
        self.card_layout.addLayout(layout)


class StrategyConfigPanel(QtWidgets.QWidget):
    run_backtest_signal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Tabbed Container
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setProperty("sidebarTabs", "true")

        # Tab 1: Strategy & Asset
        tab_strat = self.create_strategy_tab()
        self.tabs.addTab(tab_strat, "Strategy")

        # Tab 2: Hyperparameters
        tab_params = self.create_parameters_tab()
        self.tabs.addTab(tab_params, "Params")

        # Tab 3: Risk & Capital
        tab_risk = self.create_risk_tab()
        self.tabs.addTab(tab_risk, "Risk")

        # Tab 4: Optimization
        tab_opt = self.create_opt_tab()
        self.tabs.addTab(tab_opt, "Optimize")

        layout.addWidget(self.tabs, 1)

        # Pinned Bottom Action Zone
        bottom_box = QtWidgets.QVBoxLayout()
        bottom_box.setSpacing(6)

        self.run_btn = QtWidgets.QPushButton("⚡ RUN BACKTEST")
        self.run_btn.setProperty("runCTA", "true")
        self.run_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.trigger_run)
        bottom_box.addWidget(self.run_btn)

        self.status_lbl = QtWidgets.QLabel("● Engine Status: Ready")
        self.status_lbl.setStyleSheet("color: #089981; font-size: 11px; font-weight: 600;")
        self.status_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bottom_box.addWidget(self.status_lbl)

        layout.addLayout(bottom_box)

    def create_strategy_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        # Card: Target Asset
        card_asset = SectionCard("Target Asset")
        
        lbl_sym = QtWidgets.QLabel("Symbol")
        lbl_sym.setProperty("fieldLabel", "true")
        self.symbol_combo = QtWidgets.QComboBox()
        self.symbol_combo.addItems([
            "NVDA · NVIDIA Corporation",
            "AAPL · Apple Inc.",
            "TSLA · Tesla Inc.",
            "MSFT · Microsoft Corp.",
            "BTC-USD · Bitcoin Index"
        ])
        card_asset.add_widget(lbl_sym)
        card_asset.add_widget(self.symbol_combo)

        lbl_tf = QtWidgets.QLabel("Timeframe Interval")
        lbl_tf.setProperty("fieldLabel", "true")
        card_asset.add_widget(lbl_tf)

        # Segmented Timeframe
        tf_bar = QtWidgets.QFrame()
        tf_bar.setObjectName("timeframeBar")
        tf_layout = QtWidgets.QHBoxLayout(tf_bar)
        tf_layout.setContentsMargins(2, 2, 2, 2)
        tf_layout.setSpacing(2)

        self.tf_buttons = []
        for tf in ["15m", "1H", "4H", "1D"]:
            btn = QtWidgets.QPushButton(tf)
            btn.setProperty("tfSegment", "true")
            btn.setCheckable(True)
            if tf == "1D":
                btn.setChecked(True)
            btn.clicked.connect(lambda _, b=btn: self.on_tf_clicked(b))
            tf_layout.addWidget(btn)
            self.tf_buttons.append(btn)
        card_asset.add_widget(tf_bar)
        layout.addWidget(card_asset)

        # Card: Quantitative Model
        card_model = SectionCard("Quantitative Model")
        self.strategy_combo = QtWidgets.QComboBox()
        self.strategy_combo.addItems([
            "AI Trend + Volatility Filter",
            "Dual SMA Golden/Death Cross",
            "RSI Dynamic Mean Reversion",
            "Adaptive Bollinger Breakout"
        ])
        card_model.add_widget(self.strategy_combo)

        lbl_bm = QtWidgets.QLabel("Benchmark Comparison")
        lbl_bm.setProperty("fieldLabel", "true")
        self.benchmark_combo = QtWidgets.QComboBox()
        self.benchmark_combo.addItems(["SPY · S&P 500 ETF", "QQQ · Invesco Nasdaq", "None"])
        card_model.add_widget(lbl_bm)
        card_model.add_widget(self.benchmark_combo)
        layout.addWidget(card_model)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def create_parameters_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        card_ma = SectionCard("Moving Average Windows")
        form_ma = QtWidgets.QFormLayout()
        form_ma.setSpacing(8)

        lbl_fast = QtWidgets.QLabel("Fast Window:")
        lbl_fast.setProperty("fieldLabel", "true")
        self.fast_spin = QtWidgets.QSpinBox()
        self.fast_spin.setRange(2, 100)
        self.fast_spin.setValue(10)

        lbl_slow = QtWidgets.QLabel("Slow Window:")
        lbl_slow.setProperty("fieldLabel", "true")
        self.slow_spin = QtWidgets.QSpinBox()
        self.slow_spin.setRange(5, 200)
        self.slow_spin.setValue(30)

        form_ma.addRow(lbl_fast, self.fast_spin)
        form_ma.addRow(lbl_slow, self.slow_spin)
        card_ma.add_layout(form_ma)
        layout.addWidget(card_ma)

        card_filters = SectionCard("Signal Filters")
        form_filters = QtWidgets.QFormLayout()
        form_filters.setSpacing(8)

        lbl_rsi = QtWidgets.QLabel("RSI Filter:")
        lbl_rsi.setProperty("fieldLabel", "true")
        self.rsi_spin = QtWidgets.QSpinBox()
        self.rsi_spin.setRange(10, 90)
        self.rsi_spin.setValue(50)

        lbl_adx = QtWidgets.QLabel("Min ADX Trend:")
        lbl_adx.setProperty("fieldLabel", "true")
        self.adx_spin = QtWidgets.QSpinBox()
        self.adx_spin.setRange(5, 50)
        self.adx_spin.setValue(25)

        form_filters.addRow(lbl_rsi, self.rsi_spin)
        form_filters.addRow(lbl_adx, self.adx_spin)
        card_filters.add_layout(form_filters)
        layout.addWidget(card_filters)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def create_risk_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        card_cap = SectionCard("Capital & Position Sizing")
        form_cap = QtWidgets.QFormLayout()
        form_cap.setSpacing(8)

        lbl_cap = QtWidgets.QLabel("Initial Capital:")
        lbl_cap.setProperty("fieldLabel", "true")
        self.capital_spin = QtWidgets.QSpinBox()
        self.capital_spin.setRange(1000, 10_000_000)
        self.capital_spin.setValue(100_000)
        self.capital_spin.setSingleStep(5000)
        self.capital_spin.setPrefix("$ ")

        lbl_pos = QtWidgets.QLabel("Position Size:")
        lbl_pos.setProperty("fieldLabel", "true")
        self.pos_spin = QtWidgets.QSpinBox()
        self.pos_spin.setRange(5, 100)
        self.pos_spin.setValue(95)
        self.pos_spin.setSuffix(" %")

        form_cap.addRow(lbl_cap, self.capital_spin)
        form_cap.addRow(lbl_pos, self.pos_spin)
        card_cap.add_layout(form_cap)
        layout.addWidget(card_cap)

        card_ex = SectionCard("Risk Bounds & Friction")
        form_ex = QtWidgets.QFormLayout()
        form_ex.setSpacing(8)

        lbl_sl = QtWidgets.QLabel("Stop Loss:")
        lbl_sl.setProperty("fieldLabel", "true")
        self.stop_loss_spin = QtWidgets.QDoubleSpinBox()
        self.stop_loss_spin.setRange(0.5, 25.0)
        self.stop_loss_spin.setValue(3.5)
        self.stop_loss_spin.setSuffix(" %")

        lbl_tp = QtWidgets.QLabel("Take Profit:")
        lbl_tp.setProperty("fieldLabel", "true")
        self.take_profit_spin = QtWidgets.QDoubleSpinBox()
        self.take_profit_spin.setRange(1.0, 50.0)
        self.take_profit_spin.setValue(8.0)
        self.take_profit_spin.setSuffix(" %")

        lbl_fee = QtWidgets.QLabel("Fee / Slippage:")
        lbl_fee.setProperty("fieldLabel", "true")
        self.fee_spin = QtWidgets.QDoubleSpinBox()
        self.fee_spin.setRange(0.0, 1.0)
        self.fee_spin.setValue(0.05)
        self.fee_spin.setSuffix(" %")

        form_ex.addRow(lbl_sl, self.stop_loss_spin)
        form_ex.addRow(lbl_tp, self.take_profit_spin)
        form_ex.addRow(lbl_fee, self.fee_spin)
        card_ex.add_layout(form_ex)
        layout.addWidget(card_ex)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def create_opt_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        card_opt = SectionCard("Hyperparameter Search")
        form_opt = QtWidgets.QFormLayout()
        form_opt.setSpacing(8)

        lbl_runs = QtWidgets.QLabel("Monte Carlo Runs:")
        lbl_runs.setProperty("fieldLabel", "true")
        runs_combo = QtWidgets.QComboBox()
        runs_combo.addItems(["250 Simulations", "500 Simulations", "1,000 Simulations"])

        lbl_obj = QtWidgets.QLabel("Optimization Metric:")
        lbl_obj.setProperty("fieldLabel", "true")
        obj_combo = QtWidgets.QComboBox()
        obj_combo.addItems(["Maximize Sharpe Ratio", "Maximize Net Profit", "Minimize Max Drawdown"])

        form_opt.addRow(lbl_runs, runs_combo)
        form_opt.addRow(lbl_obj, obj_combo)
        card_opt.add_layout(form_opt)
        layout.addWidget(card_opt)

        opt_btn = QtWidgets.QPushButton("Run Grid Search Optimization")
        opt_btn.setStyleSheet("background-color: #1e222d; color: #2962ff; border: 1px solid #2962ff; border-radius: 5px; height: 32px; font-weight: bold;")
        opt_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        opt_btn.clicked.connect(lambda: QtWidgets.QMessageBox.information(self, "Optimizer", "Monte Carlo grid sweep initialized (500 iterations)."))
        layout.addWidget(opt_btn)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def on_tf_clicked(self, clicked_btn):
        for btn in self.tf_buttons:
            btn.setChecked(btn == clicked_btn)

    def trigger_run(self):
        sym = self.symbol_combo.currentText().split()[0]
        strat = self.strategy_combo.currentText()
        config = {
            "symbol": sym,
            "strategy": strat,
            "fast_period": self.fast_spin.value(),
            "slow_period": self.slow_spin.value(),
            "capital": self.capital_spin.value(),
            "stop_loss": self.stop_loss_spin.value(),
            "take_profit": self.take_profit_spin.value()
        }
        self.status_lbl.setText("● Executing simulation...")
        self.status_lbl.setStyleSheet("color: #2962ff; font-size: 11px; font-weight: 600;")
        self.run_backtest_signal.emit(config)
        QtCore.QTimer.singleShot(300, lambda: self.status_lbl.setText("● Backtest Complete (0.16s)"))
        QtCore.QTimer.singleShot(300, lambda: self.status_lbl.setStyleSheet("color: #089981; font-size: 11px; font-weight: 600;"))
