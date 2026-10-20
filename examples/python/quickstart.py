"""Find a city, search it, then open the cheapest listing.

    python quickstart.py "austin"
"""

import sys

from client import get, management_name

query = sys.argv[1] if len(sys.argv) > 1 else "austin"

# 1. Resolve the place name to a location_slug. Search endpoints take the slug, not the name.
locations = get("/locations", query=query, limit=5)["locations"]
if not locations:
    raise SystemExit(f"No Rent.com location matches {query!r}")
place = locations[0]
print(f"Using {place['name']} ({place['location_slug']})")

# 2. Two-bedroom rentals under $2,000, cheapest first.
results = get(
    "/search",
    location_slug=place["location_slug"],
    beds=2,
    max_price=2000,
    sort="price_low_to_high",
    page_size=10,
)
print(f"{results['total']} matching listings, showing {len(results['listings'])}\n")
for row in results["listings"]:
    # A community matches when any floor plan has 2 beds, and its headline price is the cheapest
    # plan overall (often a studio). Read the 2-bed rent from price_by_beds instead.
    two_bed = next((p for p in row.get("price_by_beds") or [] if p["beds"] == 2), None)
    rent = f"${two_bed['min']:,}" if two_bed else row["price_text"]
    print(f"{rent:>10}  {row['beds_text']:<14} {row['name']}  ({row['listing_id']})")

# 3. Full record for the first result: floor plans, fees, pet policies, schools.
if results["listings"]:
    listing = get("/listing-details", listing_id=results["listings"][0]["listing_id"])
    print(f"\n{listing['name']}, {listing['full_address']}")
    print(f"Managed by: {management_name(listing)}")
    print(f"Units available: {listing['units_available']} ({listing['units_available_text']})")
    for plan in listing.get("floor_plans") or []:
        print(f"  {plan['name']:<10} {plan['beds_text']:<8} {plan['price_range_text']}")
