from app.models.action_log import ActionLog


def execute_growth_action(
    opportunity: dict,
    analysis: dict,
    db
):

    action = analysis.get("recommended_action", "")
    incentive = analysis.get("incentive", "")
    message = analysis.get("customer_message", "")

    # Determine action type
    if "cart" in action.lower():
        action_type = "cart_recovery"

    elif "recommendation" in action.lower():
        action_type = "personalized_recommendation"

    else:
        action_type = "general_growth_action"

    # Create action log
    action_log = ActionLog(
        user_id=opportunity["user_id"],
        product_id=opportunity["product_id"],
        action_type=action_type,
        message=message,
        incentive=incentive,
        status="simulated"
    )

    db.add(action_log)
    db.commit()
    db.refresh(action_log)

    return {
        "id": action_log.id,

        "status": action_log.status,
        "action_type": action_log.action_type,

        "user_id": opportunity["user_id"],
        "customer": opportunity["user_name"],

        "product_id": opportunity["product_id"],
        "product": opportunity["product_name"],

        "message": message,
        "incentive": incentive,

        "execution_note": (
            "Action simulated successfully. "
            "No real email, SMS, notification, "
            "or payment was triggered."
        )
    }