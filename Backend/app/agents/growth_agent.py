
import json


SYSTEM_PROMPT = """
You are GrowthOS Growth Agent.

You are a local rule-based e-commerce growth strategist.

Your job is to analyze a customer growth opportunity and recommend
the best action to increase conversion or revenue.

You must:

1. Analyze customer behavior.
2. Identify the growth opportunity.
3. Determine the customer's purchase intent.
4. Use the learned strategy when historical performance is available.
5. Recommend ONE primary growth action.
6. Suggest an appropriate incentive only when justified.
7. Generate a concise personalized customer message.
8. Explain why the action was selected.

Do not invent customer behavior that is not present in the input.

Return a structured growth recommendation.
"""


def analyze_opportunity(
    opportunity: dict,
    decision: dict = None
):

    user_name = opportunity["user_name"]
    product_name = opportunity["product_name"]
    price = opportunity["product_price"]
    score = opportunity["intent_score"]
    intent = opportunity["intent"]
    reasons = opportunity["reasons"]

    # ---------------------------------------------------------
    # LEARNED DECISION
    # ---------------------------------------------------------

    learned_strategy = None
    confidence = 0
    historical_conversion_rate = 0

    if decision:

        learned_strategy = decision.get(
            "recommended_strategy"
        )

        confidence = decision.get(
            "confidence",
            0
        )

        historical_conversion_rate = decision.get(
            "historical_conversion_rate",
            0
        )

    # ---------------------------------------------------------
    # HIGH INTENT
    # ---------------------------------------------------------

    if intent == "HIGH" or score >= 70:

        opportunity_type = "Cart Recovery"
        priority = "HIGH"

        # Use learned strategy when available
        if learned_strategy:
            strategy = learned_strategy
        else:
            strategy = "Recover high-intent abandoned cart"

        recommended_action = (
            f"Send a personalized cart recovery message for {product_name}"
        )

        incentive = "10% limited-time discount"

        reasoning = (
            f"{user_name} has high purchase intent for {product_name}. "
            f"The opportunity has an intent score of {score}. "
            f"Evidence: {', '.join(reasons)}. "
        )

        if learned_strategy:

            reasoning += (
                f"Historical learning selected '{learned_strategy}' "
                f"with a historical conversion rate of "
                f"{historical_conversion_rate}%. "
                f"Decision confidence is {confidence}%."
            )

        else:

            reasoning += (
                "No learned strategy was available, so the action "
                "is based primarily on current customer intent."
            )

        customer_message = (
            f"Hi {user_name}! You left {product_name} in your cart. "
            f"Complete your purchase today and get 10% off for a limited time."
        )

        expected_impact = (
            "High probability of recovering an abandoned purchase "
            "and increasing conversion."
        )

    # ---------------------------------------------------------
    # MEDIUM INTENT
    # ---------------------------------------------------------

    elif intent == "MEDIUM" or score >= 30:

        opportunity_type = "Conversion Nurture"
        priority = "MEDIUM"

        if learned_strategy:
            strategy = learned_strategy
        else:
            strategy = "Nurture interested customer"

        recommended_action = (
            f"Send a personalized follow-up recommendation for {product_name}"
        )

        incentive = "5% discount"

        reasoning = (
            f"{user_name} has moderate purchase intent for {product_name}. "
            f"The opportunity has an intent score of {score}. "
            f"Evidence: {', '.join(reasons)}. "
        )

        if learned_strategy:

            reasoning += (
                f"Historical learning selected '{learned_strategy}' "
                f"with a historical conversion rate of "
                f"{historical_conversion_rate}%. "
                f"Decision confidence is {confidence}%."
            )

        else:

            reasoning += (
                "No learned strategy was available, so the strategy "
                "is based primarily on current customer intent."
            )

        customer_message = (
            f"Hi {user_name}! Still thinking about {product_name}? "
            "Here's a special 5% offer to help you decide."
        )

        expected_impact = (
            "Increase the likelihood of conversion by re-engaging "
            "an interested customer."
        )

    # ---------------------------------------------------------
    # LOW INTENT
    # ---------------------------------------------------------

    else:

        opportunity_type = "Product Recommendation"
        priority = "LOW"

        if learned_strategy:
            strategy = learned_strategy
        else:
            strategy = "Build product interest"

        recommended_action = (
            f"Send a personalized product recommendation for {product_name}"
        )

        incentive = "No discount"

        reasoning = (
            f"{user_name} has low purchase intent for {product_name}. "
            f"The opportunity has an intent score of {score}. "
            f"Evidence: {', '.join(reasons)}. "
        )

        if learned_strategy:

            reasoning += (
                f"Historical learning selected '{learned_strategy}' "
                f"with a historical conversion rate of "
                f"{historical_conversion_rate}%. "
                f"Decision confidence is {confidence}%."
            )

        else:

            reasoning += (
                "No learned strategy was available, so the strategy "
                "is based primarily on current customer intent."
            )

        customer_message = (
            f"Hi {user_name}! We noticed you checked out {product_name}. "
            "It might be a great fit for you. "
            "Take another look when you have a moment."
        )

        expected_impact = (
            "Increase engagement and gradually move the customer "
            "toward purchase intent."
        )

    # ---------------------------------------------------------
    # RETURN GROWTH RECOMMENDATION
    # ---------------------------------------------------------

    return {

        "opportunity_type": opportunity_type,

        "priority": priority,

        "strategy": strategy,

        "recommended_action": recommended_action,

        "incentive": incentive,

        "reasoning": reasoning,

        "customer_message": customer_message,

        "expected_impact": expected_impact
    }

