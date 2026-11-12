use ipma_public_data_client::{BASE_URL, Client, http_client};
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = Client::new_with_client(BASE_URL, http_client()?);
    let locations = client.get_locations().await?.into_inner();
    let forecasts = client.get_forecast(1110600.try_into()?).await?.into_inner();
    println!(
        "{} website locations, {} mixed-period forecast rows for Lisbon",
        locations.len(),
        forecasts.len()
    );
    Ok(())
}
