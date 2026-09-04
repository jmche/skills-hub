# Human Cell Atlas (HCA)

## Base URL
```
https://service.azul.data.humancellatlas.org/
```

## Auth
No auth required.

## Catalog Discovery (do this first)

Catalog names are renamed periodically (e.g. `dcp2` was retired) and hardcoding
one will eventually break. Discover the current default catalog at request time:

```bash
curl -s "https://service.azul.data.humancellatlas.org/index/catalogs" | python3 -c "import json,sys; print(json.load(sys.stdin)['default_catalog'])"
```

As of 2026-07-15 this returns `dcp60` — use that if the discovery call is
skipped, but prefer the live lookup since it changes over time.

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/index/catalogs` | List valid catalog names + current default (no `catalog` param needed) |
| `/index/projects?size={n}&catalog={catalog}` | List/search projects |
| `/index/samples?size={n}&catalog={catalog}` | List/search samples |
| `/index/files?size={n}&catalog={catalog}` | List/search files |
| `/index/summary?catalog={catalog}` | Summary statistics |

## Example Calls
```
# List projects (verified 2026-07-15, catalog=dcp60)
https://service.azul.data.humancellatlas.org/index/projects?size=5&catalog=dcp60

# Summary stats
https://service.azul.data.humancellatlas.org/index/summary?catalog=dcp60
```

Supports JSON filter parameters for organ, species, library construction, etc.

**Verified 2026-07-15:** `catalog=dcp2` returns 404 ("Catalog name 'dcp2' does
not exist") — that catalog was retired. The current default catalog is
`dcp60` (532 projects, 592K files as of this check). Always resolve the
catalog via `/index/catalogs` rather than hardcoding a name.

## Response Format
JSON. `hits` array with project/sample/file metadata + pagination.

## Rate Limits
No published limits. Be reasonable.
