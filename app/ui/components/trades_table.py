"""
Trade Execution Log Table Component
Refactored using jakubkrehel/skills principles:
- Tabular numbers on all financial data to prevent horizontal alignment shifts
- Distinct pill badges for WIN / LOSS states with high-contrast text
- Alternating row contrast for quick visual scanning
"""

from PySide6 import QtWidgets, QtCore, QtGui


class TradeLogTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        headers = [
            "Trade ID", "Direction", "Entry Date", "Entry Price", 
            "Exit Date", "Exit Price", "Shares", "P&L ($)", "Return (%)", "Result"
        ]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    def load_trades(self, trades):
        self.setRowCount(0)
        self.setRowCount(len(trades))

        for row_idx, t in enumerate(trades):
            # ID
            item_id = QtWidgets.QTableWidgetItem(f"TRD-{t['id']:03d}")
            item_id.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_id.setForeground(QtGui.QBrush(QtGui.QColor("#8b949e")))
            self.setItem(row_idx, 0, item_id)

            # Direction
            item_type = QtWidgets.QTableWidgetItem(t["type"])
            item_type.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_type.setForeground(QtGui.QBrush(QtGui.QColor("#58a6ff")))
            self.setItem(row_idx, 1, item_type)

            # Dates
            item_edate = QtWidgets.QTableWidgetItem(t["entry_date"])
            item_xdate = QtWidgets.QTableWidgetItem(t["exit_date"])
            item_edate.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_xdate.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.setItem(row_idx, 2, item_edate)
            self.setItem(row_idx, 4, item_xdate)

            # Prices
            item_eprice = QtWidgets.QTableWidgetItem(f"${t['entry_price']:.2f}")
            item_xprice = QtWidgets.QTableWidgetItem(f"${t['exit_price']:.2f}")
            item_eprice.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            item_xprice.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row_idx, 3, item_eprice)
            self.setItem(row_idx, 5, item_xprice)

            # Shares
            item_shares = QtWidgets.QTableWidgetItem(f"{t['shares']:,}")
            item_shares.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row_idx, 6, item_shares)

            # P&L
            pnl = t["pnl"]
            pnl_color = "#2ea043" if pnl >= 0 else "#f85149"
            item_pnl = QtWidgets.QTableWidgetItem(f"{pnl:+,.2f}")
            item_pnl.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            item_pnl.setForeground(QtGui.QBrush(QtGui.QColor(pnl_color)))
            self.setItem(row_idx, 7, item_pnl)

            # Return %
            ret_pct = t["return_pct"]
            item_ret = QtWidgets.QTableWidgetItem(f"{ret_pct:+.2f}%")
            item_ret.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            item_ret.setForeground(QtGui.QBrush(QtGui.QColor(pnl_color)))
            self.setItem(row_idx, 8, item_ret)

            # Result Badge
            status_text = "WIN" if pnl >= 0 else "LOSS"
            item_status = QtWidgets.QTableWidgetItem(status_text)
            item_status.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_status.setForeground(QtGui.QBrush(QtGui.QColor(pnl_color)))
            self.setItem(row_idx, 9, item_status)
