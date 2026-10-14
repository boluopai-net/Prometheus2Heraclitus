---
name: network
description: "Diagnose and repair macOS DNS, proxy, Clash, endpoint and IP-quality failures through their actual owners, with bounded profile recovery and explicit recipient configuration."
user-invocable: false
---

# Network

Restore the affected request by locating where its connected path fails: hostname resolution, routing/TUN interception, proxy rules and selected exit, transport, or service response. Persisted profiles, generated configuration, active core and physical service settings are distinct evidence.

## Authorization and continuity

A network-repair request authorizes necessary diagnosis, coherent in-scope repair, durable source convergence and verification. An unrelated browsing/download obstacle does not authorize a Clash/configuration/DNS/TUN/routing change: obtain approval for that concrete change unless prior applicable authorization exists. Advice-only or diagnostic scope remains so. Executable access is not authorization.

Use available local execution; a cloud conversation/container does not prove Mac reachability. Read back uncertain outcomes before repeating mutations. Before a potentially connection-breaking action, preserve prior state and make application/recovery locally complete without depending on the next remote model message. Report expected interruption. Retain any unfinished process identity across transport failures. Noninteractive sudo must fail visibly rather than store credentials or launch an unrequested authentication flow.

## Diagnose the real path

Compare affected-domain system DNS with Mihomo resolution and actual routes; compare normal and explicit-proxy requests where useful. Preserve hostname/SNI when probing returned IPs. Sample addresses or repeat intermittent failures; one success does not prove stability or the earlier cause.

A physical-interface resolver can escape TUN interception despite dns-hijack configuration. Before binding service DNS to a TUN resolver, verify route/response and preserve that exact service's prior DNS for restoration. DNS/exit mismatch calls for domain-specific resolution/route evidence, not a reset of every service. Profile loss calls for [profile recovery](references/profile-recovery.md), not a DNS workaround.

## Owners and downloadable companions

Download this complete package and [Clash Auto Switch](../clash-auto-switch/README.md) when using controller, node/mode switching or DNS/TUN guard methods. That companion owns controller discovery, same-region/fallback selection, reversible primary-service DNS transitions and bounded DNS-cache guard recovery. Its authorization boundary is this section, including direct entry during other tasks.

Included [scripts/proxy_purity.py](scripts/proxy_purity.py) requires Python 3.12+ and PyYAML. selectors/nodes read a configured live controller. profile-scan runs isolated Mihomo in a recipient's existing Colima VM; it can download an executable, copy selected subscription data into private scan output/VM files, make external exit-IP/reputation requests and switch only the isolated selector. It does not switch the live core. Configure explicit runtime/profile/output/VM paths using [proxy-purity.config.example.json](proxy-purity.config.example.json); use check-config first. Colima, curl, gunzip and a compatible VM architecture/network are genuine external dependencies, not installed by copying this Skill. Reputation is provider evidence, not a guarantee about an IP.

colima_profile selects the recipient's existing named VM for every Colima command; no VM is created or guessed. Binary bootstrap selects a Linux ARM64 Mihomo release; other VM architectures require a compatible preinstalled Mihomo/Clash binary. Output and VM configuration are private runtime data; never commit them or upload them with this package.

controller_url explicitly supplies this scanner's HTTP(S) target; a configured app runtime controller can override it when read from the recipient-selected config file. For Unix-controller inspection use the companion's controller tool. No controller secret belongs in these public JSON templates.

Included [scripts/network_repair.py](scripts/network_repair.py) is the actual recovery helper, not a command stub. Python/PyYAML, Clash Verge Rev, a configured controller executable, recipient baseline and healthy snapshots are its execution dependencies. [repair.config.example.json](repair.config.example.json) declares every destination, probe and mutex. Provide your own known-good Script.js/Merge.yaml; none is distributed here. Files-only status/check-config can inspect fixtures without app/controller/network access.

Every mutation requires a real configured mutex executable and exact shared lock path. The included [scripts/macos-home-mutex](scripts/macos-home-mutex) implements descriptor-inherited flock serialization and requires MACOS_HOME_MUTEX_PATH; install it at the configured mutex_command with executable mode. Recovery checks the inherited descriptor's file identity before accepting it. Other live writers must use the same mutex path. A missing executable fails closed.

## Apply and verify

Preserve TUN, subscriptions, profile identity/selectors, unrelated services and credentials unless their change is the supported remedy. Do not hand-edit generated final configuration as the durable fix. For durable installation/capture, [Chezmoi](../chezmoi/README.md) is optional; use the recipient's actual publication/runtime owner and shared serialization.

Complete with an affected-service request plus intended DNS/route/TUN/core readback and relevant preservation checks. HTTP 401/403/405 may establish transport while leaving service usability unproven. Report repair, verified effects, uncertainty, recovery ID and actual durable convergence. Do not add recurring monitoring without a request.
