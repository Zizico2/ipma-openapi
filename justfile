default:
    @just --list

# Rewrite generated code and readable references after reviewing a spec change.
generate:
    cargo run --locked -p ipma-codegen
    uv run --locked python tools/reference.py

# Offline verification; never fetches new IPMA responses.
verify:
    cargo run --locked -p ipma-codegen -- --check
    uv run --locked python tools/reference.py --check
    uv run --locked python tools/contracts.py validate
    uv run --locked python -m unittest discover -s tools -p 'test_*.py'
    uv run --locked ruff check tools
    uv run --locked ruff format --check tools
    cargo fmt --all --check
    cargo clippy --locked --workspace --all-targets -- -D warnings
    cargo test --locked --workspace --all-targets
    cargo test --locked --workspace --doc

# Live network probe: saves a separate report and never rewrites approved fixtures.
probe:
    uv run --locked python tools/contracts.py probe
