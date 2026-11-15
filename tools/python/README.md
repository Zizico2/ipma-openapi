# Contract maintenance tooling

Python dependencies, lockfile, interpreter pin and Just recipes live here.
The scripts discover the repository root from their own location, so their
working directory does not change spec, fixture or output lookup.

- `rtk just generate`: regenerate each API's readable reference.
- `rtk just verify`: validate both specs and API-local fixture manifests; run
  drift/capture tests and Python lint/format checks.
- `rtk just probe`: capture and compare live responses under root `.artifacts/`.

From the repository root, `rtk just capture .artifacts/review-candidate` writes
an aggregate review report plus separate `open-data/fixtures/` and
`public-data/fixtures/` candidate folders, including their local manifests.
Neither capture nor probe rewrites approved fixtures or OpenAPI documents.
Path parameters use their spec `example`, except those with
`x-probe-current-utc`, which format the capture's current UTC time with that
strftime pattern because rolling feeds expire old files.
