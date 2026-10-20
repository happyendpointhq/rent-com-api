"""Re-check saved listings for rent changes and delistings.

    python watchlist.py lc6705165 lc6820590      # add ids and check
    python watchlist.py                           # check the saved list again later

Uses /listings-by-ids: up to 50 listings per call, returned in the order asked, with ids that
came off the market reported in `not_found` instead of being silently dropped.
"""

import json
import sys
from datetime import date
from pathlib import Path

from client import get

STATE = Path("watchlist.json")


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for listing_id in sys.argv[1:]:
        state.setdefault(listing_id, {})
    if not state:
        raise SystemExit("Pass at least one listing id, for example lc6705165")

    ids = list(state)
    for start in range(0, len(ids), 50):
        data = get("/listings-by-ids", listing_ids=",".join(ids[start:start + 50]))
        for gone in data["not_found"]:
            print(f"OFF MARKET  {gone}  {state[gone].get('name', '')}")
            state[gone]["off_market_since"] = state[gone].get("off_market_since") or str(date.today())
        for row in data["listings"]:
            before = state[row["listing_id"]].get("price")
            if before is None:
                change = "new"
            elif row["price"] != before:
                change = f"{before} -> {row['price']} ({row['price'] - before:+})"
            else:
                change = "unchanged"
            drop = " price drop flagged" if row.get("has_price_drop") else ""
            print(f"{row['price_text']:>9}  {change:<22} {row['name']}{drop}")
            state[row["listing_id"]] = {
                "name": row["name"],
                "price": row["price"],
                "checked": str(date.today()),
            }

    STATE.write_text(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
