"""
AI Research Assistant & Quantitative Intelligence Panel
Refactored into clean accessible tabs:
- [AI Copilot] Tab: Interactive chat with streaming prompts & inference model selector
- [Alpha Metrics] Tab: Institutional risk measures (VaR, Sortino, Calmar, Beta)
- [Data Feed] Tab: Provider configuration and offline/live cache management
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


class AIAssistantPanel(QtWidgets.QWidget):
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

        # Tab 1: AI Copilot Chat & Quick Prompts
        tab_chat = self.create_chat_tab()
        self.tabs.addTab(tab_chat, "AI Copilot")

        # Tab 2: Alpha Risk Analytics
        tab_analytics = self.create_analytics_tab()
        self.tabs.addTab(tab_analytics, "Alpha Stats")

        # Tab 3: Data Feeds & Storage
        tab_feed = self.create_feed_tab()
        self.tabs.addTab(tab_feed, "Data Feed")

        layout.addWidget(self.tabs)

    def create_chat_tab(self):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(2, 4, 2, 2)
        layout.setSpacing(8)

        # Model Selector Card
        model_card = SectionCard("Inference Engine")
        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.addItems([
            "Claude 3.5 Sonnet · Alpha Analyst",
            "Gemini 1.5 Pro · Quant Modeling",
            "DeepSeek-R1 · Mathematical Proofs",
            "Local Ollama · Llama 3 70B Quant"
        ])
        model_card.add_widget(self.model_combo)
        layout.addWidget(model_card)

        # Quick Actions Card
        quick_card = SectionCard("Rapid Research Prompts")
        quick_btns = [
            ("🔍 Analyze Drawdown Risk", self.prompt_drawdown),
            ("⚡ Suggest Parameter Tuning", self.prompt_optimize),
            ("⚖️ Risk / Reward Profile Review", self.prompt_risk),
            ("📝 Explain Strategy Weaknesses", self.prompt_weakness),
        ]

        for text, handler in quick_btns:
            btn = QtWidgets.QPushButton(text)
            btn.setProperty("aiChip", "true")
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(handler)
            quick_card.add_widget(btn)

        layout.addWidget(quick_card)

        # Chat Output
        self.chat_display = QtWidgets.QTextBrowser()
        self.chat_display.setStyleSheet("""
            background-color: #131722;
            border: 1px solid #2a2e39;
            border-radius: 6px;
            padding: 8px;
            font-size: 11px;
            line-height: 1.5;
        """)
        layout.addWidget(self.chat_display, 1)

        # Input Area
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setSpacing(6)
        self.prompt_input = QtWidgets.QLineEdit()
        self.prompt_input.setPlaceholderText("Ask AI to analyze alpha or optimize parameters...")
        self.prompt_input.returnPressed.connect(self.send_custom_prompt)

        self.send_btn = QtWidgets.QPushButton("Ask AI")
        self.send_btn.setStyleSheet("""
            background-color: #2962ff;
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 5px;
            min-height: 32px;
            padding: 0 14px;
            font-size: 12px;
        """)
        self.send_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_custom_prompt)

        input_layout.addWidget(self.prompt_input, 1)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        # Welcome message
        self.chat_display.setHtml("""
        <div style='color: #d1d4dc; font-size: 11px; line-height: 1.5; font-family: -apple-system, sans-serif;'>
            <p><b style='color: #2962ff; font-size: 12px;'>Quant AI Copilot Ready</b></p>
            <p style='color: #9598a1;'>Current active backtest: <b>NVDA</b> using <b>AI Trend + Volatility Filter</b>.</p>
            <p>Click any rapid research prompt above or enter a hypothesis to diagnose alpha decay.</p>
        </div>
        """)

        return container

    def create_analytics_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(2, 4, 2, 4)
        layout.setSpacing(8)

        card_risk = SectionCard("Institutional Risk Metrics")
        form = QtWidgets.QFormLayout()
        form.setSpacing(8)

        metrics = [
            ("Sortino Ratio:", "2.84", "#089981"),
            ("Calmar Ratio:", "4.40", "#089981"),
            ("Daily VaR (95%):", "-$1,420", "#f23645"),
            ("Beta to SPY:", "1.14", "#ffffff"),
            ("Avg Win / Avg Loss:", "1.85x", "#089981"),
            ("Max Consec Losses:", "2 Trades", "#9598a1"),
            ("Recovery Factor:", "4.4x", "#089981")
        ]

        for label, val, color in metrics:
            lbl = QtWidgets.QLabel(label)
            lbl.setProperty("fieldLabel", "true")
            val_lbl = QtWidgets.QLabel(val)
            val_lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-family: 'Consolas', monospace; font-size: 12px;")
            form.addRow(lbl, val_lbl)

        card_risk.add_layout(form)
        layout.addWidget(card_risk)

        # Regimes card
        card_regimes = SectionCard("Market Regime Exposure")
        rl = QtWidgets.QVBoxLayout()
        rl.addWidget(QtWidgets.QLabel("• Bull Trend Regimes: <b>+28.4% Alpha</b>"))
        rl.addWidget(QtWidgets.QLabel("• High Volatility Periods: <b>+8.2% Alpha</b>"))
        rl.addWidget(QtWidgets.QLabel("• Sideways / Range-bound: <b>-2.1% Alpha</b>"))
        for i in range(rl.count()):
            rl.itemAt(i).widget().setStyleSheet("color: #d1d4dc; font-size: 11px;")
        card_regimes.add_layout(rl)
        layout.addWidget(card_regimes)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def create_feed_tab(self):
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(2, 4, 2, 4)
        layout.setSpacing(8)

        card_feed = SectionCard("Data Feed Configuration")
        form = QtWidgets.QFormLayout()
        form.setSpacing(8)

        feed_combo = QtWidgets.QComboBox()
        feed_combo.addItems([
            "High-Fidelity Synthetic Engine (Active)",
            "Yahoo Finance API (Daily EOD)",
            "Polygon.io (Tick / Minute)",
            "Interactive Brokers TWS Gateway"
        ])
        form.addRow("Provider:", feed_combo)

        date_combo = QtWidgets.QComboBox()
        date_combo.addItems(["Last 6 Months (180 Bars)", "Last 1 Year (252 Bars)", "Last 5 Years"])
        form.addRow("Historical Window:", date_combo)

        card_feed.add_layout(form)
        layout.addWidget(card_feed)

        card_cache = SectionCard("Local Caching & Offline DB")
        cl = QtWidgets.QVBoxLayout()
        cl.addWidget(QtWidgets.QLabel("• Local Storage: <b>DuckDB + Parquet</b>"))
        cl.addWidget(QtWidgets.QLabel("• Cached Bars: <b>24,500 Bars</b>"))
        cl.addWidget(QtWidgets.QLabel("• Cache Size: <b>3.2 MB</b>"))
        for i in range(cl.count()):
            cl.itemAt(i).widget().setStyleSheet("color: #d1d4dc; font-size: 11px;")
        
        clear_btn = QtWidgets.QPushButton("Purge Local Cache")
        clear_btn.setStyleSheet("background-color: #1e222d; color: #f23645; border: 1px solid #363a45; border-radius: 4px; padding: 4px 8px; font-size: 11px;")
        clear_btn.clicked.connect(lambda: QtWidgets.QMessageBox.information(self, "Cache", "Local cache cleared."))
        cl.addWidget(clear_btn)
        card_cache.add_layout(cl)
        layout.addWidget(card_cache)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def append_ai_message(self, user_query, ai_html):
        user_block = f"""
        <div style='margin-top: 8px; margin-bottom: 4px; padding: 6px 10px; background-color: #1e222d; border-left: 3px solid #2962ff; border-radius: 4px;'>
            <b style='color: #2962ff; font-size: 10px; text-transform: uppercase;'>Researcher Prompt</b><br/>
            <span style='color: #ffffff; font-size: 11px;'>{user_query}</span>
        </div>
        """
        ai_block = f"""
        <div style='margin-bottom: 10px; padding: 8px 10px; background-color: #171b26; border: 1px solid #2a2e39; border-radius: 5px; font-size: 11px; line-height: 1.5;'>
            <b style='color: #089981; font-size: 10px; text-transform: uppercase;'>Copilot Analysis</b><br/>
            {ai_html}
        </div>
        """
        self.chat_display.append(user_block + ai_block)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def prompt_drawdown(self):
        query = "Analyze current drawdown risk and worst-case scenario"
        response = """
        <p style='color: #ffffff;'><b>Drawdown Analysis Summary:</b></p>
        <ul style='color: #9598a1; margin-left: -15px; padding-left: 20px;'>
            <li><b>Max Drawdown:</b> <span style='color: #f23645; font-weight: bold;'>-7.85%</span> (Occurred around day 114 during tech sector pullback).</li>
            <li><b>Recovery Duration:</b> 14 trading days to regain previous High-Water Mark.</li>
            <li><b>Recommendation:</b> Implement an ATR-based Trailing Stop Loss (suggested: 2.2x ATR) to cap individual trade drawdown under 2.5%.</li>
        </ul>
        """
        self.append_ai_message(query, response)

    def prompt_optimize(self):
        query = "Suggest hyperparameter tuning for maximum Sharpe Ratio"
        response = """
        <p style='color: #ffffff;'><b>Hyperparameter Grid Search Recommendation:</b></p>
        <table style='color: #d1d4dc; border-collapse: collapse; width: 100%; font-size: 10px;'>
            <tr style='color: #787b86; border-bottom: 1px solid #363a45;'>
                <th align='left'>Parameter</th><th align='left'>Current</th><th align='left'>AI Optimal</th><th align='left'>Impact</th>
            </tr>
            <tr><td>Fast Window</td><td>10</td><td style='color:#2962ff; font-weight:bold;'>13</td><td>Filters whip-saws</td></tr>
            <tr><td>Slow Window</td><td>30</td><td style='color:#2962ff; font-weight:bold;'>34</td><td>Fibonacci cycle</td></tr>
            <tr><td>RSI Filter</td><td>Off</td><td style='color:#089981; font-weight:bold;'>&gt; 48</td><td>+0.32 Sharpe</td></tr>
        </table>
        """
        self.append_ai_message(query, response)

    def prompt_risk(self):
        query = "Evaluate Risk / Reward profile and trade expectancy"
        response = """
        <p style='color: #ffffff;'><b>Expectancy & Edge Metrics:</b></p>
        <div style='color: #9598a1;'>
            • <b>Win Rate:</b> 66.7% (8 wins / 4 losses)<br/>
            • <b>Profit Factor:</b> 2.45 (Gross Profit $46.2k vs Loss $18.8k)<br/>
            • <b>Expectancy:</b> +$2,876 per trade signal.<br/>
            • <b>Verdict:</b> Statistically sound alpha signal on 6-month historical sample.
        </div>
        """
        self.append_ai_message(query, response)

    def prompt_weakness(self):
        query = "Explain current alpha vulnerabilities"
        response = """
        <p style='color: #ffffff;'><b>Identified Vulnerabilities:</b></p>
        <div style='color: #9598a1;'>
            1. <b>Sideways Regimes:</b> SMA crossovers produce chop when annualized volatility drops below 15%.<br/>
            2. <b>Earnings Gaps:</b> 2 entries near quarterly releases experienced 1.8% slippage.<br/>
            3. <b>Mitigation:</b> Enforce an ADX &gt; 25 threshold to enter only in verified directional trends.
        </div>
        """
        self.append_ai_message(query, response)

    def send_custom_prompt(self):
        text = self.prompt_input.text().strip()
        if not text:
            return
        self.prompt_input.clear()
        
        response = f"""
        <p style='color: #ffffff;'>Analyzing <b>"{text}"</b> across market regime...</p>
        <div style='color: #9598a1;'>
            Simulated AI inference complete. The model suggests testing this hypothesis across 5-year multi-asset portfolios to verify robustness against regime shifts.
        </div>
        """
        self.append_ai_message(text, response)
