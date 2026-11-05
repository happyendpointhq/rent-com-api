# Sample responses

Example `200` responses for six Rent.com API endpoints, copied from the API's public
documentation. Long arrays are cut to their first few items, and listing agent contact
fields are removed. Phone numbers are replaced with the fictional `(555) 010-0100`.
Field names and values are otherwise unchanged.

Privacy review (4 Nov 2026): the single house in `listings-by-ids.json` (`lc6820590`) keeps its street, city and ZIP but not its house number, its `url` reads `[removed]`, and the condo unit in `rent-estimate.json` (`lv3258870131`) keeps its tower address but not its unit (`unit_name` reads `[removed]`). Both homes' coordinates are rounded to three decimals (about 100 m). Apartment communities are unchanged.

| File | Request |
|---|---|
| `locations.json` | `GET /locations?query=austin` |
| `search.json` | `GET /search?location_slug=texas/austin` |
| `listing-details.json` | `GET /listing-details?listing_id=lc6705165` |
| `listings-by-ids.json` | `GET /listings-by-ids?listing_ids=lc6705165,lc6820590` |
| `rent-estimate.json` | `GET /rent-estimate?latitude=30.2672&longitude=-97.7431&beds=2` |
| `walk-score.json` | `GET /walk-score?listing_id=lc6705165` |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
