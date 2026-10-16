# Public Site maintenance

For publication, read [README.md's publication route](README.md#publication-and-interrupted-transfers)
before selecting native Sites operations. That section owns this Site's Git-first
route, archive fallback, credential handling and interrupted-operation recovery.

This repository owns independent Site source. The public collection's `website/`
directory is generated from an exact committed revision with its
`scripts/sync-website.py`; maintain the source here and refresh that snapshot
through its owner. Preserve the existing Site identity, audience and bindings.
