# Provenance schema compatibility

The active provenance record keeps the original schema keys used by the
repository's synchronization audit while also exposing the clearer
`tracked_upstreams`, `active_lineage`, and `project_native_paths` fields used by
the unified compiler. The aliases carry identical commit and path data; they do
not represent additional upstream dependencies.
