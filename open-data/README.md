# IPMA open-data

This directory owns the language-neutral [OpenAPI contract](openapi.yaml),
[readable reference](reference.md) and captured [fixtures](fixtures/manifest.json)
for IPMA `/open-data/` feeds.

The [Rust client](rust/) is generated with Progenitor. Each language owns its
package manifests, lockfiles, toolchain and recipes in its own directory.
Future bindings belong in sibling directories such as `typescript/` or `go/`,
reading the same `openapi.yaml` and fixtures.

Generation and validation orchestration is documented in the [repository README](../README.md).
