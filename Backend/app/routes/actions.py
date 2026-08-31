
from datetime import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents.growth_agent import analyze_opportunity
from app.models.action_log import ActionLog
from app.models.action_outcome import ActionOutcome
from app.models.growth_action import GrowthAction
from app.services.decision_service import make_growth_decision
from app.services.learning_service import get_strategy_performance
from app.services.opportunity_service import calculate_opportunities


router = APIRouter(
    prefix="/actions",
    tags=["Growth Actions"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class ActionOutcomeRequest(BaseModel):
    outcome: str = ""
    converted: bool
    revenue_generated: float = 0.0


# =========================================================
# CREATE GROWTH ACTION
# =========================================================

@router.post("/execute/{user_id}/{product_id}")
def execute_growth_action(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # 1. Find growth opportunity
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
    # 2. Get learned growth decision
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
    # 3. Analyze opportunity
    # -----------------------------------------------------

    analysis = analyze_opportunity(
        opportunity,
        decision
    )

    # -----------------------------------------------------
    # 4. Generate action ID
    # -----------------------------------------------------

    action_id = "ACT-" + uuid.uuid4().hex[:8].upper()

    # -----------------------------------------------------
    # 5. Create GrowthAction
    # -----------------------------------------------------

    growth_action = GrowthAction(
        action_id=action_id,

        user_id=opportunity["user_id"],
        product_id=opportunity["product_id"],

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
    # 6. Save
    # -----------------------------------------------------

    db.add(growth_action)
    db.commit()
    db.refresh(growth_action)

    # -----------------------------------------------------
    # 7. Return
    # -----------------------------------------------------

    return {
        "success": True,
        "action": {
            "log_id": growth_action.id,
            "action_id": growth_action.action_id,
            "created_at": (
                growth_action.created_at.isoformat()
                if growth_action.created_at
                else None
            ),
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


# =========================================================
# RUN EXISTING GROWTH ACTION
# =========================================================

@router.post("/run/{action_id}")
def run_growth_action(
    action_id: str,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # 1. Find action
    # -----------------------------------------------------

    action = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.action_id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Action not found"
        )

    # -----------------------------------------------------
    # 2. Check status
    # -----------------------------------------------------

    if action.status != "READY":
        raise HTTPException(
            status_code=400,
            detail=(
                "Action cannot be executed. "
                f"Current status: {action.status}"
            )
        )

    # -----------------------------------------------------
    # 3. Mark executing
    # -----------------------------------------------------

    action.status = "EXECUTING"

    db.commit()
    db.refresh(action)

    # -----------------------------------------------------
    # 4. Execute action
    # -----------------------------------------------------

    try:

        opportunity_type = (
            action.opportunity_type or ""
        ).lower()

        if "cart" in opportunity_type:
            action_type = "cart_recovery"

        elif "upsell" in opportunity_type:
            action_type = "upsell"

        elif "cross" in opportunity_type:
            action_type = "cross_sell"

        else:
            action_type = "growth_action"

        # -------------------------------------------------
        # Create execution log
        # -------------------------------------------------

        execution_log = ActionLog(
            action_id=action.action_id,

            action_type=action_type,

            user_id=action.user_id,

            product_id=action.product_id,

            customer=f"Customer {action.user_id}",

            product=f"Product {action.product_id}",

            priority=action.priority,

            opportunity_type=action.opportunity_type,

            strategy=action.strategy,

            action=action.action,

            incentive=action.incentive,

            message=action.message,

            expected_impact=action.expected_impact,

            status="COMPLETED",

            created_at=datetime.utcnow()
        )

        db.add(execution_log)

        # -------------------------------------------------
        # Mark completed
        # -------------------------------------------------

        action.status = "COMPLETED"

        db.commit()

        db.refresh(action)
        db.refresh(execution_log)

        return {
            "success": True,

            "action_id": action.action_id,

            "status": action.status,

            "execution": {
                "action_type": action_type,

                "user_id": action.user_id,

                "customer": f"Customer {action.user_id}",

                "product_id": action.product_id,

                "message": action.message,

                "incentive": action.incentive,

                "execution_note": (
                    "Action simulated successfully. "
                    "No real email, SMS, notification, "
                    "or payment was triggered."
                )
            },

            "log_id": execution_log.id
        }

    except Exception as e:

        db.rollback()

        action.status = "FAILED"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Action execution failed: {str(e)}"
        )


# =========================================================
# GET ALL GROWTH ACTIONS
# =========================================================

@router.get("/")
def get_all_actions(
    db: Session = Depends(get_db)
):
    actions = (
        db.query(GrowthAction)
        .order_by(
            GrowthAction.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,

        "count": len(actions),

        "actions": [
            {
                "log_id": action.id,

                "action_id": action.action_id,

                "created_at": (
                    action.created_at.isoformat()
                    if action.created_at
                    else None
                ),

                "status": action.status,

                "user_id": action.user_id,

                "product_id": action.product_id,

                "priority": action.priority,

                "opportunity_type": action.opportunity_type,

                "strategy": action.strategy,

                "action": action.action,

                "incentive": action.incentive,

                "message": action.message,

                "expected_impact": action.expected_impact
            }
            for action in actions
        ]
    }


# =========================================================
# ACTION DASHBOARD
# =========================================================

@router.get("/dashboard")
def get_action_dashboard(
    db: Session = Depends(get_db)
):
    actions = db.query(GrowthAction).all()

    total_actions = len(actions)

    ready = sum(
        1
        for action in actions
        if action.status == "READY"
    )

    executing = sum(
        1
        for action in actions
        if action.status == "EXECUTING"
    )

    completed = sum(
        1
        for action in actions
        if action.status == "COMPLETED"
    )

    failed = sum(
        1
        for action in actions
        if action.status == "FAILED"
    )

    high = sum(
        1
        for action in actions
        if action.priority == "HIGH"
    )

    medium = sum(
        1
        for action in actions
        if action.priority == "MEDIUM"
    )

    low = sum(
        1
        for action in actions
        if action.priority == "LOW"
    )

    opportunity_types = {}

    for action in actions:

        opportunity_type = (
            action.opportunity_type
            or "UNKNOWN"
        )

        opportunity_types[opportunity_type] = (
            opportunity_types.get(
                opportunity_type,
                0
            ) + 1
        )

    return {
        "success": True,

        "summary": {
            "total_actions": total_actions,
            "ready": ready,
            "executing": executing,
            "completed": completed,
            "failed": failed
        },

        "priority": {
            "high": high,
            "medium": medium,
            "low": low
        },

        "opportunity_types": opportunity_types
    }


# =========================================================
# GET ACTIONS FOR USER
# =========================================================

@router.get("/user/{user_id}")
def get_user_actions(
    user_id: int,
    db: Session = Depends(get_db)
):
    actions = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.user_id == user_id
        )
        .order_by(
            GrowthAction.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,

        "user_id": user_id,

        "count": len(actions),

        "actions": [
            {
                "log_id": action.id,

                "action_id": action.action_id,

                "created_at": (
                    action.created_at.isoformat()
                    if action.created_at
                    else None
                ),

                "status": action.status,

                "product_id": action.product_id,

                "priority": action.priority,

                "opportunity_type": action.opportunity_type,

                "strategy": action.strategy,

                "action": action.action,

                "incentive": action.incentive,

                "message": action.message,

                "expected_impact": action.expected_impact
            }
            for action in actions
        ]
    }


# =========================================================
# ACTION STATISTICS
# =========================================================

@router.get("/stats")
def get_action_stats(
    db: Session = Depends(get_db)
):
    total_actions = (
        db.query(GrowthAction).count()
    )

    ready = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "READY"
        )
        .count()
    )

    executing = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "EXECUTING"
        )
        .count()
    )

    completed = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "COMPLETED"
        )
        .count()
    )

    failed = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "FAILED"
        )
        .count()
    )

    success_rate = (
        round(
            (completed / total_actions) * 100,
            2
        )
        if total_actions > 0
        else 0
    )

    return {
        "success": True,

        "stats": {
            "total_actions": total_actions,
            "ready": ready,
            "executing": executing,
            "completed": completed,
            "failed": failed,
            "success_rate": success_rate
        }
    }


