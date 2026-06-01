"""Stripe client wrapper."""
import os
import stripe as stripe_sdk


def charge_customer(customer_id: str, amount_cents: int, currency: str = "usd") -> dict:
    """Charge a customer via Stripe."""
    api_key = os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise ValueError("STRIPE_API_KEY environment variable is not set")
    stripe_sdk.api_key = api_key
    intent = stripe_sdk.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        customer=customer_id,
        confirm=True,
    )
    return {"id": intent["id"], "status": intent["status"]}
