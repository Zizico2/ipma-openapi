# IPMA open-data: upstream HTTP reference

Generated from the canonical specification; do not edit this document directly.

[OpenAPI YAML](openapi.yaml) · [Capture provenance](fixtures/manifest.json)

Describes source HTTP responses, not the normalized gRPC API. This specification is maintained independently and is not published or endorsed by IPMA. Based on the official HTML reference and captured responses. Missing measurements, numeric strings, JSON numbers, nulls and -99 sentinels are kept in their source representation. Unknown fields are permitted. Response fields are required only where the source reference and/or consumer invariants provide evidence. Capture fixtures do not establish universal guarantees. Naive timestamps are source strings interpreted as UTC by the website; no RFC3339 timezone suffix is invented. Attribution and reuse conditions: https://api.ipma.pt/.

Base URL: `https://api.ipma.pt/open-data`

Verified: 2026-11-12 · Evidence: [documented-html](https://api.ipma.pt/)

## Operations

| Operation | HTTP path |
| --- | --- |
| `get_city_daily_forecast` | `GET /forecast/meteorology/cities/daily/{globalIdLocal}.json` |
| `get_daily_forecasts` | `GET /forecast/meteorology/cities/daily/hp-daily-forecast-day{idDay}.json` |
| `get_warnings` | `GET /forecast/warnings/warnings_www.json` |
| `get_observations` | `GET /observation/meteorology/stations/observations.json` |
| `get_sea_forecasts` | `GET /forecast/oceanography/daily/hp-daily-sea-forecast-day{idDay}.json` |
| `get_fire_risk` | `GET /forecast/meteorology/rcm/rcm-d{idDay}.json` |
| `get_uv_forecasts` | `GET /forecast/meteorology/uv/uv.json` |
| `get_seismic_events` | `GET /observation/seismic/{idArea}.json` |
| `get_locations` | `GET /distrits-islands.json` |
| `get_sea_locations` | `GET /sea-locations.json` |
| `get_weather_codes` | `GET /weather-type-classe.json` |
| `get_wind_codes` | `GET /wind-speed-daily-classe.json` |
| `get_precipitation_codes` | `GET /precipitation-classe.json` |
| `get_recent_observations_geojson` | `GET /observation/meteorology/stations/obs-surface.geojson` |
| `get_stations` | `GET /observation/meteorology/stations/stations.json` |
| `get_bivalve_zones` | `GET /observation/biology/bivalves/CI_SNMB.geojson` |
| `get_climate_precipitation` | `GET /observation/climate/precipitation/prec-p1d-continental-obssup-idw-concelhos-20d.csv` |
| `get_climate_temperature` | `GET /observation/climate/temperature/t2m-p1d-continental-obssup-idw-concelhos-20d.csv` |
| `get_weather_icons` | `GET /forecast/meteorology/icons_ipma_weather.zip` |
| `get_climate_evapotranspiration` | `GET /observation/climate/evapotranspiration/et0-p1d-continental-obssup-idw-concelhos-20d.csv` |

## get_city_daily_forecast

Five-day daily forecast for one city

`GET /forecast/meteorology/cities/daily/{globalIdLocal}.json`

Five-day daily forecast for one city

- `globalIdLocal`: IPMA weather location ID from distrits-islands.json. Example: `1110600`. Constraints: `{'minimum': 1, 'maximum': 4294967295}`.

Success: **200**, `application/json`, `CityDailyForecastResponse`.

[Captured response](fixtures/get_city_daily_forecast.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_daily_forecasts

Daily forecasts across locations

`GET /forecast/meteorology/cities/daily/hp-daily-forecast-day{idDay}.json`

Daily forecasts across locations

- `idDay`: Day offset: 0 today, 1 tomorrow, 2 the following day. Example: `0`. Constraints: `{'minimum': 0, 'maximum': 2}`.

Success: **200**, `application/json`, `DailyForecastResponse`.

[Captured response](fixtures/get_daily_forecasts.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_warnings

Published weather warnings

`GET /forecast/warnings/warnings_www.json`

Published weather warnings


Success: **200**, `application/json`, `array<Warning>`.

[Captured response](fixtures/get_warnings.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_observations

Rolling hourly station observations, approximately 24 hours

`GET /observation/meteorology/stations/observations.json`

Rolling hourly station observations, approximately 24 hours


Success: **200**, `application/json`, `ObservationsResponse`.

[Captured response](fixtures/get_observations.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_sea_forecasts

Daily coastal forecasts

`GET /forecast/oceanography/daily/hp-daily-sea-forecast-day{idDay}.json`

Daily coastal forecasts

- `idDay`: Day offset: 0 today, 1 tomorrow, 2 the following day. Example: `0`. Constraints: `{'minimum': 0, 'maximum': 2}`.

Success: **200**, `application/json`, `SeaForecastResponse`.

[Captured response](fixtures/get_sea_forecasts.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_fire_risk

Municipal fire danger

`GET /forecast/meteorology/rcm/rcm-d{idDay}.json`

Municipal fire danger

- `idDay`: Day offset: 0 today, 1 tomorrow, 2 the following day. Example: `0`. Constraints: `{'minimum': 0, 'maximum': 2}`.

Success: **200**, `application/json`, `FireRiskResponse`.

[Captured response](fixtures/get_fire_risk.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_uv_forecasts

Published UV forecasts

`GET /forecast/meteorology/uv/uv.json`

Published UV forecasts


Success: **200**, `application/json`, `array<UvForecast>`.

[Captured response](fixtures/get_uv_forecasts.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_seismic_events

Rolling thirty-day seismic catalogue

`GET /observation/seismic/{idArea}.json`

Rolling thirty-day seismic catalogue

- `idArea`: Seismic region: 3 Azores, 7 mainland/Madeira. Example: `7`. Constraints: `{'enum': [3, 7]}`.

Success: **200**, `application/json`, `SeismicResponse`.

[Captured response](fixtures/get_seismic_events.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_locations

Weather locations and reference identifiers

`GET /distrits-islands.json`

Weather locations and reference identifiers


Success: **200**, `application/json`, `LocationsResponse`.

[Captured response](fixtures/get_locations.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_sea_locations

Coastal locations

`GET /sea-locations.json`

Coastal locations


Success: **200**, `application/json`, `array<Location>`.

[Captured response](fixtures/get_sea_locations.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_weather_codes

Weather-type reference table

`GET /weather-type-classe.json`

Weather-type reference table


Success: **200**, `application/json`, `WeatherCodeResponse`.

[Captured response](fixtures/get_weather_codes.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_wind_codes

Wind-speed reference table

`GET /wind-speed-daily-classe.json`

Wind-speed reference table


Success: **200**, `application/json`, `WindCodeResponse`.

[Captured response](fixtures/get_wind_codes.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_precipitation_codes

Precipitation-intensity reference table

`GET /precipitation-classe.json`

Precipitation-intensity reference table


Success: **200**, `application/json`, `PrecipitationCodeResponse`.

[Captured response](fixtures/get_precipitation_codes.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_recent_observations_geojson

Recent station observations as GeoJSON

`GET /observation/meteorology/stations/obs-surface.geojson`

Recent station observations as GeoJSON The live server advertises text/plain; the body contains GeoJSON. The schema describes the decoded JSON. Progenitor returns a raw ByteStream for this media type; deserialize it into GeoFeatureCollection explicitly.


Success: **200**, `text/plain`, `GeoFeatureCollection`.

[Captured response](fixtures/get_recent_observations_geojson.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_stations

Station catalogue as an array of GeoJSON Features

`GET /observation/meteorology/stations/stations.json`

Station catalogue as an array of GeoJSON Features


Success: **200**, `application/json`, `array<GeoFeature>`.

[Captured response](fixtures/get_stations.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_bivalve_zones

Bivalve harvesting permissions and zone geometries

`GET /observation/biology/bivalves/CI_SNMB.geojson`

Bivalve harvesting permissions and zone geometries The live server advertises text/plain; the body contains GeoJSON. The schema describes the decoded JSON. Progenitor returns a raw ByteStream for this media type; deserialize it into GeoFeatureCollection explicitly.


Success: **200**, `text/plain`, `GeoFeatureCollection`.

[Captured response](fixtures/get_bivalve_zones.json) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_climate_precipitation

Rolling twenty-day municipal precipitation

`GET /observation/climate/precipitation/prec-p1d-continental-obssup-idw-concelhos-20d.csv`

Municipal precipitation statistics; mean_tp and related totals are mm, maximum rate statistics are mm/h. CSV columns time,zname,zid plus dataset-specific statistics. Values are kept as CSV; DICO identifiers retain leading zeroes. Missing-value sentinels remain raw.


Success: **200**, `text/csv`, `string`.

[Captured response](fixtures/get_climate_precipitation.csv) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

CSV is returned as raw bytes. Columns and units:

| Column | Meaning |
| --- | --- |
| `time` | Source UTC time string. |
| `zname` | Municipality name. |
| `zid` | Municipality DICO string; preserve leading zeroes. |
| `mean_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `std_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `min_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `max_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `percentile_25_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `median_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `percentile_75_maxprate` | Raw numeric CSV value. -99 is nodata. Units: mm/h. |
| `mean_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `std_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `min_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `max_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `percentile_25_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `median_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `percentile_75_tp` | Raw numeric CSV value. -99 is nodata. Units: mm. |

## get_climate_temperature

Rolling twenty-day municipal temperature

`GET /observation/climate/temperature/t2m-p1d-continental-obssup-idw-concelhos-20d.csv`

Municipal air-temperature statistics, °C. CSV columns time,zname,zid plus dataset-specific statistics. Values are kept as CSV; DICO identifiers retain leading zeroes. Missing-value sentinels remain raw.


Success: **200**, `text/csv`, `string`.

[Captured response](fixtures/get_climate_temperature.csv) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

CSV is returned as raw bytes. Columns and units:

| Column | Meaning |
| --- | --- |
| `time` | Source UTC time string. |
| `zname` | Municipality name. |
| `zid` | Municipality DICO string; preserve leading zeroes. |
| `mean_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `std_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `min_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `max_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `percentile_25_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `median_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `percentile_75_maxt2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `mean_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `std_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `min_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `max_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `percentile_25_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `median_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `percentile_75_mint2m` | Raw numeric CSV value. -99 is nodata. Units: °C. |
| `mean_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `std_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `min_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `max_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `percentile_25_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `median_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |
| `percentile_75_meant2m` | Raw statistic for daily mean air temperature, °C. -99 is nodata. |

## get_weather_icons

Source weather icons ZIP

`GET /forecast/meteorology/icons_ipma_weather.zip`

Auxiliary ZIP linked from the official API reference. Returned as raw bytes; filenames are not a normalized icon API.


Success: **200**, `application/zip`, `string`.

[Captured response](fixtures/get_weather_icons.zip) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

## get_climate_evapotranspiration

Rolling twenty-day municipal evapotranspiration

`GET /observation/climate/evapotranspiration/et0-p1d-continental-obssup-idw-concelhos-20d.csv`

Daily reference evapotranspiration, mm. CSV columns time,zname,zid plus dataset-specific statistics. Values are kept as CSV; DICO identifiers retain leading zeroes. Missing-value sentinels remain raw. The source reference lists slightly different legacy filenames; this path is verified against the current service.


Success: **200**, `text/csv`, `string`.

[Captured response](fixtures/get_climate_evapotranspiration.csv) · [Source evidence](https://api.ipma.pt/)

HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.

**Reference discrepancy:** The published filename returned HTTP 404 on 2026-11-12. This operation uses the working filename listed in the live directory and captured in fixtures/manifest.json.

Published path: `/observation/climate/evapotranspiration/et0-p1d-continental-obssup-idw-20d-concelhos.csv`.

CSV is returned as raw bytes. Columns and units:

| Column | Meaning |
| --- | --- |
| `time` | Source UTC time string. |
| `zname` | Municipality name. |
| `zid` | Municipality DICO string; preserve leading zeroes. |
| `mean_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `std_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `min_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `max_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `percentile_25_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `median_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |
| `percentile_75_et0` | Raw numeric CSV value. -99 is nodata. Units: mm. |

## Schemas

Unknown source fields are accepted and preserved in generated `extra` maps. Optional known null fields deserialize, but generated `Option` fields collapse null and omission; retain the original response bytes if that distinction matters.

### NumericValue

Raw measurement. Null, empty strings and -99 are missing-data representations; clients do not normalize them.

Shape: `number or null or string`.

### CodeValue

Raw category code. Unknown integers and numeric strings are allowed; no closed category enum is inferred.

Shape: `integer or null or string`.

### DailyForecast



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `latitude` | NumericValue | no | Latitude in WGS84 degrees. |
| `longitude` | NumericValue | no | Longitude in WGS84 degrees. |
| `tMin` | NumericValue | no | Daily minimum air temperature, °C. |
| `tMax` | NumericValue | no | Daily maximum air temperature, °C. |
| `precipitaProb` | NumericValue | no | Daily precipitation probability, %. The source key is precipitaProb; prose reference also spells probPrecipita. |
| `idWeatherType` | CodeValue | no | Weather-type source code. |
| `classWindSpeed` | CodeValue | no | Daily wind-speed class. |
| `classPrecInt` | CodeValue | no | Precipitation intensity class. |
| `predWindDir` | string or null | no | Prevailing compass direction. |
| `forecastDate` | string | no | Forecast civil date, YYYY-MM-DD; not a timestamp. |
| `globalIdLocal` | integer | no | Location identifier when supplied per row. |

### CityDailyForecastResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<DailyForecast> | yes |  |
| `globalIdLocal` | integer | yes | Location identifier. |

### DailyForecastResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<DailyForecast> | yes |  |
| `forecastDate` | string | yes | Civil date applying to rows without their own forecastDate. |

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

### StationObservation



Shape: `object or null`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `temperatura` | NumericValue | no | Mean air temperature over the hour, °C. |
| `intensidadeVento` | NumericValue | no | Wind speed, m/s. |
| `intensidadeVentoKM` | NumericValue | no | Wind speed, km/h. |
| `precAcumulada` | NumericValue | no | Accumulated precipitation during the hour, mm. |
| `humidade` | NumericValue | no | Hourly mean relative humidity, %. |
| `pressao` | NumericValue | no | Hourly mean sea-level pressure, hPa. |
| `radiacao` | NumericValue | no | Solar radiation, kJ/m². |
| `idDireccVento` | CodeValue | no | Source wind direction code; do not treat code as degrees. |

### ObservationsResponse

UTC observation timestamp → station-ID string → measurement object or null. Station records can be null. Timestamp keys usually omit seconds and timezone suffixes.

Shape: `map<string, map<string, StationObservation>>`.

### SeaForecast



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `latitude` | NumericValue | no | Latitude in WGS84 degrees. |
| `longitude` | NumericValue | no | Longitude in WGS84 degrees. |
| `globalIdLocal` | integer | yes | Coastal location identifier. |
| `predWaveDir` | string or null | no | Prevailing wave direction. |
| `wavePeriodMin` | NumericValue | no | Minimum daily swell peak period, s. |
| `wavePeriodMax` | NumericValue | no | Maximum daily swell peak period, s. |
| `waveHighMin` | NumericValue | no | Minimum daily swell height, m. |
| `waveHighMax` | NumericValue | no | Maximum daily swell height, m. |
| `totalSeaMin` | NumericValue | no | Minimum daily significant wave height, m. |
| `totalSeaMax` | NumericValue | no | Maximum daily significant wave height, m. |
| `sstMin` | NumericValue | no | Minimum daily sea-surface temperature, °C. |
| `sstMax` | NumericValue | no | Maximum daily sea-surface temperature, °C. |

### SeaForecastResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<SeaForecast> | yes |  |
| `forecastDate` | string | yes | Forecast civil date. |

### MunicipalFireRisk



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `latitude` | NumericValue | no | Latitude in WGS84 degrees. |
| `longitude` | NumericValue | no | Longitude in WGS84 degrees. |
| `dico` | string or null | no | Municipality DICO string; preserve leading zeroes. Live feed uses lowercase dico; the reference example uses uppercase DICO, which remains accepted and preserved as an additional field. |
| `data` | object | yes |  |

### FireRiskResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `dataPrev` | string | yes | Forecast civil date. |
| `dataRun` | string | yes | Model run civil date. |
| `fileDate` | string or null | no | Source update timestamp; observed space separator, UTC. |
| `local` | map<string, MunicipalFireRisk> | yes | Municipality DICO → risk record. Keys are strings with leading zeroes. |

### UvForecast



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `globalIdLocal` | integer | yes | Location identifier; zero is supplied for some unmapped locations. |
| `data` | string | yes | Forecast civil date. |
| `iUv` | NumericValue | no | UV index. |
| `idPeriodo` | CodeValue | no | Source-internal period code; meaning not inferred. |
| `intervaloHora` | string or null | no | Published peak-hour interval; may be empty. |

### SeismicEvent



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `lat` | NumericValue | no | Epicentre latitude in WGS84 degrees. |
| `lon` | NumericValue | no | Epicentre longitude in WGS84 degrees. |
| `magnitud` | NumericValue | no | Reported magnitude; -99 is nodata. |
| `depth` | NumericValue | no | Hypocentral depth, km. |
| `time` | string or null | yes | Event timestamp, UTC. |
| `dataUpdate` | string or null | no | Record update timestamp, UTC. |
| `magType` | string or null | no | Raw magnitude-type token. |
| `source` | string or null | no | Reporting source. |
| `obsRegion` | string or null | no | Source observation-region label. |
| `shakemapid` | string or null | no | Source ShakeMap ID. |
| `shakemapref` | string or null | no | Source ShakeMap reference. |
| `sismoId` | string or null | no | Source event identifier. |
| `googlemapref` | string or null | no | Source map reference. |
| `tensorRef` | string or null | no | Source tensor reference. |
| `local` | string or null or number | no | Locality token; preserved without coercion. |
| `degree` | string or null or number | no | Reported intensity token; may be numeric, text, or null. |
| `sensed` | boolean or null | no | Reported felt flag, if supplied. |

### SeismicResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<SeismicEvent> | yes |  |
| `idArea` | integer | no | Source region selector. |
| `updateDate` | string or null | no | Source catalogue update timestamp, UTC. |
| `lastSismicActivityDate` | string or null | no | Most recent reported activity timestamp, UTC. |

### Location



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `latitude` | NumericValue | no | Latitude in WGS84 degrees. |
| `longitude` | NumericValue | no | Longitude in WGS84 degrees. |
| `globalIdLocal` | integer | yes | Location identifier. |
| `local` | string | yes | Location name. |
| `idAreaAviso` | string or null | no | Warning-area identifier. |
| `idRegiao` | CodeValue | no | Region ID; currently 1 mainland, 2 Madeira, 3 Azores. |
| `idDistrito` | CodeValue | no | District/island ID. |
| `idConcelho` | CodeValue | no | Municipality component scoped by district; not a complete DICO. |
| `idLocal` | CodeValue | no | Coastal location code. |

### LocationsResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<Location> | yes |  |

### WeatherCode



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `idWeatherType` | CodeValue | yes | Source category code, including unfamiliar values and reference-table sentinels. |
| `descWeatherTypePT` | string or null | no | Portuguese description. |
| `descWeatherTypeEN` | string or null | no | English description. |

### WeatherCodeResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<WeatherCode> | yes |  |

### WindCode



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `classWindSpeed` | CodeValue | yes | Source category code, including unfamiliar values and reference-table sentinels. |
| `descClassWindSpeedPT` | string or null | no | Portuguese description. |
| `descClassWindSpeedEN` | string or null | no | English description. |
| `descClassWindSpeedDailyPT` | string or null | no | Portuguese description; field spelling in the live daily wind table. |
| `descClassWindSpeedDailyEN` | string or null | no | English description; field spelling in the live daily wind table. |

### WindCodeResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<WindCode> | yes |  |

### PrecipitationCode



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `classPrecInt` | CodeValue | yes | Source category code, including unfamiliar values and reference-table sentinels. |
| `descClassPrecIntPT` | string or null | no | Portuguese description. |
| `descClassPrecIntEN` | string or null | no | English description. |

### PrecipitationCodeResponse



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `owner` | string or null | no | Source attribution. |
| `country` | string or null | no | Source country code. |
| `dataUpdate` | string or null | no | Source update timestamp; UTC, often without a timezone suffix. |
| `data` | array<PrecipitationCode> | yes |  |

### Geometry



Shape: `object or null`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `type` | string | yes | GeoJSON geometry type. |
| `coordinates` | array<source JSON> | no |  |
| `geometries` | array<source JSON> | no |  |

### GeoFeature



Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `type` | string | yes | GeoJSON Feature. |
| `geometry` | Geometry | no |  |
| `properties` | map<string, source JSON> | no | Source station/bivalve properties, including nested values. No sentinel normalization. |
| `id` | string or number | no |  |

### GeoFeatureCollection

Source metadata, CRS and foreign members are preserved through additional properties. Coordinates are not reprojected.

Shape: `object`.

| Source field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `type` | string | yes | GeoJSON FeatureCollection. |
| `features` | array<GeoFeature> | yes |  |
