from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class BrowsingEvent(Base):
    __tablename__ = "browsing_events"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True
    )

    event_type = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )