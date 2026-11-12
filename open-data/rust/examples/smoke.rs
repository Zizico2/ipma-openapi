use ipma_open_data_client::{BASE_URL, Client, http_client};
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = Client::new_with_client(BASE_URL, http_client()?);
    let locations = client.get_locations().await?.into_inner();
    let forecasts = client
        .get_city_daily_forecast(1110600.try_into()?)
        .await?
        .into_inner();
    println!(
        "{} locations, {} daily forecasts for Lisbon",
        locations.data.len(),
        forecasts.data.len()
    );
    Ok(())
}
