# IPMA public-data: upstream HTTP reference

Generated from the canonical specification; do not edit this document directly.

[OpenAPI YAML](openapi.yaml) · [Capture provenance](fixtures/manifest.json)

Describes source HTTP responses, not the normalized gRPC API. This specification is maintained independently and is not published or endorsed by IPMA. Based on the website JavaScript and captured responses; covers only the verified Portugal website feeds listed here. No complete endpoint catalogue is claimed. Missing measurements, numeric strings, JSON numbers, nulls and -99 sentinels are kept in their source representation. Unknown fields are permitted. Response fields are required only where the source reference and/or consumer invariants provide evidence. Capture fixtures do not establish universal guarantees. Naive timestamps are source strings interpreted as UTC by the website; no RFC3339 timezone suffix is invented. Attribution and reuse conditions: https://api.ipma.pt/.

Base URL: `https://api.ipma.pt/public-data`

Verified: 2026-11-15 · Evidence: [observed-website-feed](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

## Operations

| Operation | HTTP path |
| --- | --- |
| `get_forecast` | `GET /forecast/aggregate/{globalIdLocal}.json` |
| `get_locations` | `GET /forecast/locations.json` |
| `get_districts` | `GET /districts.json` |
| `get_warnings` | `GET /warnings/warnings_www.json` |
| `get_daily_station_observations` | `GET /observation/surface-stations/daily_stations/{year}/{monthDir}/obs_dia_{year}_{month}_{stationId}.json` |
| `get_fire_danger_map` | `GET /mf2_preview/{fireLayer}/{fireLayer}_{date}T00_00_00.png` |
| `get_model_map` | `GET /mf2_preview/{modelLayer}/{modelLayer}_{time}.png` |
| `get_model_wind_field` | `GET /mf2_preview/Tracers/{time}.json` |

## get_forecast

Mixed hourly, three-hourly and daily forecasts

`GET /forecast/aggregate/{globalIdLocal}.json`

Returns source rows without interpolation, sorting or filtering. To build a next-ten-hours view, select idPeriodo=1 and future UTC timestamps. A fixed horizon is not guaranteed. Additional fields and unfamiliar codes are permitted.

- `globalIdLocal`: Website location ID from forecast/locations.json. Example: `1110600`. Constraints: `{'minimum': 1, 'maximum': 4294967295}`.

Success: **200**, `application/json`, `array<Forecast>`.

[Captured response](fixtures/get_forecast.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_locations

Website forecast location catalogue

`GET /forecast/locations.json`

Website forecast location catalogue


Success: **200**, `application/json`, `array<Location>`.

[Captured response](fixtures/get_locations.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_districts

Website district/island catalogue

`GET /districts.json`

Website district/island catalogue


Success: **200**, `application/json`, `array<District>`.

[Captured response](fixtures/get_districts.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_warnings

Website warnings envelope

`GET /warnings/warnings_www.json`

Website warnings envelope


Success: **200**, `application/json`, `WarningsResponse`.

[Captured response](fixtures/get_warnings.json) · [Source evidence](https://www.ipma.pt/opencms/bin/scripts/otempo/prev.localidade.hora.js)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_daily_station_observations

Monthly series of daily surface-station summaries

`GET /observation/surface-stations/daily_stations/{year}/{monthDir}/obs_dia_{year}_{month}_{stationId}.json`

One station-month of daily summaries for the main IPMA surface stations on the mainland, Azores and Madeira. The directory month is zero-padded while the filename month is not, so monthDir and month must name the same month. Rows cover every day of the month; days not yet observed have null measurements. Archived months were observed from January 2019. Unpublished station-months, including 1200579 Lisboa listed by the website, redirect to the IPMA homepage with HTTP 302 rather than returning 404.

- `year`: Calendar year; used in the directory and filename. Example: `2026`. Constraints: `{'minimum': 2019, 'maximum': 9999}`.
- `monthDir`: Zero-padded month directory, 01-12. Example: `10`. Constraints: `{}`.
- `month`: Unpadded filename month, 1-12; the same month as monthDir. Example: `10`. Constraints: `{'minimum': 1, 'maximum': 12}`.
- `stationId`: Surface station ID. The website lists 1200501, 1200511, 1200512, 1200522, 1200524, 1200545, 1200548, 1200551, 1200554, 1200558, 1200560, 1200562, 1200567, 1200570, 1200571, 1200575, 1200579, 1210622, 1210683, 1210702, 1210718, 1210734 and 1210770. Example: `1200545`. Constraints: `{'minimum': 1, 'maximum': 4294967295}`.

Success: **200**, `application/json`, `DailyStationObservations`.

[Captured response](fixtures/get_daily_station_observations.json) · [Source evidence](https://www.ipma.pt/opencms/pt/oclima/monitoriza.dia/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_fire_danger_map

Daily LSA SAF fire-danger map frame for mainland Portugal

`GET /mf2_preview/{fireLayer}/{fireLayer}_{date}T00_00_00.png`

Transparent PNG overlay for the website fire-danger map. The image covers latitude 35.9077838 to 43.9007122 and longitude -12.8000047 to -1.2014967 (WGS84 bounds used by the website). Layers: lsasaf_fwi_continent Fire Weather Index; lsasaf_isi_continent Initial Spread Index; lsasaf_bui_continent Buildup Index; lsasaf_ffmc_continent Fine Fuel Moisture Code; lsasaf_p2000_continent probability that a detected fire reaches 2000 GJ of released energy; lsasaf_risk_continent Fire Risk Map classes. Values are colour classes; the legends live on the website page. Frames were observed from the previous UTC day through about five days ahead; older and later dates redirect to the IPMA homepage with HTTP 302. The website also references lsasaf_fwi_prc_continent, but no frame was published for any probed date.

- `fireLayer`: Fire-danger layer name; used in the directory and filename. Example: `lsasaf_fwi_continent`. Constraints: `{'enum': ['lsasaf_fwi_continent', 'lsasaf_isi_continent', 'lsasaf_bui_continent', 'lsasaf_ffmc_continent', 'lsasaf_p2000_continent', 'lsasaf_risk_continent']}`.
- `date`: UTC forecast day, YYYY-MM-DD. The website formats this name in browser-local time, which matched UTC for the November 2026 captures; daylight-saving naming is unverified. Example: `2026-11-15`. Constraints: `{}`. Rolling: the example expires; probes use the current UTC time.

Success: **200**, `image/png`, `string`.

[Captured response](fixtures/get_fire_danger_map.png) · [Source evidence](https://www.ipma.pt/opencms/pt/riscoincendio/fwi/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_model_map

Hourly ECMWF model map frame for Portugal and the Atlantic

`GET /mf2_preview/{modelLayer}/{modelLayer}_{time}.png`

Transparent PNG overlay for the website numerical-forecast map. The image covers latitude 27.9624 to 46.75 and longitude -37.05 to 0.0802303 (WGS84 bounds used by the website), including mainland Portugal, the Azores and Madeira. Layers: ecmwf_2t_atlantic 2 m temperature; ecmwf_mslp_atlantic mean sea-level pressure; ecmwf_pcp_atlantic precipitation; ecmwf_10windintensity_atlantic 10 m wind speed. Values are colour classes; the legends live on the website page. Frames were observed hourly from 00:00 UTC on the previous day to about 48 hours ahead; other hours redirect to the IPMA homepage with HTTP 302.

- `modelLayer`: Model layer name; used in the directory and filename. Example: `ecmwf_pcp_atlantic`. Constraints: `{'enum': ['ecmwf_2t_atlantic', 'ecmwf_mslp_atlantic', 'ecmwf_pcp_atlantic', 'ecmwf_10windintensity_atlantic']}`.
- `time`: UTC valid hour, YYYY-MM-DDTHH_00_00. The website formats this name in browser-local time, which matched UTC for the November 2026 captures; daylight-saving naming is unverified. Example: `2026-11-15T19_00_00`. Constraints: `{}`. Rolling: the example expires; probes use the current UTC time.

Success: **200**, `image/png`, `string`.

[Captured response](fixtures/get_model_map.png) · [Source evidence](https://www.ipma.pt/opencms/pt/otempo/prev.numerica/index-mf2.jsp)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_model_wind_field

Hourly ECMWF 10 m wind vector grid for Portugal and the Atlantic

`GET /mf2_preview/Tracers/{time}.json`

Wind field animated as particles on the website numerical-forecast map. The array holds two grid components with identical headers; the website reads the first as the eastward (u) and the second as the northward (v) component, in m/s. Each data array is row-major, starting at la1/lo1 (north-west) and stepping east by dx and south by dy. Frame availability matches get_model_map; other hours redirect to the IPMA homepage with HTTP 302.

- `time`: UTC valid hour, YYYY-MM-DDTHH_00_00. The website formats this name in browser-local time, which matched UTC for the November 2026 captures; daylight-saving naming is unverified. Example: `2026-11-15T19_00_00`. Constraints: `{}`. Rolling: the example expires; probes use the current UTC time.

Success: **200**, `application/json`, `array<WindGridComponent>`.

[Captured response](fixtures/get_model_wind_field.json) · [Source evidence](https://www.ipma.pt/opencms/pt/otempo/prev.numerica/index-mf2.jsp)

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

### DailyStationObservations



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `station_id` | string | yes | Surface station ID as a decimal string. |
| `station_name` | string | no | Station name; the website strips a trailing " (IPMA)" for display. |
| `latitude` | NumericValue | no | WGS84 latitude, degrees. |
| `longitude` | NumericValue | no | WGS84 longitude, degrees. |
| `height` | NumericValue | no | Station elevation, m. |
| `data` | array<DailyStationObservation> | yes |  |

### DailyStationObservation



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `datetime` | string | yes | Observation day as a UTC midnight timestamp with a Z suffix and milliseconds. |
| `Tar_med` | NumericValue | no | Daily mean air temperature, °C. |
| `Tar_max` | NumericValue | no | Daily maximum air temperature, °C. |
| `Tar_min` | NumericValue | no | Daily minimum air temperature, °C. |
| `RRR_qt` | NumericValue | no | Daily accumulated precipitation, mm. |
| `HR_med` | NumericValue | no | Daily mean relative humidity, %. Unit not labelled by the website; inferred from observed values. |
| `Pr_Nm_med` | NumericValue | no | Daily mean sea-level pressure, hPa. Unit not labelled by the website; inferred from observed values. |
| `ff_med` | NumericValue | no | Daily mean wind speed. Unit not labelled by the website; observed magnitudes are consistent with m/s. |

### WindGridHeader



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `nx` | integer | yes | Grid columns (longitude steps). |
| `ny` | integer | yes | Grid rows (latitude steps). |
| `numberPoints` | integer | no | Grid points; nx × ny. |
| `lo1` | number | yes | Western longitude of the first column, degrees. |
| `lo2` | number | no | Eastern longitude of the last column, degrees. |
| `la1` | number | yes | Northern latitude of the first row, degrees. |
| `la2` | number | no | Southern latitude of the last row, degrees. |
| `dx` | number | yes | Longitude step, degrees. |
| `dy` | number | yes | Latitude step, degrees. |

### WindGridComponent



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `header` | WindGridHeader | yes |  |
| `data` | array<number or null> | yes | Row-major component values, m/s. |