# =========================================================
# RECORD ACTION OUTCOME
# =========================================================

@router.post("/outcome/{action_id}")
def record_action_outcome(
    action_id: str,
    request: ActionOutcomeRequest,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # 1. Find action
    # -----------------------------------------------------

    action = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.action_id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Action not found"
        )

    # -----------------------------------------------------
    # 2. Prevent duplicate outcome
    # -----------------------------------------------------

    existing_outcome = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.action_id == action_id
        )
        .first()
    )

    if existing_outcome:
        raise HTTPException(
            status_code=400,
            detail=(
                "Outcome already recorded "
                "for this action"
            )
        )

    # -----------------------------------------------------
    # 3. Determine outcome
    # -----------------------------------------------------

    if request.converted:
        outcome_status = "CONVERTED"
    else:
        outcome_status = "NO_CONVERSION"

    # -----------------------------------------------------
    # 4. Create outcome
    # -----------------------------------------------------

    action_outcome = ActionOutcome(
        action_id=action.action_id,

        user_id=action.user_id,

        product_id=action.product_id,

        outcome=(
            request.outcome
            if request.outcome
            else outcome_status
        ),

        converted=request.converted,

        revenue_generated=(
            request.revenue_generated
        ),

        created_at=datetime.utcnow()
    )

    # -----------------------------------------------------
    # 5. Save
    # -----------------------------------------------------

    db.add(action_outcome)

    db.commit()

    db.refresh(action_outcome)

    return {
        "success": True,

        "outcome": {
            "id": action_outcome.id,

            "action_id": action_outcome.action_id,

            "user_id": action_outcome.user_id,

            "product_id": action_outcome.product_id,

            "outcome": action_outcome.outcome,

            "converted": action_outcome.converted,

            "revenue_generated": (
                action_outcome.revenue_generated
            ),

            "created_at": (
                action_outcome.created_at.isoformat()
                if action_outcome.created_at
                else None
            )
        }
    }


