# IPMA public-data: upstream HTTP reference

Generated from the canonical specification; do not edit this document directly.

[OpenAPI YAML](../specs/public-data.yaml) · [Capture provenance](../fixtures/manifest.json)

Describes source HTTP responses, not the normalized gRPC API. This specification is maintained independently and is not published or endorsed by IPMA. Based on the website JavaScript and captured responses; covers only the four verified website feeds. No complete endpoint catalogue is claimed. Missing measurements, numeric strings, JSON numbers, nulls and -99 sentinels are kept in their source representation. Unknown fields are permitted. Response fields are required only where the source reference and/or consumer invariants provide evidence. Capture fixtures do not establish universal guarantees. Naive timestamps are source strings interpreted as UTC by the website; no RFC3339 timezone suffix is invented. Attribution and reuse conditions: https://api.ipma.pt/.

Base URL: `https://api.ipma.pt/public-data`

Verified: 2026-11-12 · Evidence: [observed-website-feed](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

## Operations

| Operation | HTTP path |
| --- | --- |
| `get_forecast` | `GET /forecast/aggregate/{globalIdLocal}.json` |
| `get_locations` | `GET /forecast/locations.json` |
| `get_districts` | `GET /districts.json` |
| `get_warnings` | `GET /warnings/warnings_www.json` |

## get_forecast

Mixed hourly, three-hourly and daily forecasts

`GET /forecast/aggregate/{globalIdLocal}.json`

Returns source rows without interpolation, sorting or filtering. To build a next-ten-hours view, select idPeriodo=1 and future UTC timestamps. A fixed horizon is not guaranteed. Additional fields and unfamiliar codes are permitted.

- `globalIdLocal`: Website location ID from forecast/locations.json. Example: `1110600`. Constraints: `{'minimum': 1, 'maximum': 4294967295}`.

Success: **200**, `application/json`, `array<Forecast>`.

[Captured response](../fixtures/public-data/get_forecast.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_locations

Website forecast location catalogue

`GET /forecast/locations.json`

Website forecast location catalogue


Success: **200**, `application/json`, `array<Location>`.

[Captured response](../fixtures/public-data/get_locations.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_districts

Website district/island catalogue

`GET /districts.json`

Website district/island catalogue


Success: **200**, `application/json`, `array<District>`.

[Captured response](../fixtures/public-data/get_districts.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_warnings

Website warnings envelope

`GET /warnings/warnings_www.json`

Website warnings envelope


Success: **200**, `application/json`, `WarningsResponse`.

[Captured response](../fixtures/public-data/get_warnings.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## Schemas

Unknown source fields are accepted and preserved in generated `extra` maps. Optional known null fields deserialize, but generated `Option` fields collapse null and omission; retain the original response bytes if that distinction matters.

### NumericValue

Raw measurement. Null, empty strings and -99 are missing-data representations; clients do not normalize them.

Shape: `number or null or string`.

### CodeValue

Raw category code. Unknown integers and numeric strings are allowed; no closed category enum is inferred.

Shape: `integer or null or string`.

### Forecast



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `globalIdLocal` | integer | yes | Source location ID. |
| `dataPrev` | string | yes | Forecast timestamp, UTC. Daily rows also use this field. |
| `dataUpdate` | string or null | no | Source row update timestamp, UTC. |
| `idPeriodo` | CodeValue | no | Observed 1=hourly, 3=three-hourly, 24=daily. Unknown codes remain valid; coverage is not fixed. |
| `ddVento` | string or null | no | Wind direction source token. |
| `dirOndulacao` | string or null | no | Wave direction source token. |
| `tMed` | NumericValue | no | Air temperature, °C. |
| `tMin` | NumericValue | no | Daily minimum temperature, °C; generally daily rows. |
| `tMax` | NumericValue | no | Daily maximum temperature, °C; generally daily rows. |
| `hR` | NumericValue | no | Relative humidity, %. |
| `ffVento` | NumericValue | no | Wind speed at 10m, km/h. |
| `utci` | NumericValue | no | Source UTCI value, °C; retained as its named index. |
| `probabilidadePrecipita` | NumericValue | no | Website describes probability of >=0.3 mm precipitation during the preceding three hours. Do not reinterpret as a one-hour probability. |
| `iUv` | NumericValue | no | UV index; generally daily rows. |
| `tempAguaMar` | NumericValue | no | Sea-water temperature, °C. |
| `marTotal` | NumericValue | no | Total significant sea-wave height, m. |
| `ondulacao` | NumericValue | no | Swell height, m. |
| `periodOndulacao` | NumericValue | no | Swell period, s. |
| `periodoPico` | NumericValue | no | Peak period, s. |
| `idTipoTempo` | CodeValue | no | Weather-type source code. |
| `idIntensidadePrecipita` | CodeValue | no | Precipitation intensity source code. |
| `idFfxVento` | CodeValue | no | Daily wind-speed source class. |

### Location



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `globalIdLocal` | integer | yes | Website location ID. |
| `local` | string | yes | Location name. |
| `latitude` | NumericValue | no | WGS84 latitude, degrees. |
| `longitude` | NumericValue | no | WGS84 longitude, degrees. |
| `idAreaAviso` | string or null | no | Warning-area identifier. |
| `idRegiao` | CodeValue | no | Region ID. |
| `idDistrito` | CodeValue | no | District/island ID. |
| `idConcelho` | CodeValue | no | District-scoped municipality component. |

### District



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `idDistrito` | integer | yes | District/island identifier. |
| `idRegiao` | CodeValue | no | Region identifier. |
| `nome` | string | yes | District/island name. |

### Warning



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `idAreaAviso` | string | yes | Warning-area identifier. |
| `awarenessTypeName` | string | yes | Source phenomenon label, in Portuguese; unfamiliar values remain valid. |
| `awarenessLevelID` | string | yes | Source severity label; currently green/yellow/orange/red. Unknown values are retained. |
| `text` | string or null | no | Source description; may be empty. |
| `startTime` | string | yes | Start instant; source timestamp string, UTC. |
| `endTime` | string | yes | End instant; source timestamp string, UTC. |
| `reportDate` | string or null | no | Report timestamp, UTC. |

### WarningsResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Country code. |
| `dataAtualiza` | string or null | no | Source update timestamp, UTC; fractional seconds are observed. |
| `data` | array<Warning> | yes |  |
