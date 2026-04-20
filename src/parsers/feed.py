"""XML feed ingestion for partner reconciliation files."""
from lxml import etree


def parse_reconciliation_feed(xml_bytes: bytes) -> list[dict]:
    """Parse a partner's XML reconciliation export."""
    tree = etree.fromstring(xml_bytes)
    records = []
    for item in tree.findall(".//transaction"):
        records.append({
            "id": item.get("id"),
            "amount": item.findtext("amount"),
            "currency": item.findtext("currency"),
        })
    return records
