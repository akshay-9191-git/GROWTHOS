from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime

from app.database import Base


class ActionOutcome(Base):
    __tablename__ = "action_outcomes"

    id = Column(Integer, primary_key=True, index=True)

    action_id = Column(String(50), nullable=False, index=True)

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)

    outcome = Column(String(100), nullable=False)

    converted = Column(Boolean, nullable=False, default=False)

    revenue_generated = Column(Float, nullable=False, default=0.0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )