import numpy as np
from typing import List

def compute_rolling_returns(prices: List[float], lookback: int = 60) -> float:
    """Computes normalized lookback return."""
    if len(prices) < lookback:
        return 0.0
    p_array = np.array(prices[-lookback:])
    return (p_array[-1] - p_array[0]) / p_array[0]

def compute_daily_volatility(prices: List[float], lookback: int = 60) -> float:
    """Computes annualized daily return standard deviation."""
    if len(prices) < lookback:
        return 1e-4
    p_array = np.array(prices[-lookback:])
    daily_returns = np.diff(p_array) / p_array[:-1]
    return float(np.std(daily_returns, ddof=1) + 1e-8)