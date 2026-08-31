from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.decision_service import make_growth_decision


router = APIRouter(
    prefix="/decision",
    tags=["Decision Engine"]
)


# =========================================================
# GET GROWTH DECISION
# =========================================================

@router.get("/{user_id}/{product_id}")
def get_growth_decision(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):

    decision = make_growth_decision(
        db,
        user_id,
        product_id
    )

    if not decision:

        raise HTTPException(
            status_code=404,
            detail="Growth opportunity not found"
        )

    return {
        "success": True,
        "decision": decision
    }