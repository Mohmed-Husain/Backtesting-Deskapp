"""
Performance Metrics Summary Cards Component
Refactored using jakubkrehel/skills principles:
- Tabular numerals for jitter-free numbers
- Clear visual hierarchy: Small uppercase label -> Bold large value -> Subtext badge
- Concentric 8px card radius with 1px structural border
"""

from PySide6 import QtWidgets, QtCore


class MetricCard(QtWidgets.QFrame):
    def __init__(self, title, value, subtext="", sub_type="neutral"):
        super().__init__()
        self.setProperty("metricCard", "true")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        # Micro-label
        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setProperty("metricLabel", "true")

        # Tabular high-contrast metric value
        self.value_label = QtWidgets.QLabel(value)
        self.value_label.setProperty("metricValue", "true")

        # Delta / subtext
        self.sub_label = QtWidgets.QLabel(subtext)
        if sub_type in ["positive", "negative"]:
            self.sub_label.setProperty("metricSub", sub_type)
        else:
            self.sub_label.setStyleSheet("color: #8b949e; font-size: 11px; font-family: 'Consolas', monospace;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.sub_label)

    def update_values(self, value, subtext="", sub_type="neutral"):
        self.value_label.setText(value)
        self.sub_label.setText(subtext)
        if sub_type in ["positive", "negative"]:
            self.sub_label.setProperty("metricSub", sub_type)
        self.sub_label.style().unpolish(self.sub_label)
        self.sub_label.style().polish(self.sub_label)


class MetricsDashboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = {}
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        card_defs = [
            ("net_profit", "Net Profit", "+$34,520.00", "+34.52% ROI", "positive"),
            ("win_rate", "Win Rate", "66.7%", "8 Wins / 4 Losses", "positive"),
            ("max_dd", "Max Drawdown", "-7.85%", "Peak to Trough", "negative"),
            ("sharpe", "Sharpe Ratio", "2.18", "Annualized Risk-Adj", "positive"),
            ("profit_factor", "Profit Factor", "2.45", "Gross Win/Loss", "positive"),
            ("total_trades", "Trades Executed", "12", "Avg Hold: 6.2d", "neutral"),
        ]

        for key, title, val, sub, sub_t in card_defs:
            card = MetricCard(title, val, sub, sub_t)
            self.cards[key] = card
            layout.addWidget(card)

    def update_metrics(self, metrics):
        self.cards["net_profit"].update_values(metrics.get("net_profit", "$0"), metrics.get("roi_pct", "0% ROI"), "positive")
        self.cards["win_rate"].update_values(metrics.get("win_rate", "0%"), f"{metrics.get('total_trades', '0')} Trades", "positive")
        self.cards["max_dd"].update_values(metrics.get("max_drawdown", "0%"), "Peak to Trough", "negative")
        self.cards["sharpe"].update_values(metrics.get("sharpe_ratio", "0.0"), "Annualized Risk-Adj", "positive")
        self.cards["profit_factor"].update_values(metrics.get("profit_factor", "0.0"), "Gross Win/Loss", "positive")
        self.cards["total_trades"].update_values(metrics.get("total_trades", "0"), f"Capital: {metrics.get('initial_capital', '')}", "neutral")
