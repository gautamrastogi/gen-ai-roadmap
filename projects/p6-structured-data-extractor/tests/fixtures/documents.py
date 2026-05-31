"""Sample documents used to test prompt coverage without real model calls."""

SAMPLE_DOCUMENTS: list[dict[str, str]] = [
    {
        "schema": "invoice",
        "text": "Invoice INV-1 from Acme Cloud. Total USD 120.00. One support item.",
    },
    {
        "schema": "invoice",
        "text": "Vendor Baltic Services billed EUR 77.50 for monitoring setup. Due next Friday.",
    },
    {
        "schema": "invoice",
        "text": "Receipt with missing invoice number: DataTools, subtotal 200, tax 42, total 242 EUR.",
    },
    {
        "schema": "support_ticket",
        "text": "INC-42: production checkout is down. Priority critical. Payment service affected.",
    },
    {
        "schema": "support_ticket",
        "text": "Request REQ-77 asks for a new Grafana dashboard for the compute team.",
    },
    {
        "schema": "support_ticket",
        "text": "Question from support: how do we change alert routing for weekend coverage?",
    },
    {
        "schema": "log_incident",
        "text": "prod api01 ERROR disk full. Alert severity high. Service inventory-api failing.",
    },
    {
        "schema": "log_incident",
        "text": "stage worker-2 warning kafka consumer lag increased to 50000 messages.",
    },
    {
        "schema": "log_incident",
        "text": "dev search-service info deployment completed successfully on pod search-7.",
    },
    {
        "schema": "log_incident",
        "text": "prod payment-api critical RedisTimeout on app01 and app02; checkout latency high.",
    },
]
