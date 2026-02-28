import csv
import cloudscraper

OUT_CSV = 'data/etfs-by-assets.csv'
URL = 'https://etfdb.com/api/screener/'


def norm(v):
    if isinstance(v, dict):
        if 'text' in v:
            return v.get('text', '')
        if 'url' in v:
            return v.get('url', '')
        return str(v)
    return v


scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})

payload = {
    'page': 1,
    'per_page': 5000,
    'sort_by': 'assets',
    'sort_direction': 'desc',
}

resp = scraper.post(URL, json=payload, timeout=90)
resp.raise_for_status()
body = resp.json()
raw_rows = body.get('data', [])
meta = body.get('meta', {})

rows = []
for row in raw_rows:
    rows.append({k: norm(v) for k, v in row.items()})

all_fields = set()
for row in rows:
    all_fields.update(row.keys())

preferred_order = [
    'symbol',
    'name',
    'price',
    'assets',
    'average_volume',
    'ytd',
    'asset_class',
]
fieldnames = [k for k in preferred_order if k in all_fields] + sorted(k for k in all_fields if k not in preferred_order)

with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote={OUT_CSV}")
print(f"rows={len(rows)} total_records={meta.get('total_records')} total_pages={meta.get('total_pages')}")
