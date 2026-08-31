from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import Product
from app.models.event import BrowsingEvent
from app.models.cart import CartItem


def calculate_opportunities(db: Session):

    opportunities = []

    users = db.query(User).all()

    for user in users:

        # Get user's recent events
        recent_events = (
            db.query(BrowsingEvent)
            .filter(BrowsingEvent.user_id == user.id)
            .all()
        )

        # Group views by product
        product_views = {}

        for event in recent_events:

            if event.event_type != "view":
                continue

            product_views[event.product_id] = (
                product_views.get(event.product_id, 0) + 1
            )

        # Check every product the user viewed
        for product_id, view_count in product_views.items():

            product = (
                db.query(Product)
                .filter(Product.id == product_id)
                .first()
            )

            if not product:
                continue

            score = 0
            reasons = []

            # -----------------------------
            # VIEW SCORE
            # -----------------------------

            if view_count >= 5:

                score += 50

                reasons.append(
                    f"{view_count} product views"
                )

            elif view_count >= 3:

                score += 30

                reasons.append(
                    f"{view_count} product views"
                )

            elif view_count >= 1:

                score += 10

                reasons.append(
                    f"{view_count} product view"
                )

            # -----------------------------
            # CART SIGNAL
            # -----------------------------

            cart_item = (
                db.query(CartItem)
                .filter(
                    CartItem.user_id == user.id,
                    CartItem.product_id == product_id
                )
                .first()
            )

            if cart_item:

                score += 30

                reasons.append(
                    "Product currently in cart"
                )

            # -----------------------------
            # RECENCY SIGNAL
            # -----------------------------

            latest_event = (
                db.query(BrowsingEvent)
                .filter(
                    BrowsingEvent.user_id == user.id,
                    BrowsingEvent.product_id == product_id
                )
                .order_by(
                    BrowsingEvent.created_at.desc()
                )
                .first()
            )

            if latest_event:

                age = datetime.utcnow() - latest_event.created_at

                if age <= timedelta(days=1):

                    score += 20

                    reasons.append(
                        "Activity within last 24 hours"
                    )

            # -----------------------------
            # INTENT LEVEL
            # -----------------------------

            if score >= 70:

                intent = "HIGH"

            elif score >= 40:

                intent = "MEDIUM"

            else:

                intent = "LOW"

            # -----------------------------
            # OPPORTUNITY
            # -----------------------------

            opportunities.append(
                {
                    "user_id": user.id,
                    "user_name": user.name,
                    "product_id": product.id,
                    "product_name": product.name,
                    "product_price": product.price,
                    "intent_score": score,
                    "intent": intent,
                    "reasons": reasons,
                    "recommended_action": (
                        "Send personalized cart recovery offer"
                        if cart_item
                        else
                        "Send personalized product recommendation"
                    ),
                }
            )

    # Highest opportunities first

    opportunities.sort(
        key=lambda x: x["intent_score"],
        reverse=True
    )

    return opportunities