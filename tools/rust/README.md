# Rust generation tooling

This independent Rust package pins Progenitor and regenerates both API clients:
`open-data/rust/src/generated.rs` and `public-data/rust/src/generated.rs`.
Its manifest, lockfile and toolchain live here rather than at the repository root.
`test-support.rs` is shared only by the Rust clients' HTTP tests.

Run `rtk just generate` here to regenerate Rust, or `rtk just verify` to check
staleness and this generator package. The root `rtk just generate` also updates
readable references, and root `rtk just verify` checks all APIs and languages.