# =========================================================
# OUTCOME STATISTICS
# =========================================================

@router.get("/outcomes/stats")
def get_outcome_stats(
    db: Session = Depends(get_db)
):
    total_outcomes = (
        db.query(ActionOutcome).count()
    )

    conversions = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.converted == True
        )
        .count()
    )

    no_conversions = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.converted == False
        )
        .count()
    )

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
    )

    conversion_rate = (
        (
            conversions /
            total_outcomes
        ) * 100
        if total_outcomes > 0
        else 0
    )

    average_revenue = (
        total_revenue / conversions
        if conversions > 0
        else 0
    )

    return {
        "success": True,

        "stats": {
            "total_outcomes": total_outcomes,

            "conversions": conversions,

            "no_conversions": no_conversions,

            "conversion_rate": round(
                conversion_rate,
                2
            ),

            "total_revenue": float(
                total_revenue
            ),

            "average_revenue_per_conversion": round(
                average_revenue,
                2
            )
        }
    }


# =========================================================
# OUTCOME PERFORMANCE BY TYPE
# =========================================================

@router.get("/outcomes/by-type")
def get_outcomes_by_type(
    db: Session = Depends(get_db)
):
    actions = (
        db.query(GrowthAction)
        .all()
    )

    results = {}

    for action in actions:

        action_type = (
            action.opportunity_type
            or "UNKNOWN"
        )

        if action_type not in results:
            results[action_type] = {
                "action_type": action_type,
                "actions": 0,
                "conversions": 0,
                "revenue": 0.0
            }

        results[action_type]["actions"] += 1

        outcomes = (
            db.query(ActionOutcome)
            .filter(
                ActionOutcome.action_id
                == action.action_id
            )
            .all()
        )

        for outcome in outcomes:

            if outcome.converted:
                results[action_type][
                    "conversions"
                ] += 1

            results[action_type][
                "revenue"
            ] += (
                outcome.revenue_generated or 0
            )

    performance = []

    for item in results.values():

        total_actions = item["actions"]

        conversion_rate = (
            (
                item["conversions"]
                / total_actions
            ) * 100
            if total_actions > 0
            else 0
        )

        performance.append({
            "action_type": item["action_type"],

            "actions": total_actions,

            "conversions": item[
                "conversions"
            ],

            "conversion_rate": round(
                conversion_rate,
                2
            ),

            "revenue": round(
                item["revenue"],
                2
            )
        })

    return {
        "success": True,
        "performance": performance
    }


# =========================================================
# USER OUTCOME PERFORMANCE
# =========================================================

@router.get("/outcomes/user/{user_id}")
def get_user_outcome_performance(
    user_id: int,
    db: Session = Depends(get_db)
):
    outcomes = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.user_id == user_id
        )
        .all()
    )

    total_outcomes = len(outcomes)

    conversions = sum(
        1
        for outcome in outcomes
        if outcome.converted
    )

    revenue = sum(
        outcome.revenue_generated or 0
        for outcome in outcomes
    )

    conversion_rate = (
        (
            conversions /
            total_outcomes
        ) * 100
        if total_outcomes > 0
        else 0
    )

    return {
        "success": True,

        "user_id": user_id,

        "performance": {
            "total_outcomes": total_outcomes,

            "conversions": conversions,

            "conversion_rate": round(
                conversion_rate,
                2
            ),

            "revenue_generated": round(
                revenue,
                2
            )
        }
    }


# =========================================================
# GET OUTCOMES FOR ACTION
# =========================================================

