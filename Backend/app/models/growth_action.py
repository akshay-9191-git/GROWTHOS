from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base


class GrowthAction(Base):
    __tablename__ = "growth_actions"

    id = Column(Integer, primary_key=True, index=True)

    action_id = Column(String(50), unique=True, nullable=False, index=True)

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)

    opportunity_type = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False)

    strategy = Column(Text, nullable=False)
    action = Column(Text, nullable=False)

    incentive = Column(String(200), nullable=False)

    message = Column(Text, nullable=False)

    expected_impact = Column(Text, nullable=False)

    status = Column(String(30), default="READY", nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )