from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database import Base


class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action_id = Column(
        String,
        nullable=False,
        index=True
    )

    action_type = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    product_id = Column(
        Integer,
        nullable=False
    )

    customer = Column(
        String,
        nullable=True
    )

    product = Column(
        String,
        nullable=True
    )

    priority = Column(
        String,
        nullable=True
    )

    opportunity_type = Column(
        String,
        nullable=True
    )

    strategy = Column(
        Text,
        nullable=True
    )

    action = Column(
        Text,
        nullable=True
    )

    incentive = Column(
        String,
        nullable=True
    )

    message = Column(
        Text,
        nullable=True
    )

    expected_impact = Column(
        Text,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="COMPLETED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )