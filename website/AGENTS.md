# Public Site maintenance

For publication, read [README.md's publication route](README.md#publication-and-interrupted-transfers)
first to select content or runtime publication. Native Git-first publication,
archive fallback, credential handling and deployment recovery apply to runtime
changes only. Ordinary content updates follow [content releases](README.md#content-releases-without-runtime-deployment):
render and commit the complete projection, export the exact source revision,
then delta publish and verify the consumer without a runtime build/deploy.
The same section owns the public bucket namespace, separate publisher authority,
snapshot resource pinning, CAS promotion and irreversible bootstrap retirement.

This repository owns independent Site source. The public collection's `website/`
directory is generated from an exact committed revision with its
`scripts/sync-website.py`; maintain the source here and refresh that snapshot
through its owner. Preserve the existing Site identity, audience and bindings.
