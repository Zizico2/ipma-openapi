# ipma-openapi

Two independent, community-maintained **OpenAPI 3.0.3** contracts for IPMA's
upstream HTTP feeds, plus two checked-in **Progenitor 0.16.0** Rust clients.
They describe source responses and are not published or endorsed by IPMA.

| API | Review the reference | Canonical specification | Generated Rust client |
| --- | --- | --- | --- |
| Documented `/open-data/` | [Readable reference](open-data/reference.md) | [OpenAPI YAML](open-data/openapi.yaml) | [ipma-open-data-client](open-data/rust) |
| Website `/public-data/` | [Readable reference](public-data/reference.md) | [OpenAPI YAML](public-data/openapi.yaml) | [ipma-public-data-client](public-data/rust) |

The specs, generated clients, examples and source captures live together for one
reviewable change history. The OpenAPI documents are the source of truth;
generated Rust and Markdown are never edited by hand. Both clients can be
consumed independently from this Git repository by package name and exact SHA.
No sibling repository is needed. This repository does not depend on protobuf.

## Repository layout

The root contains language-neutral orchestration, not a Cargo package or workspace.
Each API owns its contract, documentation, captures and language-specific clients,
following the proto repositories' separation of schemas and language tooling.

```text
open-data/
  openapi.yaml
  reference.md
  fixtures/             # source samples and API-local provenance manifest
  rust/                 # ipma-open-data-client, with its own Cargo.toml/lockfile
public-data/
  openapi.yaml
  reference.md
  fixtures/
  rust/                 # ipma-public-data-client, with its own Cargo.toml/lockfile
tools/
  rust/                 # shared Progenitor generator, manifest/lockfile/toolchain
  python/               # validation, reference generation and drift tooling
justfile                # delegates to the tooling and client recipes
```

Future language clients belong at `open-data/typescript/`, `public-data/go/`, etc.
Cargo discovers the two independent Rust packages by name from a full Git checkout;
consumers need no root Cargo.toml. The shared Rust test support lives with Rust
tooling, while each client reads its own API's fixture manifest.

## Scope and evidence

