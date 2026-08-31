from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.services.opportunity_service import calculate_opportunities

from app.models.growth_action import GrowthAction
from app.models.action_outcome import ActionOutcome


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =========================================================
# GROWTHOS DASHBOARD
# =========================================================

@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Growth opportunities
    # -----------------------------------------------------

    opportunities = calculate_opportunities(db)

    total_opportunities = len(opportunities)

    high_priority = sum(
        1
        for opportunity in opportunities
        if opportunity["intent"] == "HIGH"
    )

    medium_priority = sum(
        1
        for opportunity in opportunities
        if opportunity["intent"] == "MEDIUM"
    )

    low_priority = sum(
        1
        for opportunity in opportunities
        if opportunity["intent"] == "LOW"
    )

    # -----------------------------------------------------
    # 2. Growth actions
    # -----------------------------------------------------

    total_actions = db.query(GrowthAction).count()

    ready_actions = (
        db.query(GrowthAction)
        .filter(GrowthAction.status == "READY")
        .count()
    )

    executing_actions = (
        db.query(GrowthAction)
        .filter(GrowthAction.status == "EXECUTING")
        .count()
    )

    completed_actions = (
        db.query(GrowthAction)
        .filter(GrowthAction.status == "COMPLETED")
        .count()
    )

    failed_actions = (
        db.query(GrowthAction)
        .filter(GrowthAction.status == "FAILED")
        .count()
    )

    # -----------------------------------------------------
    # 3. Action outcomes
    # -----------------------------------------------------

    total_outcomes = db.query(ActionOutcome).count()

    total_conversions = (
        db.query(ActionOutcome)
        .filter(ActionOutcome.converted == True)
        .count()
    )

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(ActionOutcome.revenue_generated),
                0
            )
        )
        .scalar()
    )

    # -----------------------------------------------------
    # 4. Conversion rate
    # -----------------------------------------------------

    conversion_rate = 0.0

    if total_outcomes > 0:
        conversion_rate = (
            total_conversions / total_outcomes
        ) * 100

    # -----------------------------------------------------
    # 5. Return dashboard
    # -----------------------------------------------------

    return {

        "success": True,

        "dashboard": {

            "opportunities": {
                "total": total_opportunities,
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            },

            "actions": {
                "total": total_actions,
                "ready": ready_actions,
                "executing": executing_actions,
                "completed": completed_actions,
                "failed": failed_actions
            },

            "performance": {
                "total_outcomes": total_outcomes,
                "total_conversions": total_conversions,
                "conversion_rate": round(
                    conversion_rate,
                    2
                ),
                "total_revenue": float(
                    total_revenue
                )
            }
        }
    }