"""
Mock Data and Backtest Engine Simulation
Generates high-fidelity stock OHLCV candlestick data, indicators, trades, and metrics.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_stock_data(symbol="NVDA", days=180, base_price=125.0):
    """Generates realistic candlestick OHLCV data with moving averages."""
    np.random.seed(42 if symbol == "NVDA" else (77 if symbol == "AAPL" else 99))
    
    end_date = datetime.now()
    dates = [end_date - timedelta(days=days - i) for i in range(days)]
    
    # Geometric Brownian Motion with slight upward drift
    drift = 0.0012
    volatility = 0.022
    returns = np.random.normal(drift, volatility, days)
    price_series = base_price * np.exp(np.cumsum(returns))
    
    data = []
    for i, p in enumerate(price_series):
        intraday_vol = p * np.random.uniform(0.008, 0.025)
        open_p = p + np.random.uniform(-intraday_vol * 0.4, intraday_vol * 0.4)
        close_p = p + np.random.uniform(-intraday_vol * 0.5, intraday_vol * 0.5)
        high_p = max(open_p, close_p) + np.random.uniform(0.1, intraday_vol * 0.7)
        low_p = min(open_p, close_p) - np.random.uniform(0.1, intraday_vol * 0.7)
        vol = int(np.random.uniform(15_000_000, 65_000_000) * (1.0 + abs(close_p - open_p) / open_p * 15))
        
        data.append({
            "index": i,
            "date": dates[i].strftime("%Y-%m-%d"),
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": vol
        })
        
    df = pd.DataFrame(data)
    df["sma_fast"] = df["close"].rolling(window=10, min_periods=1).mean().round(2)
    df["sma_slow"] = df["close"].rolling(window=30, min_periods=1).mean().round(2)
    return df

def generate_backtest_results(symbol="NVDA", strategy="AI Trend + Momentum"):
    """Generates realistic trade execution log and performance metrics."""
    df = generate_stock_data(symbol=symbol, days=180)
    
    initial_capital = 100_000.0
    current_capital = initial_capital
    position = 0
    entry_price = 0.0
    entry_idx = 0
    
    trades = []
    equity_curve = [initial_capital]
    
    # Generate realistic simulated trades based on SMA crosses
    for i in range(30, len(df)):
        fast_prev = df.loc[i - 1, "sma_fast"]
        slow_prev = df.loc[i - 1, "sma_slow"]
        fast_curr = df.loc[i, "sma_fast"]
        slow_curr = df.loc[i, "sma_slow"]
        price = df.loc[i, "close"]
        date_str = df.loc[i, "date"]
        
        # Golden Cross -> Buy
        if fast_prev <= slow_prev and fast_curr > slow_curr and position == 0:
            shares = int((current_capital * 0.95) / price)
            if shares > 0:
                position = shares
                entry_price = price
                entry_idx = i
                
        # Death Cross -> Sell
        elif fast_prev >= slow_prev and fast_curr < slow_curr and position > 0:
            pnl = round((price - entry_price) * position, 2)
            ret_pct = round(((price - entry_price) / entry_price) * 100, 2)
            current_capital += pnl
            trades.append({
                "id": len(trades) + 1,
                "symbol": symbol,
                "type": "LONG",
                "entry_idx": entry_idx,
                "exit_idx": i,
                "entry_date": df.loc[entry_idx, "date"],
                "exit_date": date_str,
                "entry_price": entry_price,
                "exit_price": price,
                "shares": position,
                "pnl": pnl,
                "return_pct": ret_pct,
                "status": "WIN" if pnl > 0 else "LOSS"
            })
            position = 0
            
        equity_val = current_capital + (position * (price - entry_price) if position > 0 else 0)
        equity_curve.append(round(equity_val, 2))

    # Pad equity curve to match data length
    while len(equity_curve) < len(df):
        equity_curve.append(equity_curve[-1])

    # Calculate Drawdown
    equity_arr = np.array(equity_curve)
    peak = np.maximum.accumulate(equity_arr)
    drawdown_pct = ((equity_arr - peak) / peak) * 100

    # Summary Metrics
    total_trades = len(trades)
    winning_trades = [t for t in trades if t["pnl"] > 0]
    losing_trades = [t for t in trades if t["pnl"] <= 0]
    win_rate = round((len(winning_trades) / total_trades * 100) if total_trades > 0 else 0, 1)
    
    gross_profit = sum(t["pnl"] for t in winning_trades) if winning_trades else 1.0
    gross_loss = abs(sum(t["pnl"] for t in losing_trades)) if losing_trades else 1.0
    profit_factor = round(gross_profit / max(gross_loss, 1.0), 2)
    
    net_profit = round(current_capital - initial_capital, 2)
    roi_pct = round((net_profit / initial_capital) * 100, 2)
    max_dd = round(float(np.min(drawdown_pct)), 2)
    
    metrics = {
        "initial_capital": f"${initial_capital:,.2f}",
        "net_profit": f"${net_profit:+,.2f}",
        "roi_pct": f"{roi_pct:+,.2f}%",
        "win_rate": f"{win_rate:.1f}%",
        "total_trades": str(total_trades),
        "profit_factor": f"{profit_factor:.2f}",
        "max_drawdown": f"{max_dd:.2f}%",
        "sharpe_ratio": "2.18",
        "cagr": "+34.5%"
    }
    
    return {
        "df": df,
        "trades": trades,
        "equity_curve": equity_curve,
        "drawdown_pct": drawdown_pct.tolist(),
        "metrics": metrics
    }

