#![allow(dead_code)]
use axum::{
    Router,
    extract::State,
    http::{StatusCode, Uri},
    response::IntoResponse,
};
use serde_json::Value;
use std::{
    collections::HashMap,
    path::Path,
    sync::{Arc, Mutex},
};

#[derive(Clone)]
struct Feed {
    responses: Arc<HashMap<String, (String, Vec<u8>)>>,
    seen: Arc<Mutex<Vec<String>>>,
    status: StatusCode,
}
pub struct Server {
    pub base: String,
    pub seen: Arc<Mutex<Vec<String>>>,
    task: tokio::task::JoinHandle<()>,
}
impl Drop for Server {
    fn drop(&mut self) {
        self.task.abort();
    }
}

async fn handler(State(feed): State<Feed>, uri: Uri) -> impl IntoResponse {
    feed.seen.lock().unwrap().push(uri.path().to_owned());
    if feed.status != StatusCode::OK {
        return (
            feed.status,
            [("content-type", "text/html".to_owned())],
            b"<html>upstream error</html>".to_vec(),
        );
    }
    let (content_type, body) = feed
        .responses
        .get(uri.path())
        .unwrap_or_else(|| panic!("unexpected upstream path: {uri}"));
    (
        StatusCode::OK,
        [("content-type", content_type.clone())],
        body.clone(),
    )
}
pub async fn server(api: &str, status: StatusCode) -> Server {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../fixtures");
    let manifest: Value =
        serde_json::from_slice(&std::fs::read(root.join("manifest.json")).unwrap()).unwrap();
    let mut responses = HashMap::new();
    for record in manifest["records"]
        .as_array()
        .unwrap()
        .iter()
        .filter(|r| r["api"] == api)
    {
        let path = reqwest::Url::parse(record["url"].as_str().unwrap())
            .unwrap()
            .path()
            .to_owned();
        responses.insert(
            path,
            (
                record["content_type"].as_str().unwrap().to_owned(),
                std::fs::read(root.join(record["file"].as_str().unwrap())).unwrap(),
            ),
        );
    }
    let seen = Arc::new(Mutex::new(Vec::new()));
    let app = Router::new().fallback(handler).with_state(Feed {
        responses: Arc::new(responses),
        seen: seen.clone(),
        status,
    });
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let base = format!("http://{}/{api}", listener.local_addr().unwrap());
    let task = tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });
    Server { base, seen, task }
}
