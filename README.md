# Rent.com API and Scraper

The Rent.com API returns US rental listings from Rent.com as JSON: apartments, houses,
condos and townhomes for rent, with rent by bedroom count, floor plans and unit
availability, fees, move-in deals, price drops, market rent estimates and walk scores.
Rent.com has no public developer API, so this REST API is the way to get its listings
into your own code without running and maintaining a Rent.com scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/rent-com-api?utm_source=github&utm_medium=readme&utm_campaign=rent-com-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/rent-com1
- Product page: https://happyendpoint.com/library/rent-com-api?utm_source=github&utm_medium=readme&utm_campaign=rent-com-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://rent-com1.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 19, all `GET` |
| Coverage | All 50 states and DC, down to city, neighborhood, ZIP code and college area |
| Property types | Apartments, houses, condos, townhouses, duplexes, triplexes |
| Page size | Up to 500 listings per page |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Search**
- Search a location (state, city, neighborhood, ZIP, county, college area) with 17 filters: beds, baths, property type, pet policy, amenities, rent and size range, move-in date, keyword, deals, recently updated, page views and more
- Search around a map point, inside a drawn polygon, nationwide by filters alone, by community name, or by pasting a Rent.com search URL
- Seven sort orders, including price, size and nearest first

**Listings**
- Rent, rent range and rent at each bedroom count
- Bed, bath and square foot ranges, availability and units available
- Move-in deals, deal types and price drops
- Management company and leasing phone number, page views, listing source, last update
- Full records: floor plans with every unit's rent, size, deposit and availability date, fees, estimated monthly and move-in costs, pet policies, parking, amenities, photos, nearby schools

**Market and neighborhood**
- Rent estimate for any US point and bedroom count: min, mean, median and max over the comparable pool, plus the nearest comparables
- Every unit listed at one building address
- Walk, transit and bike scores with sub-scores, nearby places, relative utility usage by ZIP

**Tracking**
- Refresh up to 50 saved listings in one call, with listings that came off the market reported separately

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/rent-com1). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Search endpoints take a `location_slug`, not a place name. Look it up first:

```bash
curl "https://rent-com1.p.rapidapi.com/locations?query=austin" \
  -H "x-rapidapi-host: rent-com1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://rent-com1.p.rapidapi.com/search?location_slug=texas/austin&beds=2&max_price=2000&sort=price_low_to_high" \
  -H "x-rapidapi-host: rent-com1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py austin
```

```python
from client import get

place = get("/locations", query="austin")["locations"][0]
results = get("/search", location_slug=place["location_slug"], beds=2, max_price=2000)
for row in results["listings"]:
    print(row["price_text"], row["name"], row["listing_id"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs austin
```

---

## Example response

