#[path = "../../../tools/rust/test-support.rs"]
mod support;
use axum::http::StatusCode;
use futures_util::StreamExt;
use ipma_open_data_client::{ByteStream, Client, ResponseValue, http_client, types};
use serde_json::json;

async fn bytes(response: ResponseValue<ByteStream>) -> Vec<u8> {
    let mut stream = response.into_inner_stream();
    let mut bytes = Vec::new();
    while let Some(chunk) = stream.next().await {
        bytes.extend(chunk.unwrap());
    }
    bytes
}
#[tokio::test]
async fn generated_client_calls_all_twenty_documented_data_paths() {
    let server = support::server("open-data", StatusCode::OK).await;
    let client = Client::new_with_client(&server.base, http_client().unwrap());
    let daily = client
        .get_city_daily_forecast(1110600.try_into().unwrap())
        .await
        .unwrap()
        .into_inner();
    assert!(!daily.data.is_empty());
    assert!(
        serde_json::to_value(&daily.data[0].t_max)
            .unwrap()
            .is_string()
    );
    client.get_daily_forecasts(0).await.unwrap();
    client.get_warnings().await.unwrap();
    client.get_observations().await.unwrap();
    client.get_sea_forecasts(0).await.unwrap();
    let fire = client.get_fire_risk(0).await.unwrap().into_inner();
    assert!(fire.local.keys().any(|key| key.starts_with('0')));
    client.get_uv_forecasts().await.unwrap();
    client
        .get_seismic_events(&7.try_into().unwrap())
        .await
        .unwrap();
    client.get_locations().await.unwrap();
    client.get_sea_locations().await.unwrap();
    client.get_weather_codes().await.unwrap();
    client.get_wind_codes().await.unwrap();
    client.get_precipitation_codes().await.unwrap();
    let recent: types::GeoFeatureCollection = serde_json::from_slice(
        &bytes(client.get_recent_observations_geojson().await.unwrap()).await,
    )
    .unwrap();
    assert!(!recent.features.is_empty());
    client.get_stations().await.unwrap();
    let zones: types::GeoFeatureCollection =
        serde_json::from_slice(&bytes(client.get_bivalve_zones().await.unwrap()).await).unwrap();
    assert!(!zones.features.is_empty());
    for response in [
        client.get_climate_evapotranspiration().await.unwrap(),
        client.get_climate_precipitation().await.unwrap(),
        client.get_climate_temperature().await.unwrap(),
    ] {
        let csv = bytes(response).await;
        assert!(
            std::str::from_utf8(&csv)
                .unwrap()
                .lines()
                .next()
                .unwrap()
                .contains("zid")
        );
    }
    let zip = bytes(client.get_weather_icons().await.unwrap()).await;
    assert_eq!(&zip[..4], b"PK\x03\x04");
    assert_eq!(server.seen.lock().unwrap().len(), 20);
}
#[test]
fn dynamic_observation_maps_and_reference_spelling_remain_source_shaped() {
    let raw = json!({"2026-11-12T10:00":{"1200535":null,"1200536":{"temperatura":"-99","humidade":0,"future":true}}});
    let parsed: types::ObservationsResponse = serde_json::from_value(raw.clone()).unwrap();
    let encoded = serde_json::to_value(parsed).unwrap();
    assert!(encoded["2026-11-12T10:00"]["1200535"].is_null());
    assert_eq!(
        encoded["2026-11-12T10:00"]["1200536"]["humidade"].as_f64(),
        Some(0.0)
    );
    assert_eq!(encoded["2026-11-12T10:00"]["1200536"]["temperatura"], "-99");
    assert_eq!(encoded["2026-11-12T10:00"]["1200536"]["future"], true);
    let fire: types::MunicipalFireRisk =
        serde_json::from_value(json!({"DICO":"0101","data":{"rcm":999}})).unwrap();
    let raw = serde_json::to_value(fire).unwrap();
    assert_eq!(raw["DICO"], "0101");
    assert_eq!(raw["data"]["rcm"], 999);
}
#[tokio::test]
async fn unstructured_http_error_status_is_exposed() {
    let server = support::server("open-data", StatusCode::SERVICE_UNAVAILABLE).await;
    let client = Client::new_with_client(&server.base, http_client().unwrap());
    assert_eq!(
        client.get_locations().await.unwrap_err().status(),
        Some(StatusCode::SERVICE_UNAVAILABLE)
    );
}
