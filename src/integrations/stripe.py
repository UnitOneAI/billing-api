"""Stripe client wrapper."""
import os
import stripe as stripe_sdk

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")


def charge_customer(customer_id: str, amount_cents: int, currency: str = "usd") -> dict:
    """Charge a customer via Stripe."""
    if not STRIPE_API_KEY:
        raise ValueError("STRIPE_API_KEY environment variable is not set")
    stripe_sdk.api_key = STRIPE_API_KEY
    intent = stripe_sdk.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        customer=customer_id,
        confirm=True,
    )
    return {"id": intent["id"], "status": intent["status"]}
