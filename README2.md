## Core Strategy Framework

### I. Factor Construction & Signal Generation
The strategy employs a cross-sectional momentum factor engine evaluating relative strength across a 24-asset universe over a 60-day lookback window. By ranking assets cross-sectionally, the engine isolates top-tier momentum leaders while filtering out underperforming securities.

### II. Statistical Risk Parity Allocation Model
Rather than relying on unconstrained machine learning predictors subject to regime drift and over-parameterization, position sizing is governed by an inverse-volatility Risk Parity formulation inside `src/models/`. Capital is allocated inversely proportional to asset variance ($\sigma_i$), ensuring equal risk contribution across selected assets and strictly guaranteeing zero gross leverage ($\sum \vert{}w_i\vert{} \le 1.0$).

### III. Adaptive State-Machine Execution Engine
Execution is controlled by a 2-rule adaptive state machine in `src/engine.py`. By decoupling factor evaluation from order generation, the strategy enforces position persistence via explicit state locking (`context.set_target_weights({})`). This design mitigates slippage and commission drag while maintaining a 3.0% daily drawdown circuit breaker for tail-risk protection.
