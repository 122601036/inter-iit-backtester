from strategy_base import BaseStrategy, Context, Bar
from typing import Dict
from src.models import MomentumRiskParityModel

class ParticipantStrategy(BaseStrategy):
    def initialize(self, context: Context) -> None:
        """
        Pure 2-Rule Adaptive Momentum Strategy.
        Uses statistical risk-parity model and dynamic execution decider engine.
        """
        self.universe = context.universe
        self.lookback = 60                       # 60-day rolling lookback window
        self.min_cooldown_days = 10              # Rule 1 Cooldown: Minimum holding period
        self.max_daily_drawdown_trigger = 0.03   # Rule 2 Circuit Breaker: 3.0% daily equity drop
        self.max_holding_days = 25               # Safety Cap: Force rebalance if held for 25 days
        self.top_n = 4                           # Top 4 momentum assets
        
        # Instantiate statistical model from src/models/
        self.model = MomentumRiskParityModel(lookback=self.lookback, top_n=self.top_n)
        
        self.price_history = {ticker: [] for ticker in self.universe}
        self.days_since_rebalance = 0
        self.active_top_4 = []
        self.prev_portfolio_value = getattr(context, 'initial_cash', 100000.0)

    def on_bar(self, context: Context, bars: Dict[str, Bar]) -> None:
        """
        Processes daily OHLCV bars. Evaluates adaptive decider rules and calls 
        the risk parity model strictly when a rebalance trigger fires.
        """
        # 1. Update price history buffer
        for ticker, bar in bars.items():
            if ticker in self.price_history:
                self.price_history[ticker].append(bar.close)

        self.days_since_rebalance += 1

        # Wait until 60-day lookback window is full
        if context.step < self.lookback:
            context.set_target_weights({})
            return

        # 2. Evaluate Dynamic Decider Rules
        new_top_4, potential_weights = self.model.compute_signals_and_weights(
            self.price_history, self.universe
        )

        has_rank_changed = set(new_top_4) != set(self.active_top_4) if self.active_top_4 else True
        rule_1_triggered = (self.days_since_rebalance >= self.min_cooldown_days) and has_rank_changed

        daily_equity_drop = (self.prev_portfolio_value - context.portfolio_value) / self.prev_portfolio_value if self.prev_portfolio_value > 0 else 0.0
        rule_2_triggered = daily_equity_drop >= self.max_daily_drawdown_trigger
        
        safety_cap_triggered = self.days_since_rebalance >= self.max_holding_days

        # 3. Rebalance Execution vs State Clearing
        if rule_1_triggered or rule_2_triggered or safety_cap_triggered:
            context.set_target_weights(potential_weights)
            self.active_top_4 = new_top_4
            self.days_since_rebalance = 0
        else:
            # Clear target weights so backtester skips execute_pending_orders on off-steps
            context.set_target_weights({})

        self.prev_portfolio_value = context.portfolio_value