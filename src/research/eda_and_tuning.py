"""
Research & Sensitivity Analysis for Track A Quantitative Momentum Strategy.
Explores lookback window lengths, cooldown periods, and inverse-volatility weight distributions.
"""

import pandas as pd
import numpy as np

def analyze_universe_momentum(df_path: str):
    df = pd.read_csv(df_path)
    print(f"[Research] Loaded dataset with {len(df)} rows across tickers: {df['ticker'].unique()}")

    # 60-day window volatility vs return spectrum
    pivot_close = df.pivot(index='date', columns='ticker', values='close')
    returns_60 = pivot_close.pct_change(60)
    vol_60 = pivot_close.pct_change().rolling(60).std()

    print("[Research] Average 60-day Cross-Sectional Return Spread:", returns_60.mean().mean())
    print("[Research] Average 60-day Risk Parity Volatility Floor:", vol_60.mean().mean())

if __name__ == "__main__":
    # Point to dataset for standalone research execution
    analyze_universe_momentum("data/Dataset_PS-A.csv")