@router.get("/outcomes/{action_id}")
def get_action_outcomes(
    action_id: str,
    db: Session = Depends(get_db)
):
    outcomes = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.action_id == action_id
        )
        .order_by(
            ActionOutcome.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,

        "action_id": action_id,

        "count": len(outcomes),

        "outcomes": [
            {
                "id": outcome.id,

                "action_id": outcome.action_id,

                "user_id": outcome.user_id,

                "product_id": outcome.product_id,

                "outcome": outcome.outcome,

                "converted": outcome.converted,

                "revenue_generated": (
                    outcome.revenue_generated
                ),

                "created_at": (
                    outcome.created_at.isoformat()
                    if outcome.created_at
                    else None
                )
            }
            for outcome in outcomes
        ]
    }


# =========================================================
# GROWTH ACTION ANALYTICS
# =========================================================

@router.get("/analytics")
def get_action_analytics(
    db: Session = Depends(get_db)
):
    total_actions = (
        db.query(GrowthAction).count()
    )

    completed_actions = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "COMPLETED"
        )
        .count()
    )

    failed_actions = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.status == "FAILED"
        )
        .count()
    )

    total_outcomes = (
        db.query(ActionOutcome).count()
    )

    conversions = (
        db.query(ActionOutcome)
        .filter(
            ActionOutcome.converted == True
        )
        .count()
    )

    revenue = (
        db.query(
            func.coalesce(
                func.sum(
                    ActionOutcome.revenue_generated
                ),
                0
            )
        )
        .scalar()
    )

    conversion_rate = (
        (
            conversions /
            total_outcomes
        ) * 100
        if total_outcomes > 0
        else 0
    )

    completion_rate = (
        (
            completed_actions /
            total_actions
        ) * 100
        if total_actions > 0
        else 0
    )

    return {
        "success": True,

        "analytics": {
            "actions": {
                "total": total_actions,

                "completed": completed_actions,

                "failed": failed_actions,

                "completion_rate": round(
                    completion_rate,
                    2
                )
            },

            "outcomes": {
                "total": total_outcomes,

                "conversions": conversions,

                "conversion_rate": round(
                    conversion_rate,
                    2
                )
            },

            "revenue": {
                "total": float(revenue)
            }
        }
    }


# =========================================================
# STRATEGY ANALYTICS
# =========================================================

@router.get("/analytics/strategies")
def get_strategy_analytics(
    db: Session = Depends(get_db)
):
    performance = (
        get_strategy_performance(db)
    )

    return {
        "success": True,
        "strategies": performance
    }


# =========================================================
# ACTION EXECUTION HISTORY
# =========================================================

@router.get("/history")
def get_action_history(
    db: Session = Depends(get_db)
):
    actions = (
        db.query(GrowthAction)
        .order_by(
            GrowthAction.created_at.desc()
        )
        .all()
    )

    history = []

    for action in actions:

        outcomes = (
            db.query(ActionOutcome)
            .filter(
                ActionOutcome.action_id
                == action.action_id
            )
            .order_by(
                ActionOutcome.created_at.desc()
            )
            .all()
        )

        history.append({
            "action_id": action.action_id,

            "user_id": action.user_id,

            "product_id": action.product_id,

            "opportunity_type": (
                action.opportunity_type
            ),

            "priority": action.priority,

            "status": action.status,

            "strategy": action.strategy,

            "action": action.action,

            "message": action.message,

            "created_at": (
                action.created_at.isoformat()
                if action.created_at
                else None
            ),

            "outcomes": [
                {
                    "id": outcome.id,

                    "outcome": outcome.outcome,

                    "converted": outcome.converted,

                    "revenue_generated": float(
                        outcome.revenue_generated or 0
                    ),

                    "created_at": (
                        outcome.created_at.isoformat()
                        if outcome.created_at
                        else None
                    )
                }
                for outcome in outcomes
            ]
        })

    return {
        "success": True,

        "count": len(history),

        "history": history
    }


# =========================================================
# GET SINGLE ACTION
# =========================================================

@router.get("/{action_id}")
def get_action(
    action_id: str,
    db: Session = Depends(get_db)
):
    action = (
        db.query(GrowthAction)
        .filter(
            GrowthAction.action_id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Action not found"
        )

    return {
        "success": True,

        "action": {
            "log_id": action.id,

            "action_id": action.action_id,

            "created_at": (
                action.created_at.isoformat()
                if action.created_at
                else None
            ),

            "status": action.status,

            "user_id": action.user_id,

            "product_id": action.product_id,

            "priority": action.priority,

            "opportunity_type": (
                action.opportunity_type
            ),

            "strategy": action.strategy,

            "action": action.action,

            "incentive": action.incentive,

            "message": action.message,

            "expected_impact": (
                action.expected_impact
            )
        }
    }

