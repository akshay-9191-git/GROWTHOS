from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.services.opportunity_service import calculate_opportunities
from app.services.decision_service import make_growth_decision
from app.agents.growth_agent import analyze_opportunity
from app.models.growth_action import GrowthAction


router = APIRouter(
    prefix="/growth",
    tags=["Autonomous Growth"]
)


@router.post("/auto/{user_id}/{product_id}")
def autonomous_growth(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Find opportunity
    # -----------------------------------------------------

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
        raise HTTPException(
            status_code=404,
            detail="Growth opportunity not found"
        )

    # -----------------------------------------------------
    # 2. Get learned decision
    # -----------------------------------------------------

    decision = make_growth_decision(
        db,
        user_id,
        product_id
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Growth decision could not be generated"
        )

    # -----------------------------------------------------
    # 3. Generate growth strategy
    # -----------------------------------------------------

    analysis = analyze_opportunity(
        opportunity,
        decision
    )

    # -----------------------------------------------------
    # 4. Check for existing active action
    # -----------------------------------------------------

    existing_action = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.user_id == user_id,
            GrowthAction.product_id == product_id,
            GrowthAction.status.in_([
                "READY",
                "EXECUTING"
            ])
        )
        .order_by(
            GrowthAction.created_at.desc()
        )
        .first()
    )

    if existing_action:

        return {
            "success": True,

            "message": "An active growth action already exists.",

            "pipeline": {
                "opportunity_detected": True,
                "decision_generated": True,
                "strategy_generated": True,
                "action_created": False,
                "existing_action": True
            },

            "action": {
                "action_id": existing_action.action_id,

                "status": existing_action.status,

                "user_id": existing_action.user_id,

                "product_id": existing_action.product_id,

                "priority": existing_action.priority,

                "opportunity_type": existing_action.opportunity_type,

                "strategy": existing_action.strategy,

                "action": existing_action.action,

                "incentive": existing_action.incentive,

                "message": existing_action.message,

                "expected_impact": existing_action.expected_impact
            }
        }

    # -----------------------------------------------------
    # 5. Generate action ID
    # -----------------------------------------------------

    action_id = "ACT-" + uuid.uuid4().hex[:8].upper()

    # -----------------------------------------------------
    # 6. Create GrowthAction
    # -----------------------------------------------------

    growth_action = GrowthAction(

        action_id=action_id,

        user_id=user_id,

        product_id=product_id,

        opportunity_type=analysis["opportunity_type"],

        priority=analysis["priority"],

        strategy=analysis["strategy"],

        action=analysis["recommended_action"],

        incentive=analysis["incentive"],

        message=analysis["customer_message"],

        expected_impact=analysis["expected_impact"],

        status="READY",

        created_at=datetime.utcnow()
    )

    # -----------------------------------------------------
    # 7. Save action
    # -----------------------------------------------------

    db.add(growth_action)

    db.commit()

    db.refresh(growth_action)

    # -----------------------------------------------------
    # 8. Return autonomous result
    # -----------------------------------------------------

    return {

        "success": True,

        "pipeline": {

            "opportunity_detected": True,

            "decision_generated": True,

            "strategy_generated": True,

            "action_created": True,

            "existing_action": False,

            "execution": "READY"
        },

        "decision": {

            "recommended_strategy": decision[
                "recommended_strategy"
            ],

            "confidence": decision[
                "confidence"
            ],

            "historical_conversion_rate": decision[
                "historical_conversion_rate"
            ],

            "reason": decision[
                "reason"
            ]
        },

        "action": {

            "action_id": growth_action.action_id,

            "status": growth_action.status,

            "user_id": growth_action.user_id,

            "product_id": growth_action.product_id,

            "priority": growth_action.priority,

            "opportunity_type": growth_action.opportunity_type,

            "strategy": growth_action.strategy,

            "action": growth_action.action,

            "incentive": growth_action.incentive,

            "message": growth_action.message,

            "expected_impact": growth_action.expected_impact
        }
    }