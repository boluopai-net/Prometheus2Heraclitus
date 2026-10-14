# Profile and global override recovery

Use the configured public entrypoint:

```sh
scripts/network-repair --help
scripts/network-repair --config /absolute/recipient/repair.json --check-config status
scripts/network-repair --config /absolute/recipient/repair.json --files-only status
```

Offline status does not establish running app/core/transport health. Normal status observes those boundaries and makes the configured HTTPS transport request.

| Action | Effect |
| --- | --- |
| status | Redacted index/global/app/TUN/core/transport/backup summary |
| backup | Save a complete healthy current profile set privately |
| repair | Empty valid index: newest healthy snapshot; existing subscriptions: missing/default globals only |
| restore-globals | Restore recipient's explicitly configured known-good global baseline, preserving subscriptions |
| restore-profiles ID | Restore selected complete snapshot only if current subscriptions are absent and index valid |
| rollback ID | Restore saved pre-repair files/index; may reinstate the earlier subscription set |
| flush-dns | Noninteractive sudo resolver-cache reset; preserve profiles/TUN/selectors |

Recovery backs up before app shutdown, verifies files did not race during shutdown, writes atomically, reopens the configured app in the background, and reports exact rollback identity. Failed writes attempt immediate restoration; failures retain recovery. It never removes unrelated/unreferenced profile files. Backups are outside app data, created with restrictive permissions. Never publish these snapshots, subscription payloads or controller credentials.

The helper's global reset heuristics identify empty/template files; they are evidence to assess against the recipient baseline, not proof of unintended loss. A deliberately empty baseline can be valid. Never restore the original author's personal global routing. Preserve newer subscriptions; an index without its referenced files is not a complete backup.

The original upstream failure class involved startup cleanup and global template resets. See [report #7577](https://github.com/clash-verge-rev/clash-verge-rev/issues/7577), [file loss report #7804](https://github.com/clash-verge-rev/clash-verge-rev/issues/7804), and [cleanup removal](https://github.com/clash-verge-rev/clash-verge-rev/commit/44f6f6e). These are historical locators, not a claim about the recipient's installed version; verify current upstream and installed code before recommending prevention.

If no healthy snapshot exists, reimport the recipient's subscription through authorized app controls, then restore that recipient's globals. Missing subscription access is an actual bootstrap boundary. A manual equivalent must preserve app data, restore a coherent index plus referenced files or reimport, reopen the app, then verify nodes, TUN, routing and a real affected request.

A files_restored result establishes bytes only. Inspect returned runtime and the actual affected application. The configured controller command must accept request GET /configs and /rules; use Clash Auto Switch's configured wrapper described in its README. The helper's app executable is Clash Verge Rev's clash-verge; a different product requires a deliberate adapter rather than changing the name alone.

Set controller_config in the recovery JSON to the companion's recipient configuration. Recovery supplies it as CLASH_SKILL_CONFIG to the bundled clash-controller wrapper; no undocumented shell profile is needed. A recipient's existing compatible controller executable may ignore that environment field.
