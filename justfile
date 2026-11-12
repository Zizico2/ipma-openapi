set positional-arguments

default:
    @just --list

# API/language directories own manifests, toolchains and language recipes.
open-data-rust *args:
    just --justfile open-data/rust/justfile "$@"

public-data-rust *args:
    just --justfile public-data/rust/justfile "$@"

generate:
    just --justfile tools/rust/justfile generate
    just --justfile tools/python/justfile generate

verify:
    just --justfile tools/python/justfile verify
    just --justfile tools/rust/justfile verify
    just --justfile open-data/rust/justfile verify
    just --justfile public-data/rust/justfile verify

probe:
    just --justfile tools/python/justfile probe

# Use a repository-relative path for a review candidate directory.
capture output:
    just --justfile tools/python/justfile capture "{{justfile_directory()}}/$1"
