import numpy as np
from typing import Dict, List, Tuple

class MomentumRiskParityModel:
    def __init__(self, lookback: int = 60, top_n: int = 4):
        self.lookback = lookback
        self.top_n = top_n

    def compute_signals_and_weights(
        self, price_history: Dict[str, List[float]], universe: List[str]
    ) -> Tuple[List[str], Dict[str, float]]:
        """
        Computes 60-day cross-sectional momentum ranking 
        and inverse-volatility risk parity target weights.
        """
        returns_60d = {}
        volatility_60d = {}

        for ticker in universe:
            prices = np.array(price_history[ticker][-self.lookback:])
            returns_60d[ticker] = (prices[-1] - prices[0]) / prices[0]
            daily_returns = np.diff(prices) / prices[:-1]
            volatility_60d[ticker] = np.std(daily_returns, ddof=1) + 1e-8

        # Rank universe by momentum
        ranked_tickers = sorted(universe, key=lambda t: returns_60d[t], reverse=True)
        top_picks = ranked_tickers[:self.top_n]

        # Inverse Volatility Scaling
        inv_vols = {t: 1.0 / volatility_60d[t] for t in top_picks}
        total_inv_vol = sum(inv_vols.values())

        target_weights = {t: 0.0 for t in universe}
        if total_inv_vol > 0:
            for t in top_picks:
                target_weights[t] = inv_vols[t] / total_inv_vol

        return top_picks, target_weights