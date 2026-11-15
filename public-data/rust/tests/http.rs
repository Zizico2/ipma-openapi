#[path = "../../../tools/rust/test-support.rs"]
mod support;
use axum::http::StatusCode;
use futures_util::StreamExt;
use ipma_public_data_client::{ByteStream, Client, ResponseValue, http_client, types};
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
async fn generated_client_calls_all_website_paths_and_decodes_captured_data() {
    let server = support::server("public-data", StatusCode::OK).await;
    let client = Client::new_with_client(&server.base, http_client().unwrap());
    let forecast = client
        .get_forecast(1110600.try_into().unwrap())
        .await
        .unwrap()
        .into_inner();
    assert!(
        forecast
            .iter()
            .any(|r| serde_json::to_value(&r.id_periodo).unwrap() == 1)
    );
    assert!(
        forecast
            .iter()
            .any(|r| serde_json::to_value(&r.id_periodo).unwrap() == 24)
    );
    assert!(!client.get_locations().await.unwrap().is_empty());
    assert!(!client.get_districts().await.unwrap().is_empty());
    client.get_warnings().await.unwrap();

    let station = client
        .get_daily_station_observations(
            2026,
            &"10".parse().unwrap(),
            10.try_into().unwrap(),
            1200545.try_into().unwrap(),
        )
        .await
        .unwrap()
        .into_inner();
    assert_eq!(station.station_id, "1200545");
    assert!(station.data[0].datetime.starts_with("2026-10-01"));

    let fire = client
        .get_fire_danger_map(
            types::GetFireDangerMapFireLayer::LsasafFwiContinent,
            &"2026-11-15".parse().unwrap(),
        )
        .await
        .unwrap();
    assert!(bytes(fire).await.starts_with(b"\x89PNG\r\n\x1a\n"));
    let model = client
        .get_model_map(
            types::GetModelMapModelLayer::EcmwfPcpAtlantic,
            &"2026-11-15T19_00_00".parse().unwrap(),
        )
        .await
        .unwrap();
    assert!(bytes(model).await.starts_with(b"\x89PNG\r\n\x1a\n"));

    let wind = client
        .get_model_wind_field(&"2026-11-15T19_00_00".parse().unwrap())
        .await
        .unwrap()
        .into_inner();
    assert_eq!(wind.len(), 2);
    assert_eq!(
        serde_json::to_value(&wind[0].header).unwrap(),
        serde_json::to_value(&wind[1].header).unwrap()
    );
    assert_eq!(wind[0].data.len(), wind[0].header.nx.get() as usize);
    assert_eq!(server.seen.lock().unwrap().len(), 8);
}

#[test]
fn rolling_frame_names_reject_unpublished_formats() {
    assert!(
        "2026-11-15T19_30_00"
            .parse::<types::GetModelMapTime>()
            .is_err()
    );
    assert!(
        "2026-11-15T19:00:00"
            .parse::<types::GetModelMapTime>()
            .is_err()
    );
    assert!("2026-11-15".parse::<types::GetFireDangerMapDate>().is_ok());
    assert!(
        "3".parse::<types::GetDailyStationObservationsMonthDir>()
            .is_err()
    );
}

#[test]
fn source_types_preserve_numeric_variants_sentinels_and_unknown_fields() {
    let raw = json!({"globalIdLocal":1110600,"dataPrev":"2026-11-12T10:00:00","idPeriodo":7,"idTipoTempo":777,"tMed":"-2.5","hR":0,"tMin":"-99.0","tMax":null,"utci":"","future":{"x":true}});
    let row: types::Forecast = serde_json::from_value(raw.clone()).unwrap();
    let value = serde_json::to_value(row).unwrap();
    for key in [
        "globalIdLocal",
        "dataPrev",
        "idPeriodo",
        "idTipoTempo",
        "tMed",
        "tMin",
        "utci",
        "future",
    ] {
        assert_eq!(value[key], raw[key], "changed source field {key}");
    }
    assert_eq!(value["hR"].as_f64(), Some(0.0));
    // Optional source nulls deserialize successfully; generated Option fields
    // do not preserve the distinction between explicit null and omission.
    assert!(
        serde_json::from_value::<types::Forecast>(
            json!({"globalIdLocal":1110600,"dataPrev":"2026-11-12T10:00:00","tMed":null})
        )
        .unwrap()
        .t_med
        .is_none()
    );
    assert!(
        serde_json::from_value::<types::Forecast>(
            json!({"globalIdLocal":1110600,"dataPrev":"2026-11-12T10:00:00","tMed":"rain"})
        )
        .is_err()
    );
}

#[test]
fn unobserved_station_days_keep_null_measurements() {
    let row: types::DailyStationObservation = serde_json::from_value(json!({
        "datetime":"2026-11-30T00:00:00.000Z","Tar_med":null,"RRR_qt":null,"future":1
    }))
    .unwrap();
    assert!(row.tar_med.is_none() && row.rrr_qt.is_none());
    assert_eq!(serde_json::to_value(row).unwrap()["future"], 1);
}

#[tokio::test]
async fn html_errors_and_redirects_do_not_require_a_json_error_schema() {
    for status in [
        StatusCode::NOT_FOUND,
        StatusCode::TOO_MANY_REQUESTS,
        StatusCode::INTERNAL_SERVER_ERROR,
        StatusCode::FOUND,
    ] {
        let server = support::server("public-data", status).await;
        let client = Client::new_with_client(&server.base, http_client().unwrap());
        let error = client.get_locations().await.unwrap_err();
        assert_eq!(error.status(), Some(status));
        let Err(error) = client
            .get_model_map(
                types::GetModelMapModelLayer::Ecmwf2tAtlantic,
                &"2026-11-15T19_00_00".parse().unwrap(),
            )
            .await
        else {
            panic!("missing frame {status} decoded as an image");
        };
        assert_eq!(error.status(), Some(status));
        assert_eq!(server.seen.lock().unwrap().len(), 2);
    }
}
