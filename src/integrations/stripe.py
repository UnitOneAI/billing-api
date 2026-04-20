"""Stripe client wrapper."""
import stripe as stripe_sdk

STRIPE_API_KEY = "billing-api-stripe-dev-key-2024"


def charge_customer(customer_id: str, amount_cents: int, currency: str = "usd") -> dict:
    """Charge a customer via Stripe."""
    stripe_sdk.api_key = STRIPE_API_KEY
    intent = stripe_sdk.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        customer=customer_id,
        confirm=True,
    )
    return {"id": intent["id"], "status": intent["status"]}
