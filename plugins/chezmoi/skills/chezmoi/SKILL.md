---
name: chezmoi
description: "<用户自制> 系统配置持久化：将已授权的本机配置变更保存在仓库并同步到实际环境。 Use for explicit capture/persistence or material durable macOS, global CLI, service, or model-host changes; preserve source, target, and recipient publication ownership."
user-invocable: false
---

# chezmoi

Keep the Mac reconstructible while distinguishing repository source, chezmoi's rendered target and the application/service consuming it. An intentional target edit can be new source truth; runtime drift is not automatically so. Accounts, credentials and device-bound state retain their external owners.

Use for explicit capture/persistence requests or material durable macOS/global CLI/service/model-host changes. Inspection, temporary toggles, ordinary code/docs/research are not persistence triggers.

## Resolve the recipient's actual ownership

The recipient supplies the canonical repository, managed destination, chezmoi configuration and publication/convergence owner. Inspect chezmoi source-path and current managed mapping; never infer a private repository or HOME target. Distinguish repository-only files, chezmoi dot_* source and resolved installed target. Installed wrappers/services terminate in the recipient's installed target rather than an authoring checkout.

Capture stable inputs, not logs, caches, sockets, locks, sessions or rotating state. Keep secrets with the recipient's credential authority and inject only required values. Explicitly retain login, consent, Keychain or device-bootstrap boundaries.

## Choose one authority direction

- add-target+apply: an intended unmanaged target is added to source.
- edit-source+apply: change canonical source, preview rendered target, then apply.
- edit-target+readd+apply: retain an intentional managed-target edit through re-add before apply.

Deletes/moves close the old target, stale references and broken links as well as source. See [commands](references/common-commands.md) and [script operations](references/script-loop-ops.md).

## Publication and live convergence

Writers use isolated source/destination fixtures and never mutate the real managed Home target. Publication, target apply and consumer readback cross a protected boundary owned by a real recipient service/coordinator.

Before execution, identify and verify that owner's real commands and duties: exact accepted Git tree, publication authority, process-lifetime shared mutex, mapping to only affected runtime consumers, apply/readback from that exact tree, retained recovery state, and actual restoration when apply fails. Advance the stable source checkout only after convergence. Ambiguous mapping/remote advancement or failed restoration must stop and retain recovery; do not claim a commit or apply command alone proves success. A publication owner need not copy the original implementation, but must perform these duties for the task.

The original integration is named macos-publish: a transactional publisher with protected exact-tree apply and restoration plus macos-home-mutex/runtime adapters. Its private executable service, hooks and host mappings are not shipped by this package; copying its prose would not install them. There is no public download here for that full implementation. A recipient's existing verified publication owner can realize the same boundary. If none exists, complete the isolated candidate/preview and report the missing real executable boundary before live publication/application; do not replace it with a no-op adapter or unprotected chezmoi apply.

## Tool/dependency contract

| Resource | Availability and recipient duty |
| --- | --- |
| This complete package | Downloadable method and command/script references; no background service |
| chezmoi + Git | External executable dependencies; configure actual source and target explicitly |
| Publication/runtime owner | Recipient-supplied real implementation, verified before protected live convergence |
| Shared HOME/runtime mutex | Recipient-supplied and used by all affected writers; Network distributes an optional actual descriptor-inherited implementation |
| macos-publish | Original integration name only; its full executable service is not distributed |
| Prompt and Skill Lifecycle | [Download companion](../prompt-and-skill-lifecycle/README.md) for Skill/wrapper topology changes |
| Obsidian Sync / Network | Optional specialist owners when persisting their resources; retain their configuration and authorization boundaries |

Report selected route, exact source/target/tree, preview and installed consumer readback, publication/restoration evidence, and remaining actual bootstrap. An unfinished owner boundary is unfinished live convergence.
