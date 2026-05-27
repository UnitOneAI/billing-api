"""Stripe client wrapper."""
import os
import stripe as stripe_sdk


def charge_customer(customer_id: str, amount_cents: int, currency: str = "usd") -> dict:
    """Charge a customer via Stripe."""
    stripe_sdk.api_key = os.environ.get("STRIPE_API_KEY")
    intent = stripe_sdk.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        customer=customer_id,
        confirm=True,
    )
    return {"id": intent["id"], "status": intent["status"]}