Open-data covers **20 distinct paths**: city/day forecasts, warnings, station
observations, sea forecasts, fire danger, UV, seismic events, location/code
catalogues, station/bivalve GeoJSON, three climate CSVs and the weather-icon ZIP.
The source is [IPMA's published HTML reference](https://api.ipma.pt/), checked
against live responses. Directory index pages and unrelated downloads are not
modeled as API operations. Day offsets and seismic regions use path parameters.

Public-data covers **four verified website feeds**: aggregate forecasts,
locations, districts and warnings. This is not an exhaustive public-data
catalogue. The source is [the website consumer JavaScript](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)
and captured responses. Each operation records its evidence and verification date.
Field descriptions distinguish source labels and observed meanings from formal
upstream guarantees. These schemas are our maintained understanding of IPMA.

All 24 operations have captured fixtures with [open-data provenance](open-data/fixtures/manifest.json)
and [public-data provenance](public-data/fixtures/manifest.json), verified on
2026-11-12. Each manifest records URL, actual media type, status, capture time,
response hash, fixture hash and sampling policy. JSON fixtures are structural
samples: arrays retain distinct field/type combinations, while GeoJSON collections
keep two small, unchanged source features. CSV fixtures keep the header and two
source rows; ZIP fixtures keep the complete archive. Complete responses were
validated before sampling. The initial live probe used the parameter examples in the specs; it does not establish
coverage of every city, island, offset or future weather condition.

A concrete reference discrepancy is recorded for evapotranspiration: the HTML
reference's `...idw-20d-concelhos.csv` returned 404; the live directory serves
`...idw-concelhos-20d.csv`. The spec uses the verified working path.

## Contracts and normalization

```text
OpenAPI upstream contract -> Progenitor HTTP client -> explicit conversion
                                                          -> protobuf API
```

OpenAPI preserves source key names and response envelopes. The public-data
warning envelope is separate from the open-data warning array. Dynamic station
IDs, UTC timestamp keys and DICO strings remain maps/strings. Numeric strings,
JSON numbers, empty strings, nulls and -99 sentinels are accepted where relevant;
clients do not reinterpret them as normalized measurements. Code values remain
open to unfamiliar integers. Source timestamps without timezone suffixes stay
strings rather than being mislabeled RFC3339 instants. Forecast rows retain the
source period code; the schema promises no fixed hourly horizon. The public
website's precipitation probability has a three-hour meaning, not a per-hour one.

Additional source fields are retained in generated `extra` maps. Known optional
fields use generated `Option` values, so null and omission merge on deserialize.
Numeric measurements use floating-point models, so `0` may serialize as `0.0`.
Retain original bytes when exact JSON representation matters. CSV and ZIP
operations return raw `ByteStream` responses; CSV column meanings are recorded in
`x-csv-columns` and the readable reference. No implicit CSV parsing is generated.
The two `.geojson` feeds advertise `text/plain` despite containing GeoJSON. The
spec records that actual media type and `x-body-encoding: json`; these operations
also return `ByteStream`. Their bodies can be deserialized explicitly into the
generated `GeoFeatureCollection` model, as exercised in the HTTP tests.

The generator cannot combine a typed 200 response with an untyped `default`
success response. The specs describe generic 4xx/5xx errors with no JSON body
schema instead. Generated errors expose status and headers; error bodies are not
modeled. Other statuses become unexpected responses.

## Use a client

```rust,no_run
use ipma_public_data_client::{Client, BASE_URL, http_client};

// Inside an async function returning anyhow::Result:
let client = Client::new_with_client(BASE_URL, http_client()?);
let forecasts = client.get_forecast(1110600.try_into()?).await?.into_inner();
```

`http_client()` validates TLS, enables gzip, sets 15s total/5s connection timeouts,
and disables redirects and retries. A custom base URL must include `/open-data`
or `/public-data`, without a trailing slash. Progenitor's raw constructors also
remain available. The helper does not impose a response-size cap or concurrency
limit. The typed client's JSON decoding buffers responses. Each crate also exposes
`raw::Client`, generated from the same contract with streaming success responses.
It accepts the same injected reqwest client and returns the original decompressed
bytes, allowing adapters to enforce body caps before parsing and retain exact
source JSON. This streaming projection changes response handling only, not paths,
parameters or the canonical specification. Callers own concurrency and stream limits.

## Develop and review changes

Requires Rust 1.99.1, uv and optionally Just. Python dependencies and tooling are
locked in `tools/python/uv.lock`; its `.python-version` pins the interpreter.
Each Rust directory owns its manifest, lockfile and pinned toolchain. Progenitor
is pinned exactly in `tools/rust/`. Normal verification is offline with respect
to IPMA, though first use downloads tool/dependency packages.

```sh
rtk just verify
rtk just generate
rtk just open-data-rust smoke
rtk just public-data-rust smoke
rtk just probe
```

The smoke examples make two requests each. The probe makes one request per
operation, sequentially, with a 30s timeout and 32 MiB body cap, and saves its
report under ignored `.artifacts/`. It validates complete responses, records
failures and reports newly unmodeled field names/types separately from normal
forecast value changes. Optional-field absence in finite samples cannot prove
removal. Arbitrary GeoJSON properties are intentionally source JSON, so their
internal semantics are not fully validated. No network probe runs on a schedule.

For an intentional fixture refresh:

```sh
rtk just capture .artifacts/review-candidate
```

Review the candidate manifest, failures and fields before copying approved
responses and each API's manifest into `open-data/fixtures/` or `public-data/fixtures/`.
Candidates mirror those API directories under the chosen output path. A capture
never overwrites an existing output directory. There is no automatic spec inference or auto-accept of
upstream changes. Update YAML descriptions/types and examples intentionally,
regenerate, then commit the specs, captures, reference and generated code together.
CI validates specifications/fixtures, rejects stale generated artifacts, runs
Python drift tests and exercises every generated operation against local HTTP
servers. A separate manually dispatched probe workflow uploads live reports.

Reuse of IPMA source data and icons remains subject to IPMA's conditions and
attribution. The OpenAPI maintenance project is independent of IPMA.
