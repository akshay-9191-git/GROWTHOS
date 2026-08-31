from sqlalchemy import func, Integer

from app.models.growth_action import GrowthAction
from app.models.action_outcome import ActionOutcome


def get_strategy_performance(db):

    results = (
        db.query(
            GrowthAction.strategy,
            func.count(ActionOutcome.id),
            func.sum(
                func.cast(
                    ActionOutcome.converted,
                    Integer
                )
            ),
            func.coalesce(
                func.sum(
                    ActionOutcome.revenue_generated
                ),
                0
            )
        )
        .join(
            ActionOutcome,
            ActionOutcome.action_id
            == GrowthAction.action_id
        )
        .group_by(
            GrowthAction.strategy
        )
        .all()
    )

    performance = []

    for (
        strategy,
        total_outcomes,
        conversions,
        revenue
    ) in results:

        conversions = conversions or 0
        revenue = revenue or 0

        conversion_rate = 0

        if total_outcomes > 0:
            conversion_rate = (
                conversions / total_outcomes
            ) * 100

        performance.append({

            "strategy": strategy,

            "outcomes": total_outcomes,

            "conversions": conversions,

            "conversion_rate": round(
                conversion_rate,
                2
            ),

            "revenue": float(revenue)
        })

    performance.sort(
        key=lambda x: (
            x["revenue"],
            x["conversion_rate"]
        ),
        reverse=True
    )

    return performance