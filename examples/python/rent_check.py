"""Compare a listing's asking rent with the market rent around it.

    python rent_check.py lc6705165 --beds 1

Takes the listing's price for that bedroom count (from price_by_beds), then asks
/rent-estimate for the same point. The estimate is built from houses, condos, townhomes
and duplexes (apartment listings are not comparables), so for an apartment community it
tells you how it sits against the private rentals nearby.

/rent-estimate is not included in every RapidAPI plan. On a plan without it, the call
returns "This endpoint is disabled for your subscription".
"""

import argparse

from client import get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("listing_id")
    parser.add_argument("--beds", type=int, required=True)
    parser.add_argument("--radius-miles", type=int)
    args = parser.parse_args()

    listing = get("/listing-details", listing_id=args.listing_id)
    by_beds = {row["beds"]: row for row in listing.get("price_by_beds") or []}
    if args.beds not in by_beds:
        raise SystemExit(f"{listing['name']} lists no {args.beds}-bed price. Has: {sorted(by_beds)}")
    asking = by_beds[args.beds]["min"]

    market = get(
        "/rent-estimate",
        latitude=listing["latitude"],
        longitude=listing["longitude"],
        beds=args.beds,
        radius_miles=args.radius_miles,
        include_comparables="false",
    )
    median = market["median"]
    print(f"{listing['name']} ({listing['full_address']})")
    print(f"  asking from      ${asking:,}")
    print(f"  market median    ${median:,}  (mean ${market['mean']:,}, {market['comparables_count']} comparables)")
    print(f"  difference       {(asking - median) / median:+.0%} against the median")
    # A few luxury units pull the mean far above the median; compare against the median.


if __name__ == "__main__":
    main()
