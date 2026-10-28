---
name: obsidian-sync
description: "<用户自制> 笔记同步：维护 Obsidian 多库共享配置、云端配置复制与反向同步。 Validate or maintain explicitly configured shared vault settings on macOS through File Provider-safe copies, local symlinks, and guarded reverse sync. Excludes vault note-data transport."
user-invocable: false
---

# obsidian-sync

Give several vaults common working tools while leaving their notes and compositions with their owners. This package owns only ten configuration items: plugins, themes, snippets, appearance.json, hotkeys.json, app.json, community-plugins.json, core-plugins.json under .obsidian, plus .obsidian.vimrc and .gdriveignore. It never owns notes, vault-root templates/scripts, workspace.json, or application-loaded plugin state.

## Authority and carriers

The recipient's shared configuration is the runtime authority. An explicitly selected seed supplies missing reconstructible inputs without overwriting existing authority. File Provider cloud vaults need real files/directories because symlinks can become text containing their former target. Local vaults link to that same authority. Reverse sync admits new/newer regular files from cloud copies and eligible newer nonempty files; it never infers deletion intent or follows nested symlinks. Empty/default shells and drastic file shrinkage are rejected.

Retain collision-proof backup siblings before replacing wrong types, serialized symlinks, or differing files during a source-authoritative repair. Never recursively delete recovery artifacts. An exclusive process lock protects every mutating execution, including seeding. Lock contention exits 2 before mutation. Timestamp-only drift, .DS_Store and Icon carriage-return metadata remain outside the content contract.

## Recipient configuration and execution

Download this complete directory. Requirements: macOS, Python 3.12+ (Path.exists follow_symlinks is used), and Git for repository vault preflight. No other Skill is required to execute these resources. Chezmoi is a useful companion only when the recipient wants durable installation; its publication-owner boundary remains applicable.

Copy [config.example.json](config.example.json) to recipient-owned configuration and replace every path. Declare exact cloud_vaults and local_vaults, shared authority, seed, lock, watcher state and installed wrapper. No vault/account discovery or private defaults occur. The shared authority and targets must not contain one another; groups must not overlap. Missing configured vaults cause refusal before writes.

Use [scripts/obsidian-sync](scripts/obsidian-sync) as the public entrypoint:

```sh
scripts/obsidian-sync --help
scripts/obsidian-sync --config /absolute/recipient/config.json --print-config
scripts/obsidian-sync --config /absolute/recipient/config.json --check
scripts/obsidian-sync --config /absolute/recipient/config.json --bootstrap-shared-config --dry-run
scripts/obsidian-sync --config /absolute/recipient/config.json --dry-run
```

Seed root must contain .obsidian with all managed directories/files, .obsidian.vimrc and .gdriveignore. Empty themes is valid. Review the preview and actual task authorization before removing --dry-run. Use --disable-reverse-sync for source-authoritative repair. The Git preflight refuses tracked managed paths in configured local repository vaults; migration must untrack/ignore them through that repository's owner before linking. Never bypass it.

## Watch and registration

The same JSON controls sync and watch, so observed targets and executed targets agree. Watch only the ten managed roots in the shared authority and declared vaults. kqueue vnode events coalesce after 0.75 seconds; SHA-256 content fingerprints ignore metadata-only churn. Failed/timed-out sync is retried without marking convergence. The watcher raises its file-descriptor soft limit to at least 1024 where possible.

```sh
scripts/obsidian-sync --watch --help
scripts/obsidian-sync --watch --config /absolute/recipient/config.json --once
```

--once can synchronize and write watcher state; it is not a dry run. For login registration use [scripts/setup_obsidian_sync_watch_launchd.sh](scripts/setup_obsidian_sync_watch_launchd.sh). Explicit environment LABEL, PROGRAM, CONFIG, PLIST_DIR and STATE_ROOT selects recipient carriers. Default registration mode previews; --apply, --verify and --unload act only on that named job. Preview and verify are different evidence from a loaded watcher.

Converged files may require a vault/plugin reload before Obsidian consumes externally changed plugin settings. Diagnose a plugin's configured backend separately rather than changing symlinks to cure an unavailable service.

## Completion evidence

Report exact configured authority, seed, vault count and representation groups; help/dry-run/real-run scope; lock/preflight refusals, backup paths and reverse-sync results; then validate the installed wrapper and actual configured files. For source changes use disposable vault fixtures rather than live HOME/cloud. Application consumption is a further readback boundary.
