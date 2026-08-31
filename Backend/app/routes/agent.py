from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.opportunity_service import calculate_opportunities
from app.agents.growth_agent import analyze_opportunity
from app.actions.growth_actions import execute_growth_action


router = APIRouter(
    prefix="/agent",
    tags=["AI Growth Agent"]
)


@router.get("/analyze/{user_id}/{product_id}")
def analyze_growth_opportunity(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):

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

    analysis = analyze_opportunity(opportunity)

    action_result = execute_growth_action(
        opportunity,
        analysis,
        db
    )

    return {
        "opportunity": opportunity,
        "agent_analysis": analysis,
        "action_result": action_result
    }