# ipma-public-data-client

Progenitor 0.16.0 generated HTTP client for IPMA `/public-data/` feeds.

The language-neutral [specification](../openapi.yaml), [reference](../reference.md)
and [fixtures](../fixtures/manifest.json) belong to the parent API directory.
This directory is one independent Rust crate, with its own manifest, lockfile,
toolchain, examples, tests and Just recipes; there is no root Cargo workspace.

Run `rtk just verify` here, or `rtk just public-data-rust verify` from the repository
root. Regenerate from the root with `rtk just generate`; do not edit
`src/generated.rs` manually. Generation tooling lives in `tools/rust/`.

Cargo discovers this package by name in a full Git checkout, without a root
Cargo.toml. Pin a full Git revision and commit the consuming project's lockfile:

```toml
[dependencies]
ipma-public-data-client = { git = "https://github.com/Zizico2/ipma-openapi.git", rev = "<full commit SHA>" }
```

See the [root README](../../README.md) for transport behavior, source-value
preservation limits and evidence. Compilation makes no IPMA requests.
