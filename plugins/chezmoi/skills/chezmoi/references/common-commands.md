# Common commands

Resolve actual source and destination first. The variables below are recipient-selected absolute paths, never author-specific defaults.

```sh
chezmoi source-path
chezmoi --source "$CHEZMOI_SOURCE" --destination "$CHEZMOI_DESTINATION" status
chezmoi --source "$CHEZMOI_SOURCE" --destination "$CHEZMOI_DESTINATION" diff
chezmoi --source "$CHEZMOI_SOURCE" --destination "$CHEZMOI_DESTINATION" cat "$TARGET"
```

| Route | Capture operation |
| --- | --- |
| add-target+apply | chezmoi --source "$CHEZMOI_SOURCE" --destination "$CHEZMOI_DESTINATION" add "$TARGET" |
| edit-source+apply | Edit the actual mapped source; inspect rendered cat/diff |
| edit-target+readd+apply | chezmoi --source "$CHEZMOI_SOURCE" --destination "$CHEZMOI_DESTINATION" re-add "$TARGET" |

These capture operations write source. Use the recipient's actual configuration and carefully separate intentional target changes from runtime state. An isolated fixture destination is appropriate for candidate behavior.

After accepted publication, the verified runtime owner runs the affected apply under the shared mutex from the exact accepted source tree:

```sh
chezmoi --source "$ACCEPTED_SOURCE_TREE" --destination "$CHEZMOI_DESTINATION" apply "$TARGET"
```

This command is one owner operation, not the complete publication/restoration protocol. Verify installed bytes, resolved wrapper and consuming app/service; if convergence fails, the owner restores trusted source/runtime state and retains unresolved recovery evidence.
