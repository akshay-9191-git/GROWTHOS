from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, default=1)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )