"""Export every listing in a Rent.com search to CSV.

    python search_to_csv.py texas/austin --beds 1,2 --max-price 1800 --out austin.csv

Pages at 500 rows (the maximum) and stops on `has_more`. A search can be paged through its
first 100,000 results; split bigger markets with filters or smaller areas.
"""

import argparse
import csv

from client import get, management_name

COLUMNS = [
    "listing_id", "name", "property_type", "full_address", "zip", "latitude", "longitude",
    "price", "price_max", "beds_min", "beds_max", "baths_min", "sqft_min", "sqft_max",
    "availability_status", "units_available", "has_price_drop", "deal", "management_company",
    "page_views", "listing_source", "updated_at", "url",
]


def flatten(row):
    deal = row.get("deal_types") or []
    return {
        **{k: row.get(k) for k in COLUMNS if k in row},
        "price_max": (row.get("price_range") or {}).get("max"),
        "beds_min": (row.get("beds") or {}).get("min"),
        "beds_max": (row.get("beds") or {}).get("max"),
        "baths_min": (row.get("baths") or {}).get("min"),
        "sqft_min": (row.get("sqft") or {}).get("min"),
        "sqft_max": (row.get("sqft") or {}).get("max"),
        "deal": deal[0]["text"] if deal else None,
        "management_company": management_name(row),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("location_slug", help="for example texas/austin (from /locations)")
    parser.add_argument("--beds", help="studio, 1, 2, 3, 4_plus; comma-separated for several")
    parser.add_argument("--min-price", type=int)
    parser.add_argument("--max-price", type=int)
    parser.add_argument("--property-types", help="apartments, houses, townhouses, duplexes, condos, triplexes")
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--out", default="listings.csv")
    args = parser.parse_args()

    written = 0
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for page in range(1, args.max_pages + 1):
            data = get(
                "/search",
                location_slug=args.location_slug,
                beds=args.beds,
                min_price=args.min_price,
                max_price=args.max_price,
                property_types=args.property_types,
                page=page,
                page_size=500,
            )
            for row in data["listings"]:
                writer.writerow(flatten(row))
                written += 1
            print(f"page {page}: {written} of {data['total']} listings")
            if not data.get("has_more"):
                break
    print(f"Wrote {written} rows to {args.out}")


if __name__ == "__main__":
    main()
