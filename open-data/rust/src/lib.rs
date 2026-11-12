//! Generated upstream HTTP client; source JSON is not normalized into gRPC types.
#[allow(clippy::all, clippy::pedantic)]
#[rustfmt::skip]
mod generated;
pub use generated::*;

/// Upstream base URL. Include this directory prefix when using a custom origin.
pub const BASE_URL: &str = "https://api.ipma.pt/open-data";

/// TLS-verified HTTP transport with a 15s timeout and redirects/retries disabled.
/// Generated JSON decoding buffers responses; this helper does not impose a body cap.
pub fn http_client() -> Result<reqwest::Client, reqwest::Error> {
    reqwest::Client::builder()
        .user_agent(concat!(
            env!("CARGO_PKG_NAME"),
            "/",
            env!("CARGO_PKG_VERSION")
        ))
        .timeout(std::time::Duration::from_secs(15))
        .connect_timeout(std::time::Duration::from_secs(5))
        .redirect(reqwest::redirect::Policy::none())
        .retry(reqwest::retry::never())
        .gzip(true)
        .build()
}

/// Generated operations returning the original decompressed response stream.
/// Use with an injected HTTP client to enforce caller-owned transport policy,
/// and drain the stream with a byte cap before parsing untrusted source data.
#[allow(clippy::all, clippy::pedantic)]
#[rustfmt::skip]
pub mod raw;
