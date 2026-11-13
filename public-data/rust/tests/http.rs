#[path = "../../../tools/rust/test-support.rs"]
mod support;
use axum::http::StatusCode;
use ipma_public_data_client::{Client, http_client, types};
use serde_json::json;

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
    assert_eq!(server.seen.lock().unwrap().len(), 4);
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
        assert_eq!(server.seen.lock().unwrap().len(), 1);
    }
}
