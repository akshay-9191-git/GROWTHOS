from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer

from app.database import get_db

from app.models.growth_action import GrowthAction
from app.models.action_outcome import ActionOutcome


router = APIRouter(
    prefix="/learning",
    tags=["Growth Learning"]
)


# =========================================================
# GROWTH LEARNING ENGINE
# =========================================================

@router.get("/")
def get_learning_insights(
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Total actions
    # -----------------------------------------------------

    total_actions = db.query(GrowthAction).count()

    # -----------------------------------------------------
    # 2. Total outcomes
    # -----------------------------------------------------

    total_outcomes = db.query(ActionOutcome).count()

    # -----------------------------------------------------
    # 3. Total conversions
    # -----------------------------------------------------

    total_conversions = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.converted == True
        )
        .count()
    )

    # -----------------------------------------------------
    # 4. Total revenue
    # -----------------------------------------------------

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(
                    ActionOutcome.revenue_generated
                ),
                0
            )
        )
        .scalar()
    ) or 0

    # -----------------------------------------------------
    # 5. Overall conversion rate
    # -----------------------------------------------------

    conversion_rate = 0.0

    if total_outcomes > 0:
        conversion_rate = (
            total_conversions /
            total_outcomes
        ) * 100

    # -----------------------------------------------------
    # 6. Average revenue per conversion
    # -----------------------------------------------------

    average_revenue = 0.0

    if total_conversions > 0:
        average_revenue = (
            float(total_revenue) /
            total_conversions
        )

    # -----------------------------------------------------
    # 7. Strategy performance
    #
    # IMPORTANT:
    # Group by GrowthAction.strategy instead of
    # GrowthAction.opportunity_type.
    # -----------------------------------------------------

    strategy_results = (
        db.query(
            GrowthAction.strategy.label(
                "strategy"
            ),

            func.count(
                ActionOutcome.id
            ).label(
                "total_outcomes"
            ),

            func.sum(
                func.cast(
                    ActionOutcome.converted,
                    Integer
                )
            ).label(
                "conversions"
            ),

            func.coalesce(
                func.sum(
                    ActionOutcome.revenue_generated
                ),
                0
            ).label(
                "revenue"
            )
        )
        .join(
            ActionOutcome,
            GrowthAction.action_id ==
            ActionOutcome.action_id
        )
        .group_by(
            GrowthAction.strategy
        )
        .all()
    )

    # -----------------------------------------------------
    # 8. Build strategy insights
    # -----------------------------------------------------

    strategies = []

    for result in strategy_results:

        strategy = (
            result.strategy
            or "Unknown Strategy"
        )

        outcomes = (
            result.total_outcomes
            or 0
        )

        conversions = (
            result.conversions
            or 0
        )

        revenue = float(
            result.revenue
            or 0
        )

        strategy_conversion_rate = 0.0

        if outcomes > 0:
            strategy_conversion_rate = (
                conversions /
                outcomes
            ) * 100

        strategies.append(
            {
                "strategy": strategy,

                "total_outcomes":
                    outcomes,

                "conversions":
                    conversions,

                "conversion_rate":
                    round(
                        strategy_conversion_rate,
                        2
                    ),

                "revenue":
                    revenue
            }
        )

    # -----------------------------------------------------
    # 9. Find best performing strategy
    # -----------------------------------------------------

    best_strategy = None

    if strategies:

        best_strategy = max(
            strategies,
            key=lambda x: (
                x["conversion_rate"],
                x["revenue"]
            )
        )

    # -----------------------------------------------------
    # 10. Return learning data
    # -----------------------------------------------------

    return {

        "success": True,

        "learning": {

            "overall": {

                "total_actions":
                    total_actions,

                "total_outcomes":
                    total_outcomes,

                "total_conversions":
                    total_conversions,

                "conversion_rate":
                    round(
                        conversion_rate,
                        2
                    ),

                "total_revenue":
                    float(total_revenue),

                "average_revenue_per_conversion":
                    round(
                        average_revenue,
                        2
                    )
            },

            "strategy_performance":
                strategies,

            "best_strategy":
                best_strategy
        }
    }