One row from `GET /search?location_slug=texas/austin`, trimmed. Values are the example in the
API's public documentation. The full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "total": 6747,
    "page": 1,
    "page_size": 50,
    "total_pages": 135,
    "has_more": true,
    "listings": [
      {
        "listing_id": "lc5897531",
        "name": "Centro Studio Homes",
        "property_type": "apartments",
        "full_address": "824 Camino La Costa, Austin, TX 78752",
        "price": 695,
        "price_text": "$695+",
        "price_range": { "min": 695, "max": 1114 },
        "price_by_beds": [{ "beds": 0, "min": 695, "max": 1114 }],
        "availability_status": "TODAY",
        "units_available": 8,
        "has_price_drop": true,
        "deal_types": [{ "kind": "FREE_TIME", "text": "8 Weeks Free" }],
        "management_company": "Firmus Management",
        "page_views": 283,
        "listing_source": "ZILLOW",
        "updated_at": "2026-09-22T00:00:00.000Z"
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://rent-com1.p.rapidapi.com`

### Locations

| Endpoint | Returns |
|---|---|
| `GET /locations` | Locations matching typed text, with the `location_slug` searches need |
| `GET /location-details` | One location's centre, bounding box, listing counts and optional boundary |

### Search

| Endpoint | Returns |
|---|---|
| `GET /search` | Listings in a location, with all filters and sorts |
| `GET /search-by-coordinates` | Listings within a radius of a point |
| `GET /search-by-polygon` | Listings inside a drawn area |
| `GET /search-nationwide` | Listings anywhere in the US matching the filters |
| `GET /search-by-property-name` | Communities by name |
| `GET /search-by-url` | The results of a pasted Rent.com search URL |

### Listings and buildings

| Endpoint | Returns |
|---|---|
| `GET /listing-details` | The full listing: floor plans, units, fees, costs, policies, schools |
| `GET /listing-by-url` | The same, from a Rent.com listing URL |
| `GET /listings-by-ids` | Up to 50 listings at once, plus `not_found` for ones that came off the market |
| `GET /similar-listings` | Listings similar to one listing |
| `GET /building-details` | Every unit listed at one building address |

### Market and neighborhood

| Endpoint | Returns |
|---|---|
| `GET /rent-estimate` | Min, mean, median and max rent for a bedroom count at a point, with comparables |
| `GET /utility-estimates` | Relative electricity and gas usage for a ZIP code |
| `GET /walk-score` | Walk, transit and bike scores for a listing |
| `GET /nearby-places` | Grocery, schools, transit, parks and more near a point |
| `GET /agent-contacts` | Listing agents for agent-listed rentals in a location |
| `GET /status` | Service health |

---

## Things to know about the data

These come from building against the API. They are the mistakes that produce wrong numbers
rather than errors.

- **The headline `price` is the cheapest floor plan, not the rent for the beds you asked
  for.** A `beds=2` search matches a community when any floor plan has two bedrooms, and the
  row still shows its lowest rent, often a studio's. Read the two-bed rent from
  `price_by_beds`, or from `filter_match`, which lists the floor plans that matched your
  filters. `quickstart.py` does this.
- **Student housing is priced per bed.** Communities named "Student Housing - Rent by the
  Bed" quote rent per bed, so a two-bed row at $624 is one bed in a shared unit, not the
  apartment. Filter them out by name, or keep them in a separate column, before you compare
  rents across a city.
- **`price_text` ends in `+` when the rent is a starting price.** `"$695+"` is a range,
  `"$2,100"` is one unit.
- **`units_available` and `units_available_text` can disagree on purpose.** The documented
  example for The Ivy has `units_available: 37` and the text `"10+ Units Available"`. Count
  with the number, show the text.
- **`management_company` changes type.** It is a string on search rows and an object with a
  `name` on `/listing-details`. `client.management_name()` handles both.
- **Communities and single units are both listings.** In the documented examples, apartment
  communities have IDs like `lc6705165` and `unit_name: null`, while a single condo unit has
  an ID like `lv3258870131`, its unit number in `unit_name`, and a `building_id` (`b83674`)
  that leads to `/building-details` and every other unit at that address.
- **Rent estimates exclude apartment listings.** Comparables are houses, condos, townhomes and
  duplexes. A wide spread is normal: the documented downtown Austin two-bed example has a
  median of $2,100 and a mean of $2,454, pulled up by a $20,318 maximum. Use the median.
- **Deep paging has a ceiling.** `page` times `page_size` may not exceed 100,000. Split a large
  market by filters or smaller areas, and stop on `has_more`.
- **`updated_within_days` starts at 2.** A value of `1` is a 400.
- **Filters combine differently.** Several `beds` or `property_types` values are OR; several
  `amenities` are AND, so each extra amenity narrows the result.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Location lookup, a filtered search with per-bedroom rent, one full listing with floor plans |
| [`examples/python/search_to_csv.py`](examples/python/search_to_csv.py) | Pages through a whole search at 500 rows a page and writes a flat CSV |
| [`examples/python/watchlist.py`](examples/python/watchlist.py) | Re-checks saved listings for rent changes and delistings with `/listings-by-ids` |
| [`examples/python/rent_check.py`](examples/python/rent_check.py) | Compares a listing's asking rent with the market median around it |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for six endpoints |

---

## API or your own Rent.com scraper

A homemade Rent.com scraper works until the page structure, the anti-bot rules or the
listing feed changes, and then it returns nothing or the wrong fields. This API returns
the same listings as documented JSON with a stable contract, so the work you keep is the
analysis, not the parser. If you need a one-off national file or a recurring export rather
than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=rent-com-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Rent.com
listings without code:

```json
{
  "mcpServers": {
    "rent-com": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: rent-com1.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Rent.com API?

Rent.com does not publish a public developer API for its listings. This API, built and
maintained by Happy Endpoint and independent of Rent.com, provides that access as REST and
JSON.

### Is there a free Rent.com API?

Yes. The [RapidAPI listing](https://rapidapi.com/happyendpoint/api/rent-com1) has a free plan, and every endpoint can be tried on it.

### How do I use the Rent.com API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is a 51-line client, and
the other scripts in that folder are ready to run.

### Where is the Rent.com API documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the
endpoint table above summarises them. Example responses are in [`samples/`](samples/).

### Can I scrape Rent.com rental prices by bedroom count?

Yes. Every listing row carries `price_by_beds`, the rent range at each bedroom count it
offers, and `/listing-details` adds every floor plan and unit with its own rent.

### Can I track rent changes and listings that come off the market?

Yes. Save the `listing_id` values you care about and call `/listings-by-ids` on a schedule.
Ids that no longer resolve come back in `not_found`. [`watchlist.py`](examples/python/watchlist.py)
does this.

### Do you cover other US rental and real estate sites?

Yes, including Realtor.com, Auction.com and Vrbo. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=rent-com-api).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spanish sale and rental listings, with the same kind of runnable Python examples
- [dubai-property-price-tracker](https://github.com/happyendpointhq/dubai-property-price-tracker) - the watchlist idea, built out with SQLite, a scheduler and alerts
- [bayut-api-python-examples](https://github.com/happyendpointhq/bayut-api-python-examples) - more Python patterns for a property API

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
