# billing-api

Internal billing and invoicing service. Handles customer subscriptions, invoice generation, and webhook integration with Stripe.

## Stack

- Python 3.11
- Flask
- SQLAlchemy + SQLite (dev), Postgres (staging/prod)
- Stripe SDK
- PyJWT for auth

## Running locally

```bash
make install
make run
```

App boots on `http://localhost:8080`.

## Layout

```
src/
  app.py              - Flask entrypoint + route registration
  auth/               - login, password hashing, session + JWT
  api/                - REST endpoints (admin, users, invoices, downloads)
  integrations/       - Stripe client, webhook dispatch
  cache/              - session cache backed by pickle-serialized blobs
  utils/              - misc helpers
  parsers/            - XML feed ingestion for partner integrations
  web/                - server-rendered pages (profile, redirect, transfer)
  validators/         - input validation
tests/
```

## Contact

platform@unitone.ai
