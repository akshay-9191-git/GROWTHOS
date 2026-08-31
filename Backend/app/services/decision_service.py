from app.services.opportunity_service import calculate_opportunities
from app.models.action_outcome import ActionOutcome
from app.models.growth_action import GrowthAction


def make_growth_decision(
    db,
    user_id: int,
    product_id: int
):

    # =====================================================
    # 1. Find current opportunity
    # =====================================================

    opportunities = calculate_opportunities(db)

    opportunity = next(
        (
            item
            for item in opportunities
            if item["user_id"] == user_id
            and item["product_id"] == product_id
        ),
        None
    )

    if not opportunity:
        return None

    # =====================================================
    # 2. Get historical outcomes
    # =====================================================

    results = (
        db.query(ActionOutcome, GrowthAction)
        .join(
            GrowthAction,
            ActionOutcome.action_id == GrowthAction.action_id
        )
        .all()
    )

    # =====================================================
    # 3. Calculate performance by strategy
    # =====================================================

    strategy_stats = {}

    for outcome, action in results:

        strategy = action.opportunity_type

        if strategy not in strategy_stats:

            strategy_stats[strategy] = {
                "total": 0,
                "conversions": 0,
                "revenue": 0.0
            }

        stats = strategy_stats[strategy]

        stats["total"] += 1

        if outcome.converted:
            stats["conversions"] += 1

        stats["revenue"] += (
            outcome.revenue_generated or 0
        )

    # =====================================================
    # 4. Current opportunity type
    # =====================================================

    current_type = opportunity["recommended_action"]

    # =====================================================
    # 5. Try to match historical strategy
    # =====================================================

    matching_strategy = None

    for strategy in strategy_stats:

        if (
            "cart" in current_type.lower()
            and "cart" in strategy.lower()
        ):
            matching_strategy = strategy

        elif (
            "upsell" in current_type.lower()
            and "upsell" in strategy.lower()
        ):
            matching_strategy = strategy

        elif (
            "cross" in current_type.lower()
            and "cross" in strategy.lower()
        ):
            matching_strategy = strategy

    # =====================================================
    # 6. Calculate historical confidence
    # =====================================================

    if matching_strategy:

        stats = strategy_stats[matching_strategy]

        if stats["total"] > 0:

            historical_conversion_rate = round(
                (
                    stats["conversions"]
                    / stats["total"]
                ) * 100,
                2
            )

        else:

            historical_conversion_rate = 0

    else:

        historical_conversion_rate = 0

    # =====================================================
    # 7. Calculate decision confidence
    # =====================================================

    intent_score = opportunity["intent_score"]

    if matching_strategy:

        confidence = round(
            (
                intent_score * 0.6
                + historical_conversion_rate * 0.4
            ),
            2
        )

    else:

        confidence = round(
            intent_score * 0.6,
            2
        )

    # =====================================================
    # 8. Determine strategy
    # =====================================================

    if matching_strategy:

        recommended_strategy = matching_strategy

        reason = (
            f"{matching_strategy} matches the current growth "
            f"opportunity and has a historical conversion rate "
            f"of {historical_conversion_rate}%."
        )

    else:

        recommended_strategy = opportunity["recommended_action"]

        reason = (
            "No historical performance data is available for "
            "this opportunity type, so the decision is based "
            "primarily on the customer's current intent."
        )

    # =====================================================
    # 9. Return decision
    # =====================================================

    return {

        "customer": opportunity["user_name"],

        "product": opportunity["product_name"],

        "intent_score": intent_score,

        "intent": opportunity["intent"],

        "opportunity_type": opportunity["recommended_action"],

        "recommended_strategy": recommended_strategy,

        "confidence": confidence,

        "historical_conversion_rate": (
            historical_conversion_rate
        ),

        "reason": reason,

        "recommended_action": opportunity[
            "recommended_action"
        ]
    }
def get_best_strategy(db, opportunity):

    results = (
        db.query(ActionOutcome, GrowthAction)
        .join(
            GrowthAction,
            ActionOutcome.action_id
            == GrowthAction.action_id
        )
        .all()
    )

    strategy_stats = {}

    for outcome, action in results:

        strategy = action.opportunity_type

        if strategy not in strategy_stats:
            strategy_stats[strategy] = {
                "actions": 0,
                "outcomes": 0,
                "conversions": 0,
                "revenue": 0.0
            }

        stats = strategy_stats[strategy]
        stats["actions"] += 1

        stats["outcomes"] += 1

        if outcome.converted:
            stats["conversions"] += 1

        stats["revenue"] += (
            outcome.revenue_generated or 0
        )

    # -----------------------------------------------------
    # No historical data
    # -----------------------------------------------------

    if not strategy_stats:

        return {
            "strategy": opportunity["recommended_action"],
            "confidence": opportunity["intent_score"],
            "historical_actions": 0,
            "historical_outcomes": 0,
            "historical_conversions": 0,
            "conversion_rate": 0,
            "historical_revenue": 0,
            "reason": (
                "No historical performance data is available. "
                "The decision is based on current customer intent."
            )
        }

    # -----------------------------------------------------
    # Calculate strategy performance
    # -----------------------------------------------------

    ranked = []

    for strategy, stats in strategy_stats.items():

        conversion_rate = 0

        if stats["outcomes"] > 0:
            conversion_rate = (
                stats["conversions"]
                / stats["outcomes"]
            ) * 100

        # Performance score
        performance_score = (
            conversion_rate * 0.7
            + min(stats["revenue"] / 1000, 100) * 0.3
        )

        ranked.append({
            "strategy": strategy,
            "actions": stats["actions"],
            "outcomes": stats["outcomes"],
            "conversions": stats["conversions"],
            "conversion_rate": round(
                conversion_rate,
                2
            ),
            "revenue": float(
                stats["revenue"]
            ),
            "performance_score": round(
                performance_score,
                2
            )
        })

    # -----------------------------------------------------
    # Select best strategy
    # -----------------------------------------------------

    ranked.sort(
        key=lambda x: x["performance_score"],
        reverse=True
    )

    best = ranked[0]

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    confidence = round(
        (
            opportunity["intent_score"] * 0.5
            + best["conversion_rate"] * 0.5
        ),
        2
    )

    # -----------------------------------------------------
    # Decision reason
    # -----------------------------------------------------

    reason = (
        f"{best['strategy']} is currently the best-performing "
        f"historical strategy with a "
        f"{best['conversion_rate']}% conversion rate and "
        f"₹{best['revenue']} generated revenue."
    )

    return {

        "strategy": best["strategy"],

        "confidence": confidence,

        "historical_actions": best["actions"],

        "historical_outcomes": best["outcomes"],

        "historical_conversions": best["conversions"],

        "conversion_rate": best["conversion_rate"],

        "historical_revenue": best["revenue"],

        "reason": reason
    }
