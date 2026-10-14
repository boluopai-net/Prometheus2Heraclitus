---
name: clash-auto-switch
description: "节点自动切换：维护 Clash 节点选择、地区回退与 DNS/TUN 保护。 Maintain explicitly configured one-shot node switching, reversible macOS mode/DNS transitions, and a bounded DNS-only TUN guard in Clash Verge Rev; watching nodes is a separate authorized operation."
user-invocable: false
---

# Clash Auto Switch

Deliberate node/mode choice and bounded DNS-cache recovery have different authority. Before a model-initiated Clash change, read [Network's authorization boundary](../network/SKILL.md). A network incident can authorize repair; an unrelated download failure does not authorize mode/DNS/TUN changes. Scripts do not grant permission.

## Recipient and actual implementation

Download this entire package plus [Network](../network/README.md). Python 3.12+, macOS system utilities and Clash Verge Rev/Mihomo are required; controller bridge/relay also needs recipient-installed socat. No subscription, global Script/Merge policy, account, embedded controller credential or personal default selector is included.

[scripts/clash-tool](scripts/clash-tool) configures the actual eight source-derived implementations using [config.example.json](config.example.json). Every runtime/state/log/interpreter/mutex/privileged destination and group list is recipient selected. Required fields remain explicit even when a particular inspection uses only some. check-config validates configuration without reading live state or making requests.

Controller discovery prefers a validated Unix socket belonging to the configured target Home owner. Explicit endpoints remain authoritative; configured TCP/secret is a fallback. Secrets are read at runtime from the recipient's app-owned config or environment, never copied into the public JSON. A root guard selects the configured user rather than root's socket.

Node failure first tries the same region, then declared fallback regions/exclusions and group constraints. Preserve the original TUN-aware probes, bounded concurrency, region health and cross-subscription candidate method. Use explicit --once for one cycle and --dry-run for inspection. Watching nodes is a separate authorized operation, not an installation default. Direct-group enforcement is optional and uses only recipient-declared direct_groups. Mode changes require coherent recovery, not a node scan's opportunistic TUN toggle.

## Mode and DNS transaction

mode tun|system|sys|status retains the original coupled transition: persisted Verge preferences, primary physical-service proxies/DNS, active controller TUN and guard intent. For TUN, verify configured fake-IP/utun route and resolver before changing only the service backing the physical default route. Snapshot its exact prior DNS, not a guessed DHCP setting. For system mode, restore that snapshot before disabling TUN and remove it only after convergence. Missing recovery for managed DNS fails closed.

Capture immediate DNS/proxies, original recovery snapshot, Verge preferences, guard intent and controller state before transition. Failure restores captured state in dependency order; incomplete recovery retains its checkpoint. Preserve subscription/profile identity and selectors. Never rewrite subscription payloads or global Script/Merge to perform a mode transition. Mutating node/mode entrypoints require a real configured shared mutex; Network includes the compatible executable.

## Guard and privileged service

guard check|run|status|self-test [--json] preserves the original DNS-only reflex. It observes effective generated DNS, controller TUN/auto-route/gVisor/hijack, actual fake-IP route and configured HTTPS transport. Invalid fake IP is dns_stalled; a valid fake IP routed outside utun is a non-mutating tun_down fault. Any HTTP response establishes transport, not authenticated application usability.

Only dns_stalled or transport stall confirmed across two cycles at least 15 seconds apart permits dscacheutil -flushcache and killall -HUP mDNSResponder. Success clears the incident, so persistent trouble must reconfirm. The guard never restarts Clash, reloads subscriptions/config, changes nodes/profiles/system proxies or disables TUN. State, structured events and output belong to configured runtime directories. Notifications are disabled in this public entrypoint.

setup preview|enable|disable|status controls only the recipient-named system LaunchDaemon. Preview is default; no service is installed by downloading. The installer copies actual guard/controller/config/entrypoint resources to root-owned destinations and refuses symlinks or non-root/group/world-writable privileged ancestors, including the configured Python executable. It uses sudo -n, RunAtLoad, StartInterval=15 and KeepAlive=false. User intent remains in the separate configured mode-state directory. It never removes guessed legacy services.

Set desired_mode to the recipient's actual intended mode; existing mode-state overrides that initial configuration. Root service state/logs stay private. Inspect installed guard status through the root-owned Python/entrypoint/config with sudo -n when permissions require it, rather than weakening ownership or treating an unreadable state as fresh health. setup status observes registration; it does not establish guard recovery.

Copying this method does not install Clash, socat, administrator authority, a root-owned modern Python runtime or a shared publication owner. Missing dependencies are real bootstrap boundaries. Do not weaken privileged ownership checks to make installation pass. [Chezmoi](../chezmoi/README.md) can persist resources through the recipient's verified owner.

## Evidence and completion

Use help/check-config, self-test and disposable controller/DNS fixtures for candidate validation. Self-test mocks DNS resets and local controller/HTTP responses; it is not live recovery evidence. setup preview does not prove service registration. Live acceptance requires installed command, launchctl/runtime state where relevant, exact service DNS/proxy restoration, active core route/TUN and an affected request, with preservation/recovery checks appropriate to the change.
