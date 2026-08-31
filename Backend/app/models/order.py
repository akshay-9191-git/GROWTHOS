from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_amount = Column(Float, nullable=False)

    status = Column(
        String(50),
        default="completed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )