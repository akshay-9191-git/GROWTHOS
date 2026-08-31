from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.opportunity_service import calculate_opportunities


router = APIRouter(
    prefix="/opportunities",
    tags=["Growth Opportunities"]
)


@router.get("/")
def get_opportunities(
    db: Session = Depends(get_db)
):
    opportunities = calculate_opportunities(db)

    high = [
        x for x in opportunities
        if x["intent"] == "HIGH"
    ]

    medium = [
        x for x in opportunities
        if x["intent"] == "MEDIUM"
    ]

    low = [
        x for x in opportunities
        if x["intent"] == "LOW"
    ]

    return {
        "summary": {
            "total": len(opportunities),
            "high": len(high),
            "medium": len(medium),
            "low": len(low)
        },

        "top_opportunities": opportunities[:20],

        "high_priority": high,

        "medium_priority": medium
    }