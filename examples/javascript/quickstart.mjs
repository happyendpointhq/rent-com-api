// Rent.com API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs austin

const HOST = 'rent-com1.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Rent.com API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const query = process.argv[2] ?? 'austin';
const { locations } = await get('/locations', { query, limit: 5 });
if (!locations.length) throw new Error(`No Rent.com location matches ${query}`);
const place = locations[0];
console.log(`Using ${place.name} (${place.location_slug})`);

const results = await get('/search', {
  location_slug: place.location_slug,
  beds: 2,
  max_price: 2000,
  sort: 'price_low_to_high',
  page_size: 10,
});
console.log(`${results.total} matching listings`);
for (const row of results.listings) {
  // The headline price is the cheapest floor plan overall; take the 2-bed rent instead.
  const twoBed = (row.price_by_beds ?? []).find((plan) => plan.beds === 2);
  const rent = twoBed ? `$${twoBed.min.toLocaleString('en-US')}` : row.price_text;
  console.log(`${rent.padStart(10)}  ${row.beds_text.padEnd(14)} ${row.name}`);